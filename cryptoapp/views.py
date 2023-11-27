from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .forms import RegisterForm, UpdateUserForm, TransactionForm, AddBalanceForm
from .models import Coin, Transaction, UserProfile, Portfolio
import decimal

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    if request.user.is_authenticated:
        return redirect('cryptoapp:coin_list')
    else:
        return render(request, 'cryptoapp/index.html')


def create_userprofile(request):
    uprof = UserProfile(user=request.user, balance=0.00)
    uprof.save()


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            create_userprofile(request)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})


def user_edit_view(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            user_profile = form.save()
            user_profile.user.first_name = form.cleaned_data['first_name']
            user_profile.user.last_name = form.cleaned_data['last_name']
            user_profile.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('cryptoapp:profile')
    else:
        form = UpdateUserForm(instance=request.user.userprofile,
                              initial={'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                       'password': request.user.password})

    return render(request, 'cryptoapp/edit_profile.html', {"form": form})


def get_exchange_rates():
    # For simplicity, providing static exchange rates (not recommended for production)
    # Replace these values with real exchange rates
    exchange_rates = {
        'usd': 1.0,
        'cad': 1.25,  # Example: 1 USD = 1.25 CAD
        'gbp': 0.75,  # Example: 1 USD = 0.75 GBP
        'yen': 110.0,  # Example: 1 USD = 110 JPY
    }
    return exchange_rates


def convert_currency(original_price, target_currency, exchange_rates):
    if target_currency in exchange_rates:
        rate = exchange_rates[target_currency]
        converted_price = original_price * rate
        return converted_price
    else:
        # Handle the case when the target currency is not found in exchange_rates
        return original_price


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Coin


def coin_list(request):
    # Assuming coins is your queryset
    coins_list = Coin.objects.all().order_by('-market_cap')

    # Set the number of items per page
    items_per_page = 10

    paginator = Paginator(coins_list, items_per_page)
    page = request.GET.get('page')

    try:
        coins = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        coins = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page.
        coins = paginator.page(paginator.num_pages)

    # Add currency conversion logic here
    selected_currency = request.GET.get('currency', 'usd')  # Default to USD if not specified
    exchange_rates = get_exchange_rates()  # Implement a function to fetch exchange rates
    currency_symbols = {'usd': '$', 'cad': 'CA$', 'gbp': '£', 'yen': '¥'}
    for coin in coins:
        original_price = coin.current_price
        coin.current_price = convert_currency(original_price, selected_currency, exchange_rates)

        original_market_cap = coin.market_cap
        coin.market_cap = convert_currency(original_market_cap, selected_currency, exchange_rates)

        original_total_volume = coin.total_volume
        coin.total_volume = convert_currency(original_total_volume, selected_currency, exchange_rates)

    return render(request, 'cryptoapp/coin_list.html',
                  {'coins': coins, 'selected_currency': selected_currency, 'currency_symbols': currency_symbols})


def coin_details(request, id):
    coin = get_object_or_404(Coin, pk=id)
    return render(request, 'cryptoapp/coin_details.html', {'coin': coin})


def highlight_view(request):
    # Top 10 gainers
    top_gainers = Coin.objects.order_by('-price_change_percentage_24h')[:10]

    # Top 10 losers
    top_losers = Coin.objects.order_by('price_change_percentage_24h')[:10]

    # Volume buzzers with highest volume
    volume_buzzers = Coin.objects.order_by('-total_volume')[:10]

    context = {
        'top_gainers': top_gainers,
        'top_losers': top_losers,
        'volume_buzzers': volume_buzzers,
    }

    return render(request, 'cryptoapp/highlight.html', context)


def buy_coin(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']

            if quantity:
                amount = coin.current_price * quantity
            elif amount:
                quantity = amount / (decimal.Decimal(coin.current_price))

            if amount <= user_profile.balance:
                transaction = Transaction.objects.create(
                    user=user,
                    coin=coin,
                    amount=amount,
                    quantity=quantity,
                    transaction_type='Buy',
                )

                # Update user balance
                user_profile.balance -= amount
                user_profile.save()

                try:
                    user_portfolio = Portfolio.objects.get(user_profile=user_profile, coin=coin)
                    user_portfolio.amount += float(amount)
                    user_portfolio.quantity += float(quantity)
                    user_portfolio.save()
                except:
                    Portfolio.objects.create(
                        user_profile=user_profile,
                        coin=coin,
                        amount=amount,
                        quantity=quantity,
                    )

                return redirect('cryptoapp:coin_list')  # Redirect to the highlight view or any desired page
            else:
                # Insufficient balance
                form.add_error('amount', 'Insufficient balance for the purchase.')
    else:
        form = TransactionForm()

    return render(request, 'cryptoapp/buy_sell_form.html', {'form': form, 'action': 'buy', 'coin': coin})


def sell_coin(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']

            if quantity:
                amount = coin.current_price * quantity

            elif amount:
                quantity = amount / (decimal.Decimal(coin.current_price))

            user_portfolio = Portfolio.objects.get(user_profile=user_profile, coin=coin)

            if amount <= user_portfolio.amount:
                transaction = Transaction.objects.create(
                    user=user,
                    coin=coin,
                    amount=amount,
                    quantity=quantity,
                    transaction_type='Sell',
                )

                # Update user balance
                user_profile.balance += amount
                user_profile.save()

                try:
                    user_portfolio = Portfolio.objects.get(user_profile=user_profile, coin=coin)
                    user_portfolio.amount -= float(amount)
                    user_portfolio.quantity -= float(quantity)
                    user_portfolio.save()
                except:
                    Portfolio.objects.create(
                        user_profile=user_profile,
                        coin=coin,
                        amount=amount,
                        quantity=quantity,
                    )

                return redirect('cryptoapp:highlight_view')  # Redirect to the highlight view or any desired page
            else:
                # Insufficient quantity or amount
                form.add_error('quantity', 'Insufficient quantity or amount for the sale.')
    else:
        form = TransactionForm()

    return render(request, 'cryptoapp/buy_sell_form.html', {'form': form, 'action': 'sell', 'coin': coin})


def portfolio(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_portfolio = user_profile.portfolio_set.all()

    for i in user_portfolio:
        print(i, i.user_profile.user, i.coin, i.quantity, i.amount)

    add_balance_form = AddBalanceForm()
    if request.method == 'POST':
        add_balance_form = AddBalanceForm(request.POST)
        if add_balance_form.is_valid():
            amount = add_balance_form.cleaned_data['amount']

            # Update user's balance in UserProfile
            user_profile = UserProfile.objects.get(user=user)
            user_profile.balance += amount
            user_profile.save()

            # Redirect back to the portfolio page
            return redirect('cryptoapp:portfolio')

    return render(request, 'cryptoapp/portfolio.html',
                  {'assets': user_portfolio, 'add_balance_form': add_balance_form, 'user_profile': user_profile})


def toggle_watchlist(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    user_profile = request.user.userprofile

    if coin in user_profile.coin.all():
        user_profile.coin.remove(coin)
        in_watchlist = False
    else:
        user_profile.coin.add(coin)
        in_watchlist = True

    return JsonResponse({'in_watchlist': in_watchlist})


def watchlist(request):
    user = request.user
    watchlist_coins = user.userprofile.coin.all()
    return render(request, 'cryptoapp/watchlist.html', {'watchlist_coins': watchlist_coins})

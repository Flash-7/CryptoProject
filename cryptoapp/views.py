from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, TransactionForm, AddBalanceForm
from .models import Coin, Transaction, UserProfile
from django.contrib.auth import login
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    if request.user.is_authenticated:
        return redirect('cryptoapp:coin_list')
    else:
        return render(request, 'cryptoapp/index.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form": form})


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

    return render(request, 'cryptoapp/coin_list.html', {'coins': coins})


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

            if amount <= user_profile.balance:
                transaction = Transaction.objects.create(
                    user=user,
                    coin=coin,
                    amount=amount,
                    quantity=quantity
                )

                # Update user balance
                user_profile.balance -= amount
                user_profile.save()

                # Additional logic: Update coin-related information, such as holdings
                if quantity:
                    coin.holdings += quantity
                else:
                    coin.holdings += amount / coin.current_price

                coin.save()

                return redirect('cryptoapp:highlight_view')  # Redirect to the highlight view or any desired page
            else:
                # Insufficient balance
                form.add_error('amount', 'Insufficient balance for the purchase.')
    else:
        form = TransactionForm()

    return render(request, 'cryptoapp/buy_sell_form.html', {'form': form, 'action': 'buy', 'coin': coin})


def sell_coin(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']

            if quantity and quantity <= coin.holdings:
                amount = coin.current_price * quantity

                transaction = Transaction.objects.create(
                    user=user,
                    coin=coin,
                    amount=amount,
                    quantity=quantity
                )

                # Update user balance
                user_profile.balance += amount
                user_profile.save()

                # Additional logic: Update coin-related information, such as holdings
                coin.holdings -= quantity
                coin.save()

                return redirect('cryptoapp:highlight_view')  # Redirect to the highlight view or any desired page
            elif amount and amount <= coin.holdings * coin.current_price:
                transaction = Transaction.objects.create(
                    user=user,
                    coin=coin,
                    amount=amount
                )

                # Update user balance
                user_profile.balance += amount
                user_profile.save()

                # Additional logic: Update coin-related information, such as holdings
                coin.holdings -= amount / coin.current_price
                coin.save()

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
    buy_transactions = Transaction.objects.filter(user=user, coin__holdings__gt=0).order_by('coin__name')
    total_balance = sum(transaction.amount for transaction in buy_transactions)
    user_profile = UserProfile.objects.get(user=user)

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
                  {'buy_transactions': buy_transactions, 'total_balance': total_balance,
                   'add_balance_form': add_balance_form, 'user_profile': user_profile})


def toggle_watchlist(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    user_profile = request.user.userprofile

    if coin in user_profile.watchlist.all():
        user_profile.watchlist.remove(coin)
        in_watchlist = False
    else:
        user_profile.watchlist.add(coin)
        in_watchlist = True

    return JsonResponse({'in_watchlist': in_watchlist})

def watchlist(request):
    user = request.user
    watchlist_coins = user.userprofile.watchlist.all()
    return render(request, 'cryptoapp/watchlist.html', {'watchlist_coins': watchlist_coins})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Coin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def home(request):
    if request.user.is_authenticated:
        # User is logged in, render a different template
        return redirect('cryptoapp:coin_list')
    else:
        # User is not logged in, render the default home template
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

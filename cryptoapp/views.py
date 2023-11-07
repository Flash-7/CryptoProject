from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Coin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group


@login_required(login_url="/login")
def home(request):
    return render(request, 'cryptoapp/home.html')


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
    coins = Coin.objects.all().order_by(
        '-market_cap')[:10]
    return render(request, 'cryptoapp/coin_list.html', {'coins': coins})


def coin_details(request, id):
    coin = get_object_or_404(Coin, pk=id)
    return render(request, 'cryptoapp/coin_details.html', {'coin': coin})

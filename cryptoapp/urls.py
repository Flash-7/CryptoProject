from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
app_name = "cryptoapp"
urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='reset_password'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('coins/', login_required(views.coin_list, login_url='login'), name='coin_list'),
    path('coin/<int:id>/', login_required(views.coin_details, login_url='login'), name='coin_details'),
    path('highlight/', login_required(views.highlight_view, login_url='login'), name='highlight_view'),
    path('buy_coin/<int:coin_id>/', login_required(views.buy_coin,login_url='login'), name='buy_coin'),
    path('sell_coin/<int:coin_id>/', login_required(views.sell_coin,login_url='login'), name='sell_coin'),
    path('portfolio/', login_required(views.portfolio,login_url='login'), name='portfolio'),
    path('toggle_watchlist/', views.toggle_watchlist, name='toggle_watchlist'),

]

from django.db import models
from django import forms

# Create your models here.
from django.contrib.auth.models import User


class Coin(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    current_price = models.FloatField()
    market_cap = models.BigIntegerField()
    market_cap_rank = models.PositiveIntegerField()
    fully_diluted_valuation = models.BigIntegerField()
    total_volume = models.BigIntegerField()
    high_24h = models.FloatField()
    low_24h = models.FloatField()
    price_change_24h = models.FloatField()
    price_change_percentage_24h = models.FloatField()
    market_cap_change_24h = models.FloatField()
    market_cap_change_percentage_24h = models.FloatField()
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2)
    total_supply = models.BigIntegerField()
    max_supply = models.BigIntegerField()
    ath = models.FloatField()
    ath_change_percentage = models.FloatField()
    ath_date = models.DateField()
    atl = models.FloatField()
    atl_change_percentage = models.FloatField()
    atl_date = models.DateField()
    price_change_percentage_24h_in_currency = models.FloatField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)  # Assume you have a Coin model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, blank=False, null=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    portfolio = models.ManyToManyField(Coin, blank=True, related_name='portfolio_coins')
    watchlist = models.ManyToManyField(Coin, blank=True, related_name='watchlist_coins')

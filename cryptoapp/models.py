from django.db import models

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

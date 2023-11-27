from django.contrib import admin
from .models import Coin, Transaction, UserProfile, Portfolio

# Register your models here.
admin.site.register(Coin)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Portfolio)
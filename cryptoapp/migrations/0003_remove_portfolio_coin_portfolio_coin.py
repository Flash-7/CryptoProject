# Generated by Django 4.2.6 on 2023-11-24 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0002_rename_watchlist_userprofile_coin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='coin',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='coin',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_coins', to='cryptoapp.coin'),
            preserve_default=False,
        ),
    ]
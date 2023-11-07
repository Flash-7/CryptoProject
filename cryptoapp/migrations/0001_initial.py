# Generated by Django 4.2.6 on 2023-11-07 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('current_price', models.FloatField()),
                ('market_cap', models.BigIntegerField()),
                ('market_cap_rank', models.PositiveIntegerField()),
                ('fully_diluted_valuation', models.BigIntegerField()),
                ('total_volume', models.BigIntegerField()),
                ('high_24h', models.FloatField()),
                ('low_24h', models.FloatField()),
                ('price_change_24h', models.FloatField()),
                ('price_change_percentage_24h', models.FloatField()),
                ('market_cap_change_24h', models.FloatField()),
                ('market_cap_change_percentage_24h', models.FloatField()),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_supply', models.BigIntegerField()),
                ('max_supply', models.BigIntegerField()),
                ('ath', models.FloatField()),
                ('ath_change_percentage', models.FloatField()),
                ('ath_date', models.DateField()),
                ('atl', models.FloatField()),
                ('atl_change_percentage', models.FloatField()),
                ('atl_date', models.DateField()),
                ('price_change_percentage_24h_in_currency', models.FloatField()),
            ],
        ),
    ]

from celery import shared_task
from django.utils import timezone
from .models import Currency, CurrencyHistory
import requests

@shared_task
def update_currency_rates():
    response = requests.get('https://api.monobank.ua/bank/currency')
    if response.status_code == 200:
        rates = response.json()
        for rate in rates:
            if rate["currencyCodeB"] == 980:
                last_updated = timezone.now()
                currency, created = Currency.objects.update_or_create(
                    currency_code=rate["currencyCodeA"],
                    defaults={
                        'date_updated': last_updated
                    }
                )

                CurrencyHistory.objects.create(
                    currency=currency,
                    rates={
                        'buy_rate': rate.get('rateBuy'),
                        'sell_rate': rate.get('rateSell'),
                        'cross_rate': rate.get('rateCross')
                    },
                    date_recorded=last_updated
                )

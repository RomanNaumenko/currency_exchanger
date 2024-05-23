from django.core.management.base import BaseCommand, CommandError
from rates.models import Currency, CurrencyHistory
import requests
import datetime
import json

class Command(BaseCommand):
    help = "Fetches currency rates from Monobank API"

    def handle(self, *args, **options):
        response = requests.get('https://api.monobank.ua/bank/currency')
        if response.status_code == 200:
            try:
                rates = response.json()
            except json.JSONDecodeError:
                raise CommandError("Error decoding JSON from the response")

            for rate in rates:
                if rate["currencyCodeB"] == 980:
                    last_updated = datetime.datetime.fromtimestamp(rate['date'])
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
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created new record for currency {rate["currencyCodeA"]}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated record for currency {rate["currencyCodeA"]}'))
        else:
            raise CommandError(f"API request failed with status code {response.status_code}")

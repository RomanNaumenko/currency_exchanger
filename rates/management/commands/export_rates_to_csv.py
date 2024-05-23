import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from rates.models import Currency

class Command(BaseCommand):
    help = "Exports the current exchange rates to a CSV file"

    def handle(self, *args, **kwargs):
        currencies = Currency.objects.all()
        file_path = os.path.join(settings.BASE_DIR, 'currency_rates.csv')

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Currency Code', 'Buy Rate', 'Sell Rate', 'Cross Rate', 'Date Updated'])

            for currency in currencies:
                writer.writerow([
                    currency.currency_code,
                    currency.buy_rate,
                    currency.sell_rate,
                    currency.cross_rate,
                    currency.date_updated,
                ])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported to {file_path}'))
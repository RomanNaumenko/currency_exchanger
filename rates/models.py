from django.db import models

# Create your models here.
class Currency(models.Model):
    currency_code = models.PositiveIntegerField()
    buy_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    cross_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_tracked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.currency_code} - {self.date_updated.strftime('%Y-%m-%d %H:%M:%S')}"



class CurrencyHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rates = models.JSONField(null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency.currency_code} - {self.date_recorded.strftime('%Y-%m-%d %H:%M:%S')}"


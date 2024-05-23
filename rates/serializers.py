from rest_framework import serializers
from .models import Currency, CurrencyHistory

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['currency_code', 'buy_rate', 'sell_rate', 'cross_rate', 'date_updated', 'is_tracked']

class CurrencyCodeSerializer(serializers.Serializer):
    currency_code = serializers.IntegerField(help_text="Code of the currency to track")


class CurrencyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyHistory
        fields = ['currency', 'rates', 'date_recorded']


class CurrencyTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['is_tracked']
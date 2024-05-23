from django.urls import path
from .views import (CurrentCurrencyRates,
                    TrackableCurrencies,
                    AddCurrencyForTracking,
                    CurrencyRateHistory,
                    ToggleCurrencyTracking)

urlpatterns = [
    path('currency_rates/', CurrentCurrencyRates.as_view(), name='current-currency-rates'),
    path('trackable_currencies/', TrackableCurrencies.as_view(), name='trackable-currencies'),
    path('add_trackable_currency/', AddCurrencyForTracking.as_view(), name='add-currency-for-tracking'),
    path('currency_rate_history/', CurrencyRateHistory.as_view(), name='currency-rate-history'),
    path('toggle_currency_tracking/<int:currency_code>/', ToggleCurrencyTracking.as_view(),
         name='toggle-currency-tracking'),
]

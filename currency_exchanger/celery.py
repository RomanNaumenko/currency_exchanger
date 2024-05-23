from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_exchanger.settings')

app = Celery('currency_exchanger')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_currency_rates_every_hour': {
        'task': 'rates.tasks.update_currency_rates',
        'schedule': crontab(hour='*', minute=0),  # Runs at the start of every hour
    },
}
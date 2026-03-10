from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

app = Celery('library')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify-new-books-every-day': {
        'task': 'book.tasks.notify_new_books',
        'schedule': crontab(hour=9, minute=0),
    },
    'notify-anniversary-books-every-day': {
        'task': 'book.tasks.notify_anniversary_books',
        'schedule': crontab(hour=10, minute=0),
    },
}
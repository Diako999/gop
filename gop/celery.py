import os
from gop.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gop.settings')

app = Celery('gop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

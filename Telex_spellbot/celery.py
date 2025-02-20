import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Telex_spellbot.settings')
celery_app = Celery('Telex_spellbot')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
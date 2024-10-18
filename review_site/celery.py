from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_site.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('review_site')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

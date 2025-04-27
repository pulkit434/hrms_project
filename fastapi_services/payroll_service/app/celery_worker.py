# app/celery_worker.py
from app.core.celery_config import celery_app
from app.tasks import payroll_tasks

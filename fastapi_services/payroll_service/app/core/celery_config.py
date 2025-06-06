from celery import Celery

# Create Celery instance

celery_app = Celery(
    "payroll_service",  # Name of the service
    broker="redis://localhost:6379/0",  # Redis broker URL
    backend="redis://localhost:6379/1",  # Redis backend URL for result storage
)
# celery_app.autodiscover_tasks(['app.tasks'])
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
# # Optional: Configure the Celery app
# celery_app.conf.update(
#     task_routes={
#         "app.tasks.some_task": {"queue": "payroll_queue"}
#     }
# )

# # Optional: Other configurations if required
# celery_app.conf.task_default_queue = 'default'
# celery_app.conf.task_serializer = 'json'

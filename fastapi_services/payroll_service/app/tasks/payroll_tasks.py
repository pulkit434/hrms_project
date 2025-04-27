from app.core.celery_config import celery_app

@celery_app.task
def process_payroll(employee_id: int):
    print(f"Processing payroll for employee {employee_id}...")
    net_salary = 4500  # Simulated logic
    print(f"Processed payroll for employee {employee_id}. Net salary: {net_salary}")
    return net_salary
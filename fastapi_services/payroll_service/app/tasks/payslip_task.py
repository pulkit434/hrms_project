from app.core.celery_config import celery_app
# from app.core.celery_config import celery_app

@celery_app.task
def send_payslip_email(employee_data: dict, salary_data: dict):
    payslip = f"""
    Payslip for {employee_data['name']} ({employee_data['role']})
    ------------------------------------------------------------
    Basic Salary: {salary_data['basic_salary']}
    HRA: {salary_data['hra']}
    DA: {salary_data['da']}
    Bonus: {salary_data['bonus']}
    Tax Deductions: {salary_data['tax_deductions']}
    ------------------------------------------------------------
    Net Salary: {salary_data['net_salary']}
    """
    print(f"Sending payslip to {employee_data['name']}")
    print(payslip)

    return "Payslip email task completed"


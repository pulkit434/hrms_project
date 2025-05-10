from fastapi import APIRouter
from app.tasks.payroll_tasks import process_payroll

router = APIRouter()

@router.post("/payroll/{employee_id}")
def run_payroll(employee_id: int):
    task = process_payroll.delay(employee_id)  
    return {
        "message": "Payroll processing started",
        "task_id": task.id
    }

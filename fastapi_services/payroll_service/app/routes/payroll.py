from fastapi import APIRouter
from app.schemas.payroll import GeneratePayslipRequest

router = APIRouter()

@router.post("/generate")
def generate_payslip(data: GeneratePayslipRequest):
    return{
        "message": "Payslip generation triggered",
        "employee_id": data.employee_id,
        "month": data.month,
        "year": data.year
    }
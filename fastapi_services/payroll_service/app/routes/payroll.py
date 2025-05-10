from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from app.database import get_db  # Database session

router = APIRouter()



@router.post("/salary/calculate")
def calculate_salary(request: schemas.SalaryCalculationRequest, db: Session = Depends(get_db)):
    # Fetch employee details from the database
    employee = db.query(models.Employee).filter(models.Employee.id == request.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Perform salary calculation logic
    gross_salary = request.basic_salary + request.hra + request.da + request.bonus
    net_salary = gross_salary - request.tax_deductions
    
    # Prepare response data
    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "gross_salary": gross_salary,
        "tax_deductions": request.tax_deductions,
        "net_salary": net_salary
    }

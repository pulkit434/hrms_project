from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payroll import SalaryCalculationRequest
from app.models import Employee, Salary
from app.database import get_db
from fastapi import Path
from app.tasks.payslip_task import send_payslip_email
import httpx
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()

# @router.post("/salary/calculate")
# def calculate_salary(request: SalaryCalculationRequest, db: Session = Depends(get_db)):
#     # Check if employee exists
#     employee = db.query(Employee).filter(Employee.id == request.employee_id).first()

#     # If not found, create the employee
#     if not employee:
#         employee = Employee(
#             id=request.employee_id,
#             name=request.name,
#             role=request.role
#         )
#         db.add(employee)
#         db.commit()
#         db.refresh(employee)

#     # Calculate gross and net salary
#     gross_salary = request.basic_salary + request.hra + request.da + request.bonus
#     net_salary = gross_salary - request.tax_deductions

#     # Create and store salary record
#     salary = Salary(
#         basic_salary=request.basic_salary,
#         hra=request.hra,
#         da=request.da,
#         bonus=request.bonus,
#         tax_deductions=request.tax_deductions,
#         employee_id=employee.id
#     )
#     db.add(salary)
#     db.commit()
#     db.refresh(salary)
#     employee_data = {
#         "name": employee.name,
#         "role": employee.role
#     }

#     salary_data = {
#         "basic_salary": salary.basic_salary,
#         "hra": salary.hra,
#         "da": salary.da,
#         "bonus": salary.bonus,
#         "tax_deductions": salary.tax_deductions,
#         "net_salary": salary.basic_salary + salary.hra + salary.da + salary.bonus - salary.tax_deductions
#     }
#     send_payslip_email.delay(employee_data, salary_data)

#     return {
#         "employee": {
#             "id": employee.id,
#             "name": employee.name,
#             "role": employee.role
#         },
#         "salary": {
#             "id": salary.id,
#             "basic_salary": salary.basic_salary,
#             "hra": salary.hra,
#             "da": salary.da,
#             "bonus": salary.bonus,
#             "tax_deductions": salary.tax_deductions,
#             "employee_id": salary.employee_id,
#             "net_salary": net_salary
#         }
    
#     }
# @router.put("/salary/update/{employee_id}")
# def update_salary(employee_id: int, request: SalaryCalculationRequest, db: Session = Depends(get_db)):
#     employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee Not Found")  # ✅ fixed here

#     if request.name:
#         employee.name = request.name
#     if request.role:
#         employee.role = request.role
#     db.commit()

#     new_salary = Salary(
#         basic_salary=request.basic_salary,
#         hra=request.hra,
#         da=request.da,
#         bonus=request.bonus,
#         tax_deductions=request.tax_deductions,
#         employee_id=employee.id
#     )
#     db.add(new_salary)
#     db.commit()
#     db.refresh(new_salary)

#     employee_data = {
#         "name": employee.name,
#         "role": employee.role
#     }

#     salary_data = {
#         "basic_salary": new_salary.basic_salary,
#         "hra": new_salary.hra,
#         "da": new_salary.da,
#         "bonus": new_salary.bonus,
#         "tax_deductions": new_salary.tax_deductions,
#         "net_salary": new_salary.basic_salary + new_salary.hra + new_salary.da + new_salary.bonus - new_salary.tax_deductions
#     }
#     send_payslip_email.delay(employee_data, salary_data)

#     # return {
#     #     "employee": employee_data,
#     #     "salary": salary_data
#     # }


#     return {
#         "employee": {
#             "id": employee.id,
#             "name": employee.name,
#             "role": employee.role
#         },
#         "salary": {
#             "id": new_salary.id,
#             "basic_salary": new_salary.basic_salary,
#             "hra": new_salary.hra,
#             "da": new_salary.da,
#             "bonus": new_salary.bonus,
#             "tax_deductions": new_salary.tax_deductions,
#             "employee_id": new_salary.employee_id,
#             "net_salary": new_salary.basic_salary + new_salary.hra + new_salary.da + new_salary.bonus - new_salary.tax_deductions
#         }
#     }

# @router.get("/salary/{employee_id}")
# def get_employee_salary(employee_id: int = Path(..., title="The ID of the employee to retrieve"), db: Session = Depends(get_db)):
#     employee= db.query(Employee).filter(Employee.id==employee_id).first()
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee Not Found")
#     salary= (db.query(Salary).filter(Salary.employee_id==employee_id).order_by(Salary.id.desc()).first())
#     if not salary:
#        raise HTTPException(status_code=404, detail="No salary record found for this employee")
#     return {
#         "employee": {
#              "id": employee.id,
#              "name": employee.name,
#              "role": employee.role
#         },
#         "salary": {
#             "id": salary.id,
#             "basic_salary": salary.basic_salary,
#             "hra": salary.hra,
#             "da": salary.da,
#             "bonus": salary.bonus,
#             "tax_deductions": salary.tax_deductions,
#             "employee_id": salary.employee_id,
#             "net_salary": salary.basic_salary + salary.hra + salary.da + salary.bonus - salary.tax_deductions
#         }
#     }





router = APIRouter()

@router.post("/salary/calculate")
def calculate_salary(request: SalaryCalculationRequest, db: Session = Depends(get_db)):
    try:
        # Call Django employee service
        response = httpx.get(f"http://localhost:8000/api/employees/{request.employee_id}/")
        response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx
        employee_data = response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Employee not found in employee service")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from employee service")

    try:
        # Check or create employee locally
        employee = db.query(Employee).filter(Employee.id == request.employee_id).first()
        if not employee:
            employee = Employee(
                id=request.employee_id,
                name=employee_data["name"],
                role=employee_data["role"]
            )
            db.add(employee)
            db.commit()
            db.refresh(employee)

        # Calculate salary
        gross_salary = request.basic_salary + request.hra + request.da + request.bonus
        net_salary = gross_salary - request.tax_deductions

        salary = Salary(
            basic_salary=request.basic_salary,
            hra=request.hra,
            da=request.da,
            bonus=request.bonus,
            tax_deductions=request.tax_deductions,
            employee_id=employee.id
        )
        db.add(salary)
        db.commit()
        db.refresh(salary)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    try:
        # Send payslip via Celery
        salary_data = {
            "basic_salary": salary.basic_salary,
            "hra": salary.hra,
            "da": salary.da,
            "bonus": salary.bonus,
            "tax_deductions": salary.tax_deductions,
            "net_salary": net_salary
        }
        send_payslip_email.delay({
            "name": employee.name,
            "role": employee.role
        }, salary_data)
    except Exception as e:
        # Log but don't crash
        print(f"Failed to send payslip email: {str(e)}")

    return {
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "role": employee.role
        },
        "salary": {
            "id": salary.id,
            "basic_salary": salary.basic_salary,
            "hra": salary.hra,
            "da": salary.da,
            "bonus": salary.bonus,
            "tax_deductions": salary.tax_deductions,
            "employee_id": salary.employee_id,
            "net_salary": net_salary
        }
    }


@router.get("/salary/{employee_id}")
def get_employee_salary(employee_id: int = Path(..., title="The ID of the employee to retrieve"), db: Session = Depends(get_db)):
    employee= db.query(Employee).filter(Employee.id==employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    salary= (db.query(Salary).filter(Salary.employee_id==employee_id).order_by(Salary.id.desc()).first())
    if not salary:
       raise HTTPException(status_code=404, detail="No salary record found for this employee")
    return {
        "employee": {
             "id": employee.id,
             "name": employee.name,
             "role": employee.role
        },
        "salary": {
            "id": salary.id,
            "basic_salary": salary.basic_salary,
            "hra": salary.hra,
            "da": salary.da,
            "bonus": salary.bonus,
            "tax_deductions": salary.tax_deductions,
            "employee_id": salary.employee_id,
            "net_salary": salary.basic_salary + salary.hra + salary.da + salary.bonus - salary.tax_deductions
        }
    }

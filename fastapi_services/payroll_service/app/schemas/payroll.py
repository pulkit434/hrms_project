from pydantic import BaseModel
from typing import Optional

# ========================
# Input Schemas (Request)
# ========================

class SalaryCalculationRequest(BaseModel):
    employee_id: int
    name: str
    role: str
    basic_salary: float
    hra: float
    da: float
    bonus: float
    tax_deductions: Optional[float] = 0.0

    class Config:
        from_attributes = True

# ========================
# Output Schemas (Response)
# ========================

class SalaryBase(BaseModel):
    id: int
    basic_salary: float
    hra: float
    da: float
    bonus: float
    tax_deductions: float
    employee_id: int

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    id: int
    name: str
    role: str

    class Config:
       from_attributes = True

class SalaryCalculationResponse(BaseModel):
    employee: EmployeeBase
    salary: SalaryBase

    class Config:
        from_attributes=True
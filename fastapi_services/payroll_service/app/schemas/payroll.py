from typing import Optional
from pydantic import BaseModel

class SalaryCalculationRequest(BaseModel):
    employee_id: int
    basic_salary: float
    hra: float
    da: float
    bonus: float
    tax_deductions: Optional[float] = 0.0  # Default tax deduction is 0.0 if not provided

    class Config:
        orm_mode = True
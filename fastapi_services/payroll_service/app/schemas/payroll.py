from pydantic import BaseModel

class GeneratePayslipRequest(BaseModel):
    employee_id: int
    month: int
    year: int

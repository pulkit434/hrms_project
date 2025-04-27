from fastapi import FastAPI
from app.routes import payroll
from app.api.routes import router

app = FastAPI(title="Payroll Service")
app.include_router(router)

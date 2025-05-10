from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    # Relationship with Salary Model (one-to-one relationship)
    salary = relationship("Salary", back_populates="employee", uselist=False)

# Salary Model: Stores Salary Information
class Salary(Base):
    __tablename__ = 'salaries'
    
    id = Column(Integer, primary_key=True, index=True)
    basic_salary = Column(Float)
    hra = Column(Float)
    da = Column(Float)
    bonus = Column(Float)
    tax_deductions = Column(Float)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    # Relationship with Employee Model
    employee = relationship("Employee", back_populates="salary")


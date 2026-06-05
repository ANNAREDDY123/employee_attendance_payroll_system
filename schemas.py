from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    designation: str
    monthly_salary: float

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    monthly_salary: Optional[float] = None

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance_date: date
    status: str

class PayrollCreate(BaseModel):
    employee_id: int
    month: str

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(255))


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    department = Column(String(100))
    designation = Column(String(100))
    monthly_salary = Column(Float)
    is_deleted = Column(Boolean, default=False)


class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    attendance_date = Column(Date)
    status = Column(String(20))


class Payroll(Base):
    __tablename__ = "payroll"

    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    month = Column(String(20))
    salary_amount = Column(Float)

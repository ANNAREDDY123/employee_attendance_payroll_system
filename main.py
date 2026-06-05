from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import schemas
from database import Base, engine, get_db
from auth import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Attendance & Payroll Management System")


@app.get("/")
def home():
    return {"message": "Employee Payroll API Running"}


# AUTH

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}


# EMPLOYEE MANAGEMENT

@app.post("/employees")
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    new_employee = models.Employee(**employee.dict())

    db.add(new_employee)
    db.commit()

    return {"message": "Employee added successfully"}


@app.get("/employees")
def view_employees(
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.Employee).filter(
        models.Employee.is_deleted == False
    )

    if search:
        query = query.filter(
            models.Employee.name.like(f"%{search}%")
        )

    total = query.count()

    employees = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {"total": total, "employees": employees}


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):

    db_employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()

    return {"message": "Employee updated successfully"}


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_deleted = True

    db.commit()

    return {"message": "Employee soft deleted"}


# ATTENDANCE

@app.post("/attendance")
def mark_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == attendance.employee_id,
        models.Employee.is_deleted == False
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    duplicate = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance.employee_id,
        models.Attendance.attendance_date == attendance.attendance_date
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this date"
        )

    new_attendance = models.Attendance(**attendance.dict())

    db.add(new_attendance)
    db.commit()

    return {"message": "Attendance marked successfully"}


@app.get("/attendance")
def view_attendance(db: Session = Depends(get_db)):
    return db.query(models.Attendance).all()


# PAYROLL

@app.post("/payroll")
def generate_salary(
    payroll: schemas.PayrollCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == payroll.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    duplicate = db.query(models.Payroll).filter(
        models.Payroll.employee_id == payroll.employee_id,
        models.Payroll.month == payroll.month
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Salary already generated for this month"
        )

    attendance_count = db.query(models.Attendance).filter(
        models.Attendance.employee_id == payroll.employee_id,
        models.Attendance.status == "Present"
    ).count()

    salary_amount = (employee.monthly_salary / 30) * attendance_count

    salary = models.Payroll(
        employee_id=payroll.employee_id,
        month=payroll.month,
        salary_amount=salary_amount
    )

    db.add(salary)
    db.commit()

    return {
        "message": "Salary generated successfully",
        "salary_amount": salary_amount
    }


@app.get("/payroll")
def salary_history(db: Session = Depends(get_db)):
    return db.query(models.Payroll).all()

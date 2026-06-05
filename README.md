# Employee Attendance & Payroll Management System

## Objective

Backend application to manage Employees, Attendance, and Payroll using FastAPI and SQLAlchemy.

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / MySQL
- JWT Authentication

## Features

### Employee Management
- Add Employee
- View Employees
- Update Employee
- Soft Delete Employee

### Attendance Management
- Mark Daily Attendance
- View Attendance Records
- Monthly Attendance Tracking

### Payroll Management
- Generate Monthly Salary
- Automatic Salary Calculation
- Salary History

### Business Rules
- Employee must exist before attendance
- Attendance only once per day
- Salary calculated automatically
- No duplicate payroll generation

### Bonus Features
- JWT Authentication
- Pagination
- Search & Filters
- Soft Delete
- Swagger Documentation

## Run Project

pip install -r requirements.txt
uvicorn main:app 

Swagger:

http://127.0.0.1:8000/docs

## Explanation

I created four tables: Users, Employees, Attendance, and Payroll.

Employees store employee details and salary information.

Attendance records daily employee presence.

Payroll automatically calculates salary based on attendance count.

Business rules prevent duplicate attendance and duplicate salary generation.

JWT Authentication is implemented using Register and Login APIs.

## Submission Files

- Source Code
- SQL Schema Script
- SQL Report Queries
- Postman Collection
- README

-- 1. Employees with highest attendance

SELECT e.name,
       COUNT(a.attendance_id) AS attendance_count
FROM employees e
JOIN attendance a
ON e.employee_id = a.employee_id
WHERE a.status = 'Present'
GROUP BY e.employee_id, e.name
ORDER BY attendance_count DESC;


-- 2. Department-wise salary expense

SELECT e.department,
       SUM(p.salary_amount) AS total_salary_expense
FROM employees e
JOIN payroll p
ON e.employee_id = p.employee_id
GROUP BY e.department;


-- 3. Absent employees for a given date

SELECT e.name,
       a.attendance_date
FROM employees e
JOIN attendance a
ON e.employee_id = a.employee_id
WHERE a.status = 'Absent';


-- 4. Monthly payroll report

SELECT month,
       SUM(salary_amount) AS total_payroll
FROM payroll
GROUP BY month;

-- 5. Rank employees based on attendance percentage

SELECT
    employee_name,
    attendance_count,
    RANK() OVER (ORDER BY attendance_count DESC) AS attendance_rank
FROM (
    SELECT
        e.name AS employee_name,
        COUNT(a.attendance_id) AS attendance_count
    FROM employees e
    LEFT JOIN attendance a
    ON e.employee_id = a.employee_id
    AND a.status = 'Present'
    GROUP BY e.employee_id, e.name
) ranked_employees;

# © 2020 Sam Lefever
# © 2020 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

{
    "name": "HR Calendar History",
    "category": "HR",
    "summary": "HR Calendar History",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.0.0",
    "license": "Other proprietary",
    "description": """
- Register the history of employee calendar
General purpose:
The idea is to have easy access to information without having to search through contracts. To be able to keep track of the history of each employee.

Dependencies:
/HR, HR_Timesheet

What it does:
Keeps a history of your working patterns (your hourly time). So if you were full-time a year ago and part-time today, the information is retained by the system.
This information is recorded using a new template which contains: employees, start and end dates and working hours.
This information is available to the employee.

How to use it:
It is mainly a reference tool. There is no actual use. It can be found in the employee file.
        """,
    "author": "Niboo",
    "depends": [
        "hr_timesheet",
        "hr",
    ],
    "data": [
        "report/hr_expected_log_time_report.xml",
        "security/ir.model.access.csv",
        "views/hr_employee_view.xml",
    ],
    "installable": False,
    "application": False,
}

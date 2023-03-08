# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

{
    "name": "Timesheet Analysis",
    "category": "Timesheet",
    "summary": "Timesheet Analysis",
    "website": "https://www.niboo.com/",
    "version": "13.0.2.0.0",
    "license": "Other proprietary",
    "description": """
- Allow to display report of expected and actual logged time
General Purpose:
Detect live unregistered timesheet hours and regain instant access to useful data such as invoiceable ratio, expected hours and timesheeted hours.

Description of the custom functionalities:
Custom modules have been added to the top left timesheet drop-down menu

Dependencies:
/HR_Timesheet, HR, HR_Calendar_History

What it does:

- Timesheet Analysis:
Allows users or managers to see the different portion of "timesheeted" work in a very clear interface within your Odoo. Example : expected hours, actual worked hours, timesheeted ratio, invoiceable ratio, leave time, etc.

- Timesheet Monthly Analysis:
Allows the user, or the manager, to see the different portion of "timesheeted" work in details for each month.

How to use it
To access those view, select the "Timesheet" menu and choose either "Timesheet" analysis or "Timesheet monthly analysis".
        """,
    "author": "Niboo",
    "depends": [
        "hr_timesheet",
        "hr",
        "timesheet_invoiceable_context",
        "hr_calendar_history"
    ],
    "data": [
        "report/hr_timesheet_analysis_report.xml",
        "report/hr_timesheet_analysis_monthly_report.xml",
        "security/ir.model.access.csv",
        "views/hr_job_view.xml",
        "views/project_project.xml",
    ],
    "installable": False,
    "application": False,
}

# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Timesheet - Invoiceable Context",
    "category": "Project",
    "summary": "Determine if the timesheet is in an invoiceable context",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.2.0",
    "license": "AGPL-3",
    "description": """
General purpose :
Allow timesheets to be invoiceable or not by using the boolean button
to count the TS record line.

    Description of the custom functionalities:
    - on the list view, of the boolean for "is invoiceable"
    - Add an "is invoiceable" column in list view
        """,
    "author": "Niboo",
    "depends": ["sale_timesheet_enterprise"],
    "data": ["data/server_actions_data.xml"],
    "images": [],
    "installable": False,
    "application": False,
}

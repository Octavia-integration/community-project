# © 2022 Alexandre Van Ommeslaghe
# © 2022 Niboo SPRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Timesheet - Timesheet enhancement",
    "category": "Project",
    "summary": "Improves Timesheet view",
    "description": """
    - Blocked timesheet lines being negative or null.
    - Made the fields unit_hours and name required depending on res.config.parameter.
    - Added a parameter to apply the rounding and min timesheet to all timesheets.
    """,
    "author": "Niboo",
    "website": "https://www.niboo.com",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["timesheet_grid"],
    "data": [
        "views/res_config_settings_views.xml"
    ],
    "installable": False,
    "application": False,
}

# © 2022 Albin Gilles
# © 2022 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Timesheet - Timesheet grid sort",
    "category": "Project",
    "summary": "Sort Timesheet grid view by project & task name",
    "description": """
    - Sort Timesheet grid view by project & task name.
    """,
    "author": "Niboo",
    "website": "https://www.niboo.com",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["timesheet_grid"],
    "data": [
        # "templates/assets_backend.xml"
        ],

    
     "assets": {
        "web.assets_backend": [
          "/timesheet_grid_sort/static/src/js/timer_grid_model.js",
          "/timesheet_grid_sort/static/src/js/timesheet_grid_model.js",
         
        ],
       
    },


    "installable": True,
    "application": False,
}

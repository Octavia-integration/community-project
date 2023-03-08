# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project - Tasks Categories",
    "category": "Project",
    "summary": "Adds Categories for tasks",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "description": """
- Adds Task Category model
- Adds a Task Category on Tasks
- Adds filters on tasks for the categoris
        """,
    "author": "Niboo",
    "depends": ["project"],
    "data": [
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "views/task_category_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": False,
    "application": False,
}

# © 2020 Pierre Faniel, Curatolo Gabriel
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project - Kanban View Improvement",
    "category": "Project",
    "summary": "Customer logo, task and project settings shortcut "
    "added in the Project Kanban View",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "description": """
Improvements in the Project Kanban View:

- Customer's logo has been added in the Kanban box

- Project title is a shortcut to project settings

        """,
    "author": "Niboo",
    "depends": ["project_workflow", "project_task_category"],
    "data": ["views/project_project.xml", "views/project_task.xml"],
    "assets": {
        "web.assets_backend": ["/project_kanban_improvement/static/css/project.css"]
    },
    "installable": False,
    "application": False,
}

# © 2020 Pierre Faniel, Curatolo Gabriel
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project - Light Workflow",
    "category": "Project",
    "summary": "Add a workflow to project tasks",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.0.0",
    "description": """
This module allows you to create simple workflow to manage your project.
It adds multiples models to allow you better manage the state of uor tasks:
-Project task category (a task type linked to a workflow)
-Project task workflow (a workflow composed of steps, a start step and a
    reopened step)
-Project task step (a new dedicated 'stage' to better manage your tasks)

It adds multiples features:
-possibility to archive stage and added step, workflow and category.
-a reopen mechanics to track yor reopened tasks.
-a user based personalization to fold the step based on their preferences

This modules also enhance the kanban view a lot with added tags,
 and button to switch to the next step
    """,
    "license": "AGPL-3",
    "author": "Niboo",
    "depends": ["project", "hr"],
    "data": [
        "views/project_task_category_view.xml",
        "views/project_task_step_view.xml",
        "views/project_task_view.xml",
        "views/project_task_workflow_view.xml",
        "views/res_users_view.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "/project_workflow/static/css/project.css",
            "/project_workflow/static/src/js/permanent_fold.js",
        ],
        "web.assets_qweb": [
            "project_workflow/static/src/xml/kanban_view_group_template.xml"
        ],
    },
    "images": ["static/description/project_workflow.png"],
    "installable": False,
    "application": False,
}

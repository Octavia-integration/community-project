# © 2020 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project - Task Identifier",
    "category": "Generic Modules/Others",
    "summary": "Add an identifier on tasks (project-sequence number)",
    "website": "https://www.niboo.com/",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "description": """
Project Task Identifier allows you to select an identifier for customers.
This identifier will be used to generate a unique key for all project tasks
 related to the customer, making it easier to identify tasks.
        """,
    "author": "Niboo",
    "depends": ["project", "project_identifier"],
    "data": [
        "views/project_task_view.xml",
        "views/res_partner_view.xml",
        "views/project_project_view.xml",
        "views/project_identifier_views.xml",
        "security/ir.model.access.csv",
        # "views/webclient_templates.xml",
        "views/project_portal_templates.xml",
    ],
    "assets": {
       
        "web.assets_frontend": [
            
            ],
        'web.assets_common': [
            "/project_task_identifier/static/src/js/task_search.js",
            "/project_task_identifier/static/src/css/task_search.css",
            "/project_task_identifier/static/src/xml/task_search.xml",

         ],
        "web.assets_backend": [
           
        ],
        "web.assets_qweb": [
            
        ],
       
    },

    "qweb": [],
    "images": ["static/description/project_task_identifier_cover.png"],
    "installable": True,
    "application": False,
    "post_load": "post_load",
}

# 2016 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# 2016 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project - Customer name",
    "category": "Project",
    "summary": "Add customer name to project tiles",
    "website": "https://www.niboo.com/",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "description": """
With this module, you can easily keep track on which project
belongs to which client.

- Add Customer name in Project Display Name

- Allows to search on project by customer name
        """,
    "author": "Niboo",
    "depends": ["project"],
    "data": ["views/project_task_view.xml"],
    "images": ["static/description/project_customer_name_cover.png"],
    "installable": False,
    "application": False,
}

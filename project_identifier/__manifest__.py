# © 2021 Antoine Honinckx
# © 2021 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Project Identifier",
    "category": "Generic Modules/Others",
    "summary": "Adds identifier model to create unique identifiers",
    "website": "https://www.niboo.com/",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "description": """
Project Identifier allows you to create unique identifiers.
This identifier will be used to generate a unique key for every resource
that are related, making it easier to identify them.
        """,
    "author": "Niboo",
    "depends": ["project"],
    "data": ["security/ir.model.access.csv", "views/project_identifier_views.xml"],
    "installable": True,
    "application": False,
}

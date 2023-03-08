# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    is_leave_project = fields.Boolean()

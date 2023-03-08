# © 2020 Pierre Faniel, Curatolo Gabriel, Pierre Gillissen
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTaskCategory(models.Model):
    _name = "project.task.category"
    _description = "category"

    active = fields.Boolean(default=True)

    name = fields.Char("Name", required=True)
    workflow_id = fields.Many2one("project.task.workflow", "Workflow", required=True)

    icon_file = fields.Binary("icon file")

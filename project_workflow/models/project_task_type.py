# © 2020 PAurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    active = fields.Boolean(default=True)

# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class TaskCategory(models.Model):
    _name = "task.category"
    _description = "Task Category"

    name = fields.Char()

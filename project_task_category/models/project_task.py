# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    task_category_id = fields.Many2one("task.category", required=True)

    @api.onchange("project_id")
    def set_default_task_category(self):
        self.ensure_one()
        if not self.task_category_id:
            self.task_category_id = self.project_id.default_task_category_id

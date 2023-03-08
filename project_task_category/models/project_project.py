# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    default_task_category_id = fields.Many2one("task.category")

    @api.constrains("default_task_category_id")
    def check_task_catgory_on_tasks(self):
        for project in self:
            task_to_update = project.task_ids.filtered(lambda x: not x.task_category_id)
            task_to_update.write(
                {"task_category_id": project.default_task_category_id.id}
            )

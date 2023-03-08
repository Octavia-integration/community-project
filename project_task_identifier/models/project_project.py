# © 2020-2022 Aurore Chevalier
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_key_ids = fields.Many2many(related="partner_id.project_key_ids")

    project_identifier_id = fields.Many2one(
        "project.identifier", domain="[('id', 'in', project_key_ids)]"
    )

    project_key = fields.Char(related="project_identifier_id.key", store=True)

    @api.onchange("partner_id")
    def check_linked_identifier(self):
        self.ensure_one()
        if self.project_identifier_id not in self.partner_id.project_key_ids:
            if len(self.partner_id.project_key_ids) == 1:
                self.project_identifier_id = self.partner_id.project_key_ids
            else:
                self.project_identifier_id = False

    @api.constrains("project_identifier_id")
    def check_project_key(self):
        for project in self:
            if project.project_identifier_id:
                # update existing tasks
                tasks = self.env["project.task"].search(
                    [("project_id", "=", project.id), ("identifier", "=", False)]
                )
                tasks._compute_identifier()

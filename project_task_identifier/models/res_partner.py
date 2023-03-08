# © 2020-2022 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    project_key_ids = fields.Many2many(
        "project.identifier",
        "project_key_partner_rel",
        "partner_id",
        "project_identifier_id",
        copy=False,
    )

    @api.constrains("project_key_ids")
    def check_project_key(self):
        for partner in self:
            if partner.project_key_ids:
                # update existing tasks
                tasks = self.env["project.task"].search(
                    [
                        ("project_id.analytic_account_id.partner_id", "=", partner.id),
                        ("identifier", "=", False),
                    ]
                )
                tasks._compute_identifier()

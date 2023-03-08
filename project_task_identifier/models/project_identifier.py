# © 2020-2022 Aurore Chevalier
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectIdentifier(models.Model):
    _inherit = "project.identifier"

    key_sequence_id = fields.Many2one("ir.sequence", readonly=True)

    code = fields.Char(
        "Sequence code", compute="_compute_code", store=True, readonly=True
    )

    @api.depends("key")
    def _compute_code(self):
        for identifier in self:
            identifier.code = f"project.task.order.{identifier.key}"

    @api.constrains("key_sequence_id")
    def check_project_key(self):
        unset_identifiers = self.filtered(
            lambda identifier: not identifier.key_sequence_id
        )
        unset_identifiers._create_sequence()

    def _create_sequence(self):
        sudo_sequence = self.env["ir.sequence"].sudo()
        for identifier in self:
            sequence = self.env["ir.sequence"].search([("code", "=", identifier.code)])
            if not sequence:
                name = f"project task order - {identifier.name}"
                sequence = sudo_sequence.create(
                    {
                        "code": identifier.code,
                        "name": name,
                        "prefix": "%s-" % identifier.key,
                        "company_id": False,
                    }
                )

            identifier.key_sequence_id = sequence

    def get_task_identifier(self):
        self.ensure_one()
        if not self.key_sequence_id:
            self._create_sequence()

        return self.key_sequence_id.next_by_code(self.code)

# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re

from odoo import api, fields, models


class ProjectIdentifier(models.Model):
    _inherit = "project.identifier"

    key_sequence_id = fields.Many2one("ir.sequence", readonly=True)

    partner_ids = fields.Many2many(
        "res.partner",
        "project_key_partner_rel",
        "project_identifier_id",
        "partner_id",
        copy=False,
    )

    code = fields.Char(
        "Sequence code", compute="_compute_code", store=True, readonly=True
    )

    # OVERRIDE
    @api.depends("key", "partner_ids")
    def _compute_name(self):
        """
    This functions compute the name of the identifier to provide the result:

    KEY (partner_1, partner_2, ...)
    or just :
    KEY
    :return:
        """
        for identifier in self:
            names = ", ".join(identifier.partner_ids.mapped("name"))
            identifier.name = (
                f"{identifier.key} ({names})"
                if identifier.partner_ids
                else f"{identifier.key}"
            )

    # OVERRIDE
    def _inverse_name(self):
        """
        The inverse function is used to set the key directly from what's put
        inside the name field.
        This helps provide a seemles experience when creating a new Trigram,
        as the field will mostly behave close to a Char field if you create
        a new Trigram.
        :return:
        """
        for identifier in self:
            if identifier.name:
                key = re.sub(r"\([^)]*\)", "", identifier.name.replace(" ", ""))
                identifier.key = key

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

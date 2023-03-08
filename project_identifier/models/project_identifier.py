# © 2020-2022 Aurore Chevalier
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectIdentifier(models.Model):
    _name = "project.identifier"
    _description = "Unique Identifier"

    active = fields.Boolean(default=True)
    name = fields.Char(compute="_compute_name", inverse="_inverse_name", store=True)
    key = fields.Char(
        "Project Identifier Key",
        required=True,
        help="Alphanumeric key that will be used for the project identifier",
    )
    partner_ids = fields.Many2many(
        "res.partner",
        "project_key_partner_rel",
        "project_identifier_id",
        "partner_id",
        string="Partners",
        required=True,
        copy=False,
    )

    _sql_constraints = [
        ("unique_key", "UNIQUE (key)", _("Project Identifier key should be unique"))
    ]

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

    @api.constrains("key")
    def check_key(self):
        for identifier in self:
            if not identifier.key.isalnum():
                raise ValidationError(_("The identifier must be alphanumeric!"))

# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectIdentifier(models.Model):
    _name = "project.identifier"
    _description = "Unique Identifier"

    active = fields.Boolean(default=True)
    name = fields.Char(compute="_compute_name", inverse="_inverse_name", store=True)

    key = fields.Char("Project Identifier Key", required=True)

    _sql_constraints = [
        ("unique_key", "UNIQUE (key)", _("Project Identifier key should be unique"))
    ]

    @api.model
    def create(self, vals):
        if "name" in vals and "key" not in vals:
            vals["key"] = re.sub(r"\([^)]*\)", "", vals["name"].replace(" ", ""))
        if not vals["key"].isalnum():
            raise ValidationError(_("The identifier must be alphanumeric!"))

        return super(ProjectIdentifier, self).create(vals)

    @api.depends("key")
    def _compute_name(self):
        for identifier in self:
            identifier.name = f"{identifier.key}"

    def _inverse_name(self):
        for identifier in self:
            if identifier.name:
                identifier.key = identifier.name

    @api.constrains("key")
    def check_key(self):
        for identifier in self:
            if not identifier.key.isalnum():
                raise ValidationError(_("The identifier must be alphanumeric!"))

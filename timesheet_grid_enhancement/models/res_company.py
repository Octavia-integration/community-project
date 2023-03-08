# © 2022 Albin Gilles
# © 2022 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    timesheet_grid_show_empty_lines = fields.Boolean(
        "Show Empty Lines",
        default=True,
        help="If checked, show task even if no timesheet have been recorded in the period",
    )

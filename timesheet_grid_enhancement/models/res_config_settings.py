# © 2022 Albin Gilles
# © 2022 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    timesheet_grid_show_empty_lines = fields.Boolean(
        "Show Empty Lines",
        related="company_id.timesheet_grid_show_empty_lines",
        readonly=False,
        config_parameter="timesheet_grid_enhancement.timesheet_grid_show_empty_lines",
        help="If checked, show task even if no timesheet have been recorded in the period",
    )

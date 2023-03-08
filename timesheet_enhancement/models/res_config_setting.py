# © 2022 Alexandre Van Ommeslaghe
# © 2022 Niboo SPRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    timesheet_min_duration_all = fields.Boolean(
        "Apply to all timesheets",
        config_parameter="timesheet_enhancement.timesheet_min_duration_all",
    )

# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = "project.task.create.timesheet"

    @api.onchange("time_spent")
    def _onchange_time_spent(self):
        self.ensure_one()
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("timesheet_enhancement.timesheet_min_duration_all")
        ):
            minimum_duration = (
                int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("timesheet_grid.timesheet_min_duration", 0)
                )
                / 60
            )
            rounding = (
                int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("timesheet_grid.timesheet_rounding", 0)
                )
                / 60
            )
            if not self.time_spent >= minimum_duration:
                # min_duration is in minute
                self.time_spent = minimum_duration
            modulo = self.time_spent % rounding
            if modulo:
                hours = self.time_spent - modulo + rounding
                self.time_spent = hours

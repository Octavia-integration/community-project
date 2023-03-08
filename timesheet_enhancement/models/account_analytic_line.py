# © 2022 Alexandre Van Ommeslaghe
# © 2022 Niboo SPRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    show_archived_tasks = fields.Boolean()

    @api.onchange("unit_amount")
    def _onchange_unit_amount(self):
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
            if not self.unit_amount >= minimum_duration:
                # min_duration is in minute
                self.unit_amount = minimum_duration
            modulo = self.unit_amount % rounding
            if modulo:
                hours = self.unit_amount - modulo + rounding
                self.unit_amount = hours

    @api.constrains("unit_amount")
    def check_time_logged(self):
        """
        Check that unit amount of lines isn't negative.
        :return: ValidationError if a line has negative amount
        """
        if any(line.is_timesheet and line.unit_amount < 0 for line in self):
            raise ValidationError(_("The Duration cannot be negative."))

    @api.onchange("show_archived_tasks", "project_id")
    def onchange_show_archived_tasks(self):
        self.ensure_one()
        domain = [("company_id", "=", self.company_id.id)]
        if self.show_archived_tasks:
            domain.append(("active", "in", (True, False)))
        if self.project_id:
            domain.append(("project_id", "=", self.project_id.id))
        return {"domain": {"task_id": domain}}

# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = "project.task.create.timesheet"

    so_line = fields.Many2one(
        "sale.order.line",
        string="Sales Order Item",
        domain=lambda self: self._default_sale_line_domain(),
    )

    def _default_sale_line_domain(self):
        """
        This is only used for delivered quantity of SO line based
        on analytic line, and timesheet
        (see sale_timesheet). This can be override to allow further customization.
        """
        return [("qty_delivered_method", "=", "analytic")]

    @api.model
    def default_get(self, fields):
        result = super(ProjectTaskCreateTimesheet, self).default_get(fields)
        result.pop("description", None)
        return result

    def save_timesheet(self):
        # Not calling super as def deprecated in timesheet_grid.
        # The wizard has to be moved to timesheet_grid in master.
        values = {
            'task_id': self.task_id.id,
            'project_id': self.task_id.project_id.id,
            'date': fields.Date.context_today(self),
            'name': self.description,
            'user_id': self.env.uid,
            'unit_amount': self.task_id._get_rounded_hours(self.time_spent * 60),
            'so_line': self.so_line.id
        }
        self.task_id.user_timer_id.unlink()
        return self.env['account.analytic.line'].create(values)

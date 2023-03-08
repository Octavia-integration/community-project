# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api

from odoo.addons.sale_timesheet.models.sale_order import SaleOrder


@api.depends("tasks_ids")
def _compute_timesheet_ids(self):
    """set timesheet_ids and timesheet_count fields acording to the linked
    tasks
    """
    for order in self:
        # PATCH START: remove condition with analytic account
        order.timesheet_ids = self.env["account.analytic.line"].search(
            [
                ("so_line", "in", order.order_line.ids),
                ("amount", "<=", 0.0),
                ("project_id", "!=", False),
            ]
        )
        # PATCH END
        order.timesheet_count = len(order.timesheet_ids)


old_method_2 = SaleOrder._compute_timesheet_ids
SaleOrder._compute_timesheet_ids = _compute_timesheet_ids

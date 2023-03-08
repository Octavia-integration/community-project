# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api

from odoo.addons.sale_project.models.sale_order import SaleOrder

@api.depends(
    "order_line.product_id.project_id", "order_line.product_id.project_id.task_ids"
)
def _compute_tasks_ids(self):
    """overrides the previous compute to include
     the task linked directly by a SO. We must use a monkey patch
     since the line "order.tasks_ids =" will trigger a constrains that will
     unlink the tasks not in "tasks_ids" from the SO"""
    for order in self:
        # PATCH START
        order.tasks_ids = self.env["project.task"].search(
            [
                "|",
                ("sale_line_id", "in", order.order_line.ids),
                ("sale_order_id", "=", order.id),
            ]
        )
        # PATCH END
        order.tasks_count = len(order.tasks_ids)


old_method_1 = SaleOrder._compute_tasks_ids
SaleOrder._compute_tasks_ids = _compute_tasks_ids

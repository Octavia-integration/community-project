# © 2020 Sam Lefever, Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.depends("project_id.pricing_type")
    def _compute_display_sale_order(self):
        for task in self:
            task.is_sale_order_to_display = task.project_id.pricing_type in [
                "no",
                "selected_rate",
            ]

    @api.depends(
        "pricing_type", "project_id.sale_order_id.state", "sale_order_id.state"
    )
    def _compute_can_timesheet(self):
        for task in self:
            order = task.project_id.sale_order_id
            if task.pricing_type == "task_rate" and order:
                task.can_timesheet = order.state in ["sale","done"]
            elif task.pricing_type == "selected_rate" and task.sale_order_id:
                task.can_timesheet = task.sale_order_id.state in ["sale", "done"]
            else:  # Includes 'no'
                task.can_timesheet = True

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sales Order",
        domain="['|',"
        "('partner_id', '=', partner_id),"
        "('partner_id.commercial_partner_id', '=', partner_id)]",
        compute=False,
        help="Sales order to which the task is linked.",
    )
    is_sale_order_to_display = fields.Boolean(compute=_compute_display_sale_order)
    can_timesheet = fields.Boolean(compute=_compute_can_timesheet, store=True)


    @api.onchange("partner_id")
    def check_sale_order_is_linked(self):
        for task in self:
            if not task.partner_id or (
                not task.sale_order_id.partner_id == task.partner_id
                and not task.sale_order_id.partner_id.commercial_partner_id
                == task.partner_id
            ):
                task.sale_order_id = False

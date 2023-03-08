# © 2020 Sam Lefever, Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("order_line.product_id.service_tracking")
    def _compute_visible_project(self):
        """ Users should be able to select a project_id on the SO
        if at least one SO line has a product with its service tracking
        configured as 'task_in_project' """
        for order in self:
            order.visible_project = any(
                service_tracking in ("task_in_project", "no")
                for service_tracking in order.order_line.mapped(
                    "product_id.service_tracking"
                )
            )

    tasks_ids = fields.One2many(
        "project.task", "sale_order_id", string="Tasks associated to this sale"
    )
    project_id = fields.Many2one(
        domain="[('analytic_account_id', '!=', False),"
               " ('company_id', '=', company_id)]",
        help="Select a project on which tasks can be created.",
    )

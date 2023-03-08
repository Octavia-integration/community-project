# © 2020 Sam Lefever
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    sale_order_ids = fields.Many2many(
        "sale.order",
        compute="_compute_sale_order_ids",
        store=True,
        string="Sales Orders",
        domain="[('partner_id', '=', partner_id)]",
        readonly=True,
        copy=False,
        help="Sales orders to which the project is linked.",
    )
    pricing_type = fields.Selection(selection_add=[("selected_rate", "Selected Rate")])

    @api.depends("task_ids.sale_order_id")
    def _compute_sale_order_ids(self):
        for project in self:
            sale_order_ids = self.env["sale.order"]
            for task in project.task_ids:
                sale_order_ids += task.sale_order_id
            project.sale_order_ids = sale_order_ids

    @api.depends(
        "sale_order_ids", "sale_order_id", "sale_line_id",
        "sale_line_employee_ids", "allow_billable"
    )
    def _compute_pricing_type(self):
        billable_projects = self.filtered('allow_billable')
        for project in billable_projects:
            if project.sale_line_employee_ids:
                project.pricing_type = 'employee_rate'
            elif project.sale_line_id:
                project.pricing_type = 'fixed_rate'
            elif project.sale_order_ids:
                project.pricing_type = 'selected_rate'
            else:
                project.pricing_type = 'selected_rate'
        (self - billable_projects).update({'pricing_type': False})

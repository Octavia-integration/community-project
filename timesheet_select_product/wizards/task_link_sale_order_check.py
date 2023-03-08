# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class TaskLinkSaleOrderWizard(models.TransientModel):
    _name = "task.link.sale.order.check.wizard"
    _description = "Link Tasks to a sale order"

    tasks_ids = fields.Many2many("project.task")
    sale_order_id = fields.Many2one("sale.order", required=True)

    def link_sale_order(self):
        self.ensure_one()
        self.tasks_ids.write({"sale_order_id": self.sale_order_id})

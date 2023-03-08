# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class TaskLinkSaleOrderWizard(models.TransientModel):
    _name = "task.link.sale.order.wizard"
    _description = "Link Tasks to a sale order"

    sale_order_id = fields.Many2one("sale.order", required=True)
    tasks_ids = fields.Many2many("project.task")

    def check_link_sale_order(self):
        self.ensure_one()
        previously_linked_tasks_ids = self.env["project.task"]
        for task in self.tasks_ids:
            if task.sale_order_id:
                previously_linked_tasks_ids |= task

        self.tasks_ids -= previously_linked_tasks_ids
        self.link_sale_order()

        if previously_linked_tasks_ids:
            return {
                "name": "WARNING: Update previous Sale Orders?",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "task.link.sale.order.check.wizard",
                "target": "new",
                "context": {
                    "default_tasks_ids": previously_linked_tasks_ids.ids,
                    "default_sale_order_id": self.sale_order_id.id,
                },
            }

    def link_sale_order(self):
        self.ensure_one()
        self.tasks_ids.write({"sale_order_id": self.sale_order_id})

# © 2016 Pierre Faniel, Sam Lefever, Chevalier Aurore
# © 2016 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    task_id = fields.Many2one(
        "project.task",
        domain="[('company_id', 'in', company_id),"
        " ('project_id', '=?', project_id),"
        " ('can_timesheet', '=', True)]",
    )

    timesheet_invoice_line_id = fields.Many2one("account.move.line", "Invoice line")
    invoice_state = fields.Selection(related="timesheet_invoice_id.state",
                                     store=True)

    @api.constrains("so_line")
    def _check_sale_line_is_required(self):
        for aal in self:
            if aal.so_line:
                aal.product_id = aal.so_line.product_id
            task = aal.task_id
            if task.pricing_type == "selected_rate" \
                    and task.sale_order_id \
                    and task.sale_order_id.order_line != [] \
                    and not aal.so_line:
                for sale_order_line in task.sale_order_id.order_line:
                    product = sale_order_line.product_id
                    if product and product.service_policy == "delivered_timesheet":
                        raise ValidationError(
                            _(
                                "You must select one of the available sale order"
                                " line for your timesheets!"
                            )
                        )

    @api.constrains("task_id")
    def _check_task_can_timesheet(self):
        for aal in self:
            if aal.task_id and not aal.task_id.can_timesheet:
                raise ValidationError(
                    _(
                        "The selected task's Sale Order hasn't been validated"
                        " yet. You can't timesheet until it's been validated"
                        " by the client!"
                    )
                )

    @api.constrains("is_invoiceable", "timesheet_invoice_id")
    def _check_related_invoice(self):
        """
        force the invoice to resfresh when the field "is_invoiceable" is updated

        if invoice is already posted, returns an error.
        :return:
        """
        invoice_to_refresh = self.env["account.move"]
        for ts in self:
            if ts.timesheet_invoice_id:
                if (
                    ts.timesheet_invoice_id.state == "draft"
                    or not ts.is_invoiceable
                    or ts.product_id.invoice_policy != "delivery"
                ):
                    if ts.timesheet_invoice_id.id not in invoice_to_refresh.ids:
                        invoice_to_refresh += ts.timesheet_invoice_id
                else:
                    raise ValidationError(
                        _(
                            f"Unable to update {ts.timesheet_invoice_id.state} invoice"
                            f" {ts.timesheet_invoice_id.name}.\n"
                            f"-Invoice should be in 'draft' state to be updated\n"
                            f"-Timesheet shouldn't be invoicable\n"
                            f"-Product should be invoiced on 'order'\n"
                        )
                    )
        invoice_to_refresh.refresh_qty_from_timesheets()

    @api.onchange("timesheet_invoice_line_id")
    def onchange_timesheet_invoice_line_id(self):
        for line in self:
            if line.timesheet_invoice_line_id:
                line.timesheet_invoice_id = line.timesheet_invoice_line_id.move_id

    @api.onchange("task_id", "project_id")
    def onchange_task_id(self):
        self.ensure_one()
        if self.so_line.id not in self.task_id.sale_order_id.order_line.ids:
            self.so_line = False

    def remove_link_to_invoice(self):
        """
        Remove the link to the invoice and recompute
        """
        invoices = self.mapped("timesheet_invoice_id")
        self.write({"timesheet_invoice_line_id": False, "timesheet_invoice_id": False})
        invoices.refresh_qty_from_timesheets(True)
        return

    def link_to_invoice(self, invoice):
        """
        links the timesheets to the given invoice if the TS is not already
        linked to an invoice and the invoice is in a draft state

        will raise an error for the invoice if it's not in draft state and
         ignore the TS with linked invoices

        :param invoice: the invoice which will be used to link the TS
        :return:
        """

        # We ignore the TS which already have a linked invoice
        blank_timesheets = self.filtered(lambda ts: not ts.timesheet_invoice_id)
        blank_timesheets.write({"timesheet_invoice_id": invoice.id})

        inv_to_check = invoice.state != "draft"

        so_lines = blank_timesheets.mapped("so_line")
        timesheets_by_sol = dict.fromkeys(so_lines, self.env["account.analytic.line"])
        for timesheet in blank_timesheets:
            timesheets_by_sol[timesheet.so_line] += timesheet
            if inv_to_check:
                if (
                    timesheet.product_id.invoice_policy == "delivery"
                    and timesheet.is_invoiceable
                ):
                    raise ValidationError(
                        _(
                            f"The timesheet {timesheet.name} "
                            f"cannot be invoiceable and linked to a not draft invoice"
                        )
                    )

        for so_line in so_lines:
            invoice_line = invoice.invoice_line_ids.filtered(
                lambda line: line.product_id.id == so_line.product_id.id
            )
            if not invoice_line:
                vals = self.get_invoice_create_vals(
                    so_line.product_id, so_line.price_unit
                )
                invoice.write(vals)
            timesheets_by_sol[so_line].write(
                {"timesheet_invoice_line_id": invoice_line.id}
            )

        invoice.refresh_qty_from_timesheets()

    def get_invoice_create_vals(self, product, price_unit):
        """
        generate the create dict for the write function of an invoice

        :param invoice: the invoice where we right the new line

        :return: vals: a dict of vals to create a new invoice line with the
        product and qty described within the timesheet
        """
        product_uom = product.uom_id
        account_id = product.property_account_income_id
        return {
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": f"{product.display_name}",
                        "product_id": product.id,
                        "product_uom_id": product_uom.id,
                        "quantity": 0,
                        "price_unit": price_unit,
                        "tax_ids": product.taxes_id.ids,
                        "account_id": account_id.id,
                    },
                )
            ]
        }

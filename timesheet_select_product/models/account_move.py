# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression


class AccountMove(models.Model):
    _inherit = "account.move"

    def refresh_qty_from_timesheets(self, force=False):
        """
        Refresh the quantity of the line following the timesheets linked to it.
        :return:
        """
        for invoice in self:
            invoice.invoice_line_ids.refresh_qty_from_timesheets(force)

    def _link_timesheets_to_invoice(self, start_date=None, end_date=None):
        """ Search timesheets from given period and link this timesheets to the invoice

            When we create an invoice from a sale order, we need to
            link the timesheets in this sale order to the invoice.
            Then, we can know which timesheets are invoiced in the sale order.
            :param start_date: the start date of the period
            :param end_date: the end date of the period
        """
        for line in self.filtered(lambda i: i.move_type == 'out_invoice' and
                                            i.state == 'draft').invoice_line_ids:
            sale_line_delivery = line.sale_line_ids.filtered(lambda
                                                                 sol: sol.product_id.invoice_policy == 'delivery'
                                                                      and sol.product_id.service_type == 'timesheet')
            if sale_line_delivery:
                domain = line._timesheet_domain_get_invoiced_lines(
                    sale_line_delivery)
                if start_date:
                    domain = expression.AND(
                        [domain, [('date', '>=', start_date)]])
                if end_date:
                    domain = expression.AND(
                        [domain, [('date', '<=', end_date)]])
                timesheets = self.env['account.analytic.line'].sudo().search(
                    domain)
                timesheets.write({"timesheet_invoice_line_id": line.id,
                                  'timesheet_invoice_id': line.move_id.id})


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    timesheet_ids = fields.One2many(
        "account.analytic.line",
        "timesheet_invoice_line_id",
        string="Timesheets",
        readonly=True,
        copy=False,
    )
    timesheet_count = fields.Integer(
        "Number of timesheets", compute="_compute_timesheet_count"
    )

    def refresh_qty_from_timesheets(self, force=False):
        for line in self:
            if line.product_id.service_policy == "delivered_timesheet" and line.move_id.state == "draft":
                qty = 0.0
                qty_per_uom = {}
                for timesheet in line.timesheet_ids:
                    if timesheet.is_invoiceable:
                        ts_uom = timesheet.product_uom_id
                        qty_per_uom[ts_uom] = timesheet.unit_amount + qty_per_uom.get(
                            ts_uom, 0
                        )

                for uom in qty_per_uom:
                    qty += uom._compute_quantity(qty_per_uom[uom], line.product_uom_id)
                # We force the name as a param due to a caching issue
                # which could lead to the lost of the name (account_move, l 1596)
                # we make sure to do that for every line of the invoice

                # TODO: find a better way to do this or fix odoo method

                vals = {"invoice_line_ids": [(1, line.id, {"quantity": qty, "name": line.name})]}
                for invoice_line in line.move_id.invoice_line_ids:
                    if invoice_line.id != line.id:
                        vals["invoice_line_ids"].append((1, invoice_line.id, {"name": invoice_line.name}))

                if line.timesheet_ids or force:
                    line.move_id.write(vals)

    @api.depends("timesheet_ids")
    def _compute_timesheet_count(self):
        timesheet_data = self.env["account.analytic.line"].read_group(
            [("timesheet_invoice_line_id", "in", self.ids)],
            ["timesheet_invoice_line_id"],
            ["timesheet_invoice_line_id"],
        )
        mapped_data = {
            t["timesheet_invoice_line_id"][0]: t["timesheet_invoice_line_id_count"]
            for t in timesheet_data
        }
        for invoice_line in self:
            invoice_line.timesheet_count = mapped_data.get(invoice_line.id, 0)

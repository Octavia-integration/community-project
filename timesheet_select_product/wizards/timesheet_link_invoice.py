# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class TimesheetLinkInvoiceWizard(models.TransientModel):
    _name = "timesheet.link.invoice.wizard"
    _description = "Link Timesheets to an Invoice"

    invoice_id = fields.Many2one(
        "account.move",
        domain="[('move_type', 'in',"
        "('out_invoice', 'out_refund', 'in_invoice', 'in_refund')),"
        "('state', '=', 'draft'),"
        "'|',('partner_id', 'in', invoice_partner_ids),"
        "('partner_id.parent_id', 'in', invoice_partner_ids)]",
        required=True,
    )

    show_all_invoices = fields.Boolean("Display all invoices (Validated)")

    wizard_timesheet_ids = fields.Many2many("account.analytic.line")

    invoice_partner_ids = fields.Many2many(
        "res.partner", compute="_compute_invoice_partner_ids"
    )

    def link_invoice(self):
        self.ensure_one()
        self.wizard_timesheet_ids.link_to_invoice(self.invoice_id)

    @api.depends("wizard_timesheet_ids")
    def _compute_invoice_partner_ids(self):
        for record in self:
            partner_ids = record.wizard_timesheet_ids.mapped("partner_id")
            record.invoice_partner_ids = partner_ids or False

    @api.onchange("show_all_invoices")
    def onchange_show_all_invoices(self):
        self.ensure_one()
        domain = [
            ("move_type", "in", ("out_invoice", "out_refund", "in_invoice", "in_refund")),
            "|",
            ("partner_id", "in", self.invoice_partner_ids.ids),
            ("partner_id.parent_id", "in", self.invoice_partner_ids.ids),
        ]
        if not self.show_all_invoices:
            domain.append(("state", "=", "draft"))
        return {"domain": {"invoice_id": domain}}

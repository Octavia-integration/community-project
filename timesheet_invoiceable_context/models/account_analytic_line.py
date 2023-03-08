# © 2022 Sam Lefever, Chevalier Aurore
# © 2022 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    is_invoiceable_context = fields.Boolean(
        compute="_compute_is_invoiceable_context", store=True
    )
    is_invoiceable = fields.Boolean()

    @api.model
    def create(self, vals):
        """ When creating  new record, we need to set the is_invoicable from
        is_invoiceable_context AFTER it has been computed"""
        res = super(AccountAnalyticLine, self).create(vals)
        res.is_invoiceable = res.is_invoiceable_context
        return res

    @api.depends("so_line")
    def _compute_is_invoiceable_context(self):
        for aa_line in self:
            aa_line.is_invoiceable_context = False
            if bool(aa_line.so_line) and aa_line.so_line.price_unit > 0:
                order = aa_line.so_line.order_id
                if (
                    order.company_id.partner_id.commercial_partner_id
                    != order.partner_id.commercial_partner_id
                ):
                    aa_line.is_invoiceable_context = True

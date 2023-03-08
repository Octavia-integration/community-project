# © 2021 Antoine Honinckx
# © 2021 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_timesheetable = fields.Boolean(string="Timesheetable Product", default=False)

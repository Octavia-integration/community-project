# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models


class HRJob(models.Model):
    _inherit = "hr.job"

    timesheet_invoice_target = fields.Float("Invoiceable Target %")

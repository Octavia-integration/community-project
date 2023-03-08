# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    is_leave_project = fields.Boolean(related="project_id.is_leave_project",
                                      store=True)

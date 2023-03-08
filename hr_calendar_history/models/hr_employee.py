# © 2020 Sam Lefever
# © 2020 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models, api


class HREmployee(models.AbstractModel):
    _inherit = "hr.employee.base"

    workschedule_history_ids = fields.One2many("hr.calendar.history",
                                               inverse_name="employee_id",
                                               string="Work Schedule History")

    resource_calendar_id = fields.Many2one("resource.calendar",
                                           compute="_compute_resource_calendar",
                                           store=True,
                                           readonly=True,
                                           required=False)

    @api.depends('workschedule_history_ids',
                 'workschedule_history_ids.end_date',
                 'workschedule_history_ids.start_date',
                 'workschedule_history_ids.employee_id',
                 'workschedule_history_ids.workschedule_id')
    def _compute_resource_calendar(self):
        for employee in self:
            current = self.env['hr.calendar.history'].search([
                ('employee_id', '=', employee.id),
                ('start_date', '<', fields.Datetime.today()),
                '|',
                    ('end_date', '>', fields.Datetime.today()),
                    ('end_date', '=', None)])
            if current:
                employee.resource_calendar_id = current[0].workschedule_id

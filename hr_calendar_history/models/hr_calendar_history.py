# © 2020 Sam Lefever
# © 2020 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models, api, exceptions, _


class HRWorkScheduleHistory(models.Model):
    _name = "hr.calendar.history"

    start_date = fields.Date("Start date", required=True)
    end_date = fields.Date("End date")
    workschedule_id = fields.Many2one("resource.calendar", "Work Schedule",
                                      required=True)
    employee_id = fields.Many2one("hr.employee")

    @api.constrains('end_date', 'employee_id')
    def _constraint_workschedule_history_ids(self):
        for history in self:
            if history.end_date <= history.start_date:
                raise exceptions.ValidationError(
                    _('You can not have an end date before your start date'))

            wrong_history = history.search_count([('id', '!=', history.id),
                            ('employee_id', '=', history.employee_id.id),
                            '|',
                                '|',
                                    '&',
                                        ('start_date', '<=', history.start_date),
                                        ('end_date', '>=', history.start_date),
                                    '&',
                                        ('start_date', '>=', history.start_date),
                                        ('end_date', '<=', history.end_date),
                            '&',
                                ('start_date', '<=', history.end_date),
                                ('end_date', '>=', history.end_date),
                            ])

            if wrong_history:
                raise exceptions.ValidationError(
                    _('You can not have overlapping workschedule history'))

            histories = history.employee_id.workschedule_history_ids
            current = histories.filtered(lambda x: not x.end_date)
            if len(current) > 1:
                raise exceptions.ValidationError(
                    _('You can not have more than one current work schedule.'))


# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models


class HRTimesheetMonthlyAnalysis(models.Model):
    _name = "hr.timesheet.monthly.analysis.report"
    _auto = False

    date = fields.Char("Date")
    employee_id = fields.Many2one("hr.employee", "Employee")
    job_id = fields.Many2one("hr.job", "Job")
    employee_company_id = fields.Many2one("res.company", "Employee Company")
    employee_active = fields.Boolean()
    expected_log_time = fields.Float("Expected")
    actual_logged_time = fields.Float("Actual")
    leave_logged_time = fields.Float("Leave")
    invoiceable_logged_time = fields.Float("Invoiceable")
    to_invoice_logged_time = fields.Float("To Invoice")
    invoiced_logged_time = fields.Float("Invoiced")
    amount_invoiceable = fields.Float("Invoiceable Amount")
    overtime = fields.Float("Overtime")
    missing_hours = fields.Float("Missing hours")
    net_invoiceable_vs_workschedule_ratio = fields.Float("Inv./Net WS.")
    net_invoiceable_vs_timesheeted_ratio = fields.Float("Inv./Net TS")
    raw_invoiceable_vs_workschedule_ratio = fields.Float("Inv./Raw WS")
    raw_invoiceable_vs_timesheeted_ratio = fields.Float("Inv./Raw TS")

    def init(self):
        self._cr.execute(
            """
CREATE OR REPLACE VIEW %s AS (
    SELECT
       row_number() OVER () AS id,
       htar.employee_id,
       htar.job_id,
       htar.employee_company_id,
       htar.employee_active,
       SUM(htar.expected_log_time) as expected_log_time,
       SUM(htar.actual_logged_time) as actual_logged_time,
       SUM(htar.leave_logged_time) as leave_logged_time,
       SUM(htar.invoiceable_logged_time) as invoiceable_logged_time,
       SUM(htar.to_invoice_logged_time) as to_invoice_logged_time,
       SUM(htar.invoiced_logged_time) as invoiced_logged_time,
       SUM(htar.amount_invoiceable) as amount_invoiceable,
       CASE WHEN SUM(htar.missing_hours) < 0 THEN SUM(htar.missing_hours) ELSE 0 END as overtime,
       CASE WHEN SUM(htar.missing_hours) > 0 THEN SUM(htar.missing_hours) ELSE 0 END as missing_hours,
       CASE WHEN (SUM(htar.expected_log_time) - SUM(htar.leave_logged_time)) > 0 THEN (SUM(htar.invoiceable_logged_time) / (SUM(htar.expected_log_time) - SUM(htar.leave_logged_time))) * 100 ELSE 100 END as net_invoiceable_vs_workschedule_ratio,
       CASE WHEN (SUM(htar.actual_logged_time) - SUM(htar.leave_logged_time)) > 0 THEN (SUM(htar.invoiceable_logged_time) / (SUM(htar.actual_logged_time) - SUM(htar.leave_logged_time))) * 100 ELSE 100 END as net_invoiceable_vs_timesheeted_ratio,
       CASE WHEN SUM(htar.expected_log_time) > 0 THEN (SUM(htar.invoiceable_logged_time) / SUM(htar.expected_log_time)) * 100 ELSE 100 END as raw_invoiceable_vs_workschedule_ratio,
       CASE WHEN SUM(htar.actual_logged_time) > 0 THEN (SUM(htar.invoiceable_logged_time) / SUM(htar.actual_logged_time)) * 100 ELSE 100 END as raw_invoiceable_vs_timesheeted_ratio,
       to_char(DATE_TRUNC('month', htar.date), 'YYYY-MM') as date
    FROM hr_timesheet_analysis_report htar
    WHERE htar.date < (CURRENT_DATE)
    GROUP BY DATE_TRUNC('month', htar.date), htar.employee_id, htar.job_id, htar.employee_company_id, htar.employee_active
)
"""
            % self._table
        )

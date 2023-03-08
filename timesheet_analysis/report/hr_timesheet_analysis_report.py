# © 2022 Sam Lefever
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models, api


class HRTimesheetAnalysis(models.Model):
    _name = "hr.timesheet.analysis.report"
    _auto = False

    employee_id = fields.Many2one("hr.employee", "Employee")
    job_id = fields.Many2one("hr.job", "Job")
    employee_company_id = fields.Many2one("res.company", "Employee Company")
    date = fields.Date("Date")
    employee_active = fields.Boolean()
    expected_log_time = fields.Float("Expected")
    actual_logged_time = fields.Float("Actual")
    leave_logged_time = fields.Float("Leave")
    missing_hours = fields.Float("Missing Hours")
    invoiceable_logged_time = fields.Float("Invoiceable")
    to_invoice_logged_time = fields.Float("To Invoice")
    invoiced_logged_time = fields.Float("Invoiced")
    amount_invoiceable = fields.Float("Invoiceable Amount")
    raw_invoiceable_vs_workschedule_ratio = fields.Float("Invoiceable / Workschedule")
    raw_invoiceable_vs_timesheeted_ratio = fields.Float("Invoiceable / Timesheeted")

    @api.model
    def read_group(self, domain, fields, groupby,
                   offset=0, limit=None, orderby=False, lazy=True):
        if not fields:
            fields.append('expected_log_time:sum')

        fields_to_remove = []

        if "raw_invoiceable_vs_workschedule_ratio:sum" in fields:
            fields.remove("raw_invoiceable_vs_workschedule_ratio:sum")
        if "raw_invoiceable_vs_timesheeted_ratio:sum" in fields:
            fields.remove("raw_invoiceable_vs_timesheeted_ratio:sum")
        fields.extend(fields_to_remove)

        res = super(HRTimesheetAnalysis, self).read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )

        if groupby:
            for line in res:
                if line.get("expected_log_time") and line.get("invoiceable_logged_time"):
                    line["raw_invoiceable_vs_workschedule_ratio"] = (
                        line["invoiceable_logged_time"] / line["expected_log_time"] * 100
                    )
                if line.get("invoiceable_logged_time") and line.get("actual_logged_time"):
                    line["raw_invoiceable_vs_timesheeted_ratio"] = (
                        line["invoiceable_logged_time"] / line["actual_logged_time"] * 100
                    )
        return res

    def init(self):
        self._cr.execute(
            """
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () AS id,
        he.id as employee_id,
        hj.id as job_id,
        rc.id as employee_company_id,
        heltr.date::date,
        he.active as employee_active,
        COALESCE(heltr.expected_log_time, 0) as expected_log_time,
        SUM(aal.unit_amount) as actual_logged_time,
        SUM(CASE aal.is_leave_project WHEN true THEN aal.unit_amount ELSE 0 END) as leave_logged_time,
        COALESCE(heltr.expected_log_time, 0) - COALESCE(SUM(aal.unit_amount), 0) as missing_hours,
        SUM(aal.unit_amount * CASE aal.is_invoiceable_context WHEN true THEN 1 WHEN false THEN 0 END) as invoiceable_logged_time,
        SUM(aal.unit_amount * CASE aal.is_invoiceable_context WHEN true THEN 1 WHEN false THEN 0 END) as to_invoice_logged_time,
        SUM(aal.unit_amount * CASE WHEN aal.timesheet_invoice_id IS NULL THEN 0 ELSE CASE WHEN aal.is_invoiceable = true THEN 1 ELSE 0 END END) as invoiced_logged_time,
        SUM(sol.price_unit * aal.unit_amount / CASE WHEN sol.product_uom = 5 THEN 1 ELSE 8 END) as amount_invoiceable

    FROM hr_employee he
        LEFT JOIN hr_job hj ON hj.id = he.job_id
        LEFT JOIN res_company rc ON rc.id = he.company_id
        LEFT JOIN hr_calendar_history hch ON he.id = hch.employee_id
        LEFT JOIN hr_expected_log_time_report heltr ON (hch.workschedule_id = heltr.calendar_id OR heltr.calendar_id IS NULL) AND heltr.date >= hch.start_date AND (heltr.date <= hch.end_date OR hch.end_date IS NULL)
        LEFT JOIN account_analytic_line aal ON aal.employee_id = he.id AND aal.date = heltr.date AND aal.project_id IS NOT NULL
        LEFT JOIN sale_order_line sol ON sol.id = aal.so_line
    GROUP BY he.id, hj.id, rc.id, heltr.date, he.active, heltr.expected_log_time
)
"""
            % self._table
        )

# © 2020 Sam Lefever
# © 2020 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import fields, models


class HRExpectedLogTime(models.Model):
    _name = "hr.expected.log.time.report"
    _auto = False

    calendar_id = fields.Many2one("resource.calendar", "Work Schedule")
    date = fields.Date("Date")
    day_of_week = fields.Float()
    expected_log_time = fields.Float()

    def init(self):
        self._cr.execute(
            """
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () AS id,
        resource_calendar_by_day.id as calendar_id,
        resource_calendar_by_day.date,
        resource_calendar_by_day.day_of_week,
        SUM(rca.hour_to - rca.hour_from) as expected_log_time
    FROM
        (SELECT
            rc.id,
            s.day::date as date,
            extract(isodow from day) as day_of_week
        FROM
            Generate_series('2015/01/01'::date,'2030/12/31'::date,'1 day') AS s(day),
            resource_calendar rc) as resource_calendar_by_day
        LEFT JOIN resource_calendar_attendance rca ON CAST(rca.dayofweek AS double precision) + 1 = resource_calendar_by_day.day_of_week AND rca.calendar_id = resource_calendar_by_day.id

    GROUP BY resource_calendar_by_day.date, resource_calendar_by_day.day_of_week, resource_calendar_by_day.id
)
"""
            % self._table
        )

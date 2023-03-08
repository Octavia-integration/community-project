# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import fields

from odoo.addons.hr_timesheet.wizard.project_task_create_timesheet import (
    ProjectTaskCreateTimesheet,
)


def save_timesheet(self):
    """
    overides the default odoo method to add a field needed for a constrain
    :param self:
    :return:
    """
    # PATCH START
    # we add the so_line field to the values
    values = {
        "task_id": self.task_id.id,
        "project_id": self.task_id.project_id.id,
        "date": datetime.now(),
        "name": self.description,
        "user_id": self.env.uid,
        "unit_amount": self.time_spent,
        "so_line": self.so_line.id,
    }
    # PATCH END
    self.task_id.write(
        {
            "timesheet_timer_start": False,
            "timesheet_timer_pause": False,
            "timesheet_timer_last_stop": fields.datetime.now(),
        }
    )
    return self.env["account.analytic.line"].create(values)


old_save_timesheet = ProjectTaskCreateTimesheet.save_timesheet
ProjectTaskCreateTimesheet.save_timesheet = save_timesheet

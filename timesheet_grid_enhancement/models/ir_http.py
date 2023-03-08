# © 2022 Albin Gilles
# © 2022 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """ The timesheet grid view needs to know if we want to show empty lines
            and which javascript widget to apply, depending on the current company.
        """
        result = super(Http, self).session_info()
        if self.env.user.has_group("base.group_user"):
            company = self.env.company

            result[
                "timesheet_grid_show_empty_lines"
            ] = company.timesheet_grid_show_empty_lines
        return result

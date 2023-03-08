# 2020 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    customer_name = fields.Char(string="Customer Name", related="partner_id.name")

    def name_get(self):
        """
        Add Customer name into the project's display name
        """
        result = []
        for project in self:
            name = project.name
            if project.partner_id:
                name = project.partner_id.name + " - " + name

            result.append((project.id, name))

        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """
        Allows to search projects by customer name
        """
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("customer_name", operator, name)]
        projects = self.search(domain + args, limit=limit)
        if projects:
            return projects.name_get()
        return super(ProjectProject, self).name_search(name, args, operator, limit)

# © 2022 Jérémy Van Driessche
# © 2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import _
from odoo.osv import expression

from odoo.addons.project.controllers.portal import ProjectCustomerPortal


class ProjectCustomerPortal(ProjectCustomerPortal):
    def _task_get_searchbar_sortings(self):
        res = super()._task_get_searchbar_sortings()
        res["identifier"] = {
            "label": _("Identifier"),
            "order": "identifier_number",
            "sequence": 11,
        }
        return res

    def _task_get_searchbar_inputs(self):
        res = super()._task_get_searchbar_inputs()
        res["identifier"] = {
            "input": "identifier",
            "label": _("Search in Identifiers"),
            "order": 11,
        }
        return res

    def _task_get_search_domain(self, search_in, search):
        search_domain = [super()._task_get_search_domain(search_in, search)]
        if search_in in ("content", "all"):
            search_domain.append([("identifier", "ilike", search)])
        if search_in in ("identifier", "all"):
            search_domain.append([("identifier", "ilike", search)])
        return expression.OR(search_domain)

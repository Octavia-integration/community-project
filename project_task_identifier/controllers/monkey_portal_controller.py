# © 2021-2022 Aurore Chevalier
# © 2021-2022 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.project.controllers.portal import ProjectCustomerPortal


@http.route(
    ["/my/projects", "/my/projects/page/<int:page>"],
    type="http",
    auth="user",
    website=True,
)
def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
    values = self._prepare_portal_layout_values()
    Project = request.env["project.project"]
    domain = []

    # NIBOO PATCH START
    searchbar_sortings = {
        "date": {"label": _("Newest"), "order": "create_date desc"},
        "name": {"label": _("Name"), "order": "project_key,name"},
    }
    # NIBOO PATCH END

    if not sortby:
        sortby = "date"
    order = searchbar_sortings[sortby]["order"]

    if date_begin and date_end:
        domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

    # projects count
    project_count = Project.search_count(domain)
    # pager
    pager = portal_pager(
        url="/my/projects",
        url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
        total=project_count,
        page=page,
        step=self._items_per_page,
    )

    # content according to pager and archive selected
    projects = Project.search(
        domain, order=order, limit=self._items_per_page, offset=pager["offset"]
    )
    request.session["my_projects_history"] = projects.ids[:100]

    values.update(
        {
            "date": date_begin,
            "date_end": date_end,
            "projects": projects,
            "page_name": "project",
            "default_url": "/my/projects",
            "pager": pager,
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        }
    )
    return request.render("project.portal_my_projects", values)


old_portal_my_projects = ProjectCustomerPortal.portal_my_projects
ProjectCustomerPortal.portal_my_projects = portal_my_projects

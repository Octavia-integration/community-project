# © 2021 Aurore Chevalier
# © 2021 Niboo SRL (<https://www.niboo.com/>)
# License Other proprietary

from collections import OrderedDict
from operator import itemgetter

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.project.controllers.portal import CustomerPortal


@http.route(
    ["/my/projects", "/my/projects/page/<int:page>"],
    type="http",
    auth="user",
    website=True,
)
def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
    """
    Monkey patch for the main method to update the order by name
    Check # NIBOO PATCH START and # NIBOO PATCH END to see
    where modifications are located
    1 modifications dones
    """
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

    # archive groups - Default Group By 'create_date'
    archive_groups = (
        self._get_archive_groups("project.project", domain)
        if values.get("my_details")
        else []
    )
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
            "archive_groups": archive_groups,
            "default_url": "/my/projects",
            "pager": pager,
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        }
    )
    return request.render("project.portal_my_projects", values)


@http.route(
    ["/my/tasks", "/my/tasks/page/<int:page>"], type="http", auth="user", website=True
)
def portal_my_tasks(
    self,
    page=1,
    date_begin=None,
    date_end=None,
    sortby=None,
    filterby=None,
    search=None,
    search_in="content",
    groupby="project",
    **kw
):
    """
    Monkey patch for the main method to add the search for identifiers
    Check # NIBOO PATCH START and # NIBOO PATCH END to see
    where modifications are located
    2 modifications dones
    """
    values = self._prepare_portal_layout_values()
    searchbar_sortings = {
        "date": {"label": _("Newest"), "order": "create_date desc"},
        "name": {"label": _("Title"), "order": "name"},
        "stage": {"label": _("Stage"), "order": "stage_id"},
        "update": {
            "label": _("Last Stage Update"),
            "order": "date_last_stage_update desc",
        },
        "identifier": {"label": _("Identifier"), "order": "identifier_number"},
    }
    searchbar_filters = {"all": {"label": _("All"), "domain": []}}
    # NIBOO PATCH START
    searchbar_inputs = {
        "content": {
            "input": "content",
            "label": _('Search <span class="nolabel"> (in Content)</span>'),
        },
        "message": {"input": "message", "label": _("Search in Messages")},
        "customer": {"input": "customer", "label": _("Search in Customer")},
        "stage": {"input": "stage", "label": _("Search in Stages")},
        "identifier": {"input": "identifier", "label": _("Search in Identifiers")},
        "all": {"input": "all", "label": _("Search in All")},
    }
    # NIBOO PATCH END
    searchbar_groupby = {
        "none": {"input": "none", "label": _("None")},
        "project": {"input": "project", "label": _("Project")},
    }

    # extends filterby criteria with project the customer has access to
    projects = request.env["project.project"].search([])
    for project in projects:
        searchbar_filters.update(
            {
                str(project.id): {
                    "label": project.name,
                    "domain": [("project_id", "=", project.id)],
                }
            }
        )

    # extends filterby criteria with project (criteria name is the project id)
    # Note: portal users can't view projects they don't follow
    project_groups = request.env["project.task"].read_group(
        [("project_id", "not in", projects.ids)], ["project_id"], ["project_id"]
    )
    for group in project_groups:
        proj_id = group["project_id"][0] if group["project_id"] else False
        proj_name = group["project_id"][1] if group["project_id"] else _("Others")
        searchbar_filters.update(
            {
                str(proj_id): {
                    "label": proj_name,
                    "domain": [("project_id", "=", proj_id)],
                }
            }
        )

    # default sort by value
    if not sortby:
        sortby = "date"
    order = searchbar_sortings[sortby]["order"]
    # default filter by value
    if not filterby:
        filterby = "all"
    domain = searchbar_filters.get(filterby, searchbar_filters.get("all"))["domain"]

    # archive groups - Default Group By 'create_date'
    archive_groups = (
        self._get_archive_groups("project.task", domain)
        if values.get("my_details")
        else []
    )
    if date_begin and date_end:
        domain += [("create_date", ">", date_begin), ("create_date", "<=", date_end)]

    # search
    if search and search_in:
        search_domain = []
        # NIBOO PATCH START
        if search_in in ("content", "all"):
            search_domain = OR(
                [
                    search_domain,
                    [
                        "|",
                        "|",
                        ("name", "ilike", search),
                        ("description", "ilike", search),
                        ("identifier", "ilike", search),
                    ],
                ]
            )
        if search_in in ("customer", "all"):
            search_domain = OR([search_domain, [("partner_id", "ilike", search)]])
        if search_in in ("message", "all"):
            search_domain = OR([search_domain, [("message_ids.body", "ilike", search)]])
        if search_in in ("stage", "all"):
            search_domain = OR([search_domain, [("stage_id", "ilike", search)]])
        if search_in in ("identifier", "all"):
            search_domain = OR([search_domain, [("identifier", "ilike", search)]])
        # NIBOO PATCH END
        domain += search_domain

    # task count
    task_count = request.env["project.task"].search_count(domain)
    # pager
    pager = portal_pager(
        url="/my/tasks",
        url_args={
            "date_begin": date_begin,
            "date_end": date_end,
            "sortby": sortby,
            "filterby": filterby,
            "search_in": search_in,
            "search": search,
        },
        total=task_count,
        page=page,
        step=self._items_per_page,
    )
    # content according to pager and archive selected
    if groupby == "project":
        order = (
            "project_id, %s" % order
        )  # force sort on project first to group by project in view
    tasks = request.env["project.task"].search(
        domain,
        order=order,
        limit=self._items_per_page,
        offset=(page - 1) * self._items_per_page,
    )
    request.session["my_tasks_history"] = tasks.ids[:100]
    if groupby == "project":
        grouped_tasks = [
            request.env["project.task"].concat(*g)
            for k, g in groupbyelem(tasks, itemgetter("project_id"))
        ]
    else:
        grouped_tasks = [tasks]

    values.update(
        {
            "date": date_begin,
            "date_end": date_end,
            "grouped_tasks": grouped_tasks,
            "page_name": "task",
            "archive_groups": archive_groups,
            "default_url": "/my/tasks",
            "pager": pager,
            "searchbar_sortings": searchbar_sortings,
            "searchbar_groupby": searchbar_groupby,
            "searchbar_inputs": searchbar_inputs,
            "search_in": search_in,
            "sortby": sortby,
            "groupby": groupby,
            "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
            "filterby": filterby,
        }
    )
    return request.render("project.portal_my_tasks", values)


old_portal_my_projects = CustomerPortal.portal_my_projects
old_portal_my_tasks = CustomerPortal.portal_my_tasks
CustomerPortal.portal_my_projects = portal_my_projects
CustomerPortal.portal_my_tasks = portal_my_tasks

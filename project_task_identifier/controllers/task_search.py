# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License Other proprietary

from odoo import http

# This dict will be used to search on the correct field on the model
# Only model where the field is not partner_id are required.
MAPPED_PARTNER_FIELDS = {
    "fleet.vehicle": "driver_id",
    "hr.employee": "user_id.partner_id",
}

MAPPED_IDENTIFIER_FIELDS = {}


class TaskController(http.Controller):
    environment = False
    company_ids = False

    @http.route("/project_task_identifier/get_task_link", type="json", auth="user")
    def task_search(self, key, company_ids, **kw):
        """
        Direct task search with full identifier.
        This one search in archived tasks too

        :param key: the full identifier
        :param company_ids: The ids of the companies for which whe should search
         the tasks in
        :param kw:
        :return: -the action to open the view if a task was found
                 -False if nothing was found
        """
        self.environment = http.request.env

        self.company_ids = (
            company_ids if company_ids else self.environment.user.company_ids.ids
        )

        task = self.environment["project.task"].search(
            [
                ("identifier", "=ilike", key),
                ("active", "in", [True, False]),
                ("company_id", "in", self.company_ids),
            ]
        )
        return self.get_action(task)

    @http.route(
        "/project_task_identifier/get_task_link_with_model", type="json", auth="user"
    )
    def task_search_with_model(self, key_int, model, record_id, company_ids, **kw):
        """
        Refined task search with number only.
        This won't search in the archived tasks but will try to gather as
        much information fro the model & record_id as possible to provide a
        satisfactory answer

        :param key_int: the number in the task identifier
        :param model: The current model of the view where we should grab
                      the res partner
        :param record_id: The id of the current record of the 'model' displayed
        :param company_ids: The ids of the companies for which whe should search
         the tasks in
        :param kw:
        :return: -the action to open a tree view if more than 1 was found
                 -the action to open a form view if only 1 task was found
                 -False if nothing was found
        """
        self.environment = http.request.env
        self.company_ids = (
            company_ids if company_ids else self.environment.user.company_ids.ids
        )

        if model and record_id:
            search_record = self.environment[model].browse(record_id).exists()

            if search_record:
                # First, we check if the model has a direct identifier field on it
                tasks = self.task_search_with_project_identifier_id(
                    key_int, model, search_record
                )
                if tasks:
                    return self.get_action(tasks)

                # Then, we look for a linked partner
                tasks = self.task_search_with_partner_id(key_int, model, search_record)
                if tasks:
                    return self.get_action(tasks)

        # If Nothing shows up, we simply try to match the input
        # to as many tasks as possible

        tasks = self.environment["project.task"].search(
            [
                ("identifier", "=like", f"%-{key_int}"),
                ("company_id", "in", self.company_ids),
            ]
        )

        return self.get_action(tasks)

    def task_search_with_project_identifier_id(self, key_int, model, search_record):
        """
        Search for a project_identifier_id on the record using
        MAPPED_IDENTIFIER_FIELDS.
        If the search_record isn't a project_identifier, isn't in
        MAPPED_IDENTIFIER_FIELDS and does not have a project_identifier_id
        field, returns false

        :param search_record: the record to look_up
        :return: a list of tasks or false
        """
        identifier = False

        if model == "project.identifier":
            identifier = search_record
        elif model in MAPPED_IDENTIFIER_FIELDS:
            identifier = search_record.mapped(MAPPED_IDENTIFIER_FIELDS[model])
        elif "project_identifier_id" in search_record._fields:
            identifier = search_record.project_identifier_id

        if identifier:
            key = f"{identifier.key}-{key_int}"

            return self.environment["project.task"].search(
                [("identifier", "=", key), ("company_id", "in", self.company_ids)]
            )
        return False

    def task_search_with_partner_id(self, key_int, model, search_record):
        """
        Search for a partner_id on the record using MAPPED_PARTNER_FIELDS.
        If the search_record isn't a res_partner, isn't in
        MAPPED_PARTNER_FIELDS and does not have a partner_id field,
         returns false

        :param search_record: the record to look_up
        :return: a list of tasks or false
        """
        partner = False

        if model == "res.partner":
            partner = search_record
        elif model in MAPPED_PARTNER_FIELDS:
            partner = search_record.mapped(MAPPED_PARTNER_FIELDS[model])
        elif "partner_id" in search_record._fields:
            partner = search_record.partner_id

        if partner and partner.project_key_ids:
            keys = [
                f"{project_key.key}-{key_int}"
                for project_key in partner.project_key_ids
            ]

            return self.environment["project.task"].search(
                [("identifier", "in", keys), ("company_id", "in", self.company_ids)]
            )
        return False

    def get_action(self, tasks):
        """
        generate the action dict from the given tasks
        :param tasks: the task we want to display in the action
        :return: action: a dict that can be used to launch an action showing
                        the matching task(s)
        """
        task_count = len(tasks)
        if task_count == 0:
            return False
        elif task_count == 1:
            return {
                "res_id": tasks.id,
                "res_model": "project.task",
                "type": "ir.actions.act_window",
                "views": [[False, "form"]],
                "target": "current",
                "context": {"active_id": tasks.id},
            }
        return {
            "name": "Search Results",
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "views": [[False, "list"], [False, "form"]],
            "target": "current",
            "domain": [["id", "in", tasks.ids]],
        }

# © 2020-2022 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    identifier = fields.Char("Identifier", compute="_compute_identifier", store=True)
    is_created = fields.Boolean(
        "Is Created", default=False, compute="_compute_is_created"
    )
    project_identifier_id = fields.Many2one(
        related="project_id.project_identifier_id", readonly=True
    )
    identifier_number = fields.Integer(compute="_compute_identifier_number", store=True)

    @api.depends("project_id.project_identifier_id")
    def _compute_identifier(self):
        for task in self:
            if (
                not task.id
                or not task.project_identifier_id
                or (task.identifier and not self.env.context.get("force_update"))
            ):
                continue

            task.identifier = task.project_identifier_id.get_task_identifier()

    @api.depends("identifier")
    def _compute_identifier_number(self):
        for task in self:
            if task.identifier:
                task.identifier_number = int(task.identifier.rsplit('-', 1)[1])
            else:
                task.identifier_number = 0

    @api.depends("project_identifier_id")
    def _compute_is_created(self):
        for task in self:
            task.is_created = False
            if task.id:
                task.is_created = True

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("identifier", operator, name)]

        pos = self.search(domain + args, limit=limit)
        return pos.name_get()

    @api.depends("name", "identifier")
    def name_get(self):
        result = []
        for task in self:
            name = f"{task.identifier} - {task.name}" if task.identifier else task.name
            result.append((task.id, name))
        return result

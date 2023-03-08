# © 2020 Pierre Faniel, Curatolo Gabriel, Pierre Gillissen
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTaskStep(models.Model):
    _name = "project.task.step"
    _order = "sequence"
    _description = "step"

    active = fields.Boolean(default=True)

    name = fields.Char("Name", required=True)
    next_step_ids = fields.Many2many(
        "project.task.step",
        "project_task_step_rel",
        "previous_step_id",
        "next_step_id",
        "Next steps",
    )
    previous_step_ids = fields.Many2many(
        "project.task.step",
        "project_task_step_rel",
        "next_step_id",
        "previous_step_id",
        "Previous steps",
    )
    sequence = fields.Integer("Sequence")
    stage_id = fields.Many2one("project.task.type", "Stage")

    workflow_ids = fields.Many2many(
        "project.task.workflow",
        "project_steps_workflows_rel",
        "step_id",
        "workflow_id",
        string="Workflows",
        required=True,
    )

    hidden = fields.Boolean(
        "Hide In Status Bar",
        default=False,
        help="Select to hide this step in the status bar",
    )
    is_reopen_available = fields.Boolean("Reopen Available")

    fold = fields.Boolean(
        string="Folded in Kanban",
        help="This step is folded in the kanban view basd on user preferences",
        compute="_compute_fold",
    )

    def _compute_fold(self):
        user = self.env["res.users"].browse(self.env.context.get("uid"))
        if user:
            for step in self:
                step.fold = step.id in user.folded_step_ids.ids

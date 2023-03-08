# © 2020 Pierre Faniel, Curatolo Gabriel, Pierre Gillissen
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def _default_category(self):
        return self.env["project.task.category"].search([], limit=1)

    @api.model
    def _default_step(self):
        default_category = self._default_category()
        start_step = default_category.workflow_id.start_step_id
        return start_step[0] if start_step else False

    step_id = fields.Many2one(
        "project.task.step",
        "Step",
        default=_default_step,
        tracking=True,
        group_expand="_expand_steps",
    )

    stage_id = fields.Many2one("project.task.type", tracking=False)

    category_id = fields.Many2one(
        "project.task.category", "Type", default=_default_category, required=True
    )

    category_icon = fields.Binary(
        related="category_id.icon_file", readonly=True, string="Task Type"
    )

    workflow_id = fields.Many2one(
        "project.task.workflow",
        "Workflow",
        related="category_id.workflow_id",
        readonly=True,
    )

    times_reopened = fields.Integer("# of times reopened", default=0)

    can_reopen = fields.Boolean(compute="_compute_can_reopen")

    @api.model
    def _expand_steps(self, states, domain, order):
        """
        Expand read_group results when grouping on the step_id,
        if User decides not to hide empty steps groups, those will be visible,
        otherwise, those won't be displayed.
        """
        user = self.env["res.users"].browse(self.env.context.get("uid"))
        step = states
        if not user.hide_empty_steps:
            step = self.env["project.task.step"].search([])
        return step

    @api.constrains("step_id")
    def check_step(self):
        """
        Ensure steps, stages and workflows are coherent.
        """
        for task in self:
            if not task.step_id and task.workflow_id:
                start_step = task.workflow_id.start_step_id
                if start_step:
                    task.step_id = start_step

            if task.step_id:
                if task.workflow_id in task.step_id.workflow_ids:
                    task.stage_id = task.step_id.stage_id
                else:
                    raise ValidationError(
                        _(
                            "The current step does not belong"
                            " to the Task's current workflow"
                        )
                    )

    @api.onchange("category_id")
    def onchange_category_set_step(self):
        """
        Makes sure that if we change the category of a task, the task will keep
        a valid step and will be set to the first step of a workflow
        if the current one isn't valid.
        """
        for task in self:
            if (
                task.category_id
                and not task.step_id
                or task.step_id not in task.category_id.workflow_id.step_ids
            ):
                step = task.category_id.workflow_id.start_step_id
                if step:
                    task.step_id = step
                else:
                    task.step_id = False

    def do_reopen(self):
        for task in self:
            if task.workflow_id.reopen_step_id:
                task.times_reopened += 1
                task.step_id = task.workflow_id.reopen_step_id
            else:
                raise ValidationError(_("Error! No reopen step defined..."))

    @api.depends("workflow_id", "step_id")
    def _compute_can_reopen(self):
        for task in self:
            task.can_reopen = (
                task.workflow_id
                and task.workflow_id.reopen_step_id
                and task.step_id
                and task.step_id.is_reopen_available
            )

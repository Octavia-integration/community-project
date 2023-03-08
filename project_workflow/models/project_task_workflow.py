# © 2020 Pierre Faniel, Curatolo Gabriel, Pierre Gillissen
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTaskWorkflow(models.Model):
    _name = "project.task.workflow"
    _description = "workflow"

    active = fields.Boolean(default=True)

    name = fields.Char("Name", required=True)
    step_ids = fields.Many2many(
        "project.task.step",
        "project_steps_workflows_rel",
        "workflow_id",
        "step_id",
        string="Steps",
    )

    start_step_id = fields.Many2one(
        "project.task.step",
        required=True,
        domain="[('id', 'in', step_ids)]",
        help="Step by which the workflow begins",
    )
    end_step_ids = fields.Many2many(
        "project.task.step", domain="[('id', 'in', step_ids)]"
    )

    reopen_step_id = fields.Many2one(
        "project.task.step", domain="[('id', 'in', step_ids)]"
    )

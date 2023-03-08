# © 2020 Aurore Chevalier
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    _inherit = ["res.users"]

    folded_step_ids = fields.Many2many("project.task.step")
    hide_empty_steps = fields.Boolean(default=True)

    # pylint: disable=E0101
    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on hide_empty_steps
            and folded_step_ids fields. Access rights are disabled by default, but
            allowed on some specific fields defined in self.SELF_{READ/WRITE}
            ABLE_FIELDS.

            This is because users are specificaly given access to write/read
            on their own model, for instance, a user can read/write its lang,
            but not its groups.
        """
        init_res = super(ResUsers, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(["folded_step_ids", "hide_empty_steps"])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(["folded_step_ids", "hide_empty_steps"])
        return init_res

    def add_folded_step(self, step_id):
        """
        add the requested step to the user's folded steps
        """
        self.ensure_one()
        step = self.env["project.task.step"].browse(step_id).exists()
        if step:
            self.write({"folded_step_ids": [(4, step_id, 0)]})

    def remove_folded_step(self, step_id):
        """
        remove the requested step from the user's folded steps
        """
        self.ensure_one()
        if step_id in self.folded_step_ids.ids:
            self.write({"folded_step_ids": [(3, step_id, 0)]})

    def get_folded_step_ids(self):
        self.ensure_one()
        return self.folded_step_ids.ids

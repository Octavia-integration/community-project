# © 2020 Pierre Faniel, Curatolo Gabriel
# © 2020 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    customer_image = fields.Binary(related="partner_id.image_1920")

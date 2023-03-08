# © 2020-2022 Aurore Chevalier, Albin Gilles
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import task_search
from . import portal


def post_load():
    from . import monkey_portal_controller

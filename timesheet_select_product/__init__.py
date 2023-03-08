# © 2016 Pierre Faniel, Sam Lefever
# © 2016 Niboo SPRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from . import wizards


def load_monkey_patches():
    from .models import monkey_sale_order_compute_tasks_id
    from .models import monkey_sale_order_compute_timesheet_id
    from .wizards import monkey_project_task_create_timesheet

# © 2020-2022 Jérôme Guerriat, Sam Lefever, Curatolo Gabriel
# © 2020-2022 Niboo SRL (<https://www.niboo.com/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from . import controllers


def post_load():
    controllers.post_load()

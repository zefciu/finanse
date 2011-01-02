from finanse.controllers.common import CommonController
from finanse.models import Podkategoria

class PodkategorieController(CommonController):
    Model = Podkategoria
    params = ['kategoria_id']

from finanse.controllers.common import CommonController
from finanse.models import Produkt

class ProduktyController(CommonController):
    Model = Produkt
    params = ['podkategoria_id']

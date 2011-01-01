import cherrypy as cp
import json

from finanse.controllers.common_dispatcher import CommonDispatcher
from finanse.models import Session, Kategoria

class KategorieDispatcher(CommonDispatcher):

    @cp.expose
    def index(self, *args, **kwargs):
        s = Session()
        cats = s.query(Kategoria).order_by(Kategoria.nazwa).all()
        result = [{id: c.id, nazwa: c.nazwa} for c in cats]
        cp.result.headers['Content-Type'] = 'application/json'
        return json.dumps(result)

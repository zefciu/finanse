import cherrypy as cp
import json

from finanse.controllers.common_dispatcher import CommonDispatcher
from finanse.models import Session, Kategoria, init_model

class KategorieController(CommonDispatcher):

    @cp.expose
    def GET(self, *args, **kwargs):
        init_model() 
        s = Session()
        cats = s.query(Kategoria).all()
        result = [{'id': c.id, 'nazwa': c.nazwa} for c in cats]
        cp.response.headers['Content-Type'] = 'application/json'
        return json.dumps(result)

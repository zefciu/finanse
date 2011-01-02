import cherrypy as cp
import json

from finanse.models import Session, init_model

class CommonController(object):
    exposed = True
    params = []

    def GET(self, *args, **kwargs):
        init_model() 
        s = Session()
        q = s.query(self.Model)
        for p in self.params:
            try:
                q = q.filter(getattr(self.Model, p) == kwargs[p])
            except KeyError:
                raise cp.HTTPError(400, 'Bad request: %s not specified' % p)
        items = q.order_by(self.Model.nazwa).all()
        result = [{'id': i.id, 'nazwa': i.nazwa} for i in items]
        cp.response.headers['Content-Type'] = 'application/json'
        return json.dumps(result)

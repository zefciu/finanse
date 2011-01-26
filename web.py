#!/usr/bin/env python

import cherrypy as cp
import os.path
from wsgiref.simple_server import make_server

import finanse
from finanse.controllers.kategorie import KategorieController
from finanse.controllers.podkategorie import PodkategorieController
from finanse.controllers.produkty import ProduktyController
from finanse.controllers.sklepy import SklepyController
from finanse.controllers.zakupy import ZakupyController

finanse.current_dir = os.path.dirname(os.path.abspath(__file__))

class Root:
    @cp.expose
    def GET(self):
        return cp.lib.static.serve_file(os.path.join(
            finanse.current_dir, 'index.html'
        ))
    kategorie = KategorieController()
    podkategorie = PodkategorieController()
    produkty = ProduktyController()
    sklepy = SklepyController()
    zakupy = ZakupyController()
    exposed = True

root = Root()

application = cp.tree.mount(
    Root(), '/', os.path.join(finanse.current_dir, 'web.ini')
)
application.test = False

if __name__ == '__main__':
    httpd = make_server('', 8080, application)
    httpd.serve_forever()

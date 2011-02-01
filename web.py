#!/usr/bin/env python

import sys
sys.path.append('/home/szymon/Projekty/')

import cherrypy as cp
import os.path
from wsgiref.simple_server import make_server

import finanse
from finanse.controllers.kategorie import KategorieController
from finanse.controllers.podkategorie import PodkategorieController
from finanse.controllers.produkty import ProduktyController
from finanse.controllers.sklepy import SklepyController
from finanse.controllers.zakupy import ZakupyController
from finanse.current_dir import current_dir

class Root:
    @cp.expose
    def GET(self):
        return cp.lib.static.serve_file(os.path.join(
            current_dir, 'index.html'
        ))
    kategorie = KategorieController()
    podkategorie = PodkategorieController()
    produkty = ProduktyController()
    sklepy = SklepyController()
    zakupy = ZakupyController()
    exposed = True

root = Root()

application = cp.tree.mount(
    Root(), '/', os.path.join(current_dir, 'web.ini')
)
application.test = False

if __name__ == '__main__':
    httpd = make_server('', 8080, application)
    httpd.serve_forever()

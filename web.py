#!/usr/bin/env python

import cherrypy as cp
import os.path
import finanse

finanse.current_dir = os.path.dirname(os.path.abspath(__file__))

class Root:
    @cp.expose
    def index(self):
        return cp.lib.static.serve_file(os.path.join(
            finanse.current_dir, 'index.html'
        ))


if __name__ == '__main__':
    root = Root()
    cp.quickstart(Root(), '/', 'web.ini')

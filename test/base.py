from finanse.models import init_model, meta
from finanse.test import datasets as ds
from finanse.web import application
from fixture import SQLAlchemyFixture, DataTestCase, NamedDataStyle
from webtest import TestApp
from finanse import models

import cherrypy

class BaseTest(DataTestCase):
    def __init__(self):
        init_model(True)
        application.test = True
        cherrypy.config.update({ "environment": "embedded" })
        self.app = TestApp(application)
        self.fixture = SQLAlchemyFixture(env = models, engine = meta.engine, style = NamedDataStyle())
        self.datasets = (
            ds.KategoriaData, ds.PodkategoriaData, ds.ProduktData, ds.SiecData,
            ds.MiastoData, ds.SklepData, ds.ZakupData)


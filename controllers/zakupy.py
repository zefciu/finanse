from decimal import Decimal
import json

import cherrypy as cp
from sqlalchemy import orm

from finanse.models import Session, init_model, Zakup, Sklep, Produkt

def to_dec(v):
    return Decimal(v.replace(',', '.'))

class ZakupyController(object):

    exposed = True
    params = []

    def POST(self):
        if ('application/json' not in cp.request.headers['Content-Type']):
            raise cp.HTTPError('400', 'JSON needed') 

        try:
            inp = json.load(cp.request.body)
        except ValueError:
            raise cp.HTTPError('400', 'Malformed JSON')

        init_model()
        s = Session()

        data = inp['data']
        sklep_id = inp['sklep']
        try:
            sklep = s.query(Sklep).filter(Sklep.id == sklep_id).one()
        except orm.exc.NoResultFound:
            raise cp.HTTPError('400', 'Bad shop')

        zakupy = []
        
        for z in inp['zakupy']:
            try:
                produkt = s.query(Produkt).filter(
                    Produkt.id == z['produkt-id']
                ).one()
            except orm.exc.NoResultFound:
                raise cp.HTTPError('400', 'Bad product')
            
            zakupy.append(Zakup(
                data, sklep, produkt, to_dec(z['cena']), to_dec(z['ilosc'])
            ))

        s.commit()
        for z in inp['zakupy']:
            z['id'] = zakupy.pop(0).id

        cp.response.headers['Content-Type'] = 'application/json'
        return json.dumps({"success": True, 'message': '', 'zakupy': inp['zakupy']})

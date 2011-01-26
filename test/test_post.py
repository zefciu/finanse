from base import BaseTest
from finanse.models import Session, Sklep, Produkt, Zakup
import json

class TestPost(BaseTest):

    def zakupy_test(self):
        s = Session()
        d = '2011-1-26'
        sklep_id = s.query(Sklep).all()[0].id
        produkt_ids = [pr.id for pr in s.query(Produkt).all()[0:3]]
        print(produkt_ids)
        input_data = json.dumps({
            'data': d,
            'sklep': sklep_id,
            'zakupy': [{
                'produkt.id': prid, 'cena': 10, 'ilosc': 1
            } for prid in produkt_ids]
        })

        self.app.post('/zakupy', input_data, {'Content-Type': 'application/json'})
        zakupy = s.query(Zakup).all()
        assert len(zakupy) == 7



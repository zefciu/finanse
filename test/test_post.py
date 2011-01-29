from base import BaseTest
from finanse.models import Session, Sklep, Produkt, Zakup, Kategoria
import json

class TestPost(BaseTest):

    def zakupy_test(self):
        s = Session()
        d = '2011-1-26'
        sklep_id = s.query(Sklep).all()[0].id
        produkt_ids = [pr.id for pr in s.query(Produkt).all()[0:3]]
        input_data = json.dumps({
            'data': d,
            'sklep': sklep_id,
            'zakupy': [{
                'produkt.id': prid, 'cena': 10, 'ilosc': 1
            } for prid in produkt_ids]
        })
        print input_data

        self.app.post(
            '/zakupy', input_data, {'Content-Type': 'application/json'}
        )
        zakupy = s.query(Zakup).all()
        assert len(zakupy) == 7
        s.query(Zakup).delete()
        s.commit()

    def kategoria_test(self):
        s = Session()
        input_data = json.dumps({'nazwa': 'Lekarstwa'})
        res = self.app.post(
            '/kategorie', input_data, {'Content-Type': 'application/json'}
        )
        print res

        kats = s.query(Kategoria).all()
        print kats
        assert len(kats) == 3
        assert 'Lekarstwa' in [kat.nazwa for kat in kats]
        s.query(Kategoria).filter(
            Kategoria.id == json.loads(res.body)['id']
        ).delete()

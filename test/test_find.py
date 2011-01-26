# vim: set fileencoding=utf-8

from base import BaseTest
from finanse.models import Session, Kategoria
import json

class TestFind(BaseTest):

    def cat_test(self):
        result = json.loads(self.app.get('/kategorie').body)
        assert len(result) == 2
        assert len([r for r in result if r['nazwa'] == 'Chemia']) == 1

    def subcat_test(self):
        cats = json.loads(self.app.get('/kategorie').body)
        cat_id = [c for c in cats if c['nazwa'] == 'Jedzenie'][0]['id']
        result = json.loads(self.app.get(
            '/podkategorie', {'kategoria_id': cat_id}
        ).body)
        print result
        assert len(result) == 3
        assert len([r for r in result if r['nazwa'] == 'Do chleba']) == 1
        assert len([r for r in result if r['nazwa'] == 'Kosmetyki']) == 0

    def product_test(self):
        cats = json.loads(self.app.get('/kategorie').body)
        cat_id = [c for c in cats if c['nazwa'] == 'Jedzenie'][0]['id']
        subcats = json.loads(self.app.get(
            '/podkategorie', {'kategoria_id': cat_id}
        ).body)
        subcat_id = [c for c in subcats if c['nazwa'] == 'Do chleba'][0]['id']
        result = json.loads(self.app.get(
            '/produkty', {'podkategoria_id': subcat_id}
        ).body)
        print result
        assert len(result) == 3
        assert len([r for r in result if r['nazwa'] == u'Masło orzechowe']) == 1
        assert len([r for r in result if r['nazwa'] == u'Kiełbasa']) == 0

    def sklep_test(self):
        result = json.loads(self.app.get('/sklepy').body)
        assert len(result) == 3
        assert len([r for r in result if r['nazwa'] == 'Warzywniak, Mickiewicza']) == 1

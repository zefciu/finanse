from fixture import DataSet

class Kategorie(DataSet):
    class jedzenie:
        nazwa = 'Jedzenie'
    class chemia:
        nazwa = 'Chemia'

class Podkategorie(DataSet):
    class do_chleba:
        nazwa = 'Do chleba',
        kategoria_id = Kategorie.jedzenie.ref('id')
    class do_chleba:
        nazwa = 'Słodkie',
        kategoria_id = Kategorie.jedzenie.ref('id')
    class mieso:
        nazwa = 'Mięso',
        kategoria_id = Kategorie.jedzenie.ref('id')
    class srodki_czystosci:
        nazwa = 'Środki czystości',
        kategoria_id = Kategorie.chemia.ref('id')
    class kosmetyki:
        nazwa = 'Kosmetyki',
        kategoria_id = Kategorie.chemia.ref('id')

class Produkty(DataSet):
    class dzem:
        nazwa = 'Dżem',
        podkategoria_id = Podkategorie.do_chleba.ref('id')
    class maslo_orzechowe:
        nazwa = 'Masło orzechowe',
        podkategoria_id = Podkategorie.do_chleba.ref('id')
    class serek_topiony:
        nazwa = 'Serek topiony',
        podkategoria_id = Podkategorie.do_chleba.ref('id')
    class szynka:
        nazwa = 'Szynka',
        podkategoria_id = Podkategorie.mieso.ref('id')
    class kielbasa:
        nazwa = 'Kiełbasa',
        podkategoria_id = Podkategorie.mieso.ref('id')
    class mydlo:
        nazwa = 'Mydło',
        podkategoria_id = Podkategorie.srodki_czystosci.ref('id')
    class krem_do_rak:
        nazwa = 'Krem do rąk',
        podkategoria_id = Podkategorie.kosmetyki.ref('id')

class Sieci(DataSet):
    class biedronka:
        nazwa = 'Biedronka'
    class lidl:
        nazwa = 'Lidl'
    
class Miasta(DataSet):
    class poznan:
        nazwa = 'Poznań'
    class wronki:
        nazwa = 'Wronki'

class Sklepy(DataSet):
    class biedronka_piastowskie:
        nazwa = 'Biedronka Piastowskie'
        siec_id = Sieci.biedronka.ref('id')
        miasto_id = Miasta.poznan.ref('id')

    class biedronka_borek:
        nazwa = 'Biedronka Borek'
        siec_id = Sieci.biedronka.ref('id')
        miasto_id = Miasta.wronki.ref('id')

    class warzywniak_mickiewicza:
        nazwa = 'Warzywniak, Mickiewicza'
        siec_id = None
        miasto_id = Miasta.wronki.ref('id')

class Zakupy(DataSet):
    class szynka_w_biedronce:
        data = date(2011, 1, 23)
        sklep_id = Sklepy.biedronka_borek.ref('id')
        produkt_id = Produkty.szynka.ref('id')
        cena = 8
        ilosc = .300
    class krem_w_biedronce:
        data = date(2011, 1, 23)
        sklep_id = Sklepy.biedronka_borek.ref('id')
        produkt_id = Produkty.szynka.ref('id')
        cena = 20
        ilosc = 1
    class szynka_w_poznaniu:
        data = date(2011, 1, 23)
        sklep_id = Sklepy.biedronka_piastowskie.ref.('id')
        produkt_id = Produkty.szynka.ref('id')
        cena = 9.50
        ilosc = .320
    class mydlo_wczoraj:
        data = date(2011, 1, 22)
        sklep_id = Sklepy.biedronka_borek.ref.('id')
        produkt_id = Produkty.mydlo.ref('id')
        cena = 15.50
        ilosc = 1

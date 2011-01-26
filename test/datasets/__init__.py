# vim: set fileencoding=utf-8

from fixture import DataSet
from datetime import date

class KategoriaData(DataSet):
    class jedzenie:
        nazwa = 'Jedzenie'
    class chemia:
        nazwa = 'Chemia'

class PodkategoriaData(DataSet):
    class do_chleba:
        nazwa = 'Do chleba'
        kategoria = KategoriaData.jedzenie
    class slodkie:
        nazwa = 'Słodkie'
        kategoria = KategoriaData.jedzenie
    class mieso:
        nazwa = 'Mięso'
        kategoria = KategoriaData.jedzenie
    class srodki_czystosci:
        nazwa = 'Środki czystości'
        kategoria = KategoriaData.chemia
    class kosmetyki:
        nazwa = 'Kosmetyki'
        kategoria = KategoriaData.chemia

class ProduktData(DataSet):
    class dzem:
        nazwa = 'Dżem'
        podkategoria = PodkategoriaData.do_chleba
    class maslo_orzechowe:
        nazwa = 'Masło orzechowe'
        podkategoria = PodkategoriaData.do_chleba
    class serek_topiony:
        nazwa = 'Serek topiony'
        podkategoria = PodkategoriaData.do_chleba
    class szynka:
        nazwa = 'Szynka'
        podkategoria = PodkategoriaData.mieso
    class kielbasa:
        nazwa = 'Kiełbasa'
        podkategoria = PodkategoriaData.mieso
    class mydlo:
        nazwa = 'Mydło'
        podkategoria = PodkategoriaData.srodki_czystosci
    class krem_do_rak:
        nazwa = 'Krem do rąk'
        podkategoria = PodkategoriaData.kosmetyki

class SiecData(DataSet):
    class biedronka:
        nazwa = 'Biedronka'
    class lidl:
        nazwa = 'Lidl'
    
class MiastoData(DataSet):
    class poznan:
        nazwa = 'Poznań'
    class wronki:
        nazwa = 'Wronki'

class SklepData(DataSet):
    class biedronka_piastowskie:
        nazwa = 'Biedronka Piastowskie'
        siec = SiecData.biedronka
        miasto = MiastoData.poznan

    class biedronka_borek:
        nazwa = 'Biedronka Borek'
        siec = SiecData.biedronka
        miasto = MiastoData.wronki

    class warzywniak_mickiewicza:
        nazwa = 'Warzywniak, Mickiewicza'
        siec = None
        miasto = MiastoData.wronki

class ZakupData(DataSet):
    class szynka_w_biedronce:
        data = date(2011, 1, 23)
        sklep = SklepData.biedronka_borek
        produkt = ProduktData.szynka
        cena = 8
        ilosc = .300
    class krem_w_biedronce:
        data = date(2011, 1, 23)
        sklep = SklepData.biedronka_borek
        produkt = ProduktData.szynka
        cena = 20
        ilosc = 1
    class szynka_w_poznaniu:
        data = date(2011, 1, 23)
        sklep = SklepData.biedronka_piastowskie
        produkt = ProduktData.szynka
        cena = 9.50
        ilosc = .320
    class mydlo_wczoraj:
        data = date(2011, 1, 22)
        sklep = SklepData.biedronka_borek
        produkt = ProduktData.mydlo
        cena = 15.50
        ilosc = 1

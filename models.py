# vim: set fileencoding=utf-8

import sqlalchemy as sa
from sqlalchemy import orm
import shared
from string import Template
import ConfigParser as cp


Session = orm.sessionmaker()

meta = sa.MetaData()

kategorie_table = sa.Table(
    'kategorie', meta, 
    sa.Column('id', sa.types.Integer(), sa.Sequence('kategorie_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.String(128), nullable = False),
)

sa.Index('kategoria_nazwa', kategorie_table.c.nazwa, unique = True)

podkategorie_table = sa.Table(
    'podkategorie', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('podkategorie_id_seq'), primary_key=True),
    sa.Column('kategoria_id', sa.types.Integer(), sa.ForeignKey('kategorie.id'), nullable = False),
    sa.Column('nazwa', sa.types.String(128), nullable = False),
)

sa.Index('podkategoria_nazwa', podkategorie_table.c.kategoria_id, podkategorie_table.c.nazwa, unique = True)

produkty_table = sa.Table(
    'produkty', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('produkty_id_seq'), primary_key=True),
    sa.Column('podkategoria_id', sa.types.Integer(), sa.ForeignKey('podkategorie.id'), nullable = False),
    sa.Column('nazwa', sa.types.String(128), nullable = False),
)

sieci_table = sa.Table(
    'sieci', meta, 
    sa.Column('id', sa.types.Integer(), sa.Sequence('sieci_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.String(128), nullable = False),
)

sa.Index('siec_nazwa', sieci_table.c.nazwa, unique = True)

miasta_table = sa.Table(
    'miasta', meta, 
    sa.Column('id', sa.types.Integer(), sa.Sequence('miasta_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.String(128), nullable = False),
)

sa.Index('miasto_nazwa', miasta_table.c.nazwa, unique = True)

sklepy_table = sa.Table(
    'sklepy', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('sklepy_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.String(128), nullable = False, index = True),
    sa.Column('siec_id', sa.types.Integer(32), sa.ForeignKey('sieci.id'), nullable = True),
    sa.Column('miasto_id', sa.types.Integer(32), sa.ForeignKey('miasta.id'), nullable = True),
)

sa.Index('sklep_nazwa', sklepy_table.c.nazwa, unique = True)

zakupy_table = sa.Table(
    'zakupy', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('zakupy_id_seq'), primary_key=True),
    sa.Column('produkt_id', sa.types.Integer(), sa.ForeignKey('produkty.id'), nullable = False),
    sa.Column('sklep_id', sa.types.Integer(), sa.ForeignKey('sklepy.id'), nullable = True),
    sa.Column('ilosc', sa.types.Numeric(7, 3), nullable = False),
    sa.Column('cena', sa.types.Numeric(7, 2), nullable = False),
    sa.Column('data', sa.types.Date(), nullable = False),
)

sa.Index('cena_produkt', zakupy_table.c.produkt_id, zakupy_table.c.cena)

class BaseNameOnly(object):
    def __init__(self, nazwa):
        self.nazwa = nazwa

    @classmethod
    def from_name(cls, name):
        return cls(name)

    @classmethod
    def from_input(cls):
        name = shared.get_answer('Wprowadź %s: ' % cls.human_name)
        return cls(name)

class Siec(BaseNameOnly):
    human_name = 'Sieć'

class Miasto(BaseNameOnly):
    human_name = 'Miasto'

class Kategoria(BaseNameOnly):
    human_name = 'Kategorię'

class Podkategoria(object):
    def __init__(self, nazwa, kategoria):
        self.nazwa = nazwa
        self.kategoria = kategoria

    @classmethod
    def from_input(cls, kategoria):
        nazwa = shared.get_answer('Wprowadź podkategorię: ')
        return cls(nazwa, kategoria)

class Sklep(object):
    def __init__(self, siec, miasto, nazwa):
        self.nazwa = nazwa
        self.siec = siec
        self.miasto = miasto

    @classmethod
    def from_input(cls, session):
        print('Nowy sklep:')
        siec = shared.choice('Wybierz Sieć: ', session, Siec, shared.enter_new(Siec), allow_empty = True)
        miasto = shared.choice('Wybierz Miasto', session, Miasto, shared.enter_new(Miasto), allow_empty = True)
        nazwa = shared.get_answer('Nazwa sklepu: ')
        return cls(siec, miasto, nazwa)

class Zakup(object):
    def __init__(self, data, sklep, produkt, cena, ilosc = 1):
        self.data = data
        self.sklep = sklep
        self.produkt = produkt
        self.cena = cena
        self.ilosc = ilosc

class Produkt(object):
    def __init__(self, nazwa, podkategoria):
        self.nazwa = nazwa
        self.podkategoria = podkategoria

    @classmethod
    def from_input(cls, podkategoria):
        nazwa = shared.get_answer('Wprowadź produkt: ')
        return cls(nazwa, podkategoria)

orm.mapper(Siec, sieci_table)
orm.mapper(Miasto, miasta_table)
orm.mapper(Sklep, sklepy_table, properties = {
    'siec': orm.relationship(Siec, backref = 'sklep'),
    'miasto': orm.relationship(Miasto, backref = 'sklep')
})
orm.mapper(Kategoria, kategorie_table)
orm.mapper(Podkategoria, podkategorie_table, properties = {
    'kategoria': orm.relationship(Kategoria, backref = 'podkategorie')
})
orm.mapper(Produkt, produkty_table, properties = {
    'podkategoria': orm.relationship(Podkategoria, backref = 'produkty')
})
orm.mapper(Zakup, zakupy_table, properties = {
    'sklep': orm.relationship(Sklep, backref = 'zakupy'),
    'produkt': orm.relationship(Produkt, backref = 'zakupy'),
})

def init_model():
    config = cp.SafeConfigParser()
    config.read('config.ini')

    # username, password = shared.login(config.get('db', 'def_user'))

    db_path = Template('$engine://$user:$password@$host/$db').substitute({
        'engine': config.get('db', 'engine'),
        'host': config.get('db', 'host'),
        'db': config.get('db', 'name'),
        'user': config.get('db', 'user'),
        'password': config.get('db', 'password'),
    })
    meta.engine = sa.create_engine(db_path, echo=False)
    Session.configure(bind=meta.engine)

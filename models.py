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
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False),
)

sa.Index('kategoria_nazwa', kategorie_table.c.nazwa, unique = True)

podkategorie_table = sa.Table(
    'podkategorie', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('podkategorie_id_seq'), primary_key=True),
    sa.Column('kategoria_id', sa.types.Integer(), sa.ForeignKey('kategorie.id'), nullable = False),
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False),
)

sa.Index('podkategoria_nazwa', podkategorie_table.c.kategoria_id, podkategorie_table.c.nazwa, unique = True)

produkty_table = sa.Table(
    'produkty', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('produkty_id_seq'), primary_key=True),
    sa.Column('podkategoria_id', sa.types.Integer(), sa.ForeignKey('podkategorie.id'), nullable = False),
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False),
)

sieci_table = sa.Table(
    'sieci', meta, 
    sa.Column('id', sa.types.Integer(), sa.Sequence('sieci_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False),
)

sa.Index('siec_nazwa', sieci_table.c.nazwa, unique = True)

miasta_table = sa.Table(
    'miasta', meta, 
    sa.Column('id', sa.types.Integer(), sa.Sequence('miasta_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False),
)

sa.Index('miasto_nazwa', miasta_table.c.nazwa, unique = True)

sklepy_table = sa.Table(
    'sklepy', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('sklepy_id_seq'), primary_key=True),
    sa.Column('nazwa', sa.types.Unicode(128), nullable = False, index = True),
    sa.Column('siec_id', sa.types.Integer(32), sa.ForeignKey('sieci.id'), nullable = True),
    sa.Column('miasto_id', sa.types.Integer(32), sa.ForeignKey('miasta.id'), nullable = True),
)

sa.Index('sklep_nazwa', sklepy_table.c.nazwa, unique = True)

zakupy_table = sa.Table(
    'zakupy', meta,
    sa.Column('id', sa.types.Integer(), sa.Sequence('zakupy_id_seq'), primary_key=True),
    sa.Column('produkt_id', sa.types.Integer(), sa.ForeignKey('produkty.id'), nullable = False),
    sa.Column('sklep_id', sa.types.Integer(), sa.ForeignKey('sklepy.id'), nullable = True),
    sa.Column('cena', sa.types.Numeric(7, 2), nullable = False),
    sa.Column('data', sa.types.Date(), nullable = False),
)

sa.Index('cena_produkt', zakupy_table.c.produkt_id, zakupy_table.c.cena)

def init_model():
    config = cp.SafeConfigParser()
    config.read('config.ini')

    username, password = shared.login(config.get('db', 'def_user'))

    db_path = Template('$engine://$user:$password@$host/$db').substitute({
        'engine': config.get('db', 'engine'),
        'host': config.get('db', 'host'),
        'db': config.get('db', 'name'),
        'user': username,
        'password': password,
    })
    meta.engine = sa.create_engine(db_path, echo=False)
    Session.configure(bind=meta.engine)

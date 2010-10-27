#!/usr/bin/env python
# vim: set fileencoding=utf-8

import models as m
import shared
from datetime import date

def enter_new_network(session):
    siec = m.Siec.from_input()
    session.add(siec)
    return siec

def enter_new_city(session):
    miasto = m.Miasto.from_input()
    session.add(miasto)
    return miasto

def enter_new_cat(session):
    cat = m.Kategoria.from_input()
    session.add(cat)
    return cat

def enter_new_subcat(session, kategoria):
    subcat = m.Podkategoria.from_input(kategoria)
    session.add(subcat)
    return subcat

def enter_new_product(session, podkategoria):
    product = m.Podkategoria.from_input(podkategoria)
    session.add(product)
    return product


def enter_new_shop(session):
    print('Nowy sklep:')
    siec = shared.choice('Wybierz Sieć: ', session, m.Siec, enter_new_network)
    miasto = shared.choice('Wybierz Miasto', session, m.Miasto, enter_new_city)
    nazwa = shared.get_answer('Nazwa sklepu: ')
    sklep = m.Sklep(siec, miasto, nazwa)
    session.add(sklep)
    return sklep

def get_date_and_shop(session):
    d = shared.get_answer(
        'Data zakupów DD-MM-YYYY',
        date.today().strftime('%d-%m-%Y'),
        '^[0-4][0-9]-[0-1][0-9]-[0-9]{4}'
    )
    sklep = shared.choice('Wybierz sklep', session, m.Sklep, enter_new_shop) 
    return d, sklep


if __name__ == '__main__':
    m.init_model()
    m.meta.create_all(m.meta.engine)
    session = m.Session()

    (date, shop) = get_date_and_shop(session)

    while True:
        kategoria = shared.choice('Wybierz kategorię: ', session, m.Kategoria, enter_new_cat)
        podkategoria = shared.choice(
            'Wybierz podkategorię: ',
            session,
            m.Podkategoria,
            lambda s: enter_new_subcat(s, kategoria),
            query_processor = lambda x: x.filter(m.Podkategoria.kategoria_id == kategoria.id)
        )
        produkt - shared.choice(
            'Wybierz produkt: ',
            session,
            m.Produkt,
            lambda s: enter_new_product(s, podkategoria)
        )

    session.commit()

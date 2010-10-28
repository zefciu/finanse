#!/usr/bin/env python
# vim: set fileencoding=utf-8

import models as m
import shared
from decimal import Decimal
from datetime import date, datetime

def get_date_and_shop(session):
    d = shared.get_answer(
        'Data zakupów DD-MM-YYYY',
        date.today().strftime('%d-%m-%Y'),
        '^[0-4][0-9]-[0-1][0-9]-[0-9]{4}'
    )
    sklep = shared.choice('Wybierz sklep', session, m.Sklep, shared.enter_new(m.Sklep, session)) 
    return datetime.strptime(d, '%d-%m-%Y'), sklep


if __name__ == '__main__':
    m.init_model()
    m.meta.create_all(m.meta.engine)
    session = m.Session()

    (data, sklep) = get_date_and_shop(session)

    while True:
        kategoria = shared.choice('Wybierz kategorię: ', session, m.Kategoria, shared.enter_new(m.Kategoria))
        podkategoria = shared.choice(
            'Wybierz podkategorię: ',
            session,
            m.Podkategoria,
            shared.enter_new(m.Podkategoria, kategoria),
            query_processor = lambda x: x.filter(m.Podkategoria.kategoria_id == kategoria.id)
        )
        produkt = shared.choice(
            'Wybierz produkt: ',
            session,
            m.Produkt,
            shared.enter_new(m.Produkt, podkategoria),
            query_processor = lambda x: x.filter(m.Produkt.podkategoria_id == podkategoria.id)
        )
        cena = shared.get_answer(
            'Cena: ',
            None,
            '[0-9]{0,5}\.[0-9]{0,2}'
        )
        zakup = m.Zakup(data, sklep, produkt, Decimal(cena))
        session.add(zakup)
        moar = shared.get_answer(
            'Dalej?',
            't',
            't|n'
        )
        if moar is 'n':
            break

    session.commit()

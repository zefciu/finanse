# vim: set fileencoding=utf-8

import models as m
import shared
from datetime import date

def enter_new_shop(session):
    print('Nowy sklep:')
    siec = shared.get_answer('Nazwa sieci')
    miasto = shared.get_answer('Miasto')
    nazwa = shared.get_answer('Nazwa sklepu')
    return Sklep(siec, miasto, nazwa)

def get_date_and_shop(session):
    d = shared.get_answer(
        'Data zakupów DD-MM-YYYY',
        date.today().strftime('%d-%m-%Y'),
        '^[0-4][0-9]-[0-1][0-9]-[0-9]{4}'
    )
    sklep = shared.choice(session, m.Sklep, enter_new_shop) 
    return d, sklep


if __name__ == '__main__':
    m.init_model()
    m.meta.create_all(m.meta.engine)
    session = m.Session()

    (date, shop) = get_date_and_shop(session)
    session.commit()

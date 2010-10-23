# vim: set fileencoding=utf-8

import models as m
import shared
from datetime import date

def get_date_and_shop(session):
    d = shared.get_answer(
        'Data zakupów DD-MM-YYYY',
        date.today().strftime('%d-%m-%Y'),
        '^[0-4][0-9]-[0-1][0-9]-[0-9]{4}'
    )
    shop = shared.choice(session, m.Shop, m.Shop.from_choice) 

if __name__ == '__main__':
    m.init_model()
    m.meta.create_all(m.meta.engine)
    session = m.Session()

    (date, shop) = get_date_and_shop(session)

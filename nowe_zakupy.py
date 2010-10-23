# vim: set fileencoding=utf-8

import models as m
from shared import get_answer
from datetime import date

def get_date_and_shop():
    d = get_answer(
        'Data zakupów DD-MM-YYYY',
        date.today().strftime('%d-%m-%Y'),
        '^[0-4][0-9]-[0-1][0-9]-[0-9]{4}'
    )
    print d
    return (None, None)



if __name__ == '__main__':
    m.init_model()
    m.meta.create_all(m.meta.engine)
    (date, shop) = get_date_and_shop()

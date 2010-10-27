# vim: set fileencoding=utf-8

import getpass
import itertools as it
import re

def login(default_user = None):
    username = get_answer ('Login: ', default_user, '.{2,}')
    password = getpass.getpass('Hasło: ')
    return (username, password)


def get_answer(question, default = None, validator = None):
    q_string = question if default is None else '%s(%s): ' % (question, default)
    while True:
        inp = raw_input(q_string)

        if inp is '' and default is not None:
            return default

        if validator is None or re.match(validator, inp) is not None:
            return inp

def choice (question, session, model, new_item_creator, name_field = 'nazwa', query_processor = None):
    print question
    q = session.query(model)
    if query_processor is not None:
        q = query_processor(q)

    choices = q.all()
    counter = it.count(1)
    choice_tuples = [(counter.next(), choice) for choice in choices]
    for t in choice_tuples:
        print '%i\t- %s' % (t[0], getattr(t[1], name_field))

    print '0\t - wprowadź'
    
    reply = get_answer('Wybierz ', '0', '[0-9]+')
    if reply is '0':
        return new_item_creator(session)
    return choice_tuples[int(reply) - 1][1]

# vim: set fileencoding=utf-8

import getpass
import itertools as it

def login(default_user = None):
    username = get_answer ('Login: ', default_user, '.{2,}')
    password = getpass.getpass('Hasło: ')
    return (username, password)


def get_answer(question, default = None, validator = None):
    q_string = questions if default is None else '%s(%s)' % (question, default)
    while True:
        inp = raw_input(q_string)

        if inp is '' and default is not None:
            return default

        if validator is None or re.match(validator, inp) is not None:
            return inp

def choice (session, model, ItemConstructor, name_field = 'name', query_processor = None):
    q = session.query(model)
    if query_processor is not None:
        q = query_processor(q)

    choices = q.all()
    counter = it.count(1)
    choice_tuples = [count.next(), choice for choice in choices]
    for t in choice_tuples:
        print '%i\t- %s' % (t[0], getattr(t[1], name_field))

    print '0\t - wprowadź'
    
    reply = get_answer('Wybierz ', '0', '[0-9]+')
    if reply is '0':
        new_item = ItemConstructor()


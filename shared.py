# vim: set fileencoding=utf-8

import getpass

def login(default_user = None):
    username = get_answer ('Login: ', default_user, '.{2,}')
    password = getpass.getpass('Hasło: ')
    return (username, password)


def get_answer(question, default = None, validator = None):
    q_string = questions if default is None else '%s (%s)' % (question, default)
    print (q_string)
    while True:
        inp = raw_input('? ')

        if inp is '' and default is not None:
            return default

        if validator is None or re.match(validator, inp) is not None:
            return inp

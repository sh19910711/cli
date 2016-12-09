import os
import getpass
from makestack import api


def get_env_or_ask(env, ask):
    v = os.environ.get(env)

    if v is None:
        return ask()
    else:
        return v


def main(args):
    DEFAULT_URL = 'https://makestack.io'

    url = get_env_or_ask("MAKESTACK_SERVER_URL",
                         lambda: input('server URL [{}]: '.format(DEFAULT_URL)))
    if url == '':
        url = DEFAULT_URL

    username = get_env_or_ask("MAKESTACK_USERNAME",
                              lambda: input('username: '))
    password = get_env_or_ask("MAKESTACK_PASSWORD",
                              lambda: getpass.getpass('password: '))

    api.login(url, username, password)

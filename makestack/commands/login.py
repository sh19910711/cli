from makestack import api
from makestack.helpers import get_env_or_ask


def main(args):
    DEFAULT_URL = 'https://makestack.io'

    url = get_env_or_ask("MAKESTACK_SERVER_URL",
                         'server URL [{}]'.format(DEFAULT_URL))
    if url == '':
        url = DEFAULT_URL

    username = get_env_or_ask("MAKESTACK_USERNAME", 'Username')
    password = get_env_or_ask("MAKESTACK_PASSWORD", 'Password', password=True)

    api.login(url, username, password)

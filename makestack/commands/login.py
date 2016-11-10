import getpass
from makestack import api


def main(args):
    DEFAULT_URL = 'https://makestack.io'

    url = input('server URL [{}]: '.format(DEFAULT_URL))
    if url == '':
        url = DEFAULT_URL

    username = input('username: ')
    password = getpass.getpass('password: ')
    api.login(url, username, password)

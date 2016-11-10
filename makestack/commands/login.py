import getpass
from makestack import api


def main(args):
    username = input('username: ')
    password = getpass.getpass('password: ')
    api.login(username, password)

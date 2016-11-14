import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    r = api.invoke('GET', '/devices')
    for device in r.json()['devices']:
        print("{name} ({board}): {status}".format(**device))

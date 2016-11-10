import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.require_app_root_dir()
    app_name = appdir.get_current_app_name()
    r = api.invoke('POST', '/devices', params={ 'app_name': app_name })
    for device in r.json()['devices']:
        print("{name} ({board}): {status}".format(**device))

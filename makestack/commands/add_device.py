import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.require_app_root_dir()
    app_name = appdir.get_current_app_name()

    r = api.invoke('POST', '/apps/{}/devices'.format(app_name),
                   params={ 'device_name': args.device_name })

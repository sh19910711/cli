import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.chdir_to_app_dir(args.appdir)
    app_name = appdir.get_current_app_name()

    r = api.invoke('POST', '/apps/{}/devices'.format(app_name),
                   params={ 'device_name': args.device_name })

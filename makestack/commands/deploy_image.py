import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.chdir_to_app_dir(args.appdir)
    app_name = appdir.get_current_app_name()

    api.invoke('POST', '/apps/{}/deployments'.format(app_name),
               data={ 'comment': args.comment },
               files={ 'image': open(args.image, 'rb') })

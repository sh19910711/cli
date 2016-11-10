import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.require_app_root_dir()
    app_name = appdir.get_current_app_name()

    api.invoke('POST', '/apps/{}/deployments'.format(app_name),
               files={ 'image': open(image_path, 'rb') })

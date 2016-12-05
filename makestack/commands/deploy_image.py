import os
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    image_file = os.path.abspath(args.image)
    appdir.chdir_to_app_dir(args.appdir)
    app_name = appdir.get_current_app_name()

    api.invoke('POST', '/apps/{}/deployments'.format(app_name),
               params={ 'comment': args.comment },
               files={ 'image': open(image_file, 'rb') })

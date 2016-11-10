import os
import tempfile
import shutil
from makestack import appdir, api
from makestack.helpers import error


def main(args):
    appdir.require_app_root_dir()
    app_name = appdir.get_current_app_name()

    with tempfile.TemporaryDirectory() as d:
        zip_path = os.path.join(d, 'makestack-source.zip')
        shutil.make_archive(zip_path, 'zip')

        api.invoke('POST', '/apps/{}/builds'.format(app_name),
                   files={ 'source_file': open(zip_path, 'rb') })

import os
import time
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

        r = api.invoke('POST', '/apps/{}/builds'.format(app_name),
                       files={ 'source_file': open(zip_path, 'rb') })


    if r.status_code != 202:
        error("something wrong with MakeStack Server")

    # TODO: use WebSocket
    info("building...")
    build_id = r.json()['id']
    while True:
        build = api.invoke('GET', '/apps/{}/builds/{}'.format(app_name, build_id)).json()

        if build.status == "deploying":
            info("deploying...")
        elif build.status == "success":
            for l in build.log.split("\n"):
                print(l)
            success("successfully deployed")
            return
        elif build.status == "failure":
            for l in build.log.split("\n"):
                print(l)
            error("failed to build")

        time.sleep(3)

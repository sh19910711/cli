import os
import time
import tempfile
import shutil
import dulwich.porcelain
from dulwich.repo import Repo, NotGitRepository
from makestack import appdir, api
from makestack.helpers import error, info, success


def is_dirty_repo(r):
    return list(dulwich.porcelain.get_tree_changes(r).values()) != [[], [], []] or \
           list(dulwich.porcelain.get_unstaged_changes(r.open_index(), r.path)) != []


def get_latest_commit_message():
    try:
        r = Repo(".")
        latest_commit = list(r.get_walker(max_entries=1))[0].commit
        comment = latest_commit.message.decode("utf-8").split("\n")[0].strip()

        if is_dirty_repo(r):
            comment += " (modified)"
    except NotGitRepository:
        comment = ""
    except IndexError:
        # no commits
        comment = ""

    return comment


def main(args):
    appdir.chdir_to_app_dir(args.appdir)
    app_name = appdir.get_current_app_name()

    if args.comment:
        comment = arg.comment
    else:
        comment = get_latest_commit_message()

    with tempfile.TemporaryDirectory() as d:
        zip_path = os.path.join(d, 'makestack-source.zip')
        shutil.make_archive(os.path.splitext(zip_path)[0], 'zip')

        r = api.invoke('POST', '/apps/{}/deployments'.format(app_name),
                       params={ 'comment': comment },
                       files={ 'source_file': open(zip_path, 'rb') })


    if r.status_code != 200:
        error("something wrong with MakeStack Server")

    # TODO: use WebSocket
    info("building...")
    failed = False
    for deployment in r.json()["deployments"]:
        ver = deployment["version"]
        while True:
            path = '/apps/{}/deployments/{}'.format(app_name, ver)
            status = api.invoke('GET', path).json().get("status")

            if status == 'success':
                break
            elif status == 'failure':
                failed = True
                error("failed to deploy (board: {})".format(deployment.board))
                for l in deployment['buildlog'].split("\n"):
                    print(l)

            time.sleep(3)

    if not failed:
        success("successfully deployed")

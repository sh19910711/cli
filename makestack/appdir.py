import os
from makestack.helpers import error


def chdir_to_app_dir(appdir):
     os.chdir(appdir)

     if not os.path.exists('application.yaml'):
         error("You aren't in an app root directory")

def get_current_app_name():
    return os.path.basename(os.getcwd())

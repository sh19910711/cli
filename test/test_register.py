import os
from helpers import *

def test_register(server):
    app_name = "hello2"
    run(["new", app_name])
    os.chdir(app_name)
    run(["register"])
    os.chdir("..")

    assert rails("App.find_by_name('{}')".format(app_name)) != ""

import os
import yaml
from helpers import *


def test_new(server):
    app_name = "hello"
    run(["new", "--register", app_name])
    os.chdir(app_name)
    run(["register"])
    os.chdir("..")

    path = "hello/application.yaml"
    assert os.path.exists(path)

    yml = yaml.load(open(path))
    assert "api"    in yml
    assert "lang"   in yml
    assert "name"   in yml
    assert app_name in yml["name"]

    assert rails("App.find_by_name('{}')".format(app_name)) != ""

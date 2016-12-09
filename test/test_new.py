import os
import shutil
import yaml
import makestack


def test_new(server):
    app_name = "hello"
    makestack.main.main(['makestack', 'new', '--register', app_name])
    path = "hello/application.yaml"
    assert os.path.exists(path)

    yml = yaml.load(open(path))
    assert "api"    in yml
    assert "lang"   in yml
    assert "name"   in yml
    assert app_name in yml["name"]

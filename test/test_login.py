import os
import yaml
import makestack
from helpers import *


def test_login(server_no_login):
    run(['login'])
    credentials_path = "tmp/test/config/credentials.yaml"
    assert os.path.exists(credentials_path)

    yml = yaml.load(open(credentials_path))
    assert "url"      in yml
    assert "username" in yml
    assert "auth"     in yml
    assert "access-token" in yml["auth"]
    assert "client"       in yml["auth"]
    assert "expiry"       in yml["auth"]

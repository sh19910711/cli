import os
from helpers import *


def test_user(server, capsys):
    password = os.environ["MAKESTACK_PASSWORD"]
    new_password = "abcd1234"

    os.environ["MAKESTACK_CURRENT_PASSWORD"] = password
    os.environ["MAKESTACK_NEW_PASSWORD"] = new_password
    os.environ["MAKESTACK_PASSWORD_CONFIRMATION"] = new_password
    run(["user", "change-password"])

    os.environ["MAKESTACK_PASSWORD"] = new_password
    run(['login'])

    os.environ["MAKESTACK_PASSWORD"] = password

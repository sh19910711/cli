from helpers import *


def test_env(app, capsys):
    run(["env", "set", "x-wing", "FOO", "HELO"])
    run(["env", "list", "x-wing"])

    out, _ = capsys.readouterr()
    assert "FOO" in out
    assert "HELO" in out

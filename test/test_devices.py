from helpers import *


def test_devices(app, capsys):
    run(["add-device", "x-wing"])
    run(["devices"])
    out, _ = capsys.readouterr()
    assert "x-wing" in out

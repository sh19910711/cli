from helpers import *


def test_add_device(app):
    run(["add-device", "x-wing"])
    assert rails("Device.find_by_name('x-wing').app.name") == app

from helpers import *


def test_deploy(app):
    run(["config"])
    run(["add-device", "x-wing"])
    run(["deploy"])
    assert rails("Deployment.all.last.app.name") == app

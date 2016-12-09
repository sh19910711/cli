from helpers import *


def test_add_device(app):
    run(["config"])
    run(["deploy"])
    assert rails("Deployment.all.first.app.name") == app
    assert rails("Build.all.first.app.name") == app

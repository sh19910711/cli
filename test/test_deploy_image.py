from helpers import *


def test_deploy_image(app):
    run(["deploy-image", fixture_path("example.esp8266.image")])
    assert rails("Deployment.all.first") != ""

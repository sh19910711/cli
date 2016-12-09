import os
from helpers import *


def test_config(app):
    run(["config"])
    assert os.path.exists(".config.yaml")

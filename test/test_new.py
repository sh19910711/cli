import os
import time
import subprocess
import shutil
import py
import pytest
import makestack


class ServerStartupError(Exception):
    pass

class Server:
    def __init__(self):
        self.process = subprocess.Popen(["./test/launch_server.sh"],
                           stdout=subprocess.PIPE)
        os.environ["MAKESTACK_SERVER_URL"] = "http://localhost:31313"
        os.environ["MAKESTACK_USERNAME"]   = "luke"
        os.environ["MAKESTACK_PASSWORD"]   = "12345678"
        os.environ["MAKESTACK_CONFIG_DIR"] = "tmp/test/config"

        for _ in range(0, 100):
            if "Use Ctrl-C to stop" in self.process.stdout.readline().decode('utf-8'):
                break
        else:
            raise ServerStartupError()

        os.makedirs(os.environ["MAKESTACK_CONFIG_DIR"], exist_ok=True)
        makestack.main.main(['makestack', 'login'])

    def __del__(self):
        shutil.rmtree(os.environ["MAKESTACK_CONFIG_DIR"], ignore_errors=True)
        self.process.kill()
        self.process.wait()


@pytest.fixture
def server():
    return Server()

def test_register(server):
    makestack.main.main(['makestack', 'new', '--register', 'hello'])
    yml = py.path.local("hello/application.yaml")
    assert yml.ensure()
    assert "name: hello" in yml.read()

def teardown_function(function):
    shutil.rmtree("hello", ignore_errors=True)
    shutil.rmtree("tmp/test", ignore_errors=True)

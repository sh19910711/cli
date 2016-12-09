import os
import subprocess
import shutil
import signal
import pytest
import makestack

class ServerStartupError(Exception):
    pass

class Server:
    def __enter__(self):
        self.process = subprocess.Popen(["./test/launch_server.sh"],
                           stdout=subprocess.PIPE, preexec_fn=os.setsid)

        for _ in range(0, 100):
            if "Use Ctrl-C to stop" in self.process.stdout.readline().decode('utf-8'):
                break
        else:
            raise ServerStartupError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(os.environ["MAKESTACK_CONFIG_DIR"], ignore_errors=True)
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        self.process.wait()


def remove_dirs():
    shutil.rmtree("hello", ignore_errors=True)
    shutil.rmtree("tmp/test", ignore_errors=True)


@pytest.yield_fixture
def server():
    with Server() as s:
        remove_dirs()
        makestack.main.main(['makestack', 'login'])
        yield s
        remove_dirs()


@pytest.yield_fixture
def server_no_login():
    with Server() as s:
        remove_dirs()
        yield s
        remove_dirs()


@pytest.yield_fixture
def app(server):
    app_name = 'test-app'

    cwd = os.getcwd()
    os.chdir('tmp/test')
    makestack.main.main(['makestack', 'new', '--register', app_name])
    os.chdir(app_name)
    yield app_name
    os.chdir(cwd)

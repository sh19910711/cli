import os
import subprocess
import shutil
import signal
import pytest
import makestack


def remove_dirs():
    shutil.rmtree("hello", ignore_errors=True)
    shutil.rmtree("tmp/test", ignore_errors=True)


@pytest.yield_fixture
def server():
    remove_dirs()
    rb = "require 'database_cleaner'; DatabaseCleaner.strategy = :truncation; DatabaseCleaner.clean"
    subprocess.Popen(["bundle", "exec", "rails", "runner", rb],
                     cwd=os.path.abspath("server")).wait()
    subprocess.Popen(["bundle", "exec", "rails", "db:seed"],
                     cwd=os.path.abspath("server")).wait()
    makestack.main.main(['makestack', 'login'])
    yield
    remove_dirs()


@pytest.yield_fixture
def server_no_login():
    remove_dirs()
    subprocess.Popen(["bundle", "exec", "rails", "db:reset"],
                     cwd=os.path.abspath("server")).wait()
    yield
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

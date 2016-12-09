import os
import subprocess
import makestack


server_dir = os.path.abspath("server")
def rails(rb):
    cwd = os.getcwd()
    os.chdir(server_dir)
    p = subprocess.run(["bundle", "exec", "rails", "runner", "puts " + rb],
                       universal_newlines=True, stdout=subprocess.PIPE)
    os.chdir(cwd)
    return p.stdout.rstrip()


fixture_dir = os.path.abspath(os.path.join("test", "fixtures"))
def fixture_path(fixture):
    return os.path.join(fixture_dir, fixture)


def run(cmd):
    makestack.main.main(["makestack"] + cmd)

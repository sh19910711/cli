import os
import subprocess
import makestack

server_dir = os.path.join(os.getcwd(), "server")

def server(rb):
    cwd = os.getcwd()
    os.chdir(server_dir)
    p = subprocess.run(["bundle", "exec", "rails", "runner", "puts " + rb],
                       universal_newlines=True, stdout=subprocess.PIPE)
    os.chdir(cwd)
    return p.stdout.rstrip()

def run(cmd):
    makestack.main.main(["makestack"] + cmd)

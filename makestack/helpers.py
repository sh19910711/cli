import os
import sys
import jinja2
from termcolor import cprint, colored


def import_module(module):
    m = __import__(module)

    for x in module.split('.'):
        m = getattr(m, x)

    return m


def error(msg):
    cprint("makestack: " + msg, 'red', attrs=['bold'], file=sys.stderr)
    sys.exit(1)


def progress(cmd, target):
    print('{:16}{}'.format(colored(cmd, 'cyan'), target))


def generate_dir(path):
    progress('MKDIR', path)
    try:
        os.makedirs(path)
    except FileExistsError:
        error("'{}' already exists".format(path))


def generate_file(path, tmpl, args=None):
    if args == None:
        args = {}

    progress('GEN', path)
    with open(path, 'w') as f:
        f.write(jinja2.Template(tmpl).render(args))

import sys
from termcolor import cprint


def import_module(module):
    m = __import__(module)

    for x in module.split('.'):
        m = getattr(m, x)

    return m


def error(msg):
    cprint("makestack: " + msg, 'red', attrs=['bold'], file=sys.stderr)
    sys.exit(1)

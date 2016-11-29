import glob
import os
import re
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


def info(msg):
    cprint("makestack: " + msg, 'blue', attrs=['bold'])


def success(msg):
    cprint("makestack: " + msg, 'green', attrs=['bold'])


def progress(cmd, target):
    print('{:16}{}'.format(colored(cmd, 'cyan'), target))


def generate_dir(path):
    progress('MKDIR', path)
    try:
        os.makedirs(path)
    except FileExistsError:
        error("'{}' already exists".format(path))


def detect_device_path():
    DEVICE_FILE_PATTERNS = [ r"ttyUSB[0-9]", "tty.usbserial-" ]
    files = []

    for path in glob.glob("/dev/tty*"):
        filename = os.path.basename(path)
        for pattern in DEVICE_FILE_PATTERNS:
            if re.match(pattern, filename) is not None:
                files.append(path)

    if len(files) == 0:
        error("No devices found.")
    elif len(files) > 1:
        error("Multiple device found. Speicify by --device-path.")

    return files[0]


def generate_file(path, tmpl, args=None):
    if args == None:
        args = {}

    progress('GEN', path)
    with open(path, 'w') as f:
        f.write(jinja2.Template(tmpl).render(args))

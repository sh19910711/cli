import os
import tempfile
import urllib.request
from makestack import api
from makestack.consts import *
from makestack.helpers import *


def main(args):
    try:
        board = import_module('makestack.boards.{}'.format(args.board))
    except ImportError:
        error('unknown board type: {}'.format(args.board))

    if args.device_secret is None:
        r = api.invoke('POST', 'devices', params={ name: args.device_name, board: args.board })
        device_secret = r.json()['device_secret']
    else:
        device_secret = args.device_secret

    if args.firmware is None:
        original = os.path.join(CONFIG_DIR_PATH,
                                'cache',
                                'firmware',
                                args.board, '.img')

        if not os.path.exists(original):
            urllib.request.urlretrive(board.get_firmware_url(), original)
    else:
        original = args.firmware

    with tempfile.NamedTemporaryFile() as f:
        image = open(original, 'rb').read()
        f.write(image)
        f.flush()
        board.install(args.path, f.name)

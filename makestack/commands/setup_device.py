import os
import tempfile
import struct
import urllib.request
import urllib.parse
from makestack import api
from makestack.consts import *
from makestack.helpers import *


def register_new_device(device_name, board):
    r = api.invoke('POST', 'devices', params={ name: device_name, board: board })
    return r.json()['device_secret']


def get_stable_firmware(firmware_url):
    path = os.path.join(CONFIG_DIR_PATH, 'cache', 'firmware',
                        os.path.basename(firmware_url))

    if not os.path.exists(path):
        urllib.request.urlretrive(firmware_url, path)

    return path


def replace_and_fill(b, old, new):
    if len(old) < len(new):
        error("too long string: {}".format(new))

    return b.replace(bytes(old, encoding='utf-8'),
                     struct.pack("{}s".format(len(old)), bytes(new, encoding='utf-8')))


def main(args):
    try:
        board = import_module('makestack.boards.{}'.format(args.board))
    except ImportError:
        error('unknown board type: {}'.format(args.board))

    if args.device_secret is None:
        device_secret = register_new_device(args.device_name, args.board)
    else:
        device_secret = args.device_secret

    url = get_credentials()['url']
    parsed_url = urllib.parse.urlparse(url)
    port = str(parsed_url.port)
    tls = 'yes' if parsed_url.scheme == 'https' else 'no'

    if args.firmware is None:
        original = get_stable_firmware(board.get_firmware_url())
    else:
        original = args.firmware

    with tempfile.NamedTemporaryFile() as f:
        image = open(original, 'rb').read()

	image = replace_and_fill(image, "__VERY_VERY_LONG_SERVER_HOST_NAME__REPLACE_ME__", url)
	image = replace_and_fill(image, "__PORT__REPLACE_ME__", port)
	image = replace_and_fill(image, "__TLS__REPLACE_ME__", tls)
	image = replace_and_fill(image, "__VERY_VERY_LONG_DEVICE_SECRET__REPLACE_ME__", device_secret)
	image = replace_and_fill(image, "__WIFI_SSID__REPLACE_ME__", args.wifi_ssid)
	image = replace_and_fill(image, "__WIFI_PASSWORD__REPLACE_ME__", args.wifi_password)

        f.write(image)
        f.flush()
        board.install(args.path, f.name)

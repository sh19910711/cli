import os
import sys
import serial
import time
from makestack.helpers import *


def main(args):
    if args.device_path:
        device_path = args.device_path
    else:
        device_path = detect_device_path()

    serial_port = serial.Serial(device_path, 115200, timeout=1)
    info("listening {}...".format(device_path))

    try:
        while True:
            try:
                b = serial_port.read()
                s = b.decode('ascii')
            except UnicodeDecodeError:
                print(repr(b), end='')
                pass
            else:
                print(s, end='')
                sys.stdout.flush()
    except KeyboardInterrupt:
        serial_port.close()
        sys.exit()


if __name__ == '__main__':
    main()

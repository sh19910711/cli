import sys
import argparse
from makestack import commands


def main(argv):
    parser = argparse.ArgumentParser(description='MakeStack CLI')
    subparsers = parser.add_subparsers()

    login_command = subparsers.add_parser('login')
    login_command.set_defaults(func=commands.login.main)

    register_command = subparsers.add_parser('register')
    register_command.set_defaults(func=commands.register.main)

    setup_device_command = subparsers.add_parser('setup-device')
    setup_device_command.set_defaults(func=commands.setup_device.main)
    setup_device_command.add_argument('board', help='The board type.')
    setup_device_command.add_argument('path', help='The file path to the device.')
    setup_device_command.add_argument('device_name', help='The device name.')
    setup_device_command.add_argument('--wifi-ssid', default='', help='The Wi-Fi SSID.')
    setup_device_command.add_argument('--wifi-password', default='', help='The Wi-Fi password.')
    setup_device_command.add_argument('--firmware', help='The firmware file.')
    setup_device_command.add_argument('--device-secret', help='The device secret token.')

    devices_command = subparsers.add_parser('devices')
    devices_command.set_defaults(func=commands.devices.main)

    deploy_command = subparsers.add_parser('deploy')
    deploy_command.set_defaults(func=commands.deploy.main)

    deploy_image_command = subparsers.add_parser('deploy-image')
    deploy_image_command.set_defaults(func=commands.deploy_image.main)
    deploy_image_command.add_argument('image', help='The image file.')

    args = parser.parse_args(argv[1:])

    if 'func' not in dir(args):
        parser.print_help()
        sys.exit(1)

    args.func(args)

import sys
import argparse
from makestack import commands, VERSION


def main(argv):
    parser = argparse.ArgumentParser(description='MakeStack CLI')
    parser.add_argument('--version', action='version',
                        version='MakeStack CLI version {}'.format(VERSION))
    subcommands = parser.add_subparsers()

    new_command = subcommands.add_parser('new')
    new_command.set_defaults(func=commands.new.main)
    new_command.add_argument('path', help='The path to the directory to be created.')
    new_command.add_argument('--register', help='Register the newly created app in the server.')

    config_command = subcommands.add_parser('config')
    config_command.set_defaults(func=commands.config.main)

    log_command = subcommands.add_parser('log')
    log_command.set_defaults(func=commands.log.main)

    login_command = subcommands.add_parser('login')
    login_command.set_defaults(func=commands.login.main)

    register_command = subcommands.add_parser('register')
    register_command.set_defaults(func=commands.register.main)

    setup_device_command = subcommands.add_parser('setup-device')
    setup_device_command.set_defaults(func=commands.setup_device.main)
    setup_device_command.add_argument('board', help='The board type.')
    setup_device_command.add_argument('path', help='The file path to the device.')
    setup_device_command.add_argument('device_name', help='The device name.')
    setup_device_command.add_argument('--wifi-ssid', default='', help='The Wi-Fi SSID.')
    setup_device_command.add_argument('--wifi-password', default='', help='The Wi-Fi password.')
    setup_device_command.add_argument('--firmware', help='The firmware file.')
    setup_device_command.add_argument('--device-secret', help='The device secret token.')

    devices_command = subcommands.add_parser('devices')
    devices_command.set_defaults(func=commands.devices.main)

    env_command = subcommands.add_parser('env')
    env_commands = env_command.add_subparsers()

    env_list_command = env_commands.add_parser('list')
    env_list_command.add_argument('device_name')
    env_list_command.set_defaults(func=commands.env.list_)

    env_set_command = env_commands.add_parser('set')
    env_set_command.add_argument('device_name')
    env_set_command.add_argument('key')
    env_set_command.add_argument('value')
    env_set_command.set_defaults(func=commands.env.set_)

    deploy_command = subcommands.add_parser('deploy')
    deploy_command.set_defaults(func=commands.deploy.main)

    deploy_image_command = subcommands.add_parser('deploy-image')
    deploy_image_command.set_defaults(func=commands.deploy_image.main)
    deploy_image_command.add_argument('image', help='The image file.')

    args = parser.parse_args(argv[1:])

    if 'func' not in dir(args):
        parser.print_help()
        sys.exit(1)

    args.func(args)

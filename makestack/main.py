import sys
import argparse
from makestack import commands, __version__


def main(argv):
    parser = argparse.ArgumentParser(prog='makestack', description='MakeStack CLI')
    parser.add_argument('--version', action='version',
                        version='MakeStack CLI version {}'.format(__version__))
    subcommands = parser.add_subparsers()

    new_command = subcommands.add_parser('new')
    new_command.set_defaults(func=commands.new.main)
    new_command.add_argument('path', help='The path to the directory to be created.')
    new_command.add_argument('--register', action='store_true', help='Register the newly created app in the server.')

    config_command = subcommands.add_parser('config')
    config_command.set_defaults(func=commands.config.main)
    config_command.add_argument('--appdir', default='.', help='The app directory.')

    add_device_command = subcommands.add_parser('add-device')
    add_device_command.set_defaults(func=commands.add_device.main)
    add_device_command.add_argument('device_name', help="The device name.")
    add_device_command.add_argument('--appdir', default='.', help='The app directory.')

    log_command = subcommands.add_parser('log')
    log_command.set_defaults(func=commands.log.main)

    login_command = subcommands.add_parser('login')
    login_command.set_defaults(func=commands.login.main)

    register_command = subcommands.add_parser('register')
    register_command.set_defaults(func=commands.register.main)
    register_command.add_argument('--appdir', default='.', help='The app directory.')

    setup_device_command = subcommands.add_parser('setup-device')
    setup_device_command.set_defaults(func=commands.setup_device.main)
    setup_device_command.add_argument('board', help='The board type.')
    setup_device_command.add_argument('device_name', help='The device name.')
    setup_device_command.add_argument('--device-path', help='The file path to the device file.')
    setup_device_command.add_argument('--wifi-ssid', default='', help='The Wi-Fi SSID.')
    setup_device_command.add_argument('--wifi-password', default='', help='The Wi-Fi password.')
    setup_device_command.add_argument('--firmware', help='The firmware file.')
    setup_device_command.add_argument('--device-secret', help='The device secret token.')
    setup_device_command.add_argument('--reinstall', action='store_true', help='Reinstall the firmware.')

    serial_command = subcommands.add_parser('serial')
    serial_command.set_defaults(func=commands.serial.main)
    serial_command.add_argument('--device-path', help='The file path to the device file')

    devices_command = subcommands.add_parser('devices')
    devices_command.set_defaults(func=commands.devices.main)

    user_command = subcommands.add_parser('user')
    user_commands = user_command.add_subparsers()

    user_change_password_command = user_commands.add_parser('change-password')
    user_change_password_command.set_defaults(func=commands.user.change_password)

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
    deploy_command.add_argument('--appdir', default='.', help='The app directory.')
    deploy_command.add_argument('--comment', help="The deployment comment.")

    deploy_image_command = subcommands.add_parser('deploy-image')
    deploy_image_command.set_defaults(func=commands.deploy_image.main)
    deploy_image_command.add_argument('image', help='The image file.')
    deploy_image_command.add_argument('--appdir', default='.', help='The app directory.')
    deploy_image_command.add_argument('--comment', help="The deployment comment.")

    args = parser.parse_args(argv[1:])

    if 'func' not in dir(args):
        parser.print_help()
        sys.exit(1)

    args.func(args)

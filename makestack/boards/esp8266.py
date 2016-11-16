import subprocess


def get_firmware_url():
    return 'https://github.com/makestack/esp8266-firmware/releases/download/v0.1.0/firmware.bin'


def install(serial, firmware_path):
    subprocess.run(['esptool', '-v', '-cd', 'ck', '-cb', '921600',
                    '-cp', serial, '-ca', '0x00000', '-cf', firmware_path])

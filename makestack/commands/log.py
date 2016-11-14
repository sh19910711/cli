import os
import sys
import time
import datetime
from termcolor import colored
from makestack import appdir, api


def main(args):
    appdir.get_current_app_name()
    app_name = appdir.get_current_app_name()

    # TODO: use WebSocket
    since = None
    try:
        while True:
            r = api.invoke('GET', '/apps/{}/log'.format(app_name), { 'since': since })
            for line in r.json()['log']:
                timestamp, _, device, message = line.split(':', 3)
                date = datetime.datetime.fromtimestamp(float(timestamp))
                print("{date}  {device} | {message}".format(**{
                    'date': colored(date.strftime('%H:%M:%S'), 'blue'),
                    'device': colored(device, 'magenta'),
                    'message': message
                }))

                since = timestamp

            time.sleep(4)
    except KeyboardInterrupt:
        sys.exit()

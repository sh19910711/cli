import os
import sys
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
            r = api.invoke('GET', '/apps/{}/log'.format(app_name), { since: since })
            for time, _, device, message in r.json().get('lines', []):
                date = datetime.datetime.fromtimestamp(time)
                print("{date}  {device} | {message}".format(**{
                    'date': colored(date.strftime('%H:%M:%S'), 'blue'),
                    'date': colored(device, 'magenta'),
                    'message': message
                }))

                since = time

            time.sleep(4)
    except KeyboardInterrupt:
        sys.exit()

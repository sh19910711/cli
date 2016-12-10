import os
from urllib.parse import urljoin
import requests
import yaml
from makestack.helpers import error
from makestack.consts import *


def get_credentials():
    try:
        yml = yaml.load(open(CREDENTIAL_YAML_PATH))
    except FileNotFoundError:
        error('Credentials not found. Do `makestack login`.')

    return yml


def request(method, url, params=None, headers=None, files=None):
    return requests.request(method, url, params=params,
              headers=headers, files=files)


def login(baseurl, username, password):
    url = urljoin(baseurl, 'api/auth/sign_in')

    r = request('POST', url, params={
        "name": username,
        "password": password
    })

    if 'Access-Token' not in r.headers:
        error('authentication failed')

    headers = {}
    for k, v in r.headers.items():
        if k.lower() in ["access-token", "token-type", "client", "expiry", "uid"]:
            headers[k] = v

    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)
    open(CREDENTIAL_YAML_PATH, 'w').close()
    os.chmod(CREDENTIAL_YAML_PATH, 0o600)

    yaml.dump({ "username": username, "url": baseurl, "auth": headers },
              open(CREDENTIAL_YAML_PATH, 'w'))


def invoke(method, path, params=None, headers=None, files=None, prepend_user_path=True):
    credentials = get_credentials()

    if prepend_user_path:
        url = urljoin(credentials['url'], 'api/{}/{}'.format(
            credentials['username'], path))
    else:
        url = urljoin(credentials['url'], 'api/{}'.format(path))

    if headers is None:
        headers = {}

    headers.update(credentials["auth"])

    try:
        r = request(method, url, params, headers, files)
    except requests.exceptions.ConnectionError as e:
        error("connection error: {}".format(e))

    if 500 <= r.status_code <= 599:
        error("server: something went wrong :(")

    if not (200 <= r.status_code <= 299):
        j = r.json()
        if "error" in j:
            if "validation_errors" in j:
                details = ""
                for column, msgs in j["validation_errors"].items():
                    for msg in msgs:
                        details += "\n- `{}' {}".format(column, msg)
            else:
                details = ""

            error("server ({}): {}{}".format(r.status_code, j["error"], details))

    return r

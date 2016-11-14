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
        "username": username,
        "password": password
    })

    if 'Token' not in r.headers:
        error('authentication failed')

    token = r.headers['Token']

    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)
    open(CREDENTIAL_YAML_PATH, 'w').close()
    os.chmod(CREDENTIAL_YAML_PATH, 0o600)

    yaml.dump({ "username": username, "url": baseurl, "token": token },
              open(CREDENTIAL_YAML_PATH, 'w'))


def invoke(method, path, params=None, headers=None, files=None):
    credentials = get_credentials()
    url = urljoin(credentials['url'], 'api/{}/{}'.format(credentials['username'], path))

    if headers is None:
        headers = {}

    headers['Authorization'] = 'token ' + credentials['token']
    try:
        r = request(method, url, params, headers, files)
    except requests.exceptions.ConnectionError as e:
        error("connection error: {}".format(e))

    if not (200 <= r.status_code <= 299):
        error("server returned {}".format(r.status_code))

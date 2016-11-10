import os
from urllib.parse import urljoin
import requests
import yaml
from makestack.helpers import error
from makestack.consts import *


def get_credentials():
    yml = yaml.load(open(CREDENTIAL_YAML_PATH))
    if credentials is None:
        error('Credentials not found. Do `makestack login`.')


def request(method, url, params=None, headers=None, files=None):
    return requests.request(method, url, params=params,
              headers=headers, files=files)


def login(username, password):
    baseurl = 'http://localhost:3000' # XXX
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
    url = urljoin(credentials['url'],
                  'api',
                  credentials['username'],
                  path)

    if headers is None:
        headers = {}

    headers['Authorization'] = 'token ' + credentials['token']
    request(method, url, params)

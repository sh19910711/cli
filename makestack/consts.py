import os


CONFIG_DIR_PATH = os.path.abspath(
    os.environ.get("MAKESTACK_CONFIG_DIR", os.path.expanduser('~/.makestack')))

CREDENTIAL_YAML_PATH = os.path.join(CONFIG_DIR_PATH,
                                    'credentials.yaml')

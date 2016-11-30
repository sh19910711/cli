import yaml
from makestack import appdir
from makestack.helpers import progress


DEFAULT_CONFIG = {
    'BOARD': {
        'type': 'str',
        'value': 'esp8266'
    }
}

def main(args):
    appdir.chdir_to_app_dir(args.appdir)

    application_yaml = yaml.load(open('application.yaml'))
    app_config = {} if application_yaml['config'] is None else application_yaml['config']

    config = DEFAULT_CONFIG
    for k, c in app_config.items():
        if 'default' in c:
            c['value'] = c['default']
            del c['default']

        config[k] = c

    progress('GEN', '.config.yaml')
    yaml.dump(config, open('.config.yaml', 'w'), default_flow_style=False)

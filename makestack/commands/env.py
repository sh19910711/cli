from makestack import api


def list_(args):
    r = api.invoke('GET', '/devices/{}/envvars'.format(args.device_name))
    for env in r.json()['envvars']:
        print("{name}={value}".format(**env))


def set_(args):
    api.invoke('PUT', '/devices/{}/envvars/{}'.format(
        args.device_name, args.key), params={ "value": args.value })

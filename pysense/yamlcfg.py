import confuse


config = confuse.LazyConfig('pySense', __name__)
template = {
    'sense': {
        'username': str,
        'password': str,
        'api': {
            'url': str,
            'timeout': int,
        },
        'realtime': {
            'url': str,
        },
    },
    'websocket': {
        'timeout': int,
    }
}


yamlcfg = config.get(template)

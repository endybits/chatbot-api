import os
import json


path = './core/config.json'

if not os.path.exists(path):
    raise Exception(f'The config file config.json is missing')

def get_config(filename: str = None):
    config = json.loads(open(filename, 'r').read())
    return config

cfg = get_config(path)

OPENAI_APIKEY = cfg.get('api').get('openai_apikey')
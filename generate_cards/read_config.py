import os

import yaml


def read_config(config_file='config.yaml'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, config_file), 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


CONFIG = read_config()

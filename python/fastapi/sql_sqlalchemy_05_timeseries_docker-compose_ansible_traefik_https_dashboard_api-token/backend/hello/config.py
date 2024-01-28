import os
import yaml
import random
import string
#from dataclasses import dataclass

import hello.path

DEFAULT_CONFIG_PATH = "~/.hello.yml"

DEFAULT_CONFIG_STR = f"""# Hello configuration file

# The API token
# Generate random token: tr -dc A-Za-z0-9 </dev/urandom | head -c 64 ; echo ''
api_token: "..."
"""


# # Dataclass: c.f. https://docs.python.org/3/library/dataclasses.html and https://stackoverflow.com/questions/31252939/changing-values-of-a-list-of-namedtuples/31253184
# @dataclass
# class Config:
#     api_token: str



def get_config(config_path: str = None) -> (dict, str):
    """
    Get the configuration dictionary and the path to the configuration file.

    Parameters
    ----------
    config_path : str, optional
        The path to the configuration file.

    Returns
    -------
    (dict, str)
        The configuration dictionary and the path to the configuration file.
    """   
    if config_path is None:
        if 'HELLO_CONFIG_PATH' in os.environ:
            config_path = os.environ['HELLO_CONFIG_PATH']
        else:
            config_path = DEFAULT_CONFIG_PATH

    config_path = hello.path.expand_path(config_path)

    # Make sure the configuration file exists
    if not os.path.exists(config_path):
        make_default_config_file(config_path)

    with open(config_path) as stream:
        config_dict = yaml.safe_load(stream)
        # config = Config(**config_dict)

    return config_dict, config_path


def make_default_config_file(config_path: str = None):
    """
    Make a default configuration file.

    Parameters
    ----------
    config_path : str, optional
        The path to the configuration file.
    """    
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    config_path = hello.path.expand_path(config_path)
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as stream:
            stream.write(DEFAULT_CONFIG_STR)

import os
import sys
import configparser


def read_configs(path):
    config_path = os.path.abspath(path)
    config = configparser.ConfigParser()
    config.read(path)
    config = config['update-route53-ip']
    config['config_path'] = config_path
    _validate_configs(config)
    return config


def _validate_configs(config):
    required_keys = ['aws_key', 'aws_key_id', 'hosted_zone_id', 'domain_name', 'ip_lookup_url', 'record_type']
    for item in required_keys:
        _validate_config(config, item)


def _validate_config(config, item_name):
    if not item_name in config or len(config[item_name]) == 0 or "~" in config[item_name]:
        sys.exit(f"{item_name} was set incorrectly.  Please check {config['config_path']}")

import os
import sys
import configparser
from pathlib import Path


def read_configs():
    path = _locateConfigFile()
    config_path = os.path.abspath(path)
    config = configparser.ConfigParser()
    config.read(path)
    config = config['update-route53-ip']
    config['config_path'] = config_path
    _validate_configs(config)
    return config


def _locateConfigFile():
    prod_path = "/opt/update-route53-ip/config"
    dev_path = "../packaging/config"
    if Path(prod_path).is_file():
        return prod_path
    if Path(dev_path).is_file():
        return dev_path
    sys.exit(f"ERROR: Unable to locate config file at {prod_path}.  Exiting.")


def _validate_configs(config):
    _validate_required_keys(config)
    _validate_dry_run_value(config)


def _validate_required_keys(config):
    required_keys = ['aws_key', 'aws_key_id', 'hosted_zone_id', 'domain_name', 'ip_lookup_url', 'record_type', 'dry_run']
    for item in required_keys:
        _validate_config(config, item)


def _validate_dry_run_value(config):
    config['dry_run'] = config['dry_run'].lower()
    if config['dry_run'] == 'true' or config['dry_run'] == 'false':
        return
    sys.exit(f"ERROR: Config item dry_run must be set to either 'true' or 'false'.  Was set to {config['dry_run']}. Please check {config['config_path']}")


def _validate_config(config, item_name):
    if not item_name in config or len(config[item_name]) == 0 or "~" in config[item_name]:
        sys.exit(f"ERROR: Config item {item_name} was set incorrectly.  Please check {config['config_path']}")

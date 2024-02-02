import sys
import os
import re
import time
import requests
import boto3
import configparser

def get_external_ip(config):
    """Get the external IP address."""
    url = config['ip_lookup_url']
    response = requests.get(url)
    return response.text

def update_route53_record(config, new_ip):
    """Update the Route 53 record."""
    client = boto3.client(
        'route53',
        aws_access_key_id=config['key_id'],
        aws_secret_access_key=config['key']
    )
    response = client.change_resource_record_sets(
        HostedZoneId=config['hosted_zone_id'],
        ChangeBatch={
            'Comment': 'update IP address',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': config['domain_name'],
                    'Type': config['record_type'],
                    'TTL': 300,
                    'ResourceRecords': [{'Value': new_ip}],
                }
            }]
        }
    )
    return response

def monitor_ip_change(config, interval):
    """Monitor the IP address and update Route 53 record if it changes."""

    print("Monitoring IP address for changes...")
    current_ip = None
    while True:
        new_ip = get_external_ip(config)
        if new_ip != current_ip:
            response = update_route53_record(config, new_ip)
            print(f"Updated IP address in Route 53: {response}")
            current_ip = new_ip
        time.sleep(interval)

def read_configs(path="packaging/config"):
    config_path = pretty_path(path)
    config = configparser.ConfigParser()
    config.read(path)
    config = config['update-route53-ip']
    config['config_path'] = config_path

    validate_configs(config)

    return config

def validate_configs(config):
    config_items = ['aws_key', 'aws_key_id', 'hosted_zone_id', 'domain_name']
    for item in config_items:
        validate_config(config, item)

def validate_config(config, item_name):
    if len(config[item_name]) == 0 or "~" in config[item_name]:
        sys.exit(f"{item_name} was set incorrectly.  Please check {config['config_path']}")

def pretty_path(path):
    config_path = os.path.abspath(path)
    home_dir = os.path.expanduser("~")
    if config_path.startswith(home_dir):
        pretty_config_path = config_path.replace(home_dir, "~", 1)
    else:
        pretty_config_path = config_path
    return pretty_config_path

if __name__ == '__main__':
    config = read_configs()

    # Call the monitor function
    # monitor_ip_change(config, interval=300)

    # debug
    print("the service booted correctly.")
    time.sleep(30)

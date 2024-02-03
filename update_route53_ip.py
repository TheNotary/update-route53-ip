import sys
import os
import re
import time
import requests
import boto3
import configparser
from ipaddress import ip_address

def monitor_ip_change(config, interval):
    """Monitor the IP address and update Route 53 record if it changes."""

    print("Monitoring IP address for changes...")
    current_ip = None
    while True:
        new_ip = get_external_ip(config)
        if is_invalid_ip(new_ip):
            print(f"Recieved invalid ip from lookup url.  [{new_ip}].  Waiting to retry...")
            time.sleep(interval * 2)
            continue

        if new_ip != current_ip:
            response = update_route53_record(config, new_ip)
            print(f"Updated IP address in Route 53 to {new_ip}: {response}")
            current_ip = new_ip
        time.sleep(interval)

def get_external_ip(config):
    """Get the external IP address."""
    url = config['ip_lookup_url']
    response = requests.get(url)
    return response.text

def is_invalid_ip(ip):
    cider_things = ip.split('.')
    if len(cider_things) != 4:
        return True

    # check that all the numbers separated by '.'s have at least one number, and no more than 3
    for x in cider_things:
        if len(x) < 1 or len(x) > 3:
            return True

    return False

def update_route53_record(config, new_ip):
    """Update the Route 53 record."""
    client = boto3.client(
        'route53',
        aws_access_key_id=config['aws_key_id'],
        aws_secret_access_key=config['aws_key']
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

def read_configs(path):
    config_path = os.path.abspath(path)
    config = configparser.ConfigParser()
    config.read(path)
    config = config['update-route53-ip']
    config['config_path'] = config_path

    validate_configs(config)

    return config

def validate_configs(config):
    required_keys = ['aws_key', 'aws_key_id', 'hosted_zone_id', 'domain_name', 'ip_lookup_url', 'record_type']
    for item in required_keys:
        validate_config(config, item)

def validate_config(config, item_name):
    if not item_name in config or len(config[item_name]) == 0 or "~" in config[item_name]:
        sys.exit(f"{item_name} was set incorrectly.  Please check {config['config_path']}")

if __name__ == '__main__':
    config_path = "/opt/update-route53-ip/config"
    # config_path = "packaging/config" # for debugging
    config = read_configs(config_path)
    monitor_ip_change(config, interval=300)

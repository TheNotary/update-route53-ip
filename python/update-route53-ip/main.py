import time
from config_reader import read_configs
from aws_helper import update_route53_record
from ip_lookup_client import IpLookupClient


def monitor_for_ip_change(config, interval):
    """Monitor the IP address and update Route 53 record if it changes."""
    print("Monitoring IP address for changes...")
    ip_lookup_client = IpLookupClient(config)
    while True:
        if ip_lookup_client.check_ip_change():
            # print("IP Change detected as: ", ip_lookup_client.ip)
            update_route53_record(config, ip_lookup_client.ip)
        time.sleep(interval)


if __name__ == '__main__':
    config_path = "/opt/update-route53-ip/config"
    # config_path = "../packaging/config" # for debugging
    config = read_configs(config_path)
    monitor_for_ip_change(config, interval=300)

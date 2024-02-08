import time
from config_reader import read_configs
from aws_helper import update_route53_record, resolve_domain_name
from ip_lookup_client import IpLookupClient


class IpMonitor():
    """Monitor the IP address and update Route 53 record if it changes."""
    def __init__(self, config, interval):
        self.config = config
        self.interval = interval
        self.count = 0

    def monitor(self):
        print("Monitoring IP address for changes...")
        ip_lookup_client = IpLookupClient(self.config)
        while True:
            if ip_lookup_client.check_ip_change():
                if self.config['dry_run'] == 'true':
                    print("INFO: IP Change detected as: ", ip_lookup_client.ip)
                    print("INFO: dry_run was set, skipping.")
                else:
                    update_route53_record(self.config, ip_lookup_client.ip)
            # if the IP address is changed outside of this program, the program
            # won't know to overwrite the IP back to what it's meant to be
            if self.__should_check_dns_directly() and self.__has_route53_record_changed_externally(ip_lookup_client.ip):
                print(f"WARN: The domain {self.config['domain_name']} appears to have been modified outside of this system.  Overriding now.")
                if self.config['dry_run'] == 'true':
                    print("INFO: dry_run was set, skipping.")
                else:
                    update_route53_record(self.config, ip_lookup_client.ip)
            time.sleep(self.interval)

    def __should_check_dns_directly(self):
        '''
        This function helps us keep track of how frequently we check that nothing
        outside of this script has updated our domain which could potentially
        lock us out of the cluster until someone physically goes there.
        '''
        self.count += 1
        if self.count >= 20:
            self.count = 0
        if self.count == 1:
            return True
        return False

    def __has_route53_record_changed_externally(self, local_ip):
        registered_ip = resolve_domain_name(self.config)
        return local_ip != registered_ip


if __name__ == '__main__':
    ip_monitor = IpMonitor(read_configs(), interval=300)
    ip_monitor.monitor()

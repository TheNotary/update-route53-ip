import requests

class IpLookupClient:
    '''
    Encapsulates the logic around keeping track of the current IP and checking
    to see if it has changed since we last called 'check_ip_change'.
    '''
    def __init__(self, config):
        self.url = config['ip_lookup_url']
        self.ip = None

    def check_ip_change(self):
        '''
        returns the new ip address if the ip address has changed since the last
        time we checked.  Otherwise returns None if the ip address hasn't changed
        '''
        new_ip = self.__get_external_ip()
        if self.__is_malformed_ip(new_ip):
            print(f"Error: Recieved invalid ip from lookup url.  [{new_ip}].  Waiting to retry...")
            return False
        if self.ip == new_ip:
            return False
        self.ip = new_ip
        return True

    def __get_external_ip(self):
        """Get the external IP address."""
        url = self.url
        response = requests.get(url)
        return response.text

    def __is_malformed_ip(self, ip):
        cider_things = ip.split('.')
        if len(cider_things) != 4:
            return True
        # check that all the numbers separated by '.'s have at least one number, and no more than 3
        for x in cider_things:
            if len(x) < 1 or len(x) > 3:
                return True
        return False

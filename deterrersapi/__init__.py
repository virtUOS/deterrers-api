import requests


class Deterrers:
    __base_url = None
    __token = None

    timeout = 30
    '''Request timeout in seconds'''

    def __init__(self, base_url: str, token: str) -> None:
        '''Initialize DETERRERS client.

        :param base_url: URL of the DETERRERS installation without path
        :type base_url: str
        :param token: API token to use for authentication
        :type token: str
        '''
        self.__base_url = base_url.rstrip('/')
        self.__token = token

    def __url(self, path: str) -> str:
        '''Build request URL based on API path

        :param path: API endpoint
        :type path: str
        :return: Full URL to API endpoint
        :rtype: str
        '''
        path = path.lstrip('/')
        return f'{self.__base_url}/hostadmin/api/{path}'

    def __header(self) -> dict[str, str]:
        '''Build authorization and content typüe header for request.

        :return: Header dict to use in request
        :rtype: dict[str, str]
        '''
        return {'Authorization': f'Token {self.__token}',
                'Content-Type': 'application/json'}

    def __get(self, path: str, **params):
        '''Execute API GET request.

        :param path: Endpoint to request
        :type path: str
        :return: Decoded response data or None
        '''
        response = requests.get(self.__url(path),
                                headers=self.__header(),
                                params=params,
                                timeout=self.timeout)
        return response.json() if response.status_code == 200 else None

    def __patch(self, path: str, data: dict) -> None:
        '''Execute API PATCH request

        :param path: Endpoint to request
        :type path: str
        :param data: Data to send
        :type data: dict
        :raises RuntimeError: if patch did not succeed
        '''
        url: str = self.__url(path)
        response = requests.patch(url,
                                  headers=self.__header(),
                                  json=data,
                                  timeout=self.timeout)
        if response.status_code not in [200]:
            raise RuntimeError(f'Error updating {data}. Response: {response}')

    def __post(self, path: str, data: dict) -> None:
        '''Execute API POST request

        :param path: Endpoint to request
        :type path: str
        :param data: Data to post
        :type data: dict
        :raises RuntimeError: if adding data did not succeed
        '''
        url: str = self.__url(path)
        response = requests.post(url,
                                 headers=self.__header(),
                                 json=data,
                                 timeout=self.timeout)
        if response.status_code not in [200]:
            raise RuntimeError(f'Error adding {data}. Response: {response}')

    def __delete(self, path: str, data: dict) -> None:
        '''Execute API DELETE request.

        :param path: Endpoint to request
        :type path: str
        :param data: Data identifying entity to delete
        :type data: dict
        :raises RuntimeError: if removal did not succeed
        '''
        url: str = self.__url(path)
        response = requests.delete(url,
                                   headers=self.__header(),
                                   json=data,
                                   timeout=self.timeout)
        if response.status_code not in [200, 404]:
            raise RuntimeError(f'Error deleting {data}. Response: {response}')

    def hosts(self) -> dict:
        '''Get list of hosts added to DETERRERS

        :return: List of hosts
        :rtype: list
        '''
        return self.__get('hosts/')

    def get(self, ipv4: str):
        '''Get information about an ipv4 address from DETERRERS.

        :param ipv4: IPv4 address
        :type ipv4: str
        :return: Dictionary with information
        :rtype: dict
        '''
        return self.__get('host/', ipv4_addr=ipv4)

    def add(self, ipv4: str,
            admins: list[str],
            profile: None | str = None,
            firewall: None | str = None) -> None:
        '''Add a new IP address to DETERRERS.

        :param ipv4: IPv4 address
        :type ipv4: str
        :param admins: List of admins for address
        :type admins: list[str]
        :param profile: Firewall profile to use. Must be None, a valid profile
                        or an empty string string (default: None)
        :type profile: None | str
        :param firewall: Host firewall. Must be None, one of the UI options
                         or an empty string (default: None)
        :type firewall: None | str
        '''
        data = {'ipv4_addr': ipv4,
                'admin_ids': admins}
        if profile is not None:
            data['service_profile'] = profile
        if firewall is not None:
            data['fw'] = firewall
        return self.__post('host/', data)

    def delete(self, ipv4: str) -> None:
        '''Delete IP from DETERRERS.

        :param ipv4: IPv4 address to delete
        :type ipv4: str
        '''
        return self.__delete('host/', {'ipv4_addr': ipv4})

    def update(self, ipv4: str,
               profile: None | str = None,
               firewall: None | str = None,
               admins: None | list[str] = None) -> None:
        '''Update IP address information in DETERRERS.

        :param ipv4: IPv4 address to update
        :type ipv4: str
        :param profile: Firewall profile to use.
                        Must be a valid profile or an empty string string.
        :type profile: str | None
        :param firewall: Host firewall. Must be one of the UI options
                         or an empty string.
        :type firewall: str | None
        :param admins: List of admins for address
        :type admins: list[str] | None
        '''
        data: dict[str, str | list[str]] = {'ipv4_addr': ipv4}
        if profile is not None:
            data['service_profile'] = profile
        if firewall is not None:
            data['fw'] = firewall
        if admins is not None:
            data['admin_ids'] = admins
        return self.__patch('host/', data)

    def action(self, ipv4: str, action: str, skip_scan: bool = False) -> None:
        '''Activate firewall profile or block IP address in perimeter firewall.

        :param ipv4: IPv4 address to update
        :type ipv4: str
        :param action: Action to take. Can be 'register' or 'block'
        :type action: str
        :param skip_scan: Whether to skip the initial security scan
        :type skip_scan: bool
        '''
        data = {'ipv4_addrs': [ipv4],
                'action': action,
                'skip_scan': skip_scan}
        return self.__post('action/', data)

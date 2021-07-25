#!/usr/bin/env python3

from typing import Union


class Status(object):
    """System Information Service Class"""

    def __init__(self, fmc: object):
        self.fmc = fmc
        self._host = self.fmc._host
        self._port = self.fmc._port
        self.domain = self.fmc.domain
        self.platform = self.fmc.platform
        self.params = {'expanded': True, 'offset': None, 'limit': None}

    def server_version(self, oid: Union[str] = None):
        """Requests version information for the server. If no ID is specified, retrieves a list of all servers.

        :param oid: Object ID
        :type oid: str

        :return:
        :rtype:
        """

        if oid is None:
            url = f'{self.platform}/info/serverversion/'
        else:
            url = f'{self.platform}/info/serverversion/{oid}'

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

#!/usr/bin/env python3

from typing import Union


class Status(object):
    """Status Service Class"""

    def __init__(self, fmc: object):
        self.fmc = fmc
        self._host = self.fmc._host
        self._port = self.fmc._port
        self.domain = self.fmc.domain
        self.config = self.fmc.config
        self.params = {'expanded': True, 'offset': None, 'limit': None}

    def task_statuses(self, oid: Union[str] = None):
        """Retrieves information about a previously submitted pending job/task with the specified ID.
        This is currently supported for device registration and deployment jobs.

            * Permissions: Modify Devices/Deployment

        :param oid: Object UUID
        :type oid: str

        :return:
        :rtype:
        """

        if oid is None:
            url = f'{self.config}/domain/{self.domain}/job/taskstatuses'
        else:
            url = f'{self.config}/domain/{self.domain}/job/taskstatuses/{oid}'

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

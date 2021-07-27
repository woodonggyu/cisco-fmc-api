#!/usr/bin/env python3

from typing import Union


class Deployment(object):
    """Deployment Service Class"""

    def __init__(self, fmc: object):

        self.fmc = fmc
        self._host = self.fmc._host
        self._port = self.fmc._port
        self.domain = self.fmc.domain
        self.config = self.fmc.config
        # default request parameters for 'GET' method
        self.params = {'expanded': True, 'offset': None, 'limit': None}

    def deploy_able_devices(self) -> list:
        """Retrieves list of all devices with configuration changes, ready to be deployed.

            * Permissions: Deploy Configuration to Devices
            * Parameters available for filtering: name

        :return: uuids
        :rtype: dict
        """

        url = f'{self.config}/domain/{self.domain}/deployment/' \
              f'deployabledevices'

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

    def deployment_request(self, oid: str):
        """Creates a request for deploying configuration changes to the specified device.

            * Permissions: Deploy Configuration to Devices

        :param oid: object's UUID
        :type oid: str

        :return:
        :rtype:
        """

        url = f'{self.config}/domain/{self.domain}/deployment/' \
              f'deploymentrequests/{oid}'

        return self.fmc._requests_api(method='POST', url=url, headers=None)

    def pending_changes(self, cid: str):
        """Retrieves all the policy and object changes for the selected device.

            * Permissions: Deploy Configuration to Devices

        :param cid: container's UUID
        :type cid: str

        :return:
        :rtype:
        """

        url = f'{self.config}/domain/{self.domain}/deployment/' \
              f'deployabledevices/{cid}/pendingchanges'

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

    def job_histories(self):
        """Retrieves all the deployment jobs.

            * Permissions: Deploy Configuration to Devices
            * Parameters available for filtering: Various filter criteria can be specified using the format
                deviceUUID:{uuid};
                startTime:start_time_in_secs;
                endTime:end_time_in_secs;
                rollbackApplicable:true_or_false
        """

        url = f'{self.config}/domain/{self.domain}/deployment/jobhistories'

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

    def rollback_requests(self):
        """Creates a request for rollback configuration to devices.

            * Permissions: Deploy Configuration to Devices
        """

        url = f'{self.config}/domain/{self.domain}/deployment/rollbackrequest'

        return self.fmc._request_api(method='POST', url=url, headers=None)

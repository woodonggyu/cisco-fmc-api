#!/usr/bin/env python3

from typing import Union
from urllib.parse import urljoin


class Deployment(object):
    """"""

    def __init__(self, fmc: object):

        self.fmc = fmc
        self.host = self.fmc._host
        self.port = self.fmc._port
        self.domain = self.fmc.domain
        self.ver = self.fmc.ver
        # object's uuid
        self.oid = None
        # container's uuid
        self.cid = None
        self.params = {'expanded': True, 'offset': None, 'limit': None}

    def deploy_able_devices(self) -> list:
        """Retrieves list of all devices with configuration changes, ready to be deployed.

            * Permissions: Deploy Configuration to Devices
            * Parameters available for filtering: name

        :return: uuids
        :rtype: dict
        """

        url = urljoin(base=f'{self.host}:{self.port}',
                      url=f'{self.ver}/domain/{self.domain}/'
                          f'deployment/deployabledevices',
                      allow_fragments=True)

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

    def deployment_request(self):
        """Creates a request for deploying configuration changes to the specified device.

            * Permissions: Deploy Configuration to Devices
        """

        url = urljoin(base=f'{self.host}:{self.port}',
                      url=f'{self.ver}/domain/{self.domain}/'
                          f'deployment/deploymentrequests/{self.oid}',
                      allow_fragments=True)

        return self.fmc._requests_api(method='POST', url=url, headers=None)

    def pending_changes(self):
        """Retrieves all the policy and object changes for the selected device.

            * Permissions: Deploy Configuration to Devices
        """

        url = urljoin(base=f'{self.host}:{self.port}',
                      url=f'{self.ver}/domain/{self.domain}/'
                          f'deployment/deployabledevices/'
                          f'{self.cid}/pendingchanges',
                      allow_fragments=True)

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

        url = urljoin(base=f'{self.host}:{self.port}',
                      url=f'{self.ver}/domain/{self.domain}/'
                          f'deployment/jobhistories/',
                      allow_fragments=True)

        return self.fmc._request_api(method='GET', url=url, headers=None,
                                     params=self.params)

    def rollback_requests(self):
        """Creates a request for rollback configuration to devices.

            * Permissions: Deploy Configuration to Devices
        """

        url = urljoin(base=f'{self.host}:{self.port}',
                      url=f'{self.ver}/domain/{self.domain}/'
                          f'deployment/rollbackrequest',
                      allow_fragments=True)

        return self.fmc._request_api(method='POST', url=url, headers=None)

#!/usr/bin/env python3

import datetime
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from typing import Union
from urllib.parse import urljoin
from services.deployment.deployment import Deployment
from services.status.status import Status

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FMC(Deployment, Status):
    """FMC(Firepower Management Center) Class"""

    # Can refresh up to three times
    MAX_REFRESHES = 3
    # Use for accessing resources for up to 30 minutes (1800 seconds)
    TOKEN_LIFETIME = 1800
    #
    TOKEN_REFRESH_TIME = TOKEN_LIFETIME * 0.90

    def __init__(self, host: str, port: int, username: str, password: str,
                 domain: Union[str] = None, auto_deploy: Union[bool] = True) \
            -> None:

        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.domain = domain
        self.auto_deploy = auto_deploy
        self.platform = '/api/fmc_platform/v1'
        self.config = '/api/fmc_platform/v1'
        self.access_token = None
        self.refresh_token = None
        self.token_refresh_count = None
        self.token_generation_time = None

        self.__request_an_authentication_token()

    def __del__(self):
        if self.auto_deploy:
            pass

    def _token_validation(*args):
        """"""
        call_func = args[0]
        current = datetime.datetime.now()

        def validate(self):
            if self.token_refresh_count > self.MAX_REFRESHES or \
                    self.access_token is None:
                self.__request_an_authentication_token()
            else:
                if current > self.token_geration_time + \
                        datetime.timedelta(seconds=self.TOKEN_REFRESH_TIME):
                    self.__request_an_token_refresh()
            call_func(self)

        return validate

    def _request_an_authentication_token(self):
        """The Token Generation Utility provides an authentication token which can be used in your REST API client."""

        self.token_refresh_count = 0
        self.token_generation_time = datetime.datetime.now()

        url = f'{self.platform}/auth/genratetoken'
        headers = {'Content-Type': 'application/json'}
        auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        response = self.__request_api(method='POST', url=url, headers=headers,
                                      auth=auth, verify=False)

        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-auth-refresh-token')

    def _request_an_token_refresh(self):
        """FMC REST API authentication tokens are valid for 30 minutes, and can be refreshed up to three times."""

        url = f'{self.platform}/auth/refreshtoken'
        headers = {'Content-Type': 'application/json',
                   'X-auth-access-token': self.access_token,
                   'X-auth-refresh-token': self.access_token}

        self.token_refresh_count += 1

        response = self.__request_api(method='GET', url=url, headers=headers)

        self.access_token = response.headers.get('X-auth-access-mentstoken')
        self.refresh_token = response.headers.get('X-auth-refresh-token')

    @_token_validation
    def _request_api(self, method: str, url: str, headers: Union[dict] = None,
                     params: Union[dict] = None,
                     auth: Union[HTTPBasicAuth] = None,
                     verify: Union[bool] = True) -> dict:
        """"""

        url = urljoin(base=f'{self._host}:{self._port}',
                      url=url, allow_fragments=True)
        if headers is None:
            headers = {'Content-Type': 'application/json',
                       'X-auth-access-token': self.access_token}

        response = requests.request(method=method, url=url, headers=headers,
                                    params=params, auth=auth, verify=verify)
        if response.status_code == 401:
            pass
            # TODO: define error handling
            # raise UnAuthorizedUserError

        return response.json()

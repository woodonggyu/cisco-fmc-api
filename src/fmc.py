#!/usr/bin/env python3

import datetime
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from typing import Union
from urllib.parse import urljoin

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FMC:
    """"""

    # Can refresh up to three times
    MAX_REFRESHES = 3
    # Use for accessing resources for up to 30 minutes (1800 seconds)
    TOKEN_LIFETIME = 1800
    #
    TOKEN_REFRESH_TIME = TOKEN_LIFETIME * 0.90

    def __init__(self, host: str, username: str, password: str,
                 domain: Union[str] = None, auto_deploy: Union[bool] = True) \
            -> None:

        self.__host = host
        self.__username = username
        self.__password = password
        self.domain = domain
        self.auto_deploy = auto_deploy
        self.ver = 'api/fmc_platform/v1'
        self.access_token = None
        self.refresh_token = None
        self.token_refresh_count = None
        self.token_generation_time = None

        # self.__request_an_authentication_token()

    def __del__(self):
        if self.auto_deploy:
            pass

    def __request_an_authentication_token(self):
        """The Token Generation Utility provides an authentication token which
        can be used in your REST API client."""

        self.token_refresh_count = 0
        self.token_generation_time = datetime.datetime.now()

        url = urljoin(base=self.__host, url=f'{self.ver}/auth/generatetoken',
                      allow_fragments=True)
        headers = {'Content-Type': 'application/json'}

        response = self.__request_api(
            method='POST', url=url, headers=headers,
            auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
            verify=False)

        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-auth-refresh-token')

    def __token_validation(self):
        """"""
        current = datetime.datetime.now()

        if self.token_refresh_count <= self.MAX_REFRESHES and \
                self.access_token is not None:
            self.__request_an_token_refresh()

    def __request_an_token_refresh(self):
        """FMC REST API authentication tokens are valid for 30 minutes,
        and can be refreshed up to three times."""

        url = urljoin(base=self.__host, url=f'{self.ver}/auth/refreshtoken',
                      allow_fragments=True)
        headers = {'Content-Type': 'application/json',
                   'X-auth-access-token': self.access_token,
                   'X-auth-refresh-token': self.access_token}

        self.token_refresh_count += 1

        return self.__request_api(method='GET', url=url, headers=headers)

    def __request_api(self, method: str, url: str, headers: Union[dict] = None,
                      auth: Union[HTTPBasicAuth] = None,
                      verify: Union[bool] = True) -> dict:
        """"""

        if headers is None:
            headers = {'Content-Type': 'application/json',
                       'X-auth-access-token': self.access_token}

        response = requests.request(method=method, url=url, headers=headers,
                                    auth=auth, verify=verify)
        if response.status_code == 401:
            raise UnAuthorizedUserError

        return response.json()


class UnAuthorizedUserError(Exception):
    """"""
    pass


class DisconnectedError(Exception):
    """"""
    pass


class TokenExpiredError(Exception):
    """"""
    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

BASE_URI = 'http://api.data.gov/'


class DataGovApiError(BaseException):
    """Base class for all Data.gov API errors"""
    pass


class DataGovApiRateExceededError(DataGovApiError):
    """Data.gov API rate limit has been exceeded for this key"""

    def __init__(self):
        super(DataGovApiRateExceededError, self).__init__(
            'API rate limit has been exceeded.')


def api_request(uri, **parameters):
    """Get an API response"""
    r = requests.get(uri, parameters)
    if r.ok:
        return r.json()
    try:
        data = r.json()
    except ValueError:  # Server did not even return a JSON for the error
        r.raise_for_status()
    # The JSON error data when the API rate limit is exceeded is in a
    # different format than on parameter errors. This will handle both.
    if data.get('errors') is not None:
        err = data['errors']['error'][0]
    else:  # API rate limit exceeded error format
        err = data['error']
    if err.get('parameter') is not None:  # Wrong parameter error
        raise ValueError(
            "API responded with an error on parameter '{0}': {1}".format(
                err['parameter'], err['message']))
    elif err['code'] == "OVER_RATE_LIMIT":
        raise DataGovApiRateExceededError()
    else:
        raise DataGovApiError("{0}: {1}".format(err['code'], err['message']))


class DataGovClientBase(object):

    def __init__(self, uri_part, api, api_key, use_format=True):
        self.uri_part = uri_part
        self.api = api
        self.key = api_key
        self.use_format = use_format

    def build_uri(self, uri_action):
        return "{0}{1}{2}/{3}".format(
            BASE_URI, self.uri_part, self.api.value, uri_action.value)

    def run_request(self, uri_action, **kwargs):
        kwargs['api_key'] = self.key
        if 'format' not in kwargs and self.use_format:
            kwargs['format'] = 'json'
        return api_request(self.build_uri(uri_action), **kwargs)

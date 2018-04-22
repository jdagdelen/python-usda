#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for Data.gov API features"""

import pytest
from httmock import urlmatch, HTTMock
from usda.base import api_request, DataGovClientBase, \
    DataGovApiError, DataGovApiRateExceededError


class TestBase(object):
    """Unit tests for base Data.gov features"""

    @urlmatch(path=r'/?ok.*')
    def api_ok(self, url, request):
        return {
            'status_code': 200,
            'content': '{"key": "value"}'
        }

    @pytest.fixture
    def apimock(self):
        return HTTMock(self.api_ok)

    def test_api_request_ok(self, apimock):
        """Test api_request with a normal working response."""
        with apimock:
            data = api_request("http://api/ok")
        assert data["key"] == "value"

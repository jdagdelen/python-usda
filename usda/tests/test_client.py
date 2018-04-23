#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for Data.gov API features"""

import pytest
from httmock import urlmatch, HTTMock
from requests import HTTPError
from usda.client import UsdaClient
from usda.enums import UsdaNdbListType, UsdaNdbReportType


class TestClient(object):
    """Tests for UsdaClient"""

    @urlmatch(path=r'/?usda/ndb/list')
    def api_list(self, uri, request):
        return ""

    @urlmatch(path=r'/?usda/ndb/report')
    def api_report(self, uri, request):
        return ""

    @pytest.fixture
    def apimock(self):
        return HTTMock(self.api_list, self.api_report)

    def test_client_init(self):
        cli = UsdaClient("API_KAY")
        assert cli.uri_part == "usda/"
        assert cli.api.value == "ndb"
        assert cli.key == "API_KAY"
        assert cli.use_format

    def test_client_list_foods(self, apimock):
        pass

    def test_client_list_nutrients(self, apimock):
        pass

    def test_client_food_report(self, apimock):
        pass

    def test_client_nutrient_report(self):
        with pytest.raises(NotImplementedError):
            UsdaClient("DEMO_KEY").get_nutrient_report(None)

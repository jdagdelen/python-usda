#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for Data.gov API features"""

import pytest
import json
from httmock import urlmatch, HTTMock
from usda.client import UsdaClient
from usda.tests.sample_data import \
    FOOD_LIST_DATA, NUTRIENT_LIST_DATA, \
    FOOD_REPORT_DATA, NUTRIENT_REPORT_DATA, \
    FOOD_SEARCH_DATA


class TestClient(object):
    """Tests for UsdaClient"""

    @urlmatch(path=r'/usda/ndb/list')
    def api_list(self, uri, request):
        if "lt=f" in uri.query:
            return json.dumps(FOOD_LIST_DATA)
        elif "lt=n" in uri.query:
            return json.dumps(NUTRIENT_LIST_DATA)

    @urlmatch(path=r'/usda/ndb/reports')
    def api_report(self, uri, request):
        return json.dumps(FOOD_REPORT_DATA)

    @urlmatch(path=r'/usda/ndb/nutrients')
    def api_nutrients(self, uri, request):
        return json.dumps(NUTRIENT_REPORT_DATA)

    @urlmatch(path=r'/usda/ndb/search')
    def api_search(self, uri, request):
        return json.dumps(FOOD_SEARCH_DATA)

    @pytest.fixture
    def apimock(self):
        return HTTMock(self.api_list, self.api_report,
                       self.api_nutrients, self.api_search)

    def test_client_init(self):
        cli = UsdaClient("API_KAY")
        assert cli.uri_part == "usda/"
        assert cli.api.value == "ndb"
        assert cli.key == "API_KAY"
        assert cli.use_format

    def test_client_list_foods(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            foods = cli.list_foods(5)
        assert foods[0].name == "Pizza"
        assert foods[1].name == "Pizza with pineapple"

    def test_client_list_nutrients(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            nutrients = cli.list_nutrients(5)
        assert nutrients[0].name == "Calcium"
        assert nutrients[1].name == "Lactose"

    def test_client_food_report(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            fr = cli.get_food_report(123456)
        assert fr.food.name == "Pizza"

    def test_client_nutrient_report(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            nr = cli.get_nutrient_report([42, 1337])
        nr.foods.popitem()[0].name == "Pizza with pineapple"

    def test_client_search_foods(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            foods = cli.search_foods('pizza', 5)
        assert foods[0].name == "Pizza"
        assert foods[1].name == "Pizza with pineapple"

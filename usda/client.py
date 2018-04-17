#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .enums import *
from .domain import Nutrient, Food, FoodReport
from .base import DataGovClientBase


class UsdaClient(DataGovClientBase):

    def __init__(self, api_gov_key):
        super(UsdaClient, self).__init__('usda/', UsdaApis.ndb, api_gov_key)

    def list_nutrients(self, max, offset=0, sort='n'):
        data = self.run_request(
            UsdaUriActions.list, lt=UsdaNdbListType.all_nutrients.value,
            max=max, offset=offset, sort=sort)
        return self._build_nutrients_list(data)

    def list_foods(self, max, offset=0, sort='n'):
        data = self.run_request(
            UsdaUriActions.list, lt=UsdaNdbListType.food.value,
            max=max, offset=offset, sort=sort)
        return self._build_foods_list(data)

    def get_food_report(self, ndb_food_id,
                        report_type=UsdaNdbReportType.basic):
        data = self.run_request(
            UsdaUriActions.report, type=report_type.value, ndbno=ndb_food_id)
        return FoodReport.from_response_data(data)

    def get_nutrient_report(self, *nutrients,
                            report_type=UsdaNdbReportType.basic):
        raise NotImplementedError  # TODO
        if len(nutrients) > 20:
            raise ValueError("A nutrient report request cannot contain "
                             "more than 20 nutrients")
        data = self.run_request(
            UsdaUriActions.report, type=report_type.value, nutrients=nutrients)

    def _build_item_list(self, data, usda_class):
        result = list()
        data_list = data['list']['item']
        for raw_data in data_list:
            result.append(usda_class.from_response_data(raw_data))
        return result

    def _build_nutrients_list(self, response_data):
        return self._build_item_list(response_data, Nutrient)

    def _build_foods_list(self, response_data):
        return self._build_item_list(response_data, Food)

    def _build_food_report(self, response_data):
        return FoodReport(response_data)

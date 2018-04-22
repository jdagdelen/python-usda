#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for USDA API result objects."""

import pytest
from usda.domain import UsdaObject, Food, Nutrient, Measure, FoodReport


class TestUsdaDomain(object):
    """Unit tests for USDA API objects"""

    def test_usda_object(self):
        """Tests for UsdaObject class"""
        with pytest.raises(TypeError):
            UsdaObject()

    def test_measure(self):
        """Tests for Measure class"""
        data = {
            "qty": 1.0,
            "eqv": 42.0,
            "eunit": "g",
            "label": "Measurement",
            "value": 13.37
        }
        m = Measure.from_response_data(data)
        assert m.label == "Measurement"
        assert m.quantity == 1.0
        assert m.gram_equivalent == 42.0
        assert m.value == 13.37
        assert repr(m) == "Measure 'Measurement': 13.37 1.0"
        assert str(m) == "Measurement"

    def test_nutrient(self):
        """Tests for Nutrient class"""
        data = {
            "id": 42,
            "name": "Lactose"
        }
        n = Nutrient.from_response_data(data)
        assert n.id == 42
        assert n.name == "Lactose"
        assert repr(n) == "Nutrient ID 42 'Lactose'"
        assert str(n) == "Lactose"

    def test_food(self):
        """Tests for Food class"""
        data = {
            "id": 123456,
            "name": "Pizza"
        }
        f = Food.from_response_data(data)
        assert f.id == 123456
        assert f.name == "Pizza"
        assert repr(f) == "Food ID 123456 'Pizza'"
        assert str(f) == "Pizza"

    def test_food_report(self):
        """Tests for FoodReport class"""
        data = {
            "report": {
                "type": "Basic",
                "food": {
                    "ndbno": "123456",
                    "name": "Pizza",
                    "nutrients": [
                        {
                            "nutrient_id": 42,
                            "name": "Lactose",
                            "group": "Proximates",
                            "unit": "g",
                            "value": 0.42,
                            "measures": [
                                {
                                    "qty": 1.0,
                                    "eqv": 42.0,
                                    "eunit": "g",
                                    "label": "Measurement",
                                    "value": 13.37
                                }
                            ]
                        }
                    ]
                },
                "footnotes": [
                    "Footnote 1", "Footnote 2"
                ]
            }
        }
        fr = FoodReport.from_response_data(data)
        assert fr.report_type == "Basic"
        assert fr.foot_notes == ["Footnote 1", "Footnote 2"]
        assert fr.food_group is None
        assert fr.food.id == 123456
        assert fr.food.name == "Pizza"
        assert repr(fr) == "Food Report for 'Food ID 123456 'Pizza''"
        assert len(fr.nutrients) == 1
        n = fr.nutrients[0]
        assert n.id == 42
        assert n.name == "Lactose"
        assert n.group == "Proximates"
        assert n.unit == "g"
        assert n.value == 0.42
        assert len(n.measures) == 1
        m = n.measures[0]
        assert m.label == "Measurement"
        assert m.quantity == 1.0
        assert m.gram_equivalent == 42.0
        assert m.value == 13.37

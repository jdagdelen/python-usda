#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for USDA API result objects."""

import pytest
from usda.domain import \
    UsdaObject, Food, Nutrient, Measure, FoodReport, NutrientReport
from usda.tests.sample_data import FOOD_REPORT_DATA, NUTRIENT_REPORT_DATA


class TestUsdaDomain(object):
    """Unit tests for USDA API objects"""

    def test_usda_object(self):
        """Tests for UsdaObject class"""
        with pytest.raises(TypeError):
            UsdaObject()
        with pytest.raises(NotImplementedError):
            UsdaObject.from_response_data(None)

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
        fr = FoodReport.from_response_data(FOOD_REPORT_DATA)
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

    def test_nutrient_report(self):
        """Tests for NutrientReport class"""
        nr = NutrientReport.from_response_data(NUTRIENT_REPORT_DATA)
        assert isinstance(nr.foods, dict)
        assert len(nr.foods) == 1
        f, nlist = nr.foods.popitem()
        assert isinstance(f, Food)
        assert isinstance(nlist, list)
        assert all(isinstance(n, Nutrient) for n in nlist)
        assert f.id == 42
        assert f.name == "Pizza with pineapple"
        assert nlist[0].id == 42
        assert nlist[0].name == "Lactose"
        assert nlist[0].unit == "g"
        assert nlist[0].value == 26
        assert len(nlist[0].measures) == 1
        assert nlist[0].measures[0].label == "1.0 slice"
        assert nlist[0].measures[0].quantity == 6.9
        assert nlist[0].measures[0].gram_equivalent == 353.0
        assert nlist[0].measures[0].value == 26
        assert nlist[1].id == 1337
        assert nlist[1].name == "Calcium"
        assert nlist[1].unit == "g"
        assert nlist[1].value == 4.87
        assert len(nlist[1].measures) == 1
        assert nlist[1].measures[0].label == "1.0 slice"
        assert nlist[1].measures[0].quantity == 6.9
        assert nlist[1].measures[0].gram_equivalent == 65.8
        assert nlist[1].measures[0].value == 4.87

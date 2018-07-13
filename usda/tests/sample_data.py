#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample API response data for testing"""


def _make_list(*data, **kwargs):
    result = {
        "list": {
            "start": 0,
            "end": len(data),
            "total": len(data),
            "sr": "Legacy",
            "sort": "n",
            "item": [
                {
                    "offset": i,
                    "id": id,
                    "name": name,
                }
                for i, (id, name)
                in enumerate(data)
            ],
        }
    }
    result.update(kwargs)
    return result


FOOD_LIST_DATA = _make_list(("1337", "Pizza"), ("42", "Pizza with pineapple"))

NUTRIENT_LIST_DATA = _make_list(("1337", "Calcium"), ("42", "Lactose"))

FOOD_GROUP_LIST_DATA = _make_list(
    ("0100", "Dairy and Eggs Products"), ("0300", "Baby Foods"))

DERIVATION_CODES_LIST_DATA = _make_list(
    ("A", "Analytical data"),
    ("AR", "Analytical data; derived by linear regression"))

FOOD_SEARCH_DATA = _make_list(
    ("1337", "Pizza"), ("42", "Pizza with pineapple"),
    q="test", ds="any", group="")

FOOD_REPORT_DATA = {
    "report": {
        "type": "Basic",
        "food": {
            "ndbno": "123456",
            "name": "Pizza",
            "nutrients": [
                {
                    "nutrient_id": "42",
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

NUTRIENT_REPORT_DATA = {
    "report": {
        "sr": "Legacy",
        "groups": [
            {
                "id": "0100",
                "description": "Dairy and Egg Products"
            }
        ],
        "subset": "All foods",
        "end": 1,
        "start": 0,
        "total": 1,
        "foods": [
            {
                "ndbno": "42",
                "name": "Pizza with pineapple",
                "weight": 6.9,
                "measure": "1.0 slice",
                "nutrients": [
                    {
                        "nutrient_id": "42",
                        "nutrient": "Lactose",
                        "unit": "g",
                        "value": "26",
                        "gm": 353.0
                    },
                    {
                        "nutrient_id": "1337",
                        "nutrient": "Calcium",
                        "unit": "g",
                        "value": "4.87",
                        "gm": 65.8
                    },
                ]
            }
        ]
    }
}

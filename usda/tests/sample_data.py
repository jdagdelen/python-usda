#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample API response data for testing"""

FOOD_REPORT_DATA = {
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

FOOD_LIST_DATA = {
    "list": {
        "item": [
            {
                "offset": 0,
                "id": "1337",
                "name": "Pizza"
            },
            {
                "offset": 1,
                "id": "42",
                "name": "Pizza with pineapple"
            }
        ]
    }
}

NUTRIENT_LIST_DATA = {
    "list": {
        "item": [
            {
                "offset": 0,
                "id": "1337",
                "name": "Calcium"
            },
            {
                "offset": 1,
                "id": "42",
                "name": "Lactose"
            }
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

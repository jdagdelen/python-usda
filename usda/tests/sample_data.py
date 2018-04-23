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

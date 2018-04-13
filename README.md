# python-usda

[![Code Health](https://landscape.io/github/Lucidiot/python-usda/master/landscape.svg?style=flat)](https://landscape.io/github/Lucidiot/python-usda/master) [![Requirements Status](https://requires.io/github/Lucidiot/python-usda/requirements.svg?branch=master)](https://requires.io/github/Lucidiot/python-usda/requirements/?branch=master)

python-usda is a fork of [pygov](https://pypi.org/project/pygov/) focused on [USDA's Food Composition Database API](http://ndb.nal.usda.gov/ndb/doc/).

## Installation

python-usda is in active development. When it will be listed on the Python Package Index, you will be able to install it using:

```
pip install python-usda
```

## Usage

``` python
from usda.client import UsdaClient

client = UsdaClient("YOUR_API_KEY")
foods = client.list_foods(5)

for food in foods:
    print food.name
```

Result:

```
Abiyuch, raw
Acerola juice, raw
Acerola, (west indian cherry), raw
Acorn stew (Apache)
Agave, cooked (Southwest)
```

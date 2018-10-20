python-usda documentation
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

:ref:`genindex` - :ref:`modindex` - :ref:`search`

Introduction
------------

python-usda is a fork of `pygov <https://pypi.org/project/pygov/>`__
focused on `USDA's Food Composition Database
API <http://ndb.nal.usda.gov/ndb/doc/>`__.

It was initially created to make it easier to fetch up-to-date
nutritional data for some pseudo-scientific calculations in the
`PseudoScience <https://gitlab.com/Lucidiot/PseudoScience>`__ project
but has been extended to provide a better coverage of the API.

Setup
-----

::

    pip install python-usda

Usage
-----

API client
~~~~~~~~~~

python-usda provides an API client called ``UsdaClient`` that is the
base to all API requests.

.. code:: python

    from usda import UsdaClient
    client = UsdaClient('API_KEY')

The USDA API requires a Data.gov API key that you can get for free
`here <https://api.data.gov/signup/>`__.

Search foods
~~~~~~~~~~~~

.. code:: python

    client.search_foods(query, max, offset=0, sort='r')

-  **query** : A string specifying the search query.
-  **max** : A positive integer setting how many results should be
   fetched at once (up to 50).
-  **offset** : Index of the first row that should be returned.
-  **sort** : The sorting method. ``'r'`` for relevance, ``'n'`` for
   food item ID.

Returns a generator yielding ``Food`` instances.

Lists
~~~~~

.. code:: python

    client.list_foods(max, offset=0, sort='n')
    client.list_nutrients(max, offset=0, sort='n')
    client.list_food_groups(max, offset=0, sort='n')
    client.list_derivation_codes(max, offset=0, sort='n')

-  **max** : A positive integer setting how many list items should be
   fetched at once (up to 1500).
-  **offset** : Index of the first item that should be returned.
-  **sort** : The sorting method. ``'i'`` to sort by ID, ``'n'`` to sort
   by name.

Returns a generator yielding ``ListItem`` instances.

Food reports
~~~~~~~~~~~~

Report version 1
^^^^^^^^^^^^^^^^

.. code:: python

    client.get_food_report(ndb_food_id, report_type=UsdaNdbReportType.basic)

-  **ndb\_food\_id** : Unique identifier of the food item.
-  **report\_type** : A member of ``usda.enums.UsdaNdbReportType``
   specifying the food report type:

   -  ``basic`` (default) : Contains a limited set of nutrients, like
      what could be found on a product packaging ;
   -  ``full`` : Contains all the nutrients ;
   -  ``stats`` : Added statistics data from the Standard Reference
      database, not fully supported by python-usda.

As stated on the `food report API
documentation <https://ndb.nal.usda.gov/ndb/doc/apilist/API-FOOD-REPORT.md>`__,
``full`` and ``stats`` report types only have significance on food items
outside the Branded Food Products database. On this database, only
``basic`` food reports can be provided.

Returns a ``FoodReport`` instance.

Report version 2
^^^^^^^^^^^^^^^^

.. code:: python

    client.get_food_report_v2(*ids, report_type=UsdaNdbReportType.basic)

-  **ids** : One or more food item IDs, up to 25 at a time ;
-  **report\_type** : A member of ``usda.enums.UsdaNdbReportType``, like
   in the food report version 1.

Returns a list of ``FoodReportV2`` instances, one for each food item.

Nutrient reports
~~~~~~~~~~~~~~~~

.. code:: python

    client.get_nutient_report(*nutrients)

-  **nutrients** : One or more nutrient IDs, up to 20 at a time

Returns a list of ``NutrientReportFood`` instances, one for each
resulting food items.

Errors
~~~~~~

The API client uses `requests <https://python-requests.org>`__ to make
requests to USDA's API and does not explicitly handle its errors to let
this library's users deal with network-related errors.

As the API has a very inconsistent way of returning errors, it cannot be
fully guaranteed that all API errors are properly handled. If you
encounter a case of an unhandled error response from the API, please
file an issue.

All API errors are subclasses of ``usda.base.DataGovApiError``.

When an invalid API key is supplied, any API requests may raise a
``DataGovInvalidApiKeyError``.

When the allowed requests limit has been reached, a
``DataGovApiRateExceededError`` is raised.

Advanced topics
---------------

Result objects
~~~~~~~~~~~~~~

UsdaObject
^^^^^^^^^^

An abstract base class for all USDA result objects. Requires all its
subclasses to implement a ``from_response_data(response_data)`` static
method that should create an instance of the class from parsed JSON
data.

ListItem
^^^^^^^^

Inherits from UsdaObject. Describes any kind of item that has an ID and
a name ; all results from a list API request are of this type.

-  **id** : The unique identifier of the item.
-  **name** : A common name for the item.

Can be created from the following JSON data:

.. code:: json

    {
        "id": "...",
        "name": "..."
    }

Food
^^^^

Inherits from ListItem. Simply overrides the ``from_response_data``
static method to also handle a ``ndbno`` property instead of ``id`` in
JSON data, since some requests may return that instead.

- **id** : The unique identifier of the food item.
- **name** : A common name for the food item.

Nutrient
^^^^^^^^

Inherits from ListItem. In food and nutrient reports, holds associated
measurement data.

+--------------+-------+---------+----------+-------------------------+
| Attribute    | Lists | Food    | Nutrient | Description             |
| name         |       | reports | reports  |                         |
+==============+=======+=========+==========+=========================+
| **id**       | Yes   | Yes     | Yes      | The unique identifier   |
|              |       |         |          | of the nutrient.        |
+--------------+-------+---------+----------+-------------------------+
| **name**     | Yes   | Yes     | Yes      | A common name for the   |
|              |       |         |          | nutrient.               |
+--------------+-------+---------+----------+-------------------------+
| **value**    | No    | Yes     | Yes      | The nutrient's value    |
|              |       |         |          | for 100 grams of food   |
+--------------+-------+---------+----------+-------------------------+
| **unit**     | No    | Yes     | Yes      | The unit in which the   |
|              |       |         |          | nutrient's value is     |
|              |       |         |          | expressed.              |
+--------------+-------+---------+----------+-------------------------+
| **measures** | No    | Yes     | Yes      | A list of ``Measure```` |
|              |       |         |          | instances describing    |
|              |       |         |          | the various available   |
|              |       |         |          | measurements.           |
+--------------+-------+---------+----------+-------------------------+
| **group**    | No    | Yes     | No       | A nutrient group name.  |
+--------------+-------+---------+----------+-------------------------+


Measure
^^^^^^^

Inherits from UsdaObject. Describes a measurement made for a specific
nutrient.

-  **label** : Describes the measurement. Usually holds an indication on
   the volume of food used.
-  **quantity** : Quantity of the volume of food described in the label
   used. Most of the time, equals 1.
-  **value** : The measured value.
-  **gram\_equivalent** : 100 gram equivalent of the measurement.

Source
^^^^^^

Inherits from ListItem. Describes a source for data in a food report
version 2.

-  **id** : A unique identifier for the source.
-  **name** : The source's title.
-  **title** : An alias to **name**.
-  **authors** : A string containing the authors, in a way that could be
   formatted as a bibliography citation.
-  **vol** : The volume where the article was published.
-  **iss** : The issue where the article was published.
-  **year** : The year of publication of the source.

FoodReport
^^^^^^^^^^

Inherits from UsdaObject. Describes a food item's nutritional
information.

-  **food** : The ``Food`` instance the report is about.
-  **nutrients** : A list of ``Nutrient`` instances holding measurement
   data.
-  **report\_type** : The food report's type as a string (``Full``,
   ``Basic``, ``Statistics``)
-  **foot\_notes** : A list of strings corresponding to foot notes for
   the report.
-  **food\_group** : The food's group's name.

FoodReportV2
^^^^^^^^^^^^

Inherits from FoodReport. Describes a food item's nutritional
information with additional information.

-  **food** : The ``Food`` instance the report is about.
-  **nutrients** : A list of ``Nutrient`` instances holding measurement
   data.
-  **report\_type** : The food report's type as a string (``Full``,
   ``Basic``, ``Statistics``)
-  **foot\_notes** : A list of strings corresponding to foot notes for
   the report.
-  **food\_group** : The food's group's name.
-  **sources** A list of ``Source`` instances corresponding to sources
   for the food report's data.

NutrientReportFood
^^^^^^^^^^^^^^^^^^

Inherits from Food. Describes a food item that holds a list of
nutrients, for use in a nutrient report.

-  **id** : The unique identifier of the food item.
-  **name** : A common name for the food item.
-  **nutrients** : A list of ``Nutrient`` instances holding measurement
   data.

.. _raw-results:

Raw results
~~~~~~~~~~~

If you prefer to receive the raw JSON data instead of classes, append
``_raw`` to any client request method. For example, to retrieve the raw
JSON data for a foods list requests, use ``client.list_foods_raw``.
Those raw methods will pass all keyword arguments as parameters in the
request URL.

Enums
~~~~~

UsdaApis
^^^^^^^^

Inherited from pygov's initial want to provide support for multiple
APIs. Contains the first subpath in the USDA API's domain name as a
value.

For now, this enum only holds one member, ``ndb``, and is set by the
``UsdaClient`` on init.

UsdaUriActions
^^^^^^^^^^^^^^

Contains the available actions (API endpoints) for the NDB API.

+-----------------+------------------+--------------------------------+
| Name            | Value            | Description                    |
+=================+==================+================================+
| ``list``        | ``list``         | The Lists API endpoint         |
+-----------------+------------------+--------------------------------+
| ``report``      | ``reports``      | The food report v1 endpoint    |
+-----------------+------------------+--------------------------------+
| ``v2report``    | ``V2/reports``   | The food report v2 endpoint    |
+-----------------+------------------+--------------------------------+
| ``nutrients``   | ``nutrients``    | The nutrient report endpoint   |
+-----------------+------------------+--------------------------------+
| ``search``      | ``search``       | The food search endpoint       |
+-----------------+------------------+--------------------------------+

UsdaNdbListType
^^^^^^^^^^^^^^^

Contains the available list types for the NDB list API endpoint.

+--------------------------------+--------+---------------------------+
| Name                           | Value  | Description               |
+================================+========+===========================+
| ``all_nutrients``              | ``n``  | List all available        |
|                                |        | nutrients.                |
+--------------------------------+--------+---------------------------+
| ``specialty_nutrients``        | ``ns`` | List all nutrients        |
|                                |        | outside the Standard      |
|                                |        | Release database.         |
+--------------------------------+--------+---------------------------+
| ``standard_release_nutrients`` | ``nr`` | List all nutrients in the |
|                                |        | Standard Release          |
|                                |        | database.                 |
+--------------------------------+--------+---------------------------+
| ``food``                       | ``f``  | List all food items.      |
+--------------------------------+--------+---------------------------+
| ``food_groups``                | ``g``  | List all food groups.     |
+--------------------------------+--------+---------------------------+
| ``derivation_codes``           | ``d``  | List all derivation codes |
|                                |        | for statistics reports.   |
+--------------------------------+--------+---------------------------+

UsdaNdbReportType
^^^^^^^^^^^^^^^^^

Contains the available report types for Food Report V1 and V2 API
endpoints.

+-----------+--------+------------------------------------------------+
| Name      | Value  | Description                                    |
+===========+========+================================================+
| ``basic`` | ``b``  | Contains a limited set of nutrients, like what |
|           |        | could be found on a product packaging          |
+-----------+--------+------------------------------------------------+
| ``full``  | ``f``  | Contains all the available nutrients           |
+-----------+--------+------------------------------------------------+
| ``stats`` | ``s``  | Added statistics data from the Standard        |
|           |        | Reference database when available              |
+-----------+--------+------------------------------------------------+

.. note::

   The ``stats`` report type is currently not fully supported by
   python-usda. It is however possible to get all the returned data
   using :ref:`raw methods <raw-results>`.

Client and API requests
~~~~~~~~~~~~~~~~~~~~~~~

-  usda.base.\ **BASE\_URI** : A constant string set to Data.gov's base
   URI for any kind of API.

usda.base.api\_request
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    api_request(uri, **parameters)

A helper to run a request on a given URI with given parameters and
handle API errors. Returns parsed JSON data.

May raise exceptions from ``requests.exceptions`` as it does not handle
exceptions from the ``requests`` library. Specifically, will raise
``requests.exceptions.HTTPError`` if the API did not even return JSON
data.

If the parsed response data contains error information, may raise one of
the following exceptions:

-  ``ValueError`` : An error occured on a given parameter of the
   request. The exception message will hold the parameter name and the
   API's error message.
-  ``DataGovApiRateExceededError`` : The API rate limit has been reached
   for the given API key.
-  ``DataGovInvalidApiKeyError`` : The API key was not specified or
   invalid.
-  ``DataGovApiError`` : Another API error has occured.

usda.base.DataGovClientBase
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Describes a base client for all Data.gov APIs.

.. code:: python

    DataGovClientBase(uri_part, api, api_key, use_format=True)

-  **uri\_part** : The path to USDA's APIs from Data.gov API URI (the
   ``BASE_URI`` constant).
-  **api** : A ``usda.enums.UsdaApis`` member to specify the API
   endpoints base URI.
-  **api\_key** : A Data.gov API key to use.
-  **use\_format** : A boolean that, if set, will enforce a
   ``format=json`` parameter on all requests.

Methods
'''''''

-  ``build_uri(uri_action)`` : Build an API request URI with the given
   ``usda.enums.UsdaUriActions`` member.
-  ``run_request(uri_action, **kwargs)`` : Run an API request using the
   ``api_request`` function on the given ``usda.enums.UsdaUriActions``
   member and with specified parameters (``kwargs``). Automatically adds
   the API key as a parameter, and if ``use_format`` is set to True,
   will set the ``format`` parameter to ``json``. Returns the parsed
   JSON data.

usda.client.UsdaClient
^^^^^^^^^^^^^^^^^^^^^^

Inherits from ``DataGovClientBase``. Describes a client for USDA's NDB
API.

.. code:: python

    UsdaClient(api_gov_key)

-  **api\_gov\_key** : A Data.gov API key to use for all requests.

The client's methods are described in the **Usage** and **Raw results**
section of this documentation.

Pagination system
~~~~~~~~~~~~~~~~~

All USDA NDB API responses are paginated ; to help users not deal with
pagination, some specific generators ("paginators") have been created.
They are designed to be lazy and will only make requests when necessary.

usda.pagination.RawPaginator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A generator that yields one result at a time from parsed JSON data.

.. code:: python

    RawPaginator(client, *request_args, **request_kwargs)

-  **client** : A ``DataGovClientBase`` instance to use for making
   requests.
-  **request\_args** : Positional arguments passed to the client's
   ``run_request`` method when requests are made.
-  **request\_kwargs** : Keyword arguments passed to the client's
   ``run_request`` method when requests are made.

Class attributes
''''''''''''''''

USDA API requests will return a response of the following structure :

.. code:: json

    {
        "list": {
            "start": "...",
            "offset": "...",
            "total": "...",
            "item": [
                /* Array of JSON objects corresponding to results*/
            ]
        }
    }

Some paginated requests may change the ``"list"`` and ``"item"`` key
names, even if they return the same structure. For those reasons, two
class attributes allow setting those key names:

-  **listkey** is by default set to ``"list"``
-  **itemkey** is by default set to ``"item"``

Instance attributes
'''''''''''''''''''

-  **client** : A ``DataGovClientBase`` instance to use for making
   requests.
-  **request\_args** : Positional arguments passed to the client's
   ``run_request`` method when requests are made.
-  **request\_kwargs** : Keyword arguments passed to the client's
   ``run_request`` method when requests are made.
-  **data** : The last request's response data. Its results array is
   modified with every result yielding.
-  **current\_offset** : The start offset of the next page request.
-  **max** : The maximum amount of items to fetch with each request. Is
   set at init by the ``max`` request keyword argument, and defaults to
   30.

Methods
'''''''

-  Implements ``__next__`` : Yields one result each time. If the cached
   results are empty, will perform a synchronous request, refill the
   cache, then yield a result.
-  ``_fetch_next()`` : Fetch the next page of results.

usda.pagination.RawNutrientReportPaginator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inherits from ``RawPaginator``. The only difference is in the class
attributes: ``listkey`` is set to ``"report"`` and ``itemkey`` is set to
``"foods"``.

usda.pagination.ModelPaginator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A generator that yields instances of a given class from a RawPaginator.

.. code:: python

    ModelPaginator(model, raw)

-  **model** : A class that must implement the
   ``from_response_data(response_data)`` static method.
-  **raw** : A ``RawPaginator`` instance.

With each call to its ``__next__`` method, the RawPaginator's
``__next__`` method is called and the class' ``from_response_data`` is
applied to its result.

Development
-----------

Dev setup
~~~~~~~~~

This assumes that you set up a virtual environment beforehand. If you do
not know how to set up a Python virtual environment,
`virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/>`__ is
recommended.

::

    git clone https://gitlab.com/Lucidiot/python-usda
    cd python-usda
    pip install -e .[dev]

Unit tests
~~~~~~~~~~

Unit tests use the `pytest <https://pytest.org>`__ framework.

::

    python -m pytest

.. warning::

    Do not use the ``pytest`` command directly; this would
    execute outside the virtual environment.

Linting
~~~~~~~

This project follows the PEP 8 styling guidelines. You can use
``flake8`` to check those rules; just run it inside the project's root
directory.

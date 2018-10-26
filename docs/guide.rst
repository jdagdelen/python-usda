NDB API Guide
=============

This guide aims to provide a better help than what the USDA gives, by
describing both all of the available data and the ways to access it.

.. contents::
   :local:
   :backlinks: none

The Database
------------

The Nutritional Database is split in two parts:

* The **Standard Release** database, or **SR**: It holds nutritional
  information for common foods with no associated brands; useful to answer
  requests like "regular oatmeal". This part of the database is released
  yearly in multiple formats, including an Access Database.
* The **Branded Foods** database: Holds nutritional information for branded
  food items from US manufacturers; useful to answer more specific requests
  like "McFlurry with Oreo cookies".

There are a few Python packages to provide ways to make use of the Standard
Release database, but they only work with the yearly exports as a starting
point; not with the API. Furthermore, the API provides access to both
databases, while the yearly exports only include the Standard Release.
This is why *python-usda* was made.

Basic items
-----------

These items can be accessed using list endpoints. They provide the basics to
later access nutritional information.

Food items
^^^^^^^^^^

One of the simplest items. A food item has an ID, also called a ``ndbno``
(a Nutritional Database number), and a name. A search endpoint is available to
search food items by name.

Food groups
^^^^^^^^^^^

Food items may belong in food groups; requesting for a food item will only
give you the food group's name, but it is possible to list food groups
themselves and get an ID linked to their name.

Nutrients
^^^^^^^^^

Nutrients also can be listed, and only have an ID and a name; list endpoints
only provide you with IDs and names. However, they can hold measurement data
when they are returned inside a report.

Derivation codes
^^^^^^^^^^^^^^^^

Those codes can be listed and provide information as of how a nutrient's
measured value has been derived from multiple measurements. This information
is not fully supported by *python-usda* but can still be obtained when
requesting a report in the ``Statistics`` mode as raw JSON.
Nutrients will hold indicator codes that can be linked to descriptions using
the list endpoint for derivation codes.

Reports
-------

To get actual nutritional information, as list endpoints will not give you
anything of that sort, you need to ask for a report. There are two types of
reports available.

Food Reports
^^^^^^^^^^^^

Food Reports are what you would find on a product's packaging; all the
nutritional facts for a given food item.

Types
'''''

There are three types of Food Reports that you can request for:

Basic
   The most common nutritional information; exactly what you would find on an
   actual product's packaging.
Full
   Every single available nutrient for this item.
Statistics
   Get more statistics-related information about the nutrient's measurements;
   their standard error, the way their values have been derived from multiple
   measurements, etc. This is not fully supported by *python-usda*.

In *python-usda*, those report types are represented by the
:class:`usda.enums.UsdaNdbReportType` enum.

Measurements
''''''''''''

In each Food Report, you will find a list of nutrients. Those nutrients will
not only have an ID and a name, they will also hold a ``value`` and a
``unit`` which express the nutrient's quantity in 100 grams of the food item.
They also have a ``group`` to let you regroup nutrients in *nutrient groups*;
those are different from *food groups* and cannot be listed anywhere else.

Nutrients will also hold **measures**: their value is their "main measurement"
but there can be more than one measurement, usually performed on another
volume of the food item or in different conditions.

Those measurements will have a ``label`` which describes the measurement
itself; most of the time, it just states the volume of food used to perform
the measurement.

The official documentation differs from what the API actually returns; what
we have is a measured quantity as a decimal value with a missing unit, and a
100-gram equivalent for the measurement. *python-usda* tries to handle this
misconception simply by abstracting away the problem and using as properties
what the API actually says.

Versions
''''''''

There are two versions of Food Reports:

* **Version 1** Food Reports provide foot notes as a list of strings that you
  have to deal with yourself; you cannot link them to any data. It is only
  possible to request for one Version 1 food report at once.
* **Version 2** Food Reports are provided with another endpoint that lets you
  request up to 25 reports at once, saving some time, and give you footnotes
  with unique IDs and a new list of Sources that are more easily handled by
  code.

Sources
'''''''

Version 2 Food Reports provide a new ``sources`` property; a list of sources,
mostly articles, for the measurements returned in the report.

Sources are mostly designed to hold information about scientific publications:
they have an ID, a title, a year of publication, names of the volume and issue
they were first published in, and a list of authors as a long string formatted
like in a bibliography citation. While this is perfectible, it is already
easier to toy with those sources than with raw footnotes.

Nutrient Reports
^^^^^^^^^^^^^^^^

The Nutritional Database API provides another kind of report; the Nutrient
Report. They actually use a list endpoint, not a report endpoint, because they
return a list of **food items**.

For up to 20 nutrients, you can fetch pages and pages of food items with
associated nutrients and measurements data. This is perfect to get statistics
about a great number of food items and a reduced set of nutrients.

*python-usda* handles nutrient reports by letting you iterate over them
seamlessly, without ever caring about those pages and lists. You can then get
food items with an added attribute for a nutrients list, that contain the
same kind of information you would get in a Food Report.

API endpoints
-------------

This section goes deeper in detail about the API endpoints themselves and the
implementation in *python-usda*, for those who want to understand some of the
design choices or use the API themselves without the assistance of this Python
API client.

There are many quirks that are not described in the API documentation and that
are important to know to deal with this API properly, as with many other APIs
that do not follow standard practices.

First of all, every endpoint requires you to give an API key as an
``?api_key=`` parameter. For basic testing while doing development, you may
use the ``DEMO_KEY`` API key; but this key is strongly rate-limited and should
not be used in production. Instead, go get a free Data.gov API key. All you
need is to have a name, an e-mail address and to
`go here <https://api.data.gov/signup/>`_.

List endpoints
^^^^^^^^^^^^^^

There are three list endpoints: ``/list``, ``/search`` and ``/nutrients``.

``/list``
   List food items, food groups, nutrients and derivation codes.
``/search``
   Search food items only, by name.
``/nutrients``
   Get a Nutrient Report.

List parameters
'''''''''''''''

You can perform GET requests on the ``/list`` endpoint with the following
parameters:

``lt``
   The list type. Defaults to ``f``.

   * ``d`` for derivation codes;
   * ``f`` for food items;
   * ``g`` for food groups;
   * ``n`` for nutrients;
   * ``nr`` for all nutrients in the Standard Release database;
   * ``ns`` for nutrients that are not in the Standard Release database,
     also known as *specialty nutrients*.

   In *python-usda*, this setting is represented by the
   :class:`usda.enums.UsdaNdbListType` enum.
``max``
   Maximum number of items to return with each page. Defaults to 50.
   The official documentation states you can get up to 1,500 items at once;
   however the API actually limits to 500.
``offset``
   Zero-based index of the first item that should be returned.
   Defaults to 0. You can use this to perform pagination ;
   if you got a page with the 50 first results, you can get the next pages by
   setting this parameter to 50, then 100, then 150, etc.
``sort``
   Field to sort items on. ``n`` for name or ``i`` for ID. Defaults to ``n``.
``format``
   The response return format, ``xml`` or ``json``. Defaults to ``json``.
   Can also be set using the HTTP Accept header on the request.

Search parameters
'''''''''''''''''

You can perform GET requests on the ``/search`` endpoint with the following
parameters:

``q``
   The search query. If left empty, the endpoints acts like ``/list``.
``ds``
   A data source to restrict results to. If left empty, nutrients from all
   data sources are returned. The two exact following strings can be used:

   * ``Standard Reference``
   * ``Branded Food Products``
``fg``
   A food group ID to restrict results to. If left empty, no filtering on the
   food group is performed.
``max``
   Maximum number of items to return with each page. Defaults to 50.
   The official documentation states you can get up to 1,500 items at once;
   however the API actually limits to 500.
``offset``
   Zero-based index of the first item that should be returned.
   Defaults to 0. You can use this to perform pagination;
   if you got a page with the 50 first results, you can get the next pages by
   setting this parameter to 50, then 100, then 150, etc.
``sort``
   Field to sort items on. ``n`` for name or ``r`` for relevance to the query.
   Defaults to ``r``.
``format``
   The response return format, ``xml`` or ``json``. Defaults to ``json``.
   Can also be set using the HTTP Accept header on the request.

Nutrient Report
'''''''''''''''

You can perform GET requests on the ``/nutrient`` endpoint with the following
parameters:

``nutrients``
   A list of up to 20 nutrient IDs to use for the nutrient report.
``ndbno``
   Optionally restrict the nutrient report to a single food item by ID.
``fg``
   A list of up to 10 food group IDs to restrict results to.
   If left empty, no filtering on the food group is performed.
``subset``
   Boolean: set this to ``1`` to restrict to an abridged list of about 1,000
   most commonly consumed food items in the United States.
   Defaults to ``0`` — show all results.
``max``
   Maximum number of items to return with each page. Defaults to 50.
   The official documentation states you can get up to 1,500 items at once;
   however the API actually limits to 150.
``offset``
   Zero-based index of the first item that should be returned.
   Defaults to 0. You can use this to perform pagination;
   if you got a page with the 50 first results, you can get the next pages by
   setting this parameter to 50, then 100, then 150, etc.
``sort``
   Field to sort items on. ``f`` for food item or ``c`` for nutrient content.
   Defaults to ``f``.
``format``
   The response return format, ``xml`` or ``json``. Defaults to ``json``.
   Can also be set using the HTTP Accept header on the request.

Responses
'''''''''

List endpoint JSON responses are formatted in the following way:

.. code:: json

   {
       "list": {
           "start": "100",
           "end": "150",
           "total": "50",
           "item": [...]
       }
   }

The ``list.item`` array will hold all the items you requested for.
``list.start`` and ``list.end`` are the start and end indexes on this page,
and ``list.total`` is the length of the ``list.item`` array, *not* the total
number of results. The ``list`` objects will also usually contain other
arguments depending on what you have specified in your request, which could
make it possible to write a generic parser for any response, entirely
detached from any request.

*python-usda* uses the :class:`usda.pagination.RawPaginator` class to provide
seamless iteration over such paginated endpoints.
This class returns raw JSON data which can then be parsed using the
:class:`usda.Pagination.ModelPaginator` wrapper.

However, the Nutrient Report endpoint returns responses in the following way:

.. code:: json

   {
       "report": {
           "start": "100",
           "end": "150",
           "total": "50",
           "foods": [...]
       }
   }

For everything else, this endpoint works just like the other list endpoints,
but the most important parts of the response, the ``list`` object and its
``item`` array, are replaced by ``report`` and ``foods``.

*python-usda* solves this by using a custom class to paginate over this
endpoint: :class:`usda.pagination.RawNutrientReportPaginator`.

Reports endpoints
^^^^^^^^^^^^^^^^^

Two endpoints are available for food reports:

``/reports``
   Request a single Food Report version 1 at once
``/V2/reports``
   Request up to 25 Food Reports version 2 at once. Version 2 Reports add
   more data on sources and better footnotes.

Both endpoints can be requested using the same parameters:

``ndbno``
   On Food Reports version 1, ID of a single food item to get a report for.
   On Food Reports version 2, a list of up to 25 food item IDs to get
   reports for.
``type``
   The report type. Defaults to ``b``.

   * ``b``: Basic report type; what you could find on an actual product's
     packaging.
   * ``f``: Full report type; every nutrient available for the food item.
   * ``s``: Stats report type; additional statistics information from the
     Standard Release database.

   In *python-usda*, this parameter is represented by the
   :class:`usda.enums.UsdaNdbReportType` enum.
``format``
   The response return format, ``xml`` or ``json``. Defaults to ``json``.
   Can also be set using the HTTP Accept header on the request.

Errors
^^^^^^

The API returns errors in a very inconsistent way. First of all, a warning:

.. warning:: Do not trust the HTTP status codes.

This API often returns HTTP 200 statuses when there actually are errors. The
easiest way to handle errors is to first check for a JSON body; if there is
one, parse it and see if there is an error or if it is an actual result; if
there is none, *then* try checking the status code.

The error JSON bodies are of multiple shapes depending on the kind of error.
What follows is a non-exhaustive list of errors, as it is impossible to make
sure all errors are covered without a very thorough usage of the API.

API rate limit exceeded
'''''''''''''''''''''''

.. code:: json

   {
       "errors": {
           "error": [
               {
                   "code": "OVER_RATE_LIMIT",
                   "message": "..."
               }
           ]
       }
   }

This error is the only known error type where there is an ``errors`` *object*
that holds an ``error`` *array*. A developer must have been coding under
influence here.

Invalid API key
'''''''''''''''

.. code:: json

   {
       "error": {
           "code": "API_KEY_INVALID",
           "message": "..."
       }
   }

Parameter error
'''''''''''''''

This error occurs when one of the GET parameters in a request is invalid.
This may be the most useful error message, as it usually also describes the
correct values for the parameter in a way easier to understand than the
official documentation.

Note that in this case, the ``code`` property is a number corresponding to an
actual HTTP status code that should be returned as the response's status code,
but isn't.

.. code:: json

   {
       "error": {
           "code": 400,
           "parameter": "...",
           "message": "..."
       }
   }

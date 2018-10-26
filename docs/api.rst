API Reference
=============

Client
------

.. automodule:: usda.client
   :members:

Domain
------

.. automodule:: usda.domain
   :members:

Enums
-----

.. automodule:: usda.enums
   :members:

Low level classes
-----------------

Base client
^^^^^^^^^^^

.. automodule:: usda.base
   :members:

Pagination
^^^^^^^^^^

All USDA NDB list API responses are paginated ; to help users not deal with
pagination, some specific generators ("paginators") have been created.
They are designed to be lazy and will only make requests when necessary.

.. automodule:: usda.pagination
   :members:

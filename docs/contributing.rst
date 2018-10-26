Contributing
============

Contributing is always appreciated! To report any bugs, suggest any features,
or ask any questions that are not answered in this documentation, please
`submit an issue`_ on GitLab.

Development
-----------

Setup
^^^^^

This assumes that you set up a virtual environment beforehand. If you do not
know how to set up a Python virtual environment, `virtualenvwrapper`_ is
recommended::

    git clone https://gitlab.com/Lucidiot/python-usda
    cd python-usda
    mkvirtualenv usda -a .
    pip install -e .[dev]

Unit tests
^^^^^^^^^^

Unit tests use the `pytest`_ framework::

    python -m pytest

.. warning::

    Do not use the ``pytest`` command directly; this would
    execute outside the virtual environment.

Linting
^^^^^^^

This project follows the PEP 8 styling guidelines. You can use
``flake8`` to check those rules; just run it inside the project's root
directory.

Documentation
-------------

This project's documentation is written in `reStructuredText`_ and is
generated using the `Sphinx`_ tool. The documentation files are stored in the
``docs`` folder of the `GitLab repository`_. To generate them, use the provided
Makefile::

   make html

This will generate the documentation as HTML files in the ``docs/_build/html``
folder.

.. _submit an issue: https://gitlab.com/Lucidiot/python-usda/issues/new
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _pytest: https://pytest.org
.. _Sphinx: http://www.sphinx-doc.org/
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _GitLab repository: https://gitlab.com/Lucidiot/python-usda

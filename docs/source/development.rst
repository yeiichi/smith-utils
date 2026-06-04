Development
===========

Running tests
-------------

Tests are located in the ``tests/`` directory. Install the ``dev`` extra, then run ``pytest``:

.. code-block:: bash

   pip install -e ".[dev]"
   pytest

Building distributions
----------------------

The package uses Hatchling as its build backend. Build source and wheel distributions with:

.. code-block:: bash

   python -m build

Building the docs locally
-------------------------

To build the documentation locally, you need to install the ``docs`` extra dependencies:

.. code-block:: bash

   pip install -e ".[docs]"
   cd docs
   make html

The built documentation will be available in ``docs/_build/html/index.html``.

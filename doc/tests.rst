.. _tests:

Running the Tests
=================

After making any code change in Bana, tests need to be evaluated to ensure that
the library still behaves as expected.

.. note::

   Some of the commands below are wrapped into ``make`` targets for
   convenience, see the file ``Makefile``.


unittest
--------

The tests are written using Python's built-in |unittest|_ module. They are
available in the ``tests`` directory and can be fired through the
``tests/run.py`` file:

.. code-block:: bash

   $ mayapy tests/run.py


It is possible to run specific tests by passing a space-separated list of
partial names to match:

.. code-block:: bash

   $ mayapy tests/run.py ThisTestClass and_that_function


The ``unittest``'s command line interface is also supported:

.. code-block:: bash

   $ mayapy -m unittest discover -s tests -v


Finally, each test file is a **standalone** and can be directly executed.


coverage
--------

The package |coverage|_ is used to help localize code snippets that could
benefit from having some more testing:

.. code-block:: bash

   $ mayapy -m coverage run --source bana -m unittest discover -s tests
   $ coverage report
   $ coverage html


In no way should ``coverage`` be a race to the 100% mark since it is *not*
always meaningful to cover each single line of code. Furthermore, **having some
code fully covered isn't synonym to having quality tests**. This is our
responsability, as developers, to write each test properly regardless of the
coverage status.


Benchmarks
----------

A set of benchmarks are also available to keep the running performances in
check. They are to be found in the ``benchmarks`` folder and can be run in
a similar fashion to the tests through the ``benchmarks/run.py`` file:

.. code-block:: bash

   $ mayapy benchmarks/run.py


Or for more specificity:

.. code-block:: bash

   $ mayapy benchmarks/run.py ThisBenchClass and_that_function


Here again, each benchmark file is a **standalone** and can be directly
executed.

.. note::

   The command line interface ``mayapy -m unittest discover`` is not supported
   for the benchmarks.


.. |coverage| replace:: ``coverage``
.. |unittest| replace:: ``unittest``

.. _coverage: https://coverage.readthedocs.io
.. _unittest: https://docs.python.org/library/unittest.html

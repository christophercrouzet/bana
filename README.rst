Banana for Maya
===============

Banana for Maya is a set of extensions for the Python API of Autodesk Maya.


Documentation
-------------

Read the documentation online at <http://bananamaya.readthedocs.org> or check
their source from the ``doc`` folder.

The documentation can be built in different formats using Sphinx.


Running the Tests
-----------------

A suite of unit tests is available from the ``tests`` directory. You can run it
by firing:

.. code-block:: bash
   
   $ mayapy tests/run.py


To run specific tests, it is possible to pass names to match in the command
line.

.. code-block:: bash
   
   $ mayapy tests/run.py TestCase test_my_code


This command will run all the tests within the ``TestCase`` class as well as
the individual tests which contains ``test_my_code`` in their name.


Get the Source
--------------

The source code is available from the `GitHub project page`_.


Contributing
------------

Found a bug or got a feature request? Don't keep it for yourself, log a new
issue on
`GitHub <https://github.com/christophercrouzet/banana.maya/issues>`_.


Author
------

Christopher Crouzet
<`christophercrouzet.com <http://christophercrouzet.com>`_>


.. _GitHub project page: https://github.com/christophercrouzet/banana.maya

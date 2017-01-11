.. _installation:

Installation
============

Bana requires to be run from within an `Autodesk Maya`_'s Python environment.
This is usually done either by running the code from within an interactive
session of Maya, or through using the ``mayapy`` shell. A Python interpreter is
already distributed with Maya so there is no need to install one.

Additionally, Bana depends on the |gorilla|_ package.

.. note::

   Package dependencies are automatically being taken care off when using
   ``pip``.


Installing pip
--------------

The recommended [1]_ approach for installing a Python package such as Bana is
to use |pip|_, a package manager for projects written in Python. If ``pip`` is
not already installed on your system, you can do so by following these steps:

    1. Download |get-pip.py|_.
    2. Run ``python get-pip.py`` in a shell.


.. note::

   The installation commands described in this page might require ``sudo``
   privileges to run successfully.


System-Wide Installation
------------------------

Installing globally the most recent version of Bana can be done with ``pip``:

.. code-block:: bash

   $ pip install bana


Or using |easy_install|_ (provided with |setuptools|_):

.. code-block:: bash

   $ easy_install bana


Development Version
-------------------

To stay cutting edge with the latest development progresses, it is possible to
directly retrieve the source from the repository with the help of `Git`_:

.. code-block:: bash

   $ git clone https://github.com/christophercrouzet/bana.git
   $ cd bana
   $ pip install --editable .[dev]


.. note::

   The ``[dev]`` part installs additional dependencies required to assist
   development on Bana.

----

.. [1] See the `Python Packaging User Guide`_

.. |easy_install| replace:: ``easy_install``
.. |get-pip.py| replace:: ``get-pip.py``
.. |gorilla| replace:: ``gorilla``
.. |pip| replace:: ``pip``
.. |setuptools| replace:: ``setuptools``

.. _Autodesk Maya: http://www.autodesk.com/products/maya
.. _easy_install: https://setuptools.readthedocs.io/en/latest/easy_install.html
.. _get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
.. _Git: https://git-scm.com
.. _gorilla: https://github.com/christophercrouzet/gorilla
.. _pip: https://pip.pypa.io
.. _Python Packaging User Guide: https://packaging.python.org/current/
.. _setuptools: https://github.com/pypa/setuptools

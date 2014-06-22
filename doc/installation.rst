.. _installation:

Installation
============

Banana for Maya is written in the Python language and has been tested with
Maya 2015 running on Mac OS X 10.9.

It relies on the library `Gorilla`_.


The Easy Way
------------

If your Python-fu is up-to-date and you possess the latest trend in
installation tools [1]_, then you can install the most recent version of
Gorilla using `pip`_:

.. code-block:: bash
   
   $ pip install banana.maya


An alternative would be to use `easy_install`_ (included in `setuptools`_):

.. code-block:: bash
   
   $ easy_install banana.maya


From the Source
---------------

You can also download a compressed archive containing the source from either
`PyPI`_ or `GitHub`_. 

Then, it's only a matter of:

1. Decompressing the archive.
2. Running ``python setup.py install`` from the resulting directory.

You'll need to repeat those steps for the dependency that this library
relies on: `Gorilla`_.


Development Version
-------------------

If you want to stay cutting edge by using the development version, then
you can:

1. Install `Git`_.
2. ``git clone https://github.com/christophercrouzet/banana.maya.git``.
3. ``cd banana.maya``.
4. ``pip install --editable .`` or ``python setup.py develop``.


Installing pip
--------------

1. Download `get-pip.py`_.
2. Run ``python get-pip.py``.

----

.. [1] See the `Python Packaging User Guide`_


.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/christophercrouzet/banana.maya
.. _Gorilla: https://github.com/christophercrouzet/gorilla
.. _PyPI: https://pypi.python.org/pypi/banana.maya
.. _Python Packaging User Guide: http://python-packaging-user-guide.readthedocs.org/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
.. _pip: https://pypi.python.org/pypi/pip
.. _setuptools: https://pypi.python.org/pypi/setuptools

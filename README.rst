Bana
====

.. image:: https://img.shields.io/pypi/v/bana.svg
   :target: https://pypi.python.org/pypi/bana
   :alt: PyPI latest version

.. image:: https://readthedocs.org/projects/bana/badge/?version=latest
   :target: https://bana.readthedocs.io
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/l/bana.svg
   :target: https://pypi.python.org/pypi/bana
   :alt: License


Bana is a set of extensions for `Autodesk Maya`_'s Python API.

The Maya's Python API is often a good choice over the commands layer whenever
performances and robustness are valued. But because of its overall poor design,
it is not uncommon that some *fundamental* functionalities are **lacking** out
of the box and/or require too much **boilerplate** to get rolling.

Other gotchas to be expected include methods that became too **daunting** to
use after porting in the *worst* possible way the API from C++ to Python,
**undocumented** behaviours of certain features where error trialing is
everything that is left, and methods **throwing** an exception when returning
``None`` would have been more appropriate.

Bana aims at reducing these shortcomings to provide a more *friendly*,
*predictable*, and *efficient* developing environment.

Using the monkey patching package |gorilla|_, new methods prefixed with ``bn``
are inserted within some classes from the ``maya.OpenMaya*`` modules, thus
extending their functionalities while making these new methods feel as if they
were built-in into Maya.

Since performances are a primary reason for using the API, a set of benchmarks
built with the help of the package |revl|_ helps to ensure that these
extensions remain as fast as possible.


Notes
-----

Bana extends on Maya's Python API 1.0 rather than 2.0 because the latter
version seems to be still incomplete. That being said, it is encouraged to use
the API 2.0 whenever possible since it provides a much more Pythonic interface
with increased performances.

Bana does *not* aim at making the API more Pythonic. This could in some cases
impact the performances, which goes against Bana's goal of keeping things fast.

Bana *does* aim at following Maya's API philosophy by providing low-level
extensions that are not specific to a domain (e.g.: rigging).


Features
--------

* easy retrieval of nodes from the scene.
* robust and predictable specification for pattern matching with wildcards.
* abstract away the usage of the ``maya.OpenMaya.MScriptUtil`` class.
* performances as a top priority.


Usage
-----

.. code-block:: python

   >>> import bana
   >>> bana.initialize()
   >>> from maya import OpenMaya
   >>> # Retrieve a transform node named 'root'.
   >>> root = OpenMaya.MFnTransform.bnGet(pattern='*|root')
   >>> # Recursively iterate over all the DAG nodes child of 'root'.
   >>> for node in root.bnFindChildren():
   ...     print(node)
   >>> # Find all the mesh nodes in the scene containing the word 'Shape' but
   ... # not belonging to any namespace.
   >>> for node in OpenMaya.MFnMesh.bnFind(pattern='*|*Shape*'):
   ...     print(node)


See the `Tutorial`_ section from the documentation for more detailed examples
and explanations on how to use Bana.


Documentation
-------------

Read the documentation online at `bana.readthedocs.io`_ or check its source in
the ``doc`` directory.


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


Thanks
------

* Justin Israel for discovering that multiple instances pointing to a same
  Maya object return different hash values.


.. |gorilla| replace:: ``gorilla``
.. |revl| replace:: ``revl``

.. _Autodesk Maya: http://www.autodesk.com/products/maya
.. _bana.readthedocs.io: https://bana.readthedocs.io
.. _GitHub project page: https://github.com/christophercrouzet/bana
.. _gorilla: https://github.com/christophercrouzet/gorilla
.. _revl: https://github.com/christophercrouzet/revl
.. _Tutorial: https://bana.readthedocs.io/en/latest/tutorial.html

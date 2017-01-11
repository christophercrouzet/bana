.. currentmodule:: bana

.. _overview:

Overview
========

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


.. note::

   Bana extends on Maya's Python API 1.0 rather than 2.0 because the latter
   version seems to be still incomplete. That being said, it is encouraged
   to use the API 2.0 whenever possible since it provides a much more Pythonic
   interface with increased performances.


.. note::

   Bana does *not* aim at making the API more Pythonic. This could in some
   cases impact the performances, which goes against Bana's goal of keeping
   things fast.


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


.. seealso::

   The :ref:`tutorial` section for more detailed examples and explanations on
   how to use Bana.


.. |gorilla| replace:: ``gorilla``
.. |revl| replace:: ``revl``

.. _gorilla: https://github.com/christophercrouzet/gorilla
.. _revl: https://github.com/christophercrouzet/revl

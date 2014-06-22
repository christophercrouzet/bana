.. _overview:

Overview
========

Banana for Maya is a set of extensions for the Python API of Autodesk Maya.

Its goal is to add some features to speed-up development using the Maya Python
API.

Making the API more Pythonic is not part of the goals since it would break the
consistency with what's already built-in. For such a purpose, creating a new
API from scratch like what `PyMEL`_ did would be the way to go.

Using the extensions requires a call to the :func:`~banana.maya.patch`
function:

   >>> import banana.maya
   >>> banana.maya.patch()

The extensions will be directly inserted in the Maya Python API and will be
accessible from the usual ``maya`` submodules such as ``OpenMaya``.


.. note::
   
   Tested with Maya 2015 running on Mac OS X 10.9.


.. _PyMEL: https://github.com/LumaPictures/pymel

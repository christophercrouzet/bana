.. currentmodule:: bana

.. _categories:

Extension Categories
====================

Each extension provided with Bana is written to answer a specific need
belonging to one of these categories:

.. glossary::

   explicit
      Maya's implementation was deemed ambiguous possibly because of a lack of
      well-defined specification or documentation.

   fix
      A specific method needs to be modified but creating a new method prefixed
      with ``bn`` isn't an option. Therefore, the original method is fixed in
      place by being replaced. This approach is only used for magic methods
      such as ``__str__()`` and ``__hash__()``.

   foundation
      The extension is considered as a fundamental functionality that is
      missing from Maya's API.

   MScriptUtil
      The original method needs to be wrapped to abstract away the used of the
      ``maya.OpenMaya.MScriptUtil`` class. Some of these methods are marked as
      not implemented to document a better alternative approach.

   no throw
      By default, exceptions are being thrown whenever a method returns a
      ``maya.OpenMaya.MStatus`` object with a value that is not ``kSuccess``.
      This is not justified in cases where it is acceptable that the call to a
      method might or might not output a valid result. For example, it is
      expected for a ``MFn*`` class instance to fail accessing its
      ``maya.OpenMaya.MObject`` object if the function set hasn't been fully
      initialized yet, this doesn't have to be considered as an error. A better
      suited return value here is ``None`` since it carries the information
      that *no* valid object can be retrieved at the moment, while being even
      more convenient to check validity against.


.. note::

   The category for a specific extension can be found in the documentation
   associated with that extension.

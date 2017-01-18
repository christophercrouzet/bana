Changelog
=========

Version numbers comply with the `Sementic Versioning Specification (SemVer)`_.


`Unreleased`_
-------------

* Make minor tweaks to the code.


`v0.1.0`_ (2017-01-11)
----------------------

Changed
^^^^^^^

* Rewrite everything from scratch. Changes are not backwards compatible.


`v0.0.3`_ (2014-12-07)
----------------------

Added
^^^^^

* Add a ``__hash__()`` method for the ``MDagPath``, ``MFnDependencyNode``, and
  ``MObject`` classes.


Changed
^^^^^^^

* Make minor tweaks to the code.


`v0.0.2`_ (2014-06-22)
----------------------

Added
^^^^^

* Add a ``bnn_asFunctionSet()`` method to the ``MObject`` and ``MDagPath``
  classes.
* Add a ``bnn_getFunctionSet()`` method to the ``MObject`` class.
* Add a new internal module for data caching.


Changed
^^^^^^^

* Prepend the missing ``bnn`` identifiers for the test routines.
* Make minor tweaks to the code.


v0.0.1 (2014-06-21)
-------------------

* Initial release.


.. _Sementic Versioning Specification (SemVer): http://semver.org
.. _Unreleased: https://github.com/christophercrouzet/bana/compare/v0.1.0...HEAD
.. _v0.1.0: https://github.com/christophercrouzet/bana/compare/v0.0.3...v0.1.0
.. _v0.0.3: https://github.com/christophercrouzet/bana/compare/v0.0.2...v0.0.3
.. _v0.0.2: https://github.com/christophercrouzet/bana/compare/v0.0.1...v0.0.2

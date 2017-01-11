"""
    bana.OpenMaya.MDagPath
    ~~~~~~~~~~~~~~~~~~~~~~

    Extensions for the ``maya.OpenMaya.MDagPath`` class.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya

from bana import _iterator


@gorilla.patches(OpenMaya.MDagPath)
class MDagPath(object):

    @classmethod
    def bnFind(cls, pattern=None, fnType=OpenMaya.MFn.kInvalid, recursive=True,
               traverseUnderWorld=True, copy=True):
        """DAG path iterator.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG paths to match. Wildcards are
            allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.
        copy : bool
            ``True`` to copy each DAG path. It is useful when data persistence
            is required, such as when the DAG paths are to be stored into a
            list, otherwise it is faster to set it to ``False``.

        Yields
        ------
        maya.OpenMaya.MDagPath
            The paths found.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = _iterator.dag(fnType=fnType, skipRoot=True,
                                 recursive=recursive,
                                 traverseUnderWorld=traverseUnderWorld)
        if pattern is not None:
            if traverseUnderWorld:
                match = OpenMaya.MGlobal.bnMakeMatchFullPathFunction(pattern)
            else:
                match = OpenMaya.MGlobal.bnMakeMatchPathFunction(pattern)

            iterator = (dagPath for dagPath in iterator
                        if match(dagPath.fullPathName()))

        if copy:
            iterator = (OpenMaya.MDagPath(dagPath) for dagPath in iterator)

        return iterator

    @classmethod
    def bnGet(cls, pattern=None, fnType=OpenMaya.MFn.kInvalid, recursive=True,
              traverseUnderWorld=True):
        """Retrieve a single DAG path.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG path to match. Wildcards are
            allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Returns
        -------
        maya.OpenMaya.MDagPath
            The DAG path found. If none or many were found, ``None`` is
            returned.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = OpenMaya.MDagPath.bnFind(
            pattern=pattern, fnType=fnType, recursive=recursive,
            traverseUnderWorld=traverseUnderWorld, copy=True)
        dagPath = next(iterator, None)
        return dagPath if next(iterator, None) is None else None

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __hash__(self):
        """Hash value that can be relied on.

        This is required because the original method returns different values
        for multiple instances pointing to a same object, thus making the
        ``MDagPath`` object not usable with hash-based containers such as
        dictionaries and sets.

        Categories: :term:`fix`.

        Returns
        -------
        int
            The hash value representing this object.
        """
        return OpenMaya.MObjectHandle(self.node()).hashCode()

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __str__(self):
        """Full path name.

        It is helpful when interacting with the commands layer by not having to
        manually call the ``fullPathName()`` method each time a ``MDagPath``
        object needs to be passed to a command.

        Categories: :term:`fix`.

        Returns
        -------
        str
            The full path name.
        """
        return self.fullPathName()

    def bnFindChildren(self, pattern=None, fnType=OpenMaya.MFn.kInvalid,
                       recursive=True, traverseUnderWorld=True, copy=True):
        """DAG path iterator over the children.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG paths to match, relative to
            the current DAG path. Wildcards are allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.
        copy : bool
            ``True`` to copy each DAG path. It is useful when data persistence
            is required, such as when the DAG paths are to be stored into a
            list, otherwise it is faster to set it to ``False``.

        Yields
        ------
        maya.OpenMaya.MDagPath
            The paths found.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = _iterator.dag(fnType=fnType, root=self, skipRoot=True,
                                 recursive=recursive,
                                 traverseUnderWorld=traverseUnderWorld)
        if pattern is not None:
            length = len(self.fullPathName())
            if traverseUnderWorld:
                match = OpenMaya.MGlobal.bnMakeMatchFullPathFunction(
                    pattern, matchRelative=True)
            else:
                match = OpenMaya.MGlobal.bnMakeMatchPathFunction(pattern)

            iterator = (dagPath for dagPath in iterator
                        if match(dagPath.fullPathName()[length:]))

        if copy:
            iterator = (OpenMaya.MDagPath(dagPath) for dagPath in iterator)

        return iterator

    def bnGetChild(self, pattern=None, fnType=OpenMaya.MFn.kInvalid,
                   recursive=True, traverseUnderWorld=True):
        """Retrieve a single DAG path child.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG path to match, relative to the
            current DAG path. Wildcards are allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Returns
        -------
        maya.OpenMaya.MDagPath
            The path found.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = self.bnFindChildren(
            pattern=pattern, fnType=fnType, recursive=recursive,
            traverseUnderWorld=traverseUnderWorld, copy=True)
        dagPath = next(iterator, None)
        return dagPath if next(iterator, None) is None else None

    def bnGetParent(self):
        """Retrieve the parent DAG path.

        Categories: :term:`foundation`.

        Returns
        -------
        maya.OpenMaya.MDagPath or None
            The parent DAG path, or ``None`` if this DAG path is directly
            parented under the world.
        """
        if self.length() == 1:
            return None

        dagPath = OpenMaya.MDagPath(self)
        dagPath.pop(1)
        return dagPath

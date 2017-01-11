"""
    bana.OpenMaya.MObject
    ~~~~~~~~~~~~~~~~~~~~~

    Extensions for the ``maya.OpenMaya.MObject`` class.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patches(OpenMaya.MObject)
class MObject(object):

    @classmethod
    def bnFind(cls, pattern=None, fnType=OpenMaya.MFn.kInvalid):
        """DG node iterator.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            *Full name* pattern of the DG nodes to match. Wildcards are
            allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.

        Yields
        ------
        maya.OpenMaya.MObject
            The DG nodes found.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = OpenMaya.MItDependencyNodes(fnType)
        if pattern is None:
            while not iterator.isDone():
                yield iterator.thisNode()
                iterator.next()
        else:
            match = OpenMaya.MGlobal.bnMakeMatchFullNameFunction(pattern)
            while not iterator.isDone():
                obj = iterator.thisNode()
                if match(OpenMaya.MFnDependencyNode(obj).name()):
                    yield obj

                iterator.next()

    @classmethod
    def bnGet(cls, pattern=None, fnType=OpenMaya.MFn.kInvalid):
        """Retrieve a single DG node.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            *Full name* pattern of the DG node to match. Wildcards are allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.

        Returns
        -------
        maya.OpenMaya.MObject
            The DG node found. If none or many were found, ``None`` is
            returned.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = OpenMaya.MObject.bnFind(pattern=pattern, fnType=fnType)
        obj = next(iterator, None)
        return obj if next(iterator, None) is None else None

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __hash__(self):
        """Hash value that can be relied on.

        This is required because the original method returns different values
        for multiple instances pointing to a same object, thus making the
        ``MObject`` object not usable with hash-based containers such as
        dictionaries and sets.

        Categories: :term:`fix`.

        Returns
        -------
        int
            The hash value representing this object.
        """
        return OpenMaya.MObjectHandle(self).hashCode()

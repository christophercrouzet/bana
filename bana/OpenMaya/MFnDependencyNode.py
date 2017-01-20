"""Extensions for the ``maya.OpenMaya.MFnDependencyNode`` class.

:copyright: Copyright 2014-2017 by Christopher Crouzet.
:license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patches(OpenMaya.MFnDependencyNode)
class MFnDependencyNode(object):
    """Container for the extensions."""

    @classmethod
    def bnFind(cls, pattern=None):
        """DG node iterator.

        The calling class defines the function set type for which the nodes
        need to be compatible with. It also represents the type of the objects
        yielded.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Full name pattern of the DG nodes to match. Wildcards are allowed.

        Yields
        ------
        cls
            The DG nodes found.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = OpenMaya.MItDependencyNodes(cls().type())
        if pattern is None:
            while not iterator.isDone():
                yield cls(iterator.thisNode())
                iterator.next()
        else:
            match = OpenMaya.MGlobal.bnMakeMatchFullNameFunction(pattern)
            while not iterator.isDone():
                node = cls(iterator.thisNode())
                if match(node.name()):
                    yield node

                iterator.next()

    @classmethod
    def bnGet(cls, pattern=None):
        """Retrieve a single DG node.

        The calling class defines the function set type for which the node
        needs to be compatible with. It also represents the type of the object
        returned.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Full name pattern of the DG node to match. Wildcards are allowed.

        Returns
        -------
        cls
            The DG node found. If none or many were found, ``None`` is
            returned.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        iterator = OpenMaya.MFnDependencyNode.bnFind(pattern=pattern)
        node = next(iterator, None)
        return node if next(iterator, None) is None else None

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __hash__(self):
        """Hash value that can be relied on.

        This is required because the original method returns different values
        for multiple instances pointing to a same object, thus making the
        ``MFnDependencyNode`` object not usable with hash-based containers such
        as dictionaries and sets.

        Categories: :term:`fix`.

        Returns
        -------
        int
            The hash value representing this object.
        """
        return OpenMaya.MObjectHandle(self.object()).hashCode()

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __str__(self):
        """Name.

        It is helpful when interacting with the commands layer by not having to
        manually call the ``name()`` method each time a ``MFnDependencyNode``
        object needs to be passed to a command.

        Categories: :term:`fix`.

        Returns
        -------
        str
            The name.
        """
        return self.name()

"""Extensions for the ``maya.OpenMaya.MFnDagNode`` class."""

import gorilla
from maya import OpenMaya


@gorilla.patches(OpenMaya.MFnDagNode)
class MFnDagNode(object):
    """Container for the extensions."""

    @classmethod
    def bnFind(cls, pattern=None, recursive=True, traverseUnderWorld=True):
        """DAG node iterator.

        The calling class defines the function set type for which the nodes
        need to be compatible with. It also represents the type of the object
        returned.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG nodes to match. Wildcards are
            allowed.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Yields
        ------
        maya.OpenMaya.MDagNode
            The nodes found.

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
            pattern=pattern, fnType=cls().type(), recursive=recursive,
            traverseUnderWorld=traverseUnderWorld)
        return (cls(dagPath) for dagPath in iterator)

    @classmethod
    def bnGet(cls, pattern=None, recursive=True, traverseUnderWorld=True):
        """Retrieve a single DAG node.

        The calling class defines the function set type for which the node
        needs to be compatible with. It also represents the type of the object
        returned.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG node to match. Wildcards are
            allowed.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Returns
        -------
        maya.OpenMaya.MFnDagNode
            The DAG node found. If none or many were found, ``None`` is
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
        dagPath = OpenMaya.MDagPath.bnGet(
            pattern=pattern, fnType=cls().type(), recursive=recursive,
            traverseUnderWorld=traverseUnderWorld)
        return None if dagPath is None else cls(dagPath)

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __str__(self):
        """Full path name.

        It is helpful when interacting with the commands layer by not having to
        manually call the ``fullPathName()`` method each time a ``MFnDagNode``
        object needs to be passed to a command.

        Categories: :term:`fix`.

        Returns
        -------
        str
            The full path name.
        """
        return self.fullPathName()

    def bnFindChildren(self, pattern=None, fnType=OpenMaya.MFn.kInvalid,
                       recursive=True, traverseUnderWorld=True):
        """DAG node iterator over the children.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG nodes to match, relative to
            the current node. Wildcards are allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Yields
        ------
        maya.OpenMaya.MDagNode
            The nodes found.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        dagPath = OpenMaya.MDagPath()
        self.getPath(dagPath)
        iterator = dagPath.bnFindChildren(
            pattern=pattern, fnType=fnType, recursive=recursive,
            traverseUnderWorld=traverseUnderWorld)
        return (OpenMaya.MFnDagNode(dagPath) for dagPath in iterator)

    def bnGetChild(self, pattern=None, fnType=OpenMaya.MFn.kInvalid,
                   recursive=True, traverseUnderWorld=True):
        """Retrieve a single DAG node child.

        Categories: :term:`foundation`.

        Parameters
        ----------
        pattern : str
            Path or full path pattern of the DAG nodes to match, relative to
            the current node. Wildcards are allowed.
        fnType : maya.OpenMaya.MFn.Type
            Function set type to match.
        recursive : bool
            ``True`` to search recursively.
        traverseUnderWorld : bool
            ``True`` to search within the underworld.

        Returns
        -------
        maya.OpenMaya.MDagNode
            The node found.

        Note
        ----
        The pattern matching's global context is set to *full path* if the
        parameter ``traverseUnderWorld`` is ``True``, and to *path* otherwise.
        See :ref:`pm_matching_rules`.

        See Also
        --------
        :ref:`pattern_matching`, :ref:`retrieving_nodes`.
        """
        dagPath = OpenMaya.MDagPath()
        self.getPath(dagPath)
        dagPath = dagPath.bnGetChild(
            pattern=pattern, fnType=fnType, recursive=recursive,
            traverseUnderWorld=traverseUnderWorld)
        return None if dagPath is None else OpenMaya.MFnDagNode(dagPath)

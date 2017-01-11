"""
    bana._iterator
    ~~~~~~~~~~~~~~

    Iterators.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

from maya import OpenMaya


def dag(fnType=OpenMaya.MFn.kInvalid, root=None, skipRoot=False,
        recursive=True, traverseUnderWorld=False):
    """DAG path iterator.

    Parameters
    ----------
    fnType : maya.OpenMaya.MFn.Type
        Node type to match.
    root : maya.OpenMaya.MDagPath
        Root DAG path to begin the traversal from.
    skipRoot : bool
        True to not return the root node.
    recursive : bool
        True to search recursively.
    traverseUnderWorld : bool
        True to search within the underworld.

    Yields
    ------
    maya.OpenMaya.MDagPath
        The DAG path for each item traversed.

    Warning
    -------
        The same DAG path reference is being updated and yielded at each
        iteration. If data persistence is required, such as when the DAG paths
        are to be stored into a list, a copy needs to be made for each element.
    """
    iterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, fnType)
    if root is not None:
        iterator.reset(root, OpenMaya.MItDag.kDepthFirst, fnType)

    iterator.traverseUnderWorld(traverseUnderWorld)
    if skipRoot and iterator.depth() == 0:
        iterator.next()

    if recursive:
        def wrapper(iterator):
            dagPath = OpenMaya.MDagPath()
            while not iterator.isDone():
                iterator.getPath(dagPath)
                yield dagPath
                iterator.next()
    else:
        def wrapper(iterator):
            dagPath = OpenMaya.MDagPath()
            while not iterator.isDone():
                if iterator.depth() > 0:
                    iterator.prune()
                    if iterator.depth() > 1:
                        iterator.next()
                        continue

                iterator.getPath(dagPath)
                yield dagPath
                iterator.next()

    return wrapper(iterator)

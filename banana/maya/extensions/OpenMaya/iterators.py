"""
    banana.maya.iterators
    ~~~~~~~~~~~~~~~~~~~~~
    
    Iterators.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya

import gorilla.utils


@gorilla.patch(OpenMaya)
class bnn_MItDependencyNode(object):
    
    """Dependency nodes iterator.
    
    The traversal is done through all the nodes matching the input pattern
    and types. If both inputs are empty, all the nodes from the scene are
    retrieved.
    
    The items returned are of type `~maya.OpenMaya.MObject`.
    
    Note
    ----
        Use instead the `bnn_MItDagNode` iterator to traverse exclusively
        DAG nodes.
    
    Examples
    --------
    Retrieve all the sets from the scene:
    
    >>> import banana.maya
    >>> banana.maya.patch()
    >>> from maya import OpenMaya
    >>> iterator = OpenMaya.bnn_MItDependencyNode(types=OpenMaya.MFn.kSet)
    >>> for item in iterator:
    ...     node = OpenMaya.MFnDependencyNode(item)
    """
    
    def __init__(self, pattern='', types=None):
        """Constructor.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the dependency nodes to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        """
        if not pattern:
            pattern = '*'
        
        selection = OpenMaya.MSelectionList()
        try:
            OpenMaya.MGlobal.getSelectionListByName(pattern, selection)
        except RuntimeError:
            pass
        
        self._types = gorilla.utils.listify(types)
        self._iterator = OpenMaya.MItSelectionList(selection)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        """Iterate to the next item.
        
        Returns
        -------
        maya.OpenMaya.MObject
            The next item.
        """
        while not self._iterator.isDone():
            item = self.currentItem()
            self._iterator.next()
            if not self._types or any(map(item.hasFn, self._types)):
                return item
        
        raise StopIteration
    
    def isDone(self):
        """Check if the end of the iterator has been reached.
        
        Returns
        -------
        bool
            True if the end of the iterator has been reached.
        """
        return self._iterator.isDone()
    
    def currentItem(self):
        """Retrieve the current item.
        
        Returns
        -------
        maya.OpenMaya.MObject
            The current item.
        """
        item = OpenMaya.MObject()
        self._iterator.getDependNode(item)
        return item


@gorilla.patch(OpenMaya)
class bnn_MItDagNode(bnn_MItDependencyNode):
    
    """DAG nodes iterator.
    
    The traversal is done through all the DAG nodes matching the input
    pattern and types. If both inputs are empty, all the DAG nodes from
    the scene are retrieved.
    
    The items returned are of type `~maya.OpenMaya.MDagPath`.
    
    Examples
    --------
    Retrieve all the shapes from the scene:
    
    >>> import banana.maya
    >>> banana.maya.patch()
    >>> from maya import OpenMaya
    >>> iterator = OpenMaya.bnn_MItDagNode(types=OpenMaya.MFn.kShape)
    >>> for item in iterator:
    ...     shape = OpenMaya.MFnDagNode(item)
    """
    
    def __init__(self, pattern='', types=None):
        """Constructor.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the DAG nodes to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        """
        if not pattern:
            pattern = '*|*'
        
        selection = OpenMaya.MSelectionList()
        try:
            OpenMaya.MGlobal.getSelectionListByName(pattern, selection)
        except RuntimeError:
            pass
        
        self._types = gorilla.utils.listify(types)
        self._iterator = OpenMaya.MItSelectionList(selection,
                                                   OpenMaya.MFn.kDagNode)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        """Iterate to the next item.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The next item.
        """
        while not self._iterator.isDone():
            # Weirdly, the function `MDagPath.hasFn()` also compares the given
            # type to the direct child when a DAG path represents a transform
            # node and has a shape as a child. Hence it's necessary to call the
            # `MObject.hasFn()` function instead.
            object = OpenMaya.MObject()
            self._iterator.getDependNode(object)
            if not self._types or any(map(object.hasFn, self._types)):
                item = self.currentItem()
                self._iterator.next()
                return item
            
            self._iterator.next()
        
        raise StopIteration
    
    def isDone(self):
        """Check if the end of the iterator has been reached.
        
        Returns
        -------
        bool
            True if the end of the iterator has been reached.
        """
        return self._iterator.isDone()
    
    def currentItem(self):
        """Retrieve the current item.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The current item.
        """
        item = OpenMaya.MDagPath()
        self._iterator.getDagPath(item)
        return item


@gorilla.patch(OpenMaya)
class bnn_MItDagHierarchy(object):
    
    """DAG hierarchy iterator.
    
    Iterate over children of a specified DAG node. If no node is specified,
    the traversal starts from the world.
    
    The items returned are of type `~maya.OpenMaya.MDagPath`.
    
    Examples
    --------
    Retrieve the top level transform nodes:
    
    >>> import banana.maya
    >>> banana.maya.patch()
    >>> from maya import OpenMaya
    >>> iterator = OpenMaya.bnn_MItDagHierarchy()
    >>> for item in iterator:
    ...     transform = OpenMaya.MFnTransform(item)
    """
    
    def __init__(self, node=None, pattern='', types=None, recursive=False):
        """Constructor.
        
        Parameters
        ----------
        node : maya.OpenMaya.MObject, optional
            Root node to start the traversal from.
        pattern : str, optional
            Name or path pattern of the DAG nodes to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        recursive : bool, optional
            True to search recursively.
        """
        if pattern:
            self._pattern = OpenMaya.MGlobal.bnn_normalizePath(pattern,
                                                               wildcards=True)
        else:
            self._pattern = ''
        
        self._types = gorilla.utils.listify(types)
        self._recursive = recursive
        self._iterator = OpenMaya.MItDag(OpenMaya.MItDag.kBreadthFirst)
        if node:
            self._iterator.reset(node, OpenMaya.MItDag.kBreadthFirst)
        
        self._iterator.next()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        """Iterate to the next item.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The next item.
        """
        while not self._iterator.isDone():
            if not self._recursive:
                self._iterator.prune()
            
            # Weirdly, the function `MDagPath.hasFn()` also compares the given
            # type to the direct child when a DAG path represents a transform
            # node and has a shape as a child. Hence it's necessary to call the
            # `MObject.hasFn()` function instead.
            object = self._iterator.currentItem()
            if not self._types or any(map(object.hasFn, self._types)):
                item = self.currentItem()
                if (not self._pattern or OpenMaya.MGlobal.bnn_matchPath(
                        self._pattern, item.fullPathName())):
                    self._iterator.next()
                    return item
            
            self._iterator.next()
        
        raise StopIteration
    
    def isDone(self):
        """Check if the end of the iterator has been reached.
        
        Returns
        -------
        bool
            True if the end of the iterator has been reached.
        """
        return self._iterator.isDone()
    
    def currentItem(self):
        """Retrieve the current item.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The current item.
        """
        item = OpenMaya.MDagPath()
        self._iterator.getPath(item)
        return item

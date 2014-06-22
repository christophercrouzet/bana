"""
    banana.maya.MDagPath
    ~~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MDagPath` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patch(OpenMaya)
class MDagPath(object):
    
    @classmethod
    def bnn_get(cls, pattern, types=None):
        """Retrieve a DAG node.
        
        Parameters
        ----------
        pattern : str
            Name or path pattern of the DAG node to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The DAG path object of the node matched. If no or multiple
            nodes were found, None is returned.
        
        Examples
        --------
        Retrieve a DAG path object from its name:
        
        >>> import banana.maya
        >>> banana.maya.patch()
        >>> from maya import OpenMaya, cmds
        >>> cmds.polyCube(name='cube')
        >>> cube = OpenMaya.MDagPath.bnn_get('cube')
        """
        iterator = OpenMaya.bnn_MItDagNode(pattern=pattern, types=types)
        dagPath = None
        for item in iterator:
            if dagPath:
                return None
            
            dagPath = item
        
        return dagPath
    
    @classmethod
    def bnn_find(cls, pattern='', types=None):
        """Find DAG nodes.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the DAG nodes to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        
        Returns
        -------
        list of maya.OpenMaya.MDagPath
            The DAG path objects of the nodes found. If no nodes were
            found, an empty list is returned.
        """
        return list(OpenMaya.bnn_MItDagNode(pattern=pattern, types=types))
    
    def bnn_asFunctionSet(self):
        """Convert this DAG path into the function set it represents.
        
        Returns
        -------
        class inheriting from maya.OpenMaya.MFnBase
            The function set represented by this DAG path.
        """
        cls = self.node().bnn_getFunctionSet()
        return cls(self) if cls else OpenMaya.MFnDagNode(self)
    
    def bnn_findChild(self, pattern='', types=None, recursive=False):
        """Find a child node.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the child node to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        recursive : bool, optional
            True to search recursively.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The DAG path object of the node found. If no or multiple
            nodes were found, None is returned.
        
        Examples
        --------
        Retrieve a transform then a shape node by inspecting the child of
        a given object:
        
        >>> import banana.maya
        >>> banana.maya.patch()
        >>> from maya import OpenMaya, cmds
        >>> cmds.polyCube(name='cube')
        >>> cmds.group('|cube', name='root')
        >>> root = OpenMaya.MDagPath.bnn_get('root')
        >>> cube = root.bnn_findChild(pattern='cube')
        >>> cubeShape = root.bnn_findChild(types=OpenMaya.MFn.kShape, recursive=True)
        """
        iterator = OpenMaya.bnn_MItDagHierarchy(
            self, pattern=pattern, types=types, recursive=recursive)
        dagPath = None
        for item in iterator:
            if dagPath:
                return None
            
            dagPath = item
        
        return dagPath
    
    def bnn_findChildren(self, pattern='', types=None, recursive=False):
        """Find children nodes.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the children nodes to match.
            Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        recursive : bool, optional
            True to search recursively.
        
        Returns
        -------
        list of maya.OpenMaya.MDagPath
            The DAG path objects of the nodes found. If no nodes were
            found, an empty list is returned.
        """
        return list(OpenMaya.bnn_MItDagHierarchy(
            self, pattern=pattern, types=types, recursive=recursive))
    
    def bnn_findShape(self, pattern='', recursive=False, intermediates=False):
        """Find a shape nested below this node.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the shape node to match.
            Wildcards are allowed.
        recursive : bool, optional
            True to search recursively.
        intermediates : bool, optional
            True to also consider the intermediate shapes.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The DAG path object of the shape node found. If no or
            multiple shape nodes were found, None is returned.
        
        Examples
        --------
        Retrieve the unique shape node of an object:
        
        >>> import banana.maya
        >>> banana.maya.patch()
        >>> from maya import OpenMaya, cmds
        >>> cmds.polyCube(name='cube')
        >>> cube = OpenMaya.MDagPath.bnn_get(pattern='cube')
        >>> cubeShape = cube.bnn_findShape()
        """
        iterator = OpenMaya.bnn_MItDagHierarchy(
            self, pattern=pattern, types=OpenMaya.MFn.kShape,
            recursive=recursive)
        if not intermediates:
            iterator = (
                item for item in iterator
                if not OpenMaya.MFnDagNode(item).isIntermediateObject())
        
        dagPath = None
        for item in iterator:
            if dagPath:
                return None
            
            dagPath = item
        
        return dagPath
    
    def bnn_findShapes(self, pattern='', recursive=False, intermediates=False):
        """Find the shapes nested below this node.
        
        Parameters
        ----------
        pattern : str, optional
            Path of the shape nodes to match. Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Shape types to match.
        recursive : bool, optional
            True to search recursively.
        intermediates : bool, optional
            True to also consider the intermediate shapes.
        
        Returns
        -------
        list of maya.OpenMaya.MDagPath
            The DAG path objects of the shape nodes found. If no shape
            nodes were found, an empty list is returned.
        """
        iterator = OpenMaya.bnn_MItDagHierarchy(
            self, pattern=pattern, types=OpenMaya.MFn.kShape,
            recursive=recursive)
        if not intermediates:
            return [
                item for item in iterator
                if not OpenMaya.MFnDagNode(item).isIntermediateObject()]
        
        return list(iterator)
    
    def bnn_parent(self):
        """Retrieve the parent DAG path.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The parent DAG path or None if the parent in the world.
        """
        if self.length() == 1:
            return None
        
        dagPath = OpenMaya.MDagPath(self)
        dagPath.pop(1)
        return dagPath

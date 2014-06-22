"""
    banana.maya.MObject
    ~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MObject` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya

import banana.maya._cache


@gorilla.patch(OpenMaya)
class MObject(object):
    
    @classmethod
    def bnn_get(cls, pattern, types=None):
        """Retrieve a node.
        
        Parameters
        ----------
        pattern : str
            Name or path pattern of the node to match. Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        
        Returns
        -------
        maya.OpenMaya.MObject
            The object of the node matched. If no or multiple
            nodes were found, None is returned.
        """
        iterator = OpenMaya.bnn_MItDependencyNode(pattern=pattern, types=types)
        object = None
        for item in iterator:
            if object:
                return None
            
            object = item
        
        return object
    
    @classmethod
    def bnn_find(cls, pattern='', types=None):
        """Find DAG nodes.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the nodes to match. Wildcards are allowed.
        types : list of maya.OpenMaya.MFn.Type, optional
            Node types to match.
        
        Returns
        -------
        list of maya.OpenMaya.MObject
            The objects of the nodes found. If no nodes were
            found, an empty list is returned.
        """
        return list(OpenMaya.bnn_MItDependencyNode(pattern=pattern,
                                                   types=types))
    
    def bnn_getFunctionSet(self):
        """Retrieve the function set that this object represents.
        
        If the correspondance of this object's type with a function set is
        not already known, then the function set is deduced by recursively
        inspecting all the subclasses from `~maya.OpenMaya.MFnBase` until no
        matches are found. The result is then cached and accessible with a
        call to the `~maya.OpenMaya.MGlobal.bnn_getFunctionSetFromType`
        function.
        
        Returns
        -------
        class inheriting from maya.OpenMaya.MFnBase
            The function set found, None otherwise.
        """
        type = self.apiType()
        if type in banana.maya._cache.FUNCTION_SET_FROM_TYPE:
            return banana.maya._cache.FUNCTION_SET_FROM_TYPE[type]
        
        cls = OpenMaya.MFnBase
        while True:
            base = cls
            for item in base.__subclasses__():
                if self.hasFn(item().type()):
                    cls = item
                    break
            
            if cls is base:
                break
        
        if cls is OpenMaya.MFnBase:
            cls = None
        
        banana.maya._cache.FUNCTION_SET_FROM_TYPE[type] = cls
        return cls
    
    def bnn_asFunctionSet(self):
        """Convert this object into the function set it represents.
        
        Returns
        -------
        class inheriting from maya.OpenMaya.MFnBase
            The function set represented by this object. None is returned if
            the conversion couldn't be made.
        """
        cls = self.bnn_getFunctionSet()
        return cls(self) if cls else None

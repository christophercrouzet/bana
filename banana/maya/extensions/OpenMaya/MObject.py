"""
    banana.maya.MObject
    ~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MObject` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


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

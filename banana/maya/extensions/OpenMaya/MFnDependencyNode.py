"""
    banana.maya.MFnDependencyNode
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MFnDependencyNode` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patch(OpenMaya)
class MFnDependencyNode(object):
    
    @classmethod
    def bnn_get(cls, pattern):
        """Retrieve a node.
        
        Parameters
        ----------
        pattern : str
            Name or path pattern of the node to match. Wildcards are allowed.
        
        Returns
        -------
        calling class
            The node found. If no or multiple nodes were found,
            None is returned.
        """
        iterator = OpenMaya.bnn_MItDependencyNode(pattern=pattern,
                                                  types=cls().type())
        node = None
        for item in iterator:
            if node:
                return None
            
            node = item
        
        return cls(node) if node else None
    
    @classmethod
    def bnn_find(cls, pattern=''):
        """Find nodes.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the nodes to match. Wildcards are allowed.
        
        Returns
        -------
        list of calling class
            The nodes found. If no nodes were found, an empty
            list is returned.
        """
        return [cls(node) for node
                in OpenMaya.bnn_MItDependencyNode(pattern=pattern,
                                                  types=cls().type())]

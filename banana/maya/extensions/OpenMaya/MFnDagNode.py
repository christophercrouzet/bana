"""
    banana.maya.MFnDagNode
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MFnDagNode` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patch(OpenMaya)
class MFnDagNode(object):
    
    @classmethod
    def bnn_get(cls, pattern):
        """Retrieve a DAG node.
        
        Parameters
        ----------
        pattern : str
            Name or path pattern of the DAG node to match.
            Wildcards are allowed.
        
        Returns
        -------
        calling class
            The DAG node found. If no or multiple nodes were found,
            None is returned.
        
        Examples
        --------
        Retrieve a transform node from its name:
        
        >>> import banana.maya
        >>> banana.maya.patch()
        >>> from maya import OpenMaya, cmds
        >>> cmds.polyCube(name='cube')
        >>> cube = OpenMaya.MFnTransform.bnn_get('cube')
        """
        dagPath = OpenMaya.MDagPath.bnn_get(pattern, types=cls().type())
        return cls(dagPath) if dagPath else None
    
    @classmethod
    def bnn_find(cls, pattern=''):
        """Find DAG nodes.
        
        Parameters
        ----------
        pattern : str, optional
            Name or path pattern of the DAG nodes to match.
            Wildcards are allowed.
        
        Returns
        -------
        list of calling class
            The DAG nodes found. If no nodes were found, an empty
            list is returned.
        """
        iterator = OpenMaya.bnn_MItDagNode(pattern=pattern, types=cls().type())
        return [cls(dagPath) for dagPath in iterator]
    
    def bnn_dagPath(self):
        """Retrieve the DAG path object of this node.
        
        Returns
        -------
        maya.OpenMaya.MDagPath
            The DAG path object of this node.
        """
        dagPath = OpenMaya.MDagPath()
        self.getPath(dagPath)
        return dagPath

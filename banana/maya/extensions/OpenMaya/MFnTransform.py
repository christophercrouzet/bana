"""
    banana.maya.MFnTransform
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MFnTransform` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patch(OpenMaya)
class MFnTransform(object):
    
    def bnn_setWorldMatrix(self, matrix):
        """Set the transformation to a matrix defined in world space.
        
        Parameters
        ----------
        matrix : maya.OpenMaya.MMatrix
            The world matrix to set.
        """
        transform = OpenMaya.MTransformationMatrix(
            matrix * self.bnn_dagPath().exclusiveMatrixInverse())
        self.set(transform)

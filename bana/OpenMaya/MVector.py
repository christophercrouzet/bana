"""
    bana.OpenMaya.MVector
    ~~~~~~~~~~~~~~~~~~~~~

    Extensions for the ``maya.OpenMaya.MVector`` class.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


_MScriptUtil = OpenMaya.MScriptUtil


@gorilla.patches(OpenMaya.MVector)
class MVector(object):

    @gorilla.filter(True)
    @gorilla.settings(allow_hit=True)
    def __str__(self):
        """Printable-friendly version of the values.

        Categories: :term:`fix`.

        Returns
        -------
        str
            A printable-friendly version of the values.
        """
        return str(self.bnGet())

    def bnGet(self):
        """Retrieve the values as a list.

        Categories: :term:`MScriptUtil`.

        Returns
        -------
        list [x, y, z]
            The values.
        """
        return [self.x, self.y, self.z]

    def bnRotateBy(self, rotation, order=OpenMaya.MTransformationMatrix.kXYZ):
        """Rotate the vector.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        rotation : sequence of 3 floats
            Values in radian to rotate by.
        order : maya.OpenMaya.MTransformationMatrix.RotationOrder
            Rotation order.

        Returns
        -------
        maya.OpenMaya.MVector
            The new vector.
        """
        util = _MScriptUtil()
        util.createFromList(rotation, 3)
        ptr = util.asDoublePtr()
        return self.rotateBy(ptr, order)

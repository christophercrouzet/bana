"""
    bana.OpenMaya.MTransformationMatrix
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Extensions for the ``maya.OpenMaya.MTransformationMatrix`` class.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


_MScriptUtil = OpenMaya.MScriptUtil


@gorilla.patches(OpenMaya.MTransformationMatrix)
class MTransformationMatrix(object):

    def bnAddRotation(self, rotation,
                      order=OpenMaya.MTransformationMatrix.kXYZ,
                      space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> xform = transform.transformation()
        >>> rotation = OpenMaya.MEulerRotation(1.0, 2.0, 3.0,
        ...                                    OpenMaya.MEulerRotation.kXYZ)
        >>> xform.rotateBy(rotation, OpenMaya.MSpace.kTransform)
        >>> transform.set(xform)
        """
        raise NotImplementedError("See documentation.")

    def bnGetRotation(self, space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> rotation = transform.transformation().eulerRotation()
        >>> [rotation.x, rotation.y, rotation.z]
        [0.0, 0.0, 0.0]
        >>> rotation.order
        0
        """
        raise NotImplementedError("See documentation.")

    def bnSetRotation(self, rotation,
                      order=OpenMaya.MTransformationMatrix.kXYZ,
                      space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> xform = transform.transformation()
        >>> rotation = OpenMaya.MEulerRotation(1.0, 2.0, 3.0,
        ...                                    OpenMaya.MEulerRotation.kXYZ)
        >>> xform.rotateTo(rotation)
        >>> transform.set(xform)
        """
        raise NotImplementedError("See documentation.")

    def bnAddRotationQuaternion(self, rotation,
                                space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> xform = transform.transformation()
        >>> rotation = OpenMaya.MQuaternion(1.0, 2.0, 3.0, 4.0)
        >>> xform.rotateBy(rotation, OpenMaya.MSpace.kTransform)
        >>> transform.set(xform)
        """
        raise NotImplementedError("See documentation.")

    def bnGetRotationQuaternion(self, space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> rotation = transform.transformation().rotation()
        >>> [rotation.x, rotation.y, rotation.z, rotation.w]
        [0.0, 0.0, 0.0, 1.0]
        """
        raise NotImplementedError("See documentation.")

    def bnSetRotationQuaternion(self, rotation,
                                order=OpenMaya.MTransformationMatrix.kXYZ,
                                space=OpenMaya.MSpace.kTransform):
        """Not implemented. See the examples for an alternative approach.

        Categories: :term:`MScriptUtil`.

        Examples
        --------
        Alternative approach:

        >>> from maya import OpenMaya
        >>> transform = OpenMaya.MFnTransform()
        >>> transform.create()
        >>> xform = transform.transformation()
        >>> rotation = OpenMaya.MQuaternion(1.0, 2.0, 3.0, 4.0)
        >>> xform.rotateTo(rotation)
        >>> transform.set(xform)
        """
        raise NotImplementedError("See documentation.")

    def bnAddScale(self, scale, space=OpenMaya.MSpace.kTransform):
        """Add to the scale component by scaling relatively.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        scale : sequence of 3 floats
            Relative value to scale by.
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to perform the scale.
        """
        util = _MScriptUtil()
        util.createFromList(scale, 3)
        ptr = util.asDoublePtr()
        self.addScale(ptr, space)

    def bnGetScale(self, space=OpenMaya.MSpace.kTransform):
        """Retrieve the scale component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to get the scale.

        Returns
        -------
        list [x, y, z]
            The scale component.
        """
        util = _MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        self.getScale(ptr, space)
        return [
            _MScriptUtil.getDoubleArrayItem(ptr, 0),
            _MScriptUtil.getDoubleArrayItem(ptr, 1),
            _MScriptUtil.getDoubleArrayItem(ptr, 2),
        ]

    def bnSetScale(self, scale, space=OpenMaya.MSpace.kTransform):
        """Set the scale component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        scale : sequence of 3 floats
            New scale component.
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to set the scale.
        """
        util = _MScriptUtil()
        util.createFromList(scale, 3)
        ptr = util.asDoublePtr()
        self.setScale(ptr, space)

    def bnAddShear(self, shear, space=OpenMaya.MSpace.kTransform):
        """Add to the shear component by shearing relatively.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        shear : sequence of 3 floats
            Relative value to shear by.
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to perform the shear.
        """
        util = _MScriptUtil()
        util.createFromList(shear, 3)
        ptr = util.asDoublePtr()
        self.addShear(ptr, space)

    def bnGetShear(self, space=OpenMaya.MSpace.kTransform):
        """Retrieve the shear component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to get the shear.

        Returns
        -------
        list [x, y, z]
            The shear component.
        """
        util = _MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        self.getShear(ptr, space)
        return [
            _MScriptUtil.getDoubleArrayItem(ptr, 0),
            _MScriptUtil.getDoubleArrayItem(ptr, 1),
            _MScriptUtil.getDoubleArrayItem(ptr, 2),
        ]

    def bnSetShear(self, shear, space=OpenMaya.MSpace.kTransform):
        """Set the shear component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        shear : sequence of 3 floats
            New shear component.
        space : maya.OpenMaya.MSpace.Space
            Transform space in which to set the shear.
        """
        util = _MScriptUtil()
        util.createFromList(shear, 3)
        ptr = util.asDoublePtr()
        self.setShear(ptr, space)

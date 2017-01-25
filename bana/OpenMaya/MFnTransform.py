"""Extensions for the ``maya.OpenMaya.MFnTransform`` class."""

import gorilla
from maya import OpenMaya


_MScriptUtil = OpenMaya.MScriptUtil


@gorilla.patches(OpenMaya.MFnTransform)
class MFnTransform(object):
    """Container for the extensions."""

    def bnGetScale(self):
        """Retrieve the scale component.

        Categories: :term:`MScriptUtil`.

        Returns
        -------
        list [x, y, z]
            The scale component.
        """
        util = _MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        self.getScale(ptr)
        return [
            _MScriptUtil.getDoubleArrayItem(ptr, 0),
            _MScriptUtil.getDoubleArrayItem(ptr, 1),
            _MScriptUtil.getDoubleArrayItem(ptr, 2),
        ]

    def bnSetScale(self, scale):
        """Set the scale component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        scale : sequence of 3 floats
            New scale component.
        """
        util = _MScriptUtil()
        util.createFromList(scale, 3)
        ptr = util.asDoublePtr()
        self.setScale(ptr)

    def bnScaleBy(self, scale):
        """Add to the scale component by scaling relatively.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        scale : sequence of 3 floats
            Relative value to scale by.
        """
        util = _MScriptUtil()
        util.createFromList(scale, 3)
        ptr = util.asDoublePtr()
        self.scaleBy(ptr)

    def bnGetShear(self):
        """Retrieve the shear component.

        Categories: :term:`MScriptUtil`.

        Returns
        -------
        list [x, y, z]
            The shear component.
        """
        util = _MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        self.getShear(ptr)
        return [
            _MScriptUtil.getDoubleArrayItem(ptr, 0),
            _MScriptUtil.getDoubleArrayItem(ptr, 1),
            _MScriptUtil.getDoubleArrayItem(ptr, 2),
        ]

    def bnSetShear(self, shear):
        """Set the shear component.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        shear : sequence of 3 floats
            New shear component.
        """
        util = _MScriptUtil()
        util.createFromList(shear, 3)
        ptr = util.asDoublePtr()
        self.setShear(ptr)

    def bnShearBy(self, shear):
        """Add to the shear component by shearing relatively.

        Categories: :term:`MScriptUtil`.

        Parameters
        ----------
        shear : sequence of 3 floats
            Relative value to shear by.
        """
        util = _MScriptUtil()
        util.createFromList(shear, 3)
        ptr = util.asDoublePtr()
        self.shearBy(ptr)

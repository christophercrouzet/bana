"""Extensions for the ``maya.OpenMaya.MQuaternion`` class."""

import gorilla
from maya import OpenMaya


@gorilla.patches(OpenMaya.MQuaternion)
class MQuaternion(object):
    """Container for the extensions."""

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
        list [x, y, z, w]
            The values.
        """
        return [self.x, self.y, self.z, self.w]

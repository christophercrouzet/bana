"""Extensions for the ``maya.OpenMaya.MFnBase`` class."""

import gorilla
from maya import OpenMaya


@gorilla.patches(OpenMaya.MFnBase)
class MFnBase(object):
    """Container for the extensions."""

    def bnObject(self):
        """Retrieve the object attached to this function set.

        Categories: :term:`no throw`.

        Returns
        -------
        maya.OpenMaya.MObject or None
            The object or ``None`` if no valid object is attached to this
            function set.
        """
        try:
            return self.object()
        except:
            pass

        return None

"""Extensions for the ``maya.OpenMaya.MMatrix`` class."""

import sys

import gorilla
from maya import OpenMaya


if sys.version_info[0] == 2:
    _range = xrange
else:
    _range = range


_MScriptUtil = OpenMaya.MScriptUtil


@gorilla.patches(OpenMaya.MMatrix)
class MMatrix(object):
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
        return '[%s]' % ('\n '.join(str(r) for r in self.bnGet()))

    def bnGet(self):
        """Retrieve the values as a two-dimensional 4 x 4 list.

        Categories: :term:`MScriptUtil`.

        Returns
        -------
        list of list of floats
            The two-dimensional 4 x 4 list of values.
        """
        return [
            [_MScriptUtil.getDoubleArrayItem(self[r], c) for c in _range(4)]
            for r in _range(4)]

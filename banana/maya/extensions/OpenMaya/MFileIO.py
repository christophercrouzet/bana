"""
    banana.maya.MFileIO
    ~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MFileIO` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla
from maya import OpenMaya


@gorilla.patch(OpenMaya)
class MFileIO(object):
    
    @classmethod
    def bnn_importFile(cls, fileName, type='', preserveReferences=False,
                       nameSpace='', ignoreVersion=False):
        """Import a file into the current Maya session.
        
        Parameters
        ----------
        fileName : str
            File name to import.
        type : str, optional
            Type of the file to import.
        preserveReferences : bool, optional
            True if the references needs to be preserved.
        nameSpace : str, optional
            Namespace to use when importing the objects.
        ignoreVersion : bool, optional
            True to ignore the version.
        
        Returns
        -------
        list of maya.OpenMaya.MDagPath
            The top level transforms imported.
        """
        if not type:
            type = None
        
        if not nameSpace:
            nameSpace = None
        
        topLevelDagPaths = set(OpenMaya.bnn_MItDagHierarchy())
        OpenMaya.MFileIO.importFile(fileName, type, preserveReferences,
                                    nameSpace, ignoreVersion)
        return [dagPath for dagPath in OpenMaya.bnn_MItDagHierarchy()
                if not dagPath in topLevelDagPaths]

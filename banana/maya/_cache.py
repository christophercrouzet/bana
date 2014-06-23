"""
    banana.maya._cache
    ~~~~~~~~~~~~~~~~~~
    
    Cached data.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

from maya import OpenMaya


FUNCTION_SET_FROM_TYPE = {
    cls().type(): cls for name, cls in OpenMaya.__dict__.iteritems()
    if name.startswith('MFn') and name != 'MFnBase' and hasattr(cls, 'type')}

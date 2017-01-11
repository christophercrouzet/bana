#    __
#   |  |--.---.-.-----.---.-.
#   |  _  |  _  |     |  _  |
#   |_____|___._|__|__|___._|
#

"""
    bana
    ~~~~

    Set of extensions for Autodesk Maya's Python API.

    :copyright: Copyright 2014-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import importlib

import gorilla


__version__ = '0.1.0'


_PACKAGES = (
    'OpenMaya',
    'OpenMayaAnim',
    'OpenMayaFX',
    'OpenMayaRender',
    'OpenMayaUI',
)


def initialize():
    """Initialize the extensions.

    The patches from the Bana package are searched and applied to the Maya API.
    Patches that seem to have already been applied are skipped.
    """
    packages = [importlib.import_module('%s.%s' % (__package__, packageName))
                for packageName in _PACKAGES]
    defaultSettings = gorilla.Settings()
    for patch in gorilla.find_patches(packages):
        settings = (defaultSettings if patch.settings is None
                    else patch.settings)
        if not settings.allow_hit and hasattr(patch.destination, patch.name):
            continue

        gorilla.apply(patch)

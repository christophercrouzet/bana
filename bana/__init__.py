#    __
#   |  |--.---.-.-----.---.-.
#   |  _  |  _  |     |  _  |
#   |_____|___._|__|__|___._|
#

"""Set of extensions for Autodesk Maya's Python API."""

__title__ = 'bana'
__version__ = '0.1.0'
__summary__ = "Set of extensions for Autodesk Maya's Python API"
__url__ = 'https://github.com/christophercrouzet/bana'
__author__ = "Christopher Crouzet"
__contact__ = 'christopher.crouzet@gmail.com'
__license__ = "MIT"

import importlib

import gorilla


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

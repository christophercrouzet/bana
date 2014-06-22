#    __                                                                
#   |  |--.---.-.-----.---.-.-----.---.-.  .--------.---.-.--.--.---.-.
#   |  _  |  _  |     |  _  |     |  _  |__|        |  _  |  |  |  _  |
#   |_____|___._|__|__|___._|__|__|___._|__|__|__|__|___._|___  |___._|
#                                                         |_____|      
#                                                                      

"""
    banana.maya
    ~~~~~~~~~~~
    
    Set of extensions for the Python API of Autodesk Maya.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

__version__ = '0.0.1'

__all__ = [
]


def patch():
    from gorilla.extensionsregistrar import ExtensionsRegistrar
    from banana.maya import extensions
    
    ExtensionsRegistrar.register_extensions(extensions, patch=True)

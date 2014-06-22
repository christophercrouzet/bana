# -*- coding: utf-8 -*-

import os
import sys

src_path = os.path.abspath('..')
if not src_path in sys.path:
    sys.path.insert(0, src_path)


class Mock(object):
    
    __all__ = []
    
    def __init__(self, *args, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        return Mock()
    
    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mock_type = type(name, (), {})
            mock_type.__module__ = __name__
            return mock_type
        else:
            return Mock()


MOCK_MODULES = ['maya']
for module_name in MOCK_MODULES:
    sys.modules[module_name] = Mock()


import banana.maya

import sphinx


# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode'
]

if sphinx.version_info >= (1, 3):
    extensions.append('sphinx.ext.napoleon')
else:
    extensions.append('sphinxcontrib.napoleon')

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'banana.maya'
copyright = u'2014, Christopher Crouzet'
version = banana.maya.__version__
release = version

exclude_patterns = []
default_role = 'autolink'

add_module_names = False
show_authors = False

pygments_style = 'sphinx'
autodoc_member_order = 'bysource'


# -- Options for HTML output ----------------------------------------------

if os.environ.get('READTHEDOCS', None) != 'True':
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        pass

html_static_path = ['_static']
htmlhelp_basename = 'bananamayadoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
    ('index', 'bananamaya.tex', u'banana.maya Documentation',
     u'Christopher Crouzet', 'manual')
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    ('index', 'bananamaya', u'banana.maya Documentation',
     [u'Christopher Crouzet'], 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
      ('index', 'bananamaya', u'banana.maya Documentation',
       u'Christopher Crouzet', 'bananamaya',
       'Extensions for the Python API of Autodesk Maya.',
       'Miscellaneous')
]

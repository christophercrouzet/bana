import io
import os
import re
import setuptools


def _read(*paths, **kwargs):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.dirname(__file__)
    encoding = kwargs.get('encoding', 'utf8')
    with io.open(os.path.join(here, *paths), encoding=encoding) as f:
        return f.read()


def _getMetas(*filePaths):
    data = _read(*filePaths)
    out = {}
    metas = ('author', 'contact', 'license', 'summary', 'title', 'url',
             'version')
    for meta in metas:
        pattern = r'^__%s__ = u?[\'"]([^\'"]*)[\'"]' % (meta,)
        match = re.search(pattern, data, re.MULTILINE)
        if match is None:
            raise RuntimeError("Unable to find the metadata '%s'." % (meta,))

        out[meta] = match.group(1)

    return out


_METAS = _getMetas('bana', '__init__.py')

setuptools.setup(
    name=_METAS['title'],
    version=_METAS['version'],
    description=_METAS['summary'],
    url=_METAS['url'],
    author=_METAS['author'],
    author_email=_METAS['contact'],
    license=_METAS['license'],
    keywords='Autodesk Maya gorilla API extensions monkey patch patching revl',
    long_description=_read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=['gorilla>=0.2.0'],
    extras_require={
        'dev': ['coverage', 'pycodestyle', 'pydocstyle', 'pylint',
                'sphinx>=1.3', 'revl'],
        'docs': ['sphinx>=1.3'],
    },
    packages=[
        'bana',
        'bana.OpenMaya',
        'bana.OpenMayaAnim',
        'bana.OpenMayaFX',
        'bana.OpenMayaRender',
        'bana.OpenMayaUI',
    ],
    include_package_data=True
)

"""
    banana.maya.MGlobal
    ~~~~~~~~~~~~~~~~~~~
    
    Monkey patching of the `~maya.OpenMaya.MGlobal` class.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import re

import gorilla
from maya import OpenMaya

import banana.maya._cache


_SHORT_NAME_PATTERN = r'[a-zA-Z_][\w]*'
_SHORT_NAME_WILD_PATTERN = r'[a-zA-Z_\*][\w\*]*'
_NAME_PATTERN = r'(?:%s)(?:\:%s)*' % ((_SHORT_NAME_PATTERN, ) * 2)
_NAME_WILD_PATTERN = r'(?:%s)(?:\:%s)*' % ((_SHORT_NAME_WILD_PATTERN, ) * 2)

_RE_SHORT_NAME_PATTERN = re.compile(
    r'^%s$' % _SHORT_NAME_PATTERN)
_RE_SHORT_NAME_WILD_PATTERN = re.compile(
    r'^%s$' % _SHORT_NAME_WILD_PATTERN)
_RE_NAME_PATTERN = re.compile(
    r'^%s$' % _NAME_PATTERN)
_RE_NAME_WILD_PATTERN = re.compile(
    r'^%s$' % _NAME_WILD_PATTERN)
_RE_PATH_PATTERN = re.compile(
    r'^(?:\|%s)+(?:->(?:\|%s)+)*$' % ((_NAME_PATTERN, ) * 2))
_RE_PATH_WILD_PATTERN = re.compile(
    r'^(?:\*?\|%s)+(?:->(?:\|%s)+)*$' % ((_NAME_WILD_PATTERN, ) * 2))

_RE_NAME_DUPLICATES = re.compile(
    r'([\:])\1+')
_RE_NAME_DUPLICATES_WILD = re.compile(
    r'([\*\:])\1+')
_RE_NAME_STRIP_BEGIN = re.compile(
    r'^[^a-zA-Z_]+')
_RE_NAME_STRIP_BEGIN_WILD = re.compile(
    r'^[^a-zA-Z_\*]+')
_RE_NAME_STRIP_END = re.compile(
    r'[^\w\:]+$')
_RE_NAME_STRIP_END_WILD = re.compile(
    r'[^\w\*\:]+$')
_RE_NAME_INVALID_CHARACTERS = re.compile(
    r'[^\w\:]')
_RE_NAME_INVALID_CHARACTERS_WILD = re.compile(
    r'[^\w\*\:]')

_RE_PATH_DUPLICATES = re.compile(
    r'([\|\:])\1+')
_RE_PATH_DUPLICATES_WILD = re.compile(
    r'([\*\|\:])\1+')
_RE_PATH_PART_STRIP_BEGIN = re.compile(
    r'^[^a-zA-Z_\|]+')
_RE_PATH_PART_STRIP_BEGIN_WILD = re.compile(
    r'^[^a-zA-Z_\*\|]+')
_RE_PATH_PART_STRIP_END = re.compile(
    r'[^\w\:]+$')
_RE_PATH_PART_STRIP_END_WILD = re.compile(
    r'[^\w\*\:]+$')
_RE_PATH_INVALID_CHARACTERS = re.compile(
    r'[^\w\|\:]')
_RE_PATH_INVALID_CHARACTERS_WILD = re.compile(
    r'[^\w\*\|\:]')


@gorilla.patch(OpenMaya)
class MGlobal(object):
    
    @classmethod
    def bnn_getFunctionSetFromType(cls, type):
        """Retrieve the function set class from a type.
        
        Parameters
        ----------
        type : maya.OpenMaya.MFn.Type
            Type of the dunction set to look for.
        
        Returns
        -------
        class
            The function set class found, None otherwise.
        
        Examples
        --------
        Initialize the appropriate function set according to the type returned
        by a DAG path object:
        
        >>> import banana.maya
        >>> banana.maya.patch()
        >>> from maya import OpenMaya, cmds
        >>> cmds.group(name='transform', empty=True)
        >>> dagPath = OpenMaya.MDagPath.bnn_get(pattern='transform')
        >>> cls = OpenMaya.MGlobal.bnn_getFunctionSetFromType(dagPath.apiType())
        >>> transform = cls(dagPath)
        """
        return banana.maya._cache.FUNCTION_SET_FROM_TYPE.get(type, None)
    
    @classmethod
    def bnn_isValidShortNamePattern(cls, name, wildcards=False):
        """Check if a short name has a valid pattern.
        
        That is, a short name that is strictly well-formed and that is
        guaranteed to be accepted by the more forgiving syntax checker of Maya.
        
        Short names are used within simple types such as attributes.
        
        Parameters
        ----------
        name : str
            Short name to check.
        wildcards : bool
            True to consider the wildcards `*` as valid characters.
        
        Returns
        -------
        bool
            True if the short name is valid and strictly well-formed.
        """
        # The valid characters forming a name can be checked as follow:
        # >>> from maya import cmds
        # >>> tests = {'first chars': '', 'chars': '_'}
        # ... for test, append in tests.iteritems():
        # ...    valid_characters = []
        # ...    for i in range(128):
        # ...        character = chr(i).decode('ascii')
        # ...        node = cmds.group(name=append + character, empty=True)
        # ...        if node == append + character:
        # ...            valid_characters.append(character)
        # ...        cmds.delete(node)
        # ...    print('%s: %s' % (test, ''.join(valid_characters)))
        # chars: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz
        # first chars: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
        
        if wildcards and not _RE_PATH_DUPLICATES_WILD.search(name):
            return True if _RE_SHORT_NAME_WILD_PATTERN.match(name) else False
        
        if not _RE_PATH_DUPLICATES.search(name):
            return True if _RE_SHORT_NAME_PATTERN.match(name) else False
        
        return False
    
    @classmethod
    def bnn_isValidNamePattern(cls, name, wildcards=False):
        """Check if a name has a valid pattern.
        
        That is, a name that is strictly well-formed and that is guaranteed
        to be accepted by the more forgiving syntax checker of Maya.
        
        Names are used as identifiers for nodes. Namespaces are taken
        into account.
        
        Parameters
        ----------
        name : str
            Name to check.
        wildcards : bool
            True to consider the wildcards `*` as valid characters.
        
        Returns
        -------
        bool
            True if the name is valid and strictly well-formed.
        """
        # ``maya.OpenMaya.MNamespace.validateName()`` is not usable here since
        # it would discard any name containing a non-existing namespace.
        
        if wildcards and not _RE_PATH_DUPLICATES_WILD.search(name):
            return True if _RE_NAME_WILD_PATTERN.match(name) else False
        
        if not _RE_PATH_DUPLICATES.search(name):
            return True if _RE_NAME_PATTERN.match(name) else False
        
        return False
    
    @classmethod
    def bnn_isValidPathPattern(cls, path, wildcards=False):
        """Check if a DAG path has a valid pattern.
        
        That is, a DAG path that is strictly well-formed and that is
        guaranteed to be accepted by the more forgiving syntax checker of Maya.
        
        Namespaces and underworld are taken into account.
        
        Parameters
        ----------
        path : str
            DAG path to check.
        wildcards : bool
            True to consider the wildcards `*` as valid characters.
        
        Returns
        -------
        bool
            True if the path is a valid and strictly well-formed DAG path.
        """
        if wildcards and not _RE_PATH_DUPLICATES_WILD.search(path):
            return True if _RE_PATH_WILD_PATTERN.match(path) else False
        
        if not _RE_PATH_DUPLICATES.search(path):
            return True if _RE_PATH_PATTERN.match(path) else False
        
        return False
    
    @classmethod
    def bnn_matchPath(cls, pattern, path):
        """Check if a DAG path matches a given pattern.
        
        Both pattern and path should be strictly well-formed. Use
        `normalizePath()` if it is not the case.
        
        Parameters
        ----------
        pattern : str
            Pattern to match to. Wildcards are allowed.
        path : str
            DAG path to check.
        
        Returns
        -------
        bool
            True if the DAG path matches the given pattern.
        
        Raises
        ------
        ValueError
            Either the pattern or the path is not well-formed.
        
        Note
        ----
            For the pattern ``|*``, Maya matches only the top level nodes
            while ``node|shape->|*`` matches all the underworld nodes
            to be found at any depth. This is inconsistent and we assume
            here that ``node|shape->|*`` matches only the top level nodes
            from the underworld.
        """
        if not cls.bnn_isValidPathPattern(pattern, wildcards=True):
            raise ValueError(
                "The pattern '%s' is not well-formed, try to normalize it." %
                pattern)
        
        if not cls.bnn_isValidPathPattern(path):
            raise ValueError(
                "The path '%s' is not well-formed, try to normalize it." %
                path)
        
        if pattern.startswith('*'):
            pattern = pattern.lstrip('*')
            search = True
        else:
            search = False
        
        underworldParts = pattern.split('->')
        for i in range(len(underworldParts)):
            underworldPart = underworldParts[i]
            underworldPart = underworldPart.replace('*', r'[\w]*?')
            underworldPart = underworldPart.replace(':', r'\:')
            underworldPart = underworldPart.replace('|', r'\|')
            underworldParts[i] = underworldPart
        
        pattern = '->'.join(underworldParts)
        if search:
            return True if re.search(r'%s$' % pattern, path) else False
        
        return True if re.match(r'^%s$' % pattern, path) else False
    
    @classmethod
    def bnn_normalizeName(cls, name, wildcards=False):
        """Normalize a name.
        
        This results in a strictly well-formed name.
        
        Parameters
        ----------
        name : str
            Name to normalize.
        wildcards : bool
            True to consider the wildcards `*` as valid characters.
        
        Returns
        -------
        str
            The normalized name.
        
        Raises
        ------
        ValueError
            The input name is invalid and can't be normalized.
        """
        if not name:
            return '*'
        
        if wildcards:
            reNameDuplicates = _RE_NAME_DUPLICATES_WILD
            reNameStripBegin = _RE_NAME_STRIP_BEGIN_WILD
            reNameStripEnd = _RE_NAME_STRIP_END_WILD
            reNameInvalidCharacters = _RE_NAME_INVALID_CHARACTERS_WILD
        else:
            reNameDuplicates = _RE_NAME_DUPLICATES
            reNameStripBegin = _RE_NAME_STRIP_BEGIN
            reNameStripEnd = _RE_NAME_STRIP_END
            reNameInvalidCharacters = _RE_NAME_INVALID_CHARACTERS
        
        normalized = reNameDuplicates.sub(r'\1', name)
        normalized = reNameStripBegin.sub('', normalized)
        normalized = reNameStripEnd.sub('', normalized)
        normalized = reNameInvalidCharacters.sub('_', normalized)
        if not cls.bnn_isValidNamePattern(normalized, wildcards=wildcards):
            raise ValueError("The input name '%s' is invalid" % name)
        
        return normalized
    
    @classmethod
    def bnn_normalizePath(cls, path, wildcards=False):
        """Normalize a DAG path.
        
        This results in a strictly well-formed DAG path.
        
        Parameters
        ----------
        path : str
            DAG path to normalize.
        wildcards : bool
            True to consider the wildcards `*` as valid characters.
        
        Returns
        -------
        str
            The normalized DAG path.
        
        Raises
        ------
        ValueError
            The input path is invalid and can't be normalized.
        """
        if not path:
            return '*|*'
        
        if wildcards:
            rePathDuplicates = _RE_PATH_DUPLICATES_WILD
            rePathPartStripBegin = _RE_PATH_PART_STRIP_BEGIN_WILD
            rePathPartStripEnd = _RE_PATH_PART_STRIP_END_WILD
            rePathInvalidCharacters = _RE_PATH_INVALID_CHARACTERS_WILD
        else:
            rePathDuplicates = _RE_PATH_DUPLICATES
            rePathPartStripBegin = _RE_PATH_PART_STRIP_BEGIN
            rePathPartStripEnd = _RE_PATH_PART_STRIP_END
            rePathInvalidCharacters = _RE_PATH_INVALID_CHARACTERS
        
        normalized = rePathDuplicates.sub(r'\1', path)
        underworldParts = normalized.split('->')
        for i in range(len(underworldParts)):
            underworldPart = underworldParts[i]
            pathParts = underworldPart.split('|')
            for j in range(len(pathParts)):
                pathPart = pathParts[j]
                pathPart = rePathPartStripBegin.sub('', pathPart)
                pathPart = rePathPartStripEnd.sub('', pathPart)
                pathPart = rePathInvalidCharacters.sub('_', pathPart)
                pathParts[j] = pathPart
            
            if i == 0:
                if pathParts[0] and pathParts[0] != '*':
                    pathParts.insert(0, '*')
            elif pathParts[0]:
                pathParts.insert(0, '')
            
            if not pathParts[-1]:
                del pathParts[-1]
            
            underworldParts[i] = '|'.join(pathParts)
        
        normalized = '->'.join(underworldParts)
        if not cls.bnn_isValidPathPattern(normalized, wildcards=True):
            raise ValueError("The input path '%s' is invalid" % path)
        
        return normalized

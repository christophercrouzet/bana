"""Extensions for the ``maya.OpenMaya.MGlobal`` class."""

import gorilla
from maya import OpenMaya

from bana import _pattern


@gorilla.patches(OpenMaya.MGlobal)
class MGlobal(object):
    """Container for the extensions."""

    @classmethod
    def bnIsValidName(cls, name, allowWildcards=False):
        """Check if a *name* is strictly well-formed.

        *Names* can identify DG nodes, excluding the ones carrying any
        namespace or hierarchy information. They are made of *character*
        elements, that is alphanumeric characters, underscores, and wildcards.

        Categories: :term:`explicit`.

        Parameters
        ----------
        path : str
            *Name* to check.
        allowWildcards : bool
            ``True`` to consider the wildcards as valid characters.

        Returns
        -------
        bool
            ``True`` if the *name* is strictly well-formed.

        See Also
        --------
        :ref:`pattern_matching`.
        """
        if allowWildcards:
            return bool(_pattern.NAME_WCARD_OBJ.match(name))
        else:
            return bool(_pattern.NAME_OBJ.match(name))

    @classmethod
    def bnIsValidFullName(cls, name, allowWildcards=False,
                          matchRelative=False):
        """Check if a *full name* is strictly well-formed.

        *Full names* can fully identify any DG node. They are composed by one
        or more *name* elements, each separated by the namespace delimiter
        ``:``.

        Categories: :term:`explicit`.

        Parameters
        ----------
        path : str
            *Full name* to check.
        allowWildcards : bool
            ``True`` to consider the wildcards as valid characters.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent namespace. That
            is, *full names* starting with the namespace delimiter ``:`` are
            allowed.

        Returns
        -------
        bool
            ``True`` if the *full name* is strictly well-formed.

        See Also
        --------
        :ref:`pattern_matching`.
        """
        if allowWildcards:
            if matchRelative:
                return bool(_pattern.RELATIVE_NAME_WCARD_OBJ.match(name))
            else:
                return bool(_pattern.FULL_NAME_WCARD_OBJ.match(name))
        elif matchRelative:
            return bool(_pattern.RELATIVE_NAME_OBJ.match(name))
        else:
            return bool(_pattern.FULL_NAME_OBJ.match(name))

    @classmethod
    def bnIsValidPath(cls, path, allowWildcards=False):
        """Check if a *path* is strictly well-formed.

        *Paths* can identify DAG nodes, excluding the ones carrying any
        underworld information. They are composed by one or more *full name*
        elements, each starting with the hierarchy delimiter ``|``.

        Categories: :term:`explicit`.

        Parameters
        ----------
        path : str
            *Path* to check.
        allowWildcards : bool
            ``True`` to consider the wildcards as valid characters.

        Returns
        -------
        bool
            ``True`` if the *path* is strictly well-formed.

        See Also
        --------
        :ref:`pattern_matching`.
        """
        if allowWildcards:
            return bool(_pattern.PATH_WCARD_OBJ.match(path))
        else:
            return bool(_pattern.PATH_OBJ.match(path))

    @classmethod
    def bnIsValidFullPath(cls, path, allowWildcards=False,
                          matchRelative=False):
        """Check if a *full path* is strictly well-formed.

        *Full paths* can fully identify any DAG node. They are composed by one
        or more *path* elements, each separated by the underworld delimiter
        ``->``.

        Categories: :term:`explicit`.

        Parameters
        ----------
        path : str
            *Full path* to check.
        allowWildcards : bool
            ``True`` to consider the wildcards as valid characters.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent path. That is,
            *full paths* starting with the underworld delimiter ``->`` are
            allowed.

        Returns
        -------
        bool
            ``True`` if the *full path* is strictly well-formed.

        See Also
        --------
        :ref:`pattern_matching`.
        """
        if allowWildcards:
            if matchRelative:
                return bool(_pattern.RELATIVE_PATH_WCARD_OBJ.match(path))
            else:
                return bool(_pattern.FULL_PATH_WCARD_OBJ.match(path))
        elif matchRelative:
            return bool(_pattern.RELATIVE_PATH_OBJ.match(path))
        else:
            return bool(_pattern.FULL_PATH_OBJ.match(path))

    @classmethod
    def bnMakeMatchNameFunction(cls, pattern):
        """Create a function to match *names* to a pattern.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            *Name* pattern to build. Wildcards are allowed.

        Returns
        -------
        function
            A function expecting a single parameter, that is the *name* to
            check the pattern against. The return value of this function is a
            value that evaluates to ``True`` or ``False`` in a boolean
            operation. The value passed to the parameter of this function must
            be a strictly well-formed *name*. No check is done to ensure the
            validity of the input but this can be done manually using
            :meth:`MGlobal.bnIsValidName`.

        Raises
        ------
        ValueError
            The pattern is not well-formed.

        Examples
        --------
        >>> import bana
        >>> bana.initialize()
        >>> from maya import OpenMaya
        >>> iterator = OpenMaya.MItDependencyNodes()
        >>> match = OpenMaya.MGlobal.bnMakeMatchNameFunction('*Shape*')
        >>> while not iterator.isDone():
        ...     obj = iterator.thisNode()
        ...     name = OpenMaya.MFnDependencyNode(obj).name()
        ...     if match(name):
        ...         print(name)
        ...     iterator.next()

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidName`.
        """
        hasWildcards = _pattern.hasWildcards(pattern)
        if not cls.bnIsValidName(pattern, allowWildcards=hasWildcards):
            raise ValueError("The name pattern '%s' is not valid."
                             % (pattern,))

        return _pattern.makeMatchFunction(pattern, _pattern.CONTEXT_NAME)

    @classmethod
    def bnMakeMatchFullNameFunction(cls, pattern, matchRelative=False):
        """Create a function to match *full names* to a pattern.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            Full name pattern to build. Wildcards are allowed.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent namespace. That
            is, *full names* starting with the namespace delimiter ``:`` are
            allowed.

        Returns
        -------
        function
            A function expecting a single parameter, that is the *full name* to
            check the pattern against. The return value of this function is a
            value that evaluates to ``True`` or ``False`` in a boolean
            operation. The value passed to the parameter of this function must
            be a strictly well-formed *full name*. No check is done to ensure
            the validity of the input but this can be done manually using
            :meth:`MGlobal.bnIsValidFullName`.

        Raises
        ------
        ValueError
            The pattern is not well-formed.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidFullName`.
        """
        hasWildcards = _pattern.hasWildcards(pattern)
        if not cls.bnIsValidFullName(pattern, allowWildcards=hasWildcards,
                                     matchRelative=matchRelative):
            raise ValueError("The full name pattern '%s' is not valid."
                             % (pattern,))

        return _pattern.makeMatchFunction(pattern, _pattern.CONTEXT_FULL_NAME,
                                          matchRelative=matchRelative)

    @classmethod
    def bnMakeMatchPathFunction(cls, pattern):
        """Create a function to match *paths* to a pattern.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            *Path* pattern to build. Wildcards are allowed.

        Returns
        -------
        function
            A function expecting a single parameter, that is the *path* to
            check the pattern against. The return value of this function is a
            value that evaluates to ``True`` or ``False`` in a boolean
            operation. The value passed to the parameter of this function must
            be a strictly well-formed *path*. No check is done to ensure the
            validity of the input but this can be done manually using
            :meth:`MGlobal.bnIsValidPath`.

        Raises
        ------
        ValueError
            The pattern is not well-formed.

        Examples
        --------
        >>> import bana
        >>> bana.initialize()
        >>> from maya import OpenMaya
        >>> iterator = OpenMaya.MItDag()
        >>> match = OpenMaya.MGlobal.bnMakeMatchPathFunction('*|*Shape*')
        >>> dagPath = OpenMaya.MDagPath()
        >>> while not iterator.isDone():
        ...     iterator.getPath(dagPath)
        ...     path = dagPath.fullPathName()
        ...     if match(path):
        ...         print(path)
        ...     iterator.next()

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidPath`.
        """
        hasWildcards = _pattern.hasWildcards(pattern)
        if not cls.bnIsValidPath(pattern, allowWildcards=hasWildcards):
            raise ValueError("The path pattern '%s' is not valid."
                             % (pattern,))

        return _pattern.makeMatchFunction(pattern, _pattern.CONTEXT_PATH)

    @classmethod
    def bnMakeMatchFullPathFunction(cls, pattern, matchRelative=False):
        """Create a function to match *full paths* to a pattern.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            *Full path* pattern to build. Wildcards are allowed.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent path. That is,
            *full paths* starting with the underworld delimiter ``->`` are
            allowed.

        Returns
        -------
        function
            A function expecting a single parameter, that is the *full path* to
            check the pattern against. The return value of this function is a
            value that evaluates to ``True`` or ``False`` in a boolean
            operation. The value passed to the parameter of this function must
            be a strictly well-formed *full path*. No check is done to ensure
            the validity of the input but this can be done manually using
            :meth:`MGlobal.bnIsValidFullPath`.

        Raises
        ------
        ValueError
            The pattern is not well-formed.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidFullPath`.
        """
        hasWildcards = _pattern.hasWildcards(pattern)
        if not cls.bnIsValidFullPath(pattern, allowWildcards=hasWildcards,
                                     matchRelative=matchRelative):
            raise ValueError("The full path pattern '%s' is not valid."
                             % (pattern,))

        return _pattern.makeMatchFunction(pattern, _pattern.CONTEXT_FULL_PATH,
                                          matchRelative=matchRelative)

    @classmethod
    def bnMatchName(cls, pattern, name):
        """Check if a *name* matches a given pattern.

        Both pattern and *name* must be strictly well-formed.

        If the same pattern is to be matched several times, consider using
        :meth:`MGlobal.bnMakeMatchNameFunction` instead.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            Pattern to match to. Wildcards are allowed.
        path : str
            *Name* to check.

        Returns
        -------
        bool
            ``True`` if the *name* matches the given pattern.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidName`.
        """
        if not cls.bnIsValidName(name):
            raise ValueError("The name pattern '%s' is not valid." % (name,))

        return bool(cls.bnMakeMatchNameFunction(pattern)(name))

    @classmethod
    def bnMatchFullName(cls, pattern, name, matchRelative=False):
        """Check if a *full name* matches a given pattern.

        Both pattern and *full name* must be strictly well-formed.

        If the same pattern is to be matched several times, consider using
        :meth:`MGlobal.bnMakeMatchFullNameFunction` instead.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            Pattern to match to. Wildcards are allowed.
        path : str
            *Full name* to check.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent namespace. That
            is, *full names* starting with the namespace delimiter ``:`` are
            allowed.

        Returns
        -------
        bool
            ``True`` if the *full name* matches the given pattern.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidFullName`.
        """
        if not cls.bnIsValidFullName(name, matchRelative=matchRelative):
            raise ValueError("The full name pattern '%s' is not valid."
                             % (name,))

        return bool(cls.bnMakeMatchFullNameFunction(
            pattern, matchRelative=matchRelative)(name))

    @classmethod
    def bnMatchPath(cls, pattern, path):
        """Check if a *path* matches a given pattern.

        Both pattern and *path* must be strictly well-formed.

        If the same pattern is to be matched several times, consider using
        :meth:`MGlobal.bnMakeMatchPathFunction` instead.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            Pattern to match to. Wildcards are allowed.
        path : str
            *Path* to check.

        Returns
        -------
        bool
            ``True`` if the *path* matches the given pattern.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidPath`.
        """
        if not cls.bnIsValidPath(path):
            raise ValueError("The path pattern '%s' is not valid." % (path,))

        return bool(cls.bnMakeMatchPathFunction(pattern)(path))

    @classmethod
    def bnMatchFullPath(cls, pattern, path, matchRelative=False):
        """Check if a *full path* matches a given pattern.

        Both pattern and *full path* must be strictly well-formed.

        If the same pattern is to be matched several times, consider using
        :meth:`MGlobal.bnMakeMatchFullPathFunction` instead.

        Categories: :term:`explicit`.

        Parameters
        ----------
        pattern : str
            Pattern to match to. Wildcards are allowed.
        path : str
            *Full path* to check.
        matchRelative : bool
            ``True`` to allow matching relatively to a parent path. That is,
            *full paths* starting with the underworld delimiter ``->`` are
            allowed.

        Returns
        -------
        bool
            ``True`` if the *full path* matches the given pattern.

        See Also
        --------
        :ref:`pattern_matching`, :meth:`MGlobal.bnIsValidFullPath`.
        """
        if not cls.bnIsValidFullPath(path, matchRelative=matchRelative):
            raise ValueError("The full path pattern '%s' is not valid."
                             % (path,))

        return bool(cls.bnMakeMatchFullPathFunction(
            pattern, matchRelative=matchRelative)(path))

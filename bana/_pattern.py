"""Pattern utilities.

:copyright: Copyright 2014-2017 by Christopher Crouzet.
:license: MIT, see LICENSE for details.
"""

# Here be dragons. You most likely do not want to modify or even try to
# understand any of the code in this file. Do yourself a favour and move on.
# After all, the code just works. I think. The 19629 combined tests surely
# prove it, right? Anyways, you've been warned. Send complaints directly to
# whoever wrote Maya and thought of inconsistency as a form of art.

import re


# Enumerator for the pattern matching contexts.
CONTEXT_NAME = 0
CONTEXT_FULL_NAME = 1
CONTEXT_PATH = 2
CONTEXT_FULL_PATH = 3
CONTEXT_ANY = 4


NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
FULL_NAME = r'(?:%s:)*%s' % ((NAME,) * 2)
RELATIVE_NAME = r':?%s' % (FULL_NAME,)
PATH = r'(?:\|%s)+' % (FULL_NAME,)
FULL_PATH = r'%s(?:->%s)*(?:->)?' % ((PATH,) * 2)
RELATIVE_PATH = r'(?:(?:->)|(?:(?:->)?%s))' % (FULL_PATH,)

NAME_WCARD = r'[a-zA-Z_*+?.][a-zA-Z0-9_*+?.]*'
FULL_NAME_WCARD = r'(?:(?::[*+?.]+)|(?:%s))(?::%s)*' % ((NAME_WCARD,) * 2)
RELATIVE_NAME_WCARD = r':?%s' % (FULL_NAME_WCARD,)
PATH_WCARD = r'(?:(?:\|%s)|(?:[*+?.]))+' % (FULL_NAME_WCARD,)
FULL_PATH_WCARD = r'%s(?:->%s)*(?:->)?' % ((PATH_WCARD,) * 2)
RELATIVE_PATH_WCARD = r'(?:(?:->)|(?:(?:->)?%s))' % (FULL_PATH_WCARD,)

NAME_OBJ = re.compile(r'^%s$' % (NAME,))
FULL_NAME_OBJ = re.compile(r'^%s$' % (FULL_NAME,))
RELATIVE_NAME_OBJ = re.compile(r'^%s$' % (RELATIVE_NAME,))
PATH_OBJ = re.compile(r'^%s$' % (PATH,))
FULL_PATH_OBJ = re.compile(r'^%s$' % (FULL_PATH,))
RELATIVE_PATH_OBJ = re.compile(r'^%s$' % (RELATIVE_PATH,))

NAME_WCARD_OBJ = re.compile(r'^%s$' % (NAME_WCARD,))
FULL_NAME_WCARD_OBJ = re.compile(r'^%s$' % (FULL_NAME_WCARD,))
RELATIVE_NAME_WCARD_OBJ = re.compile(r'^%s$' % (RELATIVE_NAME_WCARD,))
PATH_WCARD_OBJ = re.compile(r'^%s$' % (PATH_WCARD,))
FULL_PATH_WCARD_OBJ = re.compile(r'^%s$' % (FULL_PATH_WCARD,))
RELATIVE_PATH_WCARD_OBJ = re.compile(r'^%s$' % (RELATIVE_PATH_WCARD,))


_WCARD = r'[*+?.]'
_CHARACTER = r'[a-zA-Z0-9_]'
_WCARD_OBJ = re.compile(_WCARD)
_RELATIVE_CONTEXTS = (CONTEXT_FULL_NAME, CONTEXT_FULL_PATH)
_WCARD_ITER_OBJ = re.compile(
    r'((?:\\\|)|(?:->)|.)([*+?.]+)(?=((?:\\\|)|(?:->)|.))')
_WCARD_CONTEXTS = {
    r'^': CONTEXT_ANY,
    r'$': CONTEXT_ANY,
    r':': CONTEXT_FULL_NAME,
    r'\|': CONTEXT_PATH,
    r'->': CONTEXT_FULL_PATH,
}
_WCARD_OCCURRENCE_RANGES = {
    '*': (0, None),
    '+': (1, None),
    '?': (0, 1),
    '.': (1, 1),
}
_EXPRESSIONS = {
    CONTEXT_NAME: (_CHARACTER, r''),
    CONTEXT_FULL_NAME: (NAME, r':'),
    CONTEXT_PATH: (FULL_NAME, r'\|'),
    CONTEXT_FULL_PATH: (PATH, r'->'),
}
_COLLAPSE_WHEN_NULL = (
    (r'^', r':'),
    (r'^', r'->'),
    (r':', r':'),
    (r'\|', r':'),
    (r'\|', r'\|'),
    (r'->', r'->'),
)
_REMOVE_ROOT_NAMESPACE_WCARD_OBJ = re.compile(r'(\^|(?:\\\|)):')


def hasWildcards(pattern):
    """Check if a pattern contains any wildcard.

    Parameters
    ----------
    pattern : str
        Pattern to check.

    Returns
    -------
    bool
        True if the pattern contains any wildcard.
    """
    return bool(_WCARD_OBJ.search(pattern))


def makeMatchFunction(pattern, context, matchRelative=False):
    """Create a match function from a pattern.

    The pattern needs to be strictly well-formed.

    Parameters
    ----------
    pattern : str
        Pattern to match against.
    context : int
        Global context in which the pattern is used.
    matchRelative : bool
        True to allow matching relatively to a parent namespace or path. That
        is, full names starting with the delimiter ``:`` and full paths
        starting with the delimiter ``->`` are allowed.

    Returns
    -------
    function
        The matching function, evaluating to True or False in a boolean
        operation.
    """
    if not hasWildcards(pattern):
        # Conversion to unicode is required because Maya's MString are
        # stored as unicode and Python ASCII strings can only compare to ASCII,
        # not to unicode, whereas a unicode string can compare to both ASCII
        # and unicode.
        return unicode(pattern).__eq__

    pattern = r'^%s$' % (pattern.replace('|', r'\|'),)

    # NOTE: although a regular expression `r'ab{0,0}'` yields the exact same
    # results as `r'a'`, the latter performs slightly faster than the former,
    # which is why some conditional branches were added to optimize specific
    # cases instead of falling back to the more generic solution.

    chunks = []
    pos = 0
    # Iterate over each group of wildcards found.
    for match in _WCARD_ITER_OBJ.finditer(pattern):
        before, wildcards, after = match.groups()
        if before != r'^' or after != r'$':
            context = min(_WCARD_CONTEXTS.get(before, CONTEXT_NAME),
                          _WCARD_CONTEXTS.get(after, CONTEXT_NAME))

        ms, ns = zip(*[_WCARD_OCCURRENCE_RANGES[wildcard]
                       for wildcard in wildcards])
        quantifier = (sum(ms), None if None in ns else sum(ns))

        base, delimiter = _EXPRESSIONS[context]
        if quantifier in ((0, 1), (1, 1)):
            # Specific optimization, read the note above.
            # expression : base
            expression = base
        elif context == CONTEXT_FULL_PATH and after == r'$':
            # Special case for `^@$` and `->@$`.
            # Append an optional underworld delimiter, thanks to Maya's
            # kUnderWorld node type.
            o = min(1, max(0, quantifier[0] - 1))
            p = 1 if quantifier[1] is None else min(1, quantifier[1] - 1)
            if quantifier in ((0, 2), (1, 2), (2, 2)):
                # Specific optimization, read the note above.
                # expression : base ("->" base?){o,p}
                expression = r'%s(?:->(?:%s)?){%s,%s}' % (base, base, o, p)
            else:
                # expression : base ("->" base){m,n} ("->" base?){o,p}
                m = max(0, quantifier[0] - 2)
                n = r'' if quantifier[1] is None else quantifier[1] - 2
                expression = r'%s(?:->%s){%s,%s}(?:->(?:%s)?){%s,%s}' % (
                    base, base, m, n, base, o, p)
        else:
            # expression : base (delimiter base){m,n}
            m = max(0, quantifier[0] - 1)
            n = r'' if quantifier[1] is None else quantifier[1] - 1
            expression = r'%s(?:%s%s){%s,%s}' % (base, delimiter, base, m, n)

        if context == CONTEXT_PATH and before != r'\|':
            # Special case for `^@$`, `^@|`, and `->@|`.
            # Prepend a path delimiter, thanks to Maya requiring each path
            # to be prefixed by a delimiter, unlike for the namespaces and
            # underworlds syntaxes.
            expression = r'\|%s' % (expression,)

        if before == r'^' and matchRelative and context in _RELATIVE_CONTEXTS:
            if quantifier[0] in (0, 1):
                # Special case for when a single occurrence can be matched,
                # which could translate into the pattern matching only a
                # delimiter.
                n = r'?' if quantifier[0] == 0 else ''
                expression = r'(?:(?:%s)%s|(?:(?:%s)?%s))' % (
                    delimiter, n, delimiter, expression)
            else:
                expression = r'(?:%s)?%s' % (delimiter, expression)

        if quantifier[0] == 0:
            if (before, after) in _COLLAPSE_WHEN_NULL:
                # Collapse the end delimiter when an empty match is allowed.
                expression = r'(?:%s%s)?' % (expression, after)
            else:
                expression = r'(?:%s)?%s' % (expression, after)
        else:
            expression = r'%s%s' % (expression, after)

        chunks.append(pattern[pos:match.start() + len(before)])
        chunks.append(expression)
        pos = match.end() + len(after)

    chunks.append(pattern[pos:])
    pattern = r''.join(chunks)

    # Remove any `:` delimiter found either at the start of the pattern or just
    # after a `|` delimiter. These are leftovers from the added namespace
    # construct allowing a full name to start with the `:` delimiter if it is
    # followed by one or more wildcards.
    if matchRelative:
        def replace(match):
            if match.group(1) == r'^':
                return r'^:?'

            return match.group(1)

        # When the match might be relative, mark the `:` delimiter as optional
        # instead of removing it.
        pattern = _REMOVE_ROOT_NAMESPACE_WCARD_OBJ.sub(replace, pattern)
    else:
        pattern = _REMOVE_ROOT_NAMESPACE_WCARD_OBJ.sub(r'\1', pattern)

    return re.compile(pattern).match

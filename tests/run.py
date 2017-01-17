#!/usr/bin/env mayapy

import argparse
import collections
import os
import sys
import unittest


# Usage's syntax based on docopt.
_USAGE = "%(prog)s [<name>...]"
_DESCRIPTION = (
    "Runs the tests that have their name containing either one of the 'name' "
    "arguments passed. If no 'name' argument is passed, all the tests are run."
)


def _findTests(path, selectors=None):
    if selectors is None:
        def filter(test):
            return True
    else:
        def filter(test):
            return any(selector in _getTestFullName(test)
                       for selector in selectors)

    out = []
    loader = unittest.TestLoader()
    if path == '__main__':
        rootTest = loader.loadTestsFromModule(sys.modules[path])
    else:
        rootTest = loader.discover(path)

    stack = collections.deque((rootTest,))
    while stack:
        test = stack.popleft()
        if isinstance(test, unittest.TestSuite):
            stack.extend(case for case in test)
        elif type(test).__name__ == 'ModuleImportFailure':
            try:
                # This should always throw an ImportError exception.
                getattr(test, _getTestName(test))()
            except ImportError as e:
                sys.exit(e.message.strip())
        elif filter(test):
            out.append(test)

    return out


def _getTestName(test):
    return test._testMethodName


def _getTestFullName(test):
    return '%s.%s.%s' % (type(test).__module__, type(test).__name__,
                         _getTestName(test))


def run(startPath, verbosity=2):
    parser = argparse.ArgumentParser(usage=_USAGE, description=_DESCRIPTION)
    parser.add_argument('name', nargs='*',
                        help='partial test names to search')
    args = parser.parse_args()
    selectors = args.name if args.name else None
    tests = _findTests(startPath, selectors)
    suite = unittest.TestLoader().suiteClass(tests)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)


if __name__ == "__main__":
    run(os.path.abspath(os.path.dirname(__file__)))

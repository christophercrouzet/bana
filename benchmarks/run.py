#!/usr/bin/env mayapy

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import argparse
import collections
import sys
import timeit
import unittest


_clock = timeit.default_timer


# Usage's syntax based on docopt.
_USAGE = "%(prog)s [<name>...]"
_DESCRIPTION = (
    "Runs the benchmarks that have their name containing either one of the "
    "'name' arguments passed. If no 'name' argument is passed, all the "
    "benchmarks are run."
)


# Enumerator for the internal messages.
_MESSAGE_SUITE_SETUP = 0
_MESSAGE_SUITE_TEARDOWN = 1


_Message = collections.namedtuple(
    '_Message', (
        'type',
        'value',
    )
)


class DummyResult(object):

    def wasSuccessful(self):
        return True


class BenchLoader(unittest.TestLoader):
    testMethodPrefix = 'bench'


class BenchRunner(object):

    def run(self, bench):
        stack = collections.deque((bench,))
        while stack:
            obj = stack.popleft()
            if isinstance(obj, _Message):
                if obj.type == _MESSAGE_SUITE_SETUP:
                    obj.value.setUpClass()
                elif obj.type == _MESSAGE_SUITE_TEARDOWN:
                    obj.value.tearDownClass()
            elif isinstance(obj, unittest.TestSuite):
                suites = [suite for suite in obj
                          if isinstance(suite, unittest.TestSuite)]
                cases = [case for case in obj
                         if not isinstance(case, unittest.TestSuite)]

                stack.extend(suites)

                seen = set()
                classes = [case.__class__ for case in cases
                           if case.__class__ not in seen
                           and seen.add(case.__class__) is None]
                for cls in classes:
                    stack.append(_Message(type=_MESSAGE_SUITE_SETUP,
                                          value=cls))
                    stack.extend(case for case in cases
                                 if case.__class__ is cls)
                    stack.append(_Message(type=_MESSAGE_SUITE_TEARDOWN,
                                          value=cls))
            else:
                function = getattr(obj, _getBenchName(obj))

                obj.setUp()
                start = _clock()
                function()
                elapsed = _clock() - start
                obj.tearDown()

                elapsed, unit = _convertTimeUnit(elapsed)
                print("%s (%s.%s) ... %.3f %ss"
                      % (_getBenchName(obj), obj.__class__.__module__,
                         obj.__class__.__name__, elapsed, unit))

        return DummyResult()


def _convertTimeUnit(value):
    if not value:
        return (value, '')

    prefixes = 'munpfa'
    level = 0
    while value < 1.0 and level < len(prefixes):
        value *= 1e3
        level += 1

    return (value, prefixes[level - 1] if level else '')


def _findBenchs(path, selectors=None):
    if selectors is None:
        def filter(bench):
            return True
    else:
        def filter(bench):
            return any(selector in _getBenchFullName(bench)
                       for selector in selectors)

    out = []
    if path == '__main__':
        rootBench = BenchLoader().loadTestsFromModule(sys.modules[path])
    else:
        rootBench = BenchLoader().discover(path, pattern='bench*.py')

    stack = collections.deque((rootBench,))
    while stack:
        obj = stack.popleft()
        if isinstance(obj, unittest.TestSuite):
            stack.extend(bench for bench in obj)
        elif type(obj).__name__ == 'ModuleImportFailure':
            try:
                # This should always throw an ImportError exception.
                getattr(obj, _getBenchName(obj))()
            except ImportError as e:
                sys.exit(e.message.strip())
        elif filter(obj):
            out.append(obj)

    return out


def _getBenchName(bench):
    return bench._testMethodName


def _getBenchFullName(bench):
    return '%s.%s.%s' % (bench.__class__.__module__, bench.__class__.__name__,
                         _getBenchName(bench))


def run(startPath):
    parser = argparse.ArgumentParser(usage=_USAGE, description=_DESCRIPTION)
    parser.add_argument('name', nargs='*',
                        help='partial benchmark names to search')
    args = parser.parse_args()
    selectors = args.name if args.name else None
    benchs = _findBenchs(startPath, selectors)
    suite = BenchLoader().suiteClass(benchs)
    BenchRunner().run(suite)


if __name__ == "__main__":
    run(os.path.abspath(os.path.dirname(__file__)))

#!/usr/bin/env mayapy

import os
import sys
import unittest

import maya.standalone
import revl
from maya import OpenMaya

_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, *((os.pardir,) * 2))))

import bana

import benchmarks._preset

bana.initialize()
maya.standalone.initialize()


def _retrieveDeepestDagPath():
    dagPath = OpenMaya.MDagPath()
    iterator = OpenMaya.MItDag()
    iterator.traverseUnderWorld(True)
    while not iterator.isDone():
        if iterator.depth() > dagPath.pathCount():
            iterator.getPath(dagPath)

        iterator.next()

    return dagPath


class MDagPathDeepSceneBench(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        OpenMaya.MFileIO.newFile(True)
        revl.run(benchmarks._preset.DEEP, 10000, seed=1.23)

    def benchBnFind1(self):
        for _ in OpenMaya.MDagPath.bnFind():
            pass

    def benchBnFind2(self):
        for _ in OpenMaya.MDagPath.bnFind(copy=False):
            pass

    def benchBnFind3(self):
        for _ in OpenMaya.MDagPath.bnFind(recursive=False):
            pass

    def benchBnFind4(self):
        for _ in OpenMaya.MDagPath.bnFind(recursive=False, copy=False):
            pass

    def benchBnFind5(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*'):
            pass

    def benchBnFind6(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', copy=False):
            pass

    def benchBnFind7(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', recursive=False):
            pass

    def benchBnFind8(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', recursive=False,
                                          copy=False):
            pass

    def benchBnFind9(self):
        dagPath = _retrieveDeepestDagPath()
        dagPath.pop(1)
        pattern = '%s|*' % (dagPath.fullPathName(),)
        for _ in OpenMaya.MDagPath.bnFind(pattern=pattern):
            pass

    def benchBnFind10(self):
        dagPath = _retrieveDeepestDagPath()
        dagPath.pop(1)
        pattern = '%s|*' % (dagPath.fullPathName(),)
        for _ in OpenMaya.MDagPath.bnFind(pattern=pattern, copy=False):
            pass

    def benchBnFind11(self):
        dagPath = _retrieveDeepestDagPath()
        dagPath.pop(1)
        pattern = '%s|*' % (dagPath.fullPathName(),)
        for _ in OpenMaya.MDagPath.bnFind(pattern=pattern, recursive=False):
            pass

    def benchBnFind12(self):
        dagPath = _retrieveDeepestDagPath()
        dagPath.pop(1)
        pattern = '%s|*' % (dagPath.fullPathName(),)
        for _ in OpenMaya.MDagPath.bnFind(pattern=pattern, recursive=False,
                                          copy=False):
            pass


class MDagPathFlatSceneBench(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        OpenMaya.MFileIO.newFile(True)
        revl.run(benchmarks._preset.FLAT, 10000, seed=1.23)

    def benchBnFind1(self):
        for _ in OpenMaya.MDagPath.bnFind():
            pass

    def benchBnFind2(self):
        for _ in OpenMaya.MDagPath.bnFind(copy=False):
            pass

    def benchBnFind3(self):
        for _ in OpenMaya.MDagPath.bnFind(recursive=False):
            pass

    def benchBnFind4(self):
        for _ in OpenMaya.MDagPath.bnFind(recursive=False, copy=False):
            pass

    def benchBnFind5(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*'):
            pass

    def benchBnFind6(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', copy=False):
            pass

    def benchBnFind7(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', recursive=False):
            pass

    def benchBnFind8(self):
        for _ in OpenMaya.MDagPath.bnFind(pattern='*', recursive=False,
                                          copy=False):
            pass


if __name__ == '__main__':
    from benchmarks.run import run
    run('__main__')

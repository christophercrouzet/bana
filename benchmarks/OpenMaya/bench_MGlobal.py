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


class MGlobalBench(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        OpenMaya.MFileIO.newFile(True)
        revl.run(benchmarks._preset.DEEP, 10000, seed=1.23)

    def setUp(self):
        self.names = []
        iterator = OpenMaya.MItDependencyNodes()
        while not iterator.isDone():
            obj = iterator.thisNode()
            self.names.append(OpenMaya.MFnDependencyNode(obj).name())
            iterator.next()

        self.paths = []
        iterator = OpenMaya.MItDag()
        iterator.traverseUnderWorld(True)
        dagPath = OpenMaya.MDagPath()
        while not iterator.isDone():
            iterator.getPath(dagPath)
            self.paths.append(dagPath.fullPathName())
            iterator.next()

    def benchBnMatchFullName(self):
        match = OpenMaya.MGlobal.bnMakeMatchFullNameFunction('*Shape*')
        for name in self.names:
            match(name)

    def benchBnMatchFullPath(self):
        match = OpenMaya.MGlobal.bnMakeMatchFullPathFunction('*|*Shape*')
        for path in self.paths:
            match(path)


if __name__ == '__main__':
    from benchmarks.run import run
    run('__main__')

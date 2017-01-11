#!/usr/bin/env mayapy

import maya.standalone
maya.standalone.initialize()

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, *((os.pardir,) * 2))))

import bana
bana.initialize()


import unittest

from maya import OpenMaya
import revl

from benchmarks import _preset


class MFnDependencyNodeBench(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        OpenMaya.MFileIO.newFile(True)
        revl.run(_preset.DEEP, 10000, seed=1.23)

    def benchBnFind1(self):
        for _ in OpenMaya.MFnDependencyNode.bnFind():
            pass

    def benchBnFind2(self):
        for _ in OpenMaya.MFnDependencyNode.bnFind(pattern='*'):
            pass

    def benchBnFind3(self):
        for _ in OpenMaya.MFnDependencyNode.bnFind(pattern='*Shape*'):
            pass

    def benchBnFind4(self):
        for _ in OpenMaya.MFnDependencyNode.bnFind(pattern='*:*Shape*'):
            pass

    def benchBnFind5(self):
        for _ in OpenMaya.MFnDependencyNode.bnFind(pattern='node'):
            pass


if __name__ == '__main__':
    from benchmarks.run import run
    run('__main__')

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


class MMatrixTest(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(OpenMaya.MMatrix()), "[[1.0, 0.0, 0.0, 0.0]\n [0.0, 1.0, 0.0, 0.0]\n [0.0, 0.0, 1.0, 0.0]\n [0.0, 0.0, 0.0, 1.0]]")

    def testBnGet(self):
        matrix = OpenMaya.MMatrix()
        self.assertEqual(matrix.bnGet(), [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

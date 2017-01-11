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


class MVectorTest(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(OpenMaya.MVector()), "[0.0, 0.0, 0.0]")

    def testBnGet(self):
        vector = OpenMaya.MVector(1.0, 2.0, 3.0)
        self.assertEqual(vector.bnGet(), [1.0, 2.0, 3.0])

    def testBnRotateBy(self):
        vector = OpenMaya.MVector(0.0, 1.0, 0.0)
        vector = vector.bnRotateBy([
            OpenMaya.MAngle(90.0, OpenMaya.MAngle.kDegrees).asRadians(),
            0.0,
            0.0
        ])
        self.assertEqual([round(x, 6) for x in vector.bnGet()], [0.0, 0.0, 1.0])


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

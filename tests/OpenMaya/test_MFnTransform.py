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


class MFnTransformTest(unittest.TestCase):

    def setUp(self):
        self.transform = OpenMaya.MFnTransform()
        self.transform.create()

    def testBnScale(self):
        self.transform.findPlug('scaleX').setDouble(1.0)
        self.transform.findPlug('scaleY').setDouble(2.0)
        self.transform.findPlug('scaleZ').setDouble(3.0)
        self.assertEqual(self.transform.bnGetScale(), [1.0, 2.0, 3.0])

        self.transform.bnSetScale([3.0, 2.0, 1.0])
        self.assertEqual(self.transform.bnGetScale(), [3.0, 2.0, 1.0])
        self.assertEqual(self.transform.findPlug('scaleX').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('scaleY').asDouble(), 2.0)
        self.assertEqual(self.transform.findPlug('scaleZ').asDouble(), 1.0)

        self.transform.bnScaleBy([1.0, 2.0, 3.0])
        self.assertEqual(self.transform.bnGetScale(), [3.0, 4.0, 3.0])
        self.assertEqual(self.transform.findPlug('scaleX').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('scaleY').asDouble(), 4.0)
        self.assertEqual(self.transform.findPlug('scaleZ').asDouble(), 3.0)

    def testBnShear(self):
        self.transform.findPlug('shearXY').setDouble(1.0)
        self.transform.findPlug('shearXZ').setDouble(2.0)
        self.transform.findPlug('shearYZ').setDouble(3.0)
        self.assertEqual(self.transform.bnGetShear(), [1.0, 2.0, 3.0])

        self.transform.bnSetShear([3.0, 2.0, 1.0])
        self.assertEqual(self.transform.bnGetShear(), [3.0, 2.0, 1.0])
        self.assertEqual(self.transform.findPlug('shearXY').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('shearXZ').asDouble(), 2.0)
        self.assertEqual(self.transform.findPlug('shearYZ').asDouble(), 1.0)

        self.transform.bnShearBy([1.0, 2.0, 3.0])
        self.assertEqual(self.transform.bnGetShear(), [3.0, 4.0, 3.0])
        self.assertEqual(self.transform.findPlug('shearXY').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('shearXZ').asDouble(), 4.0)
        self.assertEqual(self.transform.findPlug('shearYZ').asDouble(), 3.0)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

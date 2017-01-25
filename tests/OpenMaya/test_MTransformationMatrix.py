#!/usr/bin/env mayapy

import os
import sys
import unittest

import maya.standalone
from maya import OpenMaya

_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, *((os.pardir,) * 2))))

import bana

bana.initialize()
maya.standalone.initialize()


class MTransformationMatrixTest(unittest.TestCase):

    def setUp(self):
        self.transform = OpenMaya.MFnTransform()
        self.transform.create()

    def testBnRotation(self):
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnAddRotation, [1.0, 2.0, 3.0])
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnGetRotation)
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnSetRotation, [1.0, 2.0, 3.0])

    def testBnRotationQuaternion(self):
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnAddRotationQuaternion, [1.0, 2.0, 3.0, 4.0])
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnGetRotationQuaternion)
        self.assertRaises(NotImplementedError, OpenMaya.MTransformationMatrix().bnSetRotationQuaternion, [1.0, 2.0, 3.0, 4.0])

    def testBnScale(self):
        self.transform.findPlug('scaleX').setDouble(1.0)
        self.transform.findPlug('scaleY').setDouble(2.0)
        self.transform.findPlug('scaleZ').setDouble(3.0)
        xform = self.transform.transformation()
        self.assertEqual(xform.bnGetScale(), [1.0, 2.0, 3.0])

        xform.bnSetScale([3.0, 2.0, 1.0])
        self.assertEqual(xform.bnGetScale(), [3.0, 2.0, 1.0])

        self.transform.set(xform)
        self.assertEqual(self.transform.findPlug('scaleX').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('scaleY').asDouble(), 2.0)
        self.assertEqual(self.transform.findPlug('scaleZ').asDouble(), 1.0)

        xform.bnAddScale([1.0, 2.0, 3.0])
        self.assertEqual(xform.bnGetScale(), [3.0, 4.0, 3.0])

        self.transform.set(xform)
        self.assertEqual(self.transform.findPlug('scaleX').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('scaleY').asDouble(), 4.0)
        self.assertEqual(self.transform.findPlug('scaleZ').asDouble(), 3.0)

    def testBnShear(self):
        self.transform.findPlug('shearXY').setDouble(1.0)
        self.transform.findPlug('shearXZ').setDouble(2.0)
        self.transform.findPlug('shearYZ').setDouble(3.0)
        xform = self.transform.transformation()
        self.assertEqual(xform.bnGetShear(), [1.0, 2.0, 3.0])

        xform.bnSetShear([3.0, 2.0, 1.0])
        self.assertEqual(xform.bnGetShear(), [3.0, 2.0, 1.0])

        self.transform.set(xform)
        self.assertEqual(self.transform.findPlug('shearXY').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('shearXZ').asDouble(), 2.0)
        self.assertEqual(self.transform.findPlug('shearYZ').asDouble(), 1.0)

        xform.bnAddShear([1.0, 2.0, 3.0])
        self.assertEqual(xform.bnGetShear(), [3.0, 4.0, 3.0])

        self.transform.set(xform)
        self.assertEqual(self.transform.findPlug('shearXY').asDouble(), 3.0)
        self.assertEqual(self.transform.findPlug('shearXZ').asDouble(), 4.0)
        self.assertEqual(self.transform.findPlug('shearYZ').asDouble(), 3.0)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

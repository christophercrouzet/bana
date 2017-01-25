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


class MQuaternionTest(unittest.TestCase):

    def test__str__(self):
        self.assertEqual(str(OpenMaya.MQuaternion()), "[0.0, 0.0, 0.0, 1.0]")

    def testBnGet(self):
        quaternion = OpenMaya.MQuaternion(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(quaternion.bnGet(), [1.0, 2.0, 3.0, 4.0])


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

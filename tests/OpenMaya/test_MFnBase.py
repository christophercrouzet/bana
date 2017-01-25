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


class MFnBaseTest(unittest.TestCase):

    def testBnObject(self):
        transform = OpenMaya.MFnTransform()
        self.assertIsNone(transform.bnObject())

        transform.create()
        self.assertIsInstance(transform.bnObject(), OpenMaya.MObject)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

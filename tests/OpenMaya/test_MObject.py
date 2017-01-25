#!/usr/bin/env mayapy

import os
import sys
import unittest

import maya.standalone
from maya import OpenMaya, cmds

_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, *((os.pardir,) * 2))))

import bana

import tests._util

bana.initialize()
maya.standalone.initialize()


class MObjectTest(unittest.TestCase):

    def setUp(self):
        OpenMaya.MFileIO.newFile(True)
        context = tests._util.Context()

        master = tests._util.createTransform(context, name='master')

        tests._util.createTransform(context, name='node', parent=master)
        tests._util.createTransform(context, name='awesome_node', parent=master)
        tests._util.createTransform(context, name='node_awesome', parent=master)
        tests._util.createTransform(context, name='n0de', parent=master)

        root1 = tests._util.createTransform(context, name='root_1', parent=master)
        child1 = tests._util.createTransform(context, name='child_1', parent=root1)
        tests._util.createTransform(context, name='node', parent=child1)

        root2 = tests._util.createTransform(context, name='root_2', parent=master)
        child2 = tests._util.createTransform(context, name='child_2', parent=root2)
        grandchild = tests._util.createTransform(context, name='grandchild', parent=child2)
        tests._util.createTransform(context, name='node', parent=grandchild)

        cube, cubeShape = tests._util.createPolyCube(context, name='cube', parent=master)

        intermediary1 = tests._util.createDagNode(context, 'mesh', name='intermediary1', parent=cube)
        context.dg.newPlugValueBool(intermediary1.findPlug('intermediateObject'), True)
        context.dg.connect(cubeShape.findPlug('outMesh'), intermediary1.findPlug('inMesh'))

        intermediary2 = tests._util.createDagNode(context, 'mesh', name='intermediary2', parent=cube)
        context.dg.newPlugValueBool(intermediary2.findPlug('intermediateObject'), True)
        context.dg.connect(cubeShape.findPlug('outMesh'), intermediary2.findPlug('inMesh'))

        template = tests._util.createDagNode(context, 'mesh', name='template', parent=cube)
        context.dg.newPlugValueBool(template.findPlug('template'), True)
        context.dg.connect(cubeShape.findPlug('outMesh'), template.findPlug('inMesh'))

        sphere, sphereShape = tests._util.createNurbsSphere(context, name='sphere', parent=master)
        circle, circleShape = tests._util.createNurbsCircle(context, name='circle', parent=master)

        OpenMaya.MNamespace.addNamespace('awesome')
        light = tests._util.createTransform(context, name='awesome:light', parent=master)
        tests._util.createDagNode(context, 'pointLight', name='awesome:lightShape', parent=light)

        context.dag.doIt()
        context.dg.doIt()

        cmds.projectCurve(circleShape.fullPathName(), sphereShape.fullPathName())

    def test__hash__(self):
        obj1 = OpenMaya.MObject.bnGet(pattern='awesome:light')
        obj2 = OpenMaya.MObject.bnGet(pattern='awesome:light')
        self.assertEqual(hash(obj1), hash(obj2))

    def testBnFind(self):
        objs = list(OpenMaya.MObject.bnFind(pattern='child_*'))
        self.assertEqual(len(objs), 2)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['child_1', 'child_2'])

        objs = list(OpenMaya.MObject.bnFind(pattern='node'))
        self.assertEqual(len(objs), 3)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['node', 'node', 'node'])

        objs = list(OpenMaya.MObject.bnFind(pattern='*node'))
        self.assertEqual(len(objs), 4)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['awesome_node', 'node', 'node', 'node'])

        objs = list(OpenMaya.MObject.bnFind(pattern='node*'))
        self.assertEqual(len(objs), 4)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['node', 'node', 'node', 'node_awesome'])

        objs = list(OpenMaya.MObject.bnFind(pattern='n*de'))
        self.assertEqual(len(objs), 4)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['n0de', 'node', 'node', 'node'])

        objs = list(OpenMaya.MObject.bnFind(pattern='default*Set'))
        self.assertEqual(len(objs), 2)
        self.assertTrue(all(type(obj) is OpenMaya.MObject for obj in objs))
        self.assertEqual(sorted(OpenMaya.MFnDependencyNode(obj).name() for obj in objs), ['defaultLightSet', 'defaultObjectSet'])

    def testBnGet(self):
        self.assertIsNone(OpenMaya.MObject.bnGet(pattern='node'))
        self.assertIsNone(OpenMaya.MObject.bnGet(pattern='child_*'))
        self.assertIsNone(OpenMaya.MObject.bnGet(fnType=OpenMaya.MFn.kMesh))
        obj = OpenMaya.MObject.bnGet(pattern='n0de', fnType=OpenMaya.MFn.kTime)

        obj = OpenMaya.MObject.bnGet(pattern='awesome:light')
        self.assertIsInstance(obj, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(obj).name(), 'awesome:light')

        obj = OpenMaya.MObject.bnGet(pattern='n0de')
        self.assertIsInstance(obj, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(obj).name(), 'n0de')

        obj = OpenMaya.MObject.bnGet(pattern='time1')
        self.assertIsInstance(obj, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(obj).name(), 'time1')

        obj = OpenMaya.MObject.bnGet(fnType=OpenMaya.MFn.kTime)
        self.assertIsInstance(obj, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(obj).name(), 'time1')


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

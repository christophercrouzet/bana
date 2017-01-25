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


class MDagPathTest(unittest.TestCase):

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
        dagPath1 = OpenMaya.MDagPath.bnGet(pattern='|master|node')
        dagPath2 = OpenMaya.MDagPath.bnGet(pattern='|master|node')
        self.assertEqual(hash(dagPath1), hash(dagPath2))

    def test__str__(self):
        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|node')
        self.assertEqual(str(dagPath), '|master|node')

    def testBnFind(self):
        dagPaths = list(OpenMaya.MDagPath.bnFind())
        self.assertEqual(len(dagPaths), 37)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(recursive=False))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|master', '|persp', '|side', '|top'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(traverseUnderWorld=False))
        self.assertEqual(len(dagPaths), 31)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|child_*'))
        self.assertEqual(len(dagPaths), 2)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1', '|master|root_2|child_2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|child_*'))
        self.assertEqual(len(dagPaths), 2)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1', '|master|root_2|child_2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|node'))
        self.assertEqual(len(dagPaths), 3)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.|node'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|*node'))
        self.assertEqual(len(dagPaths), 4)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|node*'))
        self.assertEqual(len(dagPaths), 4)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|n*de'))
        self.assertEqual(len(dagPaths), 4)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(fnType=OpenMaya.MFn.kMesh))
        self.assertEqual(len(dagPaths), 4)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(fnType=OpenMaya.MFn.kNurbsSurface))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|awesome:*'))
        self.assertEqual(len(dagPaths), 2)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|awesome:*|awesome:*'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light|awesome:lightShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|sphereShape->|*'))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='*|sphereShape->*|*Shape*'))
        self.assertEqual(len(dagPaths), 2)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind('*|*Shape*'))
        self.assertEqual(len(dagPaths), 7)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front|frontShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind('*|*:*Shape*'))
        self.assertEqual(len(dagPaths), 8)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front|frontShape', '|master|awesome:light|awesome:lightShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind('*->*|*:*Shape*'))
        self.assertEqual(len(dagPaths), 10)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front|frontShape', '|master|awesome:light|awesome:lightShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.'))
        self.assertEqual(len(dagPaths), 31)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.', recursive=False))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|master', '|persp', '|side', '|top'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.', traverseUnderWorld=False))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|master', '|persp', '|side', '|top'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='+'))
        self.assertEqual(len(dagPaths), 37)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='+', recursive=False))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|master', '|persp', '|side', '|top'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='+', traverseUnderWorld=False))
        self.assertEqual(len(dagPaths), 31)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.|.'))
        self.assertEqual(len(dagPaths), 14)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front|frontShape', '|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.|.', recursive=False))
        self.assertEqual(len(dagPaths), 0)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), [])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='.|.', fnType=OpenMaya.MFn.kShape))
        self.assertEqual(len(dagPaths), 4)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|front|frontShape', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='|master|sphere|sphereShape->*'))
        self.assertEqual(len(dagPaths), 6)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(pattern='|master|sphere|sphereShape->|*'))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(OpenMaya.MDagPath.bnFind(recursive=False, copy=False))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertTrue(all(dagPath is dagPaths[0] for dagPath in dagPaths))

    def testBnGet(self):
        self.assertIsNone(OpenMaya.MDagPath.bnGet(pattern='|node'))
        self.assertIsNone(OpenMaya.MDagPath.bnGet(pattern='*|node'))

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|node')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|master|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|node')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|root_1|child_1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|root_2|child_2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_2|child_2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|root_1|child_1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|root_2|child_2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_2|child_2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|root_1|child_*|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1|node')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|root_2|child_*|*|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_2|child_2|grandchild|node')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|awesome:light')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|awesome:light')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|awesome:light')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|awesome:light')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|*:light')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|awesome:light')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|cube|cubeShape')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|cube|cubeShape')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|cube|intermediary1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|cube|intermediary1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|cube|intermediary2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|cube|intermediary2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|cube|template')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|cube|template')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|projectionCurve1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|*|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|*|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|*|projectionCurve1_Shape1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        dagPath = OpenMaya.MDagPath.bnGet(pattern='*|sphereShape->|*|projectionCurve1_Shape2')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

    def testBnFindChildren(self):
        dpRoot = OpenMaya.MDagPath.bnGet(pattern='|master')

        dagPaths = list(dpRoot.bnFindChildren())
        self.assertEqual(len(dagPaths), 28)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(fnType=OpenMaya.MFn.kPointLight))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light|awesome:lightShape'])

        dagPaths = list(dpRoot.bnFindChildren(recursive=False))
        self.assertEqual(len(dagPaths), 10)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        dagPaths = list(dpRoot.bnFindChildren(traverseUnderWorld=False))
        self.assertEqual(len(dagPaths), 22)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='.'))
        self.assertEqual(len(dagPaths), 22)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='.', traverseUnderWorld=False))
        self.assertEqual(len(dagPaths), 10)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|:.'))
        self.assertEqual(len(dagPaths), 9)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|.:*'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|child_1'))
        self.assertEqual(len(dagPaths), 0)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), [])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*|child_1'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|*|child_1'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|node'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*|node'))
        self.assertEqual(len(dagPaths), 3)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|*|node'))
        self.assertEqual(len(dagPaths), 3)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='..|node'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='|..|node'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|root_1|child_1|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*|node', recursive=False))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|node'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*|awesome:*'))
        self.assertEqual(len(dagPaths), 2)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='+->*'))
        self.assertEqual(len(dagPaths), 6)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='+->+'))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(recursive=False, copy=False))
        self.assertEqual(len(dagPaths), 10)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertTrue(all(dagPath is dagPaths[0] for dagPath in dagPaths))

        # This should work in a normal API! But it's Maya we're talking about.
        # dagPaths = list(dpRoot.bnFindChildren(fnType=OpenMaya.MFn.kUnderWorld))
        # self.assertEqual(len(dagPaths), 1)
        # self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        # self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->'])

        dpRoot = OpenMaya.MDagPath.bnGet(pattern='|master|sphere|sphereShape')

        dagPaths = list(dpRoot.bnFindChildren())
        self.assertEqual(len(dagPaths), 6)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(recursive=False))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*'))
        self.assertEqual(len(dagPaths), 6)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='->'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='*->'))
        self.assertEqual(len(dagPaths), 1)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='->*'))
        self.assertEqual(len(dagPaths), 6)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        dagPaths = list(dpRoot.bnFindChildren(pattern='->.'))
        self.assertEqual(len(dagPaths), 5)
        self.assertTrue(all(type(dagPath) is OpenMaya.MDagPath for dagPath in dagPaths))
        self.assertEqual(sorted(dagPath.fullPathName() for dagPath in dagPaths), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

    def testBnGetChild(self):
        dpRoot = OpenMaya.MDagPath.bnGet(pattern='|master')

        self.assertIsNone(dpRoot.bnGetChild())
        self.assertIsNone(dpRoot.bnGetChild(recursive=False))
        self.assertIsNone(dpRoot.bnGetChild(traverseUnderWorld=False))
        self.assertIsNone(dpRoot.bnGetChild(pattern='.'))

        dagPath = dpRoot.bnGetChild(fnType=OpenMaya.MFn.kPointLight)
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|awesome:light|awesome:lightShape')

        dagPath = dpRoot.bnGetChild(pattern='|.:*')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|awesome:light')

        dagPath = dpRoot.bnGetChild(pattern='*|child_1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1')

        dagPath = dpRoot.bnGetChild(pattern='|*|child_1')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1')

        dagPath = dpRoot.bnGetChild(pattern='|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|node')

        dagPath = dpRoot.bnGetChild(pattern='..|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1|node')

        dagPath = dpRoot.bnGetChild(pattern='|..|node')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|root_1|child_1|node')

        dagPath = dpRoot.bnGetChild(pattern='*|node', recursive=False)
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|node')

        dpRoot = OpenMaya.MDagPath.bnGet(pattern='|master|sphere|sphereShape')

        self.assertIsNone(dpRoot.bnGetChild())

        dagPath = dpRoot.bnGetChild(recursive=False)
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->')

        dagPath = dpRoot.bnGetChild(pattern='->')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->')

        dagPath = dpRoot.bnGetChild(pattern='*->')
        self.assertIsInstance(dagPath, OpenMaya.MDagPath)
        self.assertEqual(dagPath.fullPathName(), '|master|sphere|sphereShape->')

    def testBnGetParent(self):
        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master')
        self.assertIsNone(dagPath.bnGetParent())

        dagPath = OpenMaya.MDagPath.bnGet(pattern='|master|node')
        dpParent = dagPath.bnGetParent()
        self.assertIsNot(dpParent, dagPath)
        self.assertEqual(dpParent, OpenMaya.MDagPath.bnGet(pattern='|master'))


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

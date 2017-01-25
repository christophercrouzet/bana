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


class MDagNodeTest(unittest.TestCase):

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

    def test__str__(self):
        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|node')
        self.assertEqual(str(node), '|master|node')

    def testBnFind(self):
        nodes = list(OpenMaya.MFnDagNode.bnFind())
        self.assertEqual(len(nodes), 37)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(recursive=False))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|master', '|persp', '|side', '|top'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(traverseUnderWorld=False))
        self.assertEqual(len(nodes), 31)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|child_*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1', '|master|root_2|child_2'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|child_*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1', '|master|root_2|child_2'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|node'))
        self.assertEqual(len(nodes), 3)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.|node'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|*node'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|node*'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|n*de'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(OpenMaya.MFnMesh.bnFind())
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnMesh for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template'])

        nodes = list(OpenMaya.MFnNurbsSurface.bnFind())
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnNurbsSurface for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|awesome:*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|awesome:*|awesome:*'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light|awesome:lightShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|sphereShape->|*'))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='*|sphereShape->*|*Shape*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(OpenMaya.MFnDagNode.bnFind('*|*Shape*'))
        self.assertEqual(len(nodes), 7)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front|frontShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind('*|*:*Shape*'))
        self.assertEqual(len(nodes), 8)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front|frontShape', '|master|awesome:light|awesome:lightShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind('*->*|*:*Shape*'))
        self.assertEqual(len(nodes), 10)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front|frontShape', '|master|awesome:light|awesome:lightShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.'))
        self.assertEqual(len(nodes), 31)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.', recursive=False))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|master', '|persp', '|side', '|top'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.', traverseUnderWorld=False))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|master', '|persp', '|side', '|top'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='+'))
        self.assertEqual(len(nodes), 37)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='+', recursive=False))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|master', '|persp', '|side', '|top'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='+', traverseUnderWorld=False))
        self.assertEqual(len(nodes), 31)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front', '|front|frontShape', '|master', '|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.|.'))
        self.assertEqual(len(nodes), 14)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|front|frontShape', '|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere', '|persp|perspShape', '|side|sideShape', '|top|topShape'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='.|.', recursive=False))
        self.assertEqual(len(nodes), 0)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), [])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='|master|sphere|sphereShape->*'))
        self.assertEqual(len(nodes), 6)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(OpenMaya.MFnDagNode.bnFind(pattern='|master|sphere|sphereShape->|*'))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

    def testBnGet(self):
        self.assertIsNone(OpenMaya.MFnDagNode.bnGet(pattern='|node'))
        self.assertIsNone(OpenMaya.MFnDagNode.bnGet(pattern='*|node'))

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|node')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|master|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|node')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|root_1|child_*|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|root_2|child_*|*|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2|grandchild|node')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|awesome:light')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|awesome:light')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|*:light')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|cube|cubeShape')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|cube|cubeShape')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|cube|intermediary1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|cube|intermediary1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|cube|intermediary2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|cube|intermediary2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|cube|template')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|cube|template')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|*|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|*|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|*|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')

        node = OpenMaya.MFnDagNode.bnGet(pattern='*|sphereShape->|*|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')

    def testBnFindChildren(self):
        root = OpenMaya.MFnDagNode.bnGet(pattern='|master')

        nodes = list(root.bnFindChildren())
        self.assertEqual(len(nodes), 28)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(root.bnFindChildren(fnType=OpenMaya.MFn.kPointLight))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light|awesome:lightShape'])

        nodes = list(root.bnFindChildren(recursive=False))
        self.assertEqual(len(nodes), 10)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        nodes = list(root.bnFindChildren(traverseUnderWorld=False))
        self.assertEqual(len(nodes), 22)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape'])

        nodes = list(root.bnFindChildren(pattern='.'))
        self.assertEqual(len(nodes), 22)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|cube|intermediary1', '|master|cube|intermediary2', '|master|cube|template', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape'])

        nodes = list(root.bnFindChildren(pattern='.', traverseUnderWorld=False))
        self.assertEqual(len(nodes), 10)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        nodes = list(root.bnFindChildren(pattern='|:.'))
        self.assertEqual(len(nodes), 9)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_2', '|master|sphere'])

        nodes = list(root.bnFindChildren(pattern='|.:*'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light'])

        nodes = list(root.bnFindChildren(pattern='|child_1'))
        self.assertEqual(len(nodes), 0)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), [])

        nodes = list(root.bnFindChildren(pattern='*|child_1'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1'])

        nodes = list(root.bnFindChildren(pattern='|*|child_1'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1'])

        nodes = list(root.bnFindChildren(pattern='|node'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node'])

        nodes = list(root.bnFindChildren(pattern='*|node'))
        self.assertEqual(len(nodes), 3)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(root.bnFindChildren(pattern='|*|node'))
        self.assertEqual(len(nodes), 3)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])

        nodes = list(root.bnFindChildren(pattern='..|node'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1|node'])

        nodes = list(root.bnFindChildren(pattern='|..|node'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|root_1|child_1|node'])

        nodes = list(root.bnFindChildren(pattern='*|node', recursive=False))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|node'])

        nodes = list(root.bnFindChildren(pattern='*|awesome:*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape'])

        nodes = list(root.bnFindChildren(pattern='+->*'))
        self.assertEqual(len(nodes), 6)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(root.bnFindChildren(pattern='+->+'))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        # This should work in a normal API! But it's Maya we're talking about.
        # nodes = list(root.bnFindChildren(fnType=OpenMaya.MFn.kUnderWorld))
        # self.assertEqual(len(nodes), 1)
        # self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        # self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->'])

        root = OpenMaya.MFnDagNode.bnGet(pattern='|master|sphere|sphereShape')

        nodes = list(root.bnFindChildren())
        self.assertEqual(len(nodes), 6)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(root.bnFindChildren(recursive=False))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->'])

        nodes = list(root.bnFindChildren(pattern='*'))
        self.assertEqual(len(nodes), 6)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(root.bnFindChildren(pattern='->'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->'])

        nodes = list(root.bnFindChildren(pattern='*->'))
        self.assertEqual(len(nodes), 1)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->'])

        nodes = list(root.bnFindChildren(pattern='->*'))
        self.assertEqual(len(nodes), 6)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->', '|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

        nodes = list(root.bnFindChildren(pattern='->.'))
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(type(node) is OpenMaya.MFnDagNode for node in nodes))
        self.assertEqual(sorted(node.fullPathName() for node in nodes), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])

    def testBnGetChild(self):
        root = OpenMaya.MFnDagNode.bnGet(pattern='|master')

        self.assertIsNone(root.bnGetChild())
        self.assertIsNone(root.bnGetChild(recursive=False))
        self.assertIsNone(root.bnGetChild(traverseUnderWorld=False))
        self.assertIsNone(root.bnGetChild(pattern='.'))

        node = root.bnGetChild(fnType=OpenMaya.MFn.kPointLight)
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|awesome:light|awesome:lightShape')

        node = root.bnGetChild(pattern='|.:*')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')

        node = root.bnGetChild(pattern='*|child_1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')

        node = root.bnGetChild(pattern='|*|child_1')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')

        node = root.bnGetChild(pattern='|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|node')

        node = root.bnGetChild(pattern='..|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')

        node = root.bnGetChild(pattern='|..|node')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')

        node = root.bnGetChild(pattern='*|node', recursive=False)
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|node')

        root = OpenMaya.MFnDagNode.bnGet(pattern='|master|sphere|sphereShape')

        self.assertIsNone(root.bnGetChild())

        node = root.bnGetChild(recursive=False)
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->')

        node = root.bnGetChild(pattern='->')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->')

        node = root.bnGetChild(pattern='*->')
        self.assertIsInstance(node, OpenMaya.MFnDagNode)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->')


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

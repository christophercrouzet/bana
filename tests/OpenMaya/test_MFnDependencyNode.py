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


def _nodeCount():
    count = 0
    iterator = OpenMaya.MItDependencyNodes()
    while not iterator.isDone():
        count += 1
        iterator.next()

    return count


class MFnDependencyNodeTest(unittest.TestCase):

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
        node1 = OpenMaya.MFnDependencyNode.bnGet(pattern='awesome:light')
        node2 = OpenMaya.MFnDependencyNode.bnGet(pattern='awesome:light')
        self.assertEqual(hash(node1), hash(node2))

    def test__str__(self):
        node = OpenMaya.MFnDependencyNode.bnGet(pattern='awesome:light')
        self.assertEqual(str(node), 'awesome:light')

    def testBnFind(self):
        nodes = list(OpenMaya.MFnDependencyNode.bnFind())
        self.assertEqual(len(nodes), _nodeCount())
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='child_*'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['child_1', 'child_2'])

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='node'))
        self.assertEqual(len(nodes), 3)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['node', 'node', 'node'])

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='*node'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['awesome_node', 'node', 'node', 'node'])

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='node*'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['node', 'node', 'node', 'node_awesome'])

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='n*de'))
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['n0de', 'node', 'node', 'node'])

        nodes = list(OpenMaya.MFnDependencyNode.bnFind(pattern='default*Set'))
        self.assertEqual(len(nodes), 2)
        self.assertTrue(all(type(node) is OpenMaya.MFnDependencyNode for node in nodes))
        self.assertEqual(sorted(node.name() for node in nodes), ['defaultLightSet', 'defaultObjectSet'])

    def testBnGet(self):
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnGet(pattern='node'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnGet(pattern='child_*'))

        node = OpenMaya.MFnDependencyNode.bnGet(pattern='awesome:light')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'awesome:light')

        node = OpenMaya.MFnDependencyNode.bnGet(pattern='n0de')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'n0de')

        node = OpenMaya.MFnDependencyNode.bnGet(pattern='time1')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'time1')


if __name__ == '__main__':
    from tests.run import run
    run('__main__')

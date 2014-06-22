import unittest

import banana.maya
import maya.standalone
from maya import OpenMaya, cmds


maya.standalone.initialize()
banana.maya.patch()


class MFnTransformTest(unittest.TestCase):
    
    def setUp(self):
        OpenMaya.MFileIO.newFile(True)
        master = cmds.group(name='master', empty=True)
        for i in (1, 2):
            root = cmds.group(name='root_%d' % i, parent=master, empty=True)
            child = cmds.group(name='child_%d' % i, parent=root, empty=True)
            node = cmds.group(name='node', parent=child, empty=True)
        
        cmds.group('|master|root_2|child_2|node', name='grandchild', parent='|master|root_2|child_2')
        cmds.group(name='node', parent='|master', empty=True)
        cmds.group(name='awesome_node', parent='|master', empty=True)
        cmds.group(name='node_awesome', parent='|master', empty=True)
        cmds.group(name='n0de', parent='|master', empty=True)
        cmds.polyCube(name='cube')
        cmds.parent('cube', '|master')
        cmds.sphere(name='sphere')
        cmds.parent('sphere', '|master')
        cmds.circle(name='circle')
        cmds.parent('|circle', '|master')
        cmds.projectCurve('|master|circle', '|master|sphere')
        cmds.namespace(add='awesome')
        cmds.pointLight(name='awesome:light')
        cmds.parent('|awesome:light', '|master')
    
    def test_bnn_get_1(self):
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('node'))
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('|node'))
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('*|node'))
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('*node'))
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('node*'))
        self.assertIsNone(OpenMaya.MFnTransform.bnn_get('n*de'))
    
    def test_bnn_get_2(self):
        node = OpenMaya.MFnTransform.bnn_get('|master|node')
        self.assertIsInstance(node, OpenMaya.MFnTransform)
        self.assertEqual(node.fullPathName(), '|master|node')
        
        node = OpenMaya.MFnTransform.bnn_get('*|master|node')
        self.assertIsInstance(node, OpenMaya.MFnTransform)
        self.assertEqual(node.fullPathName(), '|master|node')
        
        node = OpenMaya.MFnTransform.bnn_get('master|node')
        self.assertIsInstance(node, OpenMaya.MFnTransform)
        self.assertEqual(node.fullPathName(), '|master|node')
        
    def test_bnn_get_3(self):
        child = OpenMaya.MFnTransform.bnn_get('|master|root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_1|child_1')
        
        child = OpenMaya.MFnTransform.bnn_get('|master|root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_2|child_2')
    
        child = OpenMaya.MFnTransform.bnn_get('*|root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_1|child_1')
        
        child = OpenMaya.MFnTransform.bnn_get('*|root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_2|child_2')
    
        child = OpenMaya.MFnTransform.bnn_get('root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_1|child_1')
        
        child = OpenMaya.MFnTransform.bnn_get('root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnTransform)
        self.assertEqual(child.fullPathName(), '|master|root_2|child_2')
    
    def test_bnn_get_4(self):
        node = OpenMaya.MFnTransform.bnn_get('|master|root_1|child_*|node')
        self.assertIsInstance(node, OpenMaya.MFnTransform)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')
        
        node = OpenMaya.MFnTransform.bnn_get('|master|root_2|child_*|*|node')
        self.assertIsInstance(node, OpenMaya.MFnTransform)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2|grandchild|node')
    
    def test_bnn_find_1(self):
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='*|child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
    def test_bnn_find_2(self):
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='*|node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='*node')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='node*')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MFnTransform.bnn_find(pattern='n*de')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
    def test_bnn_find_3(self):
        nodes = OpenMaya.MFnTransform.bnn_find()
        self.assertEqual(len(nodes), 21)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnTransform)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|front', '|master', '|master|awesome_node', '|master|circle', '|master|cube', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|persp', '|side', '|top'])


if __name__ == '__main__':
    unittest.main()

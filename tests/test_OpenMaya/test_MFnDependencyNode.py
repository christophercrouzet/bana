import unittest

import banana.maya
import maya.standalone
from maya import OpenMaya, cmds


maya.standalone.initialize()
banana.maya.patch()


class MFnDependencyNodeTest(unittest.TestCase):
    
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
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('node'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('|node'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('*|node'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('*node'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('node*'))
        self.assertIsNone(OpenMaya.MFnDependencyNode.bnn_get('n*de'))
    
    def test_bnn_get_2(self):
        node = OpenMaya.MFnDependencyNode.bnn_get('|master|node')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'node')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('*|master|node')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'node')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('master|node')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'node')
        
    def test_bnn_get_3(self):
        child = OpenMaya.MFnDependencyNode.bnn_get('|master|root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_1')
        
        child = OpenMaya.MFnDependencyNode.bnn_get('|master|root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_2')
    
        child = OpenMaya.MFnDependencyNode.bnn_get('*|root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_1')
        
        child = OpenMaya.MFnDependencyNode.bnn_get('*|root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_2')
    
        child = OpenMaya.MFnDependencyNode.bnn_get('root_1|child_1')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_1')
        
        child = OpenMaya.MFnDependencyNode.bnn_get('root_2|child_2')
        self.assertIsInstance(child, OpenMaya.MFnDependencyNode)
        self.assertEqual(child.name(), 'child_2')
    
    def test_bnn_get_4(self):
        node = OpenMaya.MFnDependencyNode.bnn_get('|master|root_1|child_*|node')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'node')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('|master|root_2|child_*|*|node')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'node')
    
    def test_bnn_get_5(self):
        node = OpenMaya.MFnDependencyNode.bnn_get('time1')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'time1')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('*time1')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'time1')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('time1*')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'time1')
        
        node = OpenMaya.MFnDependencyNode.bnn_get('time*')
        self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        self.assertEqual(node.name(), 'time1')
    
    def test_bnn_find_1(self):
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['child_1', 'child_2'])
    
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='*|child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['child_1', 'child_2'])
    
    def test_bnn_find_2(self):
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['node', 'node', 'node'])
    
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='*|node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['node', 'node', 'node'])
    
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='*node')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['awesome_node', 'node', 'node', 'node'])
        
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='node*')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['node', 'node', 'node', 'node_awesome'])
        
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='n*de')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['n0de', 'node', 'node', 'node'])
    
    def test_bnn_find_3(self):
        selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName('*', selection)
        
        nodes = OpenMaya.MFnDependencyNode.bnn_find()
        self.assertEqual(len(nodes), selection.length())
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
    
    def test_bnn_find_4(self):
        nodes = OpenMaya.MFnDependencyNode.bnn_find(pattern='default*Set')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MFnDependencyNode)
        names = [node.name() for node in nodes]
        self.assertEqual(sorted(names), ['defaultLightSet', 'defaultObjectSet'])


if __name__ == '__main__':
    unittest.main()

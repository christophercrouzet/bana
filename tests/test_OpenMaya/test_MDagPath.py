import unittest

import banana.maya
import maya.standalone
from maya import OpenMaya, cmds


maya.standalone.initialize()
banana.maya.patch()


class MDagPathTest(unittest.TestCase):
    
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
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('node'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('|node'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('*|node'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('*node'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('node*'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('n*de'))
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('time1'))
    
    def test_bnn_get_2(self):
        node = OpenMaya.MDagPath.bnn_get('|master|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|node')
        
        node = OpenMaya.MDagPath.bnn_get('*|master|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|node')
        
        node = OpenMaya.MDagPath.bnn_get('master|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|node')
        
    def test_bnn_get_3(self):
        node = OpenMaya.MDagPath.bnn_get('|master|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MDagPath.bnn_get('|master|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2')
    
        node = OpenMaya.MDagPath.bnn_get('*|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MDagPath.bnn_get('*|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2')
    
        node = OpenMaya.MDagPath.bnn_get('root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MDagPath.bnn_get('root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2')
    
    def test_bnn_get_4(self):
        node = OpenMaya.MDagPath.bnn_get('|master|root_1|child_*|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')
        
        node = OpenMaya.MDagPath.bnn_get('|master|root_2|child_*|*|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2|grandchild|node')
    
    def test_bnn_get_5(self):
        node = OpenMaya.MDagPath.bnn_get('|master|awesome:light')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MDagPath.bnn_get('*|awesome:light')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MDagPath.bnn_get('awesome:light')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MDagPath.bnn_get('*:light')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')
    
    def test_bnn_get_6(self):
        node = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')
        
        node = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MDagPath.bnn_get('*|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')
        
        node = OpenMaya.MDagPath.bnn_get('*|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MDagPath.bnn_get('*|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MDagPath.bnn_get('sphereShape->|*|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MDagPath.bnn_get('sphereShape->|*|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MDagPath.bnn_get('sphereShape->|*|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MDagPath.bnn_get('sphereShape->|*|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
    
    def test_bnn_find_1(self):
        nodes = OpenMaya.MDagPath.bnn_find(pattern='child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
    def test_bnn_find_2(self):
        nodes = OpenMaya.MDagPath.bnn_find(pattern='node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*node')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MDagPath.bnn_find(pattern='node*')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MDagPath.bnn_find(pattern='n*de')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
    def test_bnn_find_3(self):
        nodes = OpenMaya.MDagPath.bnn_find()
        self.assertEqual(len(nodes), 30)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|front', '|front|frontShape', '|master', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2', '|persp', '|persp|perspShape', '|side', '|side|sideShape', '|top', '|top|topShape'])
    
    def test_bnn_find_4(self):
        nodes = OpenMaya.MDagPath.bnn_find(types=OpenMaya.MFn.kMesh)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
    
        nodes = OpenMaya.MDagPath.bnn_find(types=OpenMaya.MFn.kNurbsSurface)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape'])
    
        nodes = OpenMaya.MDagPath.bnn_find(types=[OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface])
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape', '|master|sphere|sphereShape'])
    
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|cube*', types=[OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface])
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
    
    def test_bnn_find_5(self):
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|awesome:*')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light'])
    
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|awesome:*|awesome:*')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light|awesome:lightShape'])
    
    def test_bnn_find_6(self):
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|sphereShape->|*')
        self.assertEqual(len(nodes), 5)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
        
        nodes = OpenMaya.MDagPath.bnn_find(pattern='*|sphereShape->|*Shape*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
    
    def test_bnn_asFunctionSet(self):
        node = OpenMaya.MDagPath.bnn_get(pattern='master')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnTransform)
        self.assertEqual(functionSet.fullPathName(), '|master')
        
        node = OpenMaya.MDagPath.bnn_get(pattern='cubeShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnMesh)
        self.assertEqual(functionSet.fullPathName(), '|master|cube|cubeShape')
        
        node = OpenMaya.MDagPath.bnn_get(pattern='sphereShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnNurbsSurface)
        self.assertEqual(functionSet.fullPathName(), '|master|sphere|sphereShape')
        
        node = OpenMaya.MDagPath.bnn_get(pattern='circleShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnNurbsCurve)
        self.assertEqual(functionSet.fullPathName(), '|master|circle|circleShape')
        
        node = OpenMaya.MDagPath.bnn_get(pattern='awesome:lightShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnPointLight)
        self.assertEqual(functionSet.fullPathName(), '|master|awesome:light|awesome:lightShape')
    
    def test_bnn_findChild_1(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        self.assertIsNone(master.bnn_findChild(pattern=''))
        self.assertIsNone(master.bnn_findChild(pattern='|node'))
        self.assertIsNone(master.bnn_findChild(pattern='*node'))
        self.assertIsNone(master.bnn_findChild(pattern='node*'))
        self.assertIsNone(master.bnn_findChild(pattern='child_1'))
        self.assertIsNone(master.bnn_findChild(pattern='child_2'))
        self.assertIsNone(master.bnn_findChild(types=[OpenMaya.MFn.kNurbsSurface]))
        self.assertIsNone(master.bnn_findChild(types=[OpenMaya.MFn.kMesh]))
    
    def test_bnn_findChild_2(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        node = master.bnn_findChild(pattern='*|node')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|node')
    
    def test_bnn_findChild_3(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        root = master.bnn_findChild(pattern='root_1')
        self.assertIsInstance(root, OpenMaya.MDagPath)
        self.assertEqual(root.fullPathName(), '|master|root_1')
        
        root = master.bnn_findChild(pattern='root_2')
        self.assertIsInstance(root, OpenMaya.MDagPath)
        self.assertEqual(root.fullPathName(), '|master|root_2')
        
        root = master.bnn_findChild(pattern='*|root_1')
        self.assertIsInstance(root, OpenMaya.MDagPath)
        self.assertEqual(root.fullPathName(), '|master|root_1')
        
        root = master.bnn_findChild(pattern='*|root_2')
        self.assertIsInstance(root, OpenMaya.MDagPath)
        self.assertEqual(root.fullPathName(), '|master|root_2')
    
    def test_bnn_findChild_4(self):
        root = OpenMaya.MDagPath.bnn_get('|master|root_1')
        self.assertIsNone(root.bnn_findChild(pattern='node'))
        node = root.bnn_findChild(pattern='node', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')
        
        root = OpenMaya.MDagPath.bnn_get('|master|root_2')
        self.assertIsNone(root.bnn_findChild(pattern='node'))
        node = root.bnn_findChild(pattern='node', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2|grandchild|node')
    
        root = OpenMaya.MDagPath.bnn_get('|master|root_1')
        self.assertIsNone(root.bnn_findChild(pattern='*|node'))
        node = root.bnn_findChild(pattern='*|node', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_1|child_1|node')
        
        root = OpenMaya.MDagPath.bnn_get('|master|root_2')
        self.assertIsNone(root.bnn_findChild(pattern='*|node'))
        node = root.bnn_findChild(pattern='*|node', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|root_2|child_2|grandchild|node')
    
    def test_bnn_findChild_5(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        node = master.bnn_findChild(types=[OpenMaya.MFn.kMesh], recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|cube|cubeShape')
        
        node = master.bnn_findChild(types=[OpenMaya.MFn.kNurbsSurface], recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape')
        
        node = master.bnn_findChild(types=[OpenMaya.MFn.kPointLight], recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light|awesome:lightShape')
    
    def test_bnn_findChild_6(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        node = master.bnn_findChild(pattern='awesome:*')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|awesome:light')
    
    def test_bnn_findChild_7(self):
        underworld = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1')
        
        node = underworld.bnn_findChild(pattern='projectionCurve1_1')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1')
        
        node = underworld.bnn_findChild(pattern='projectionCurve1_2')
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2')
        
        node = underworld.bnn_findChild(pattern='projectionCurve1_Shape1', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = underworld.bnn_findChild(pattern='projectionCurve1_Shape2', recursive=True)
        self.assertIsInstance(node, OpenMaya.MDagPath)
        self.assertEqual(node.fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
    
    def test_bnn_findChildren_1(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        self.assertEqual(master.bnn_findChildren(pattern='child_1'), [])
        self.assertEqual(master.bnn_findChildren(pattern='child_2'), [])
    
    def test_bnn_findChildren_2(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        nodes = master.bnn_findChildren(pattern='node')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node'])
        
        nodes = master.bnn_findChildren(pattern='*|node')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node'])
        
        nodes = master.bnn_findChildren(pattern='*node')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome_node', '|master|node'])
        
        nodes = master.bnn_findChildren(pattern='node*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|node_awesome'])
        
        nodes = master.bnn_findChildren(pattern='n*de')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|n0de', '|master|node'])
    
    def test_bnn_findChildren_3(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        nodes = master.bnn_findChildren(pattern='node', recursive=True)
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = master.bnn_findChildren(pattern='*|node', recursive=True)
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = master.bnn_findChildren(pattern='*node', recursive=True)
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = master.bnn_findChildren(pattern='node*', recursive=True)
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = master.bnn_findChildren(pattern='n*de', recursive=True)
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
    def test_bnn_findChildren_4(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        nodes = master.bnn_findChildren(recursive=True)
        self.assertEqual(len(nodes), 19)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape', '|master|awesome_node', '|master|circle', '|master|circle|circleShape', '|master|cube', '|master|cube|cubeShape', '|master|n0de', '|master|node', '|master|node_awesome', '|master|root_1', '|master|root_1|child_1', '|master|root_1|child_1|node', '|master|root_2', '|master|root_2|child_2', '|master|root_2|child_2|grandchild', '|master|root_2|child_2|grandchild|node', '|master|sphere', '|master|sphere|sphereShape'])
    
    def test_bnn_findChildren_5(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        nodes = master.bnn_findChildren(types=OpenMaya.MFn.kMesh, recursive=True)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
        
        nodes = master.bnn_findChildren(types=OpenMaya.MFn.kNurbsSurface, recursive=True)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape'])
        
        nodes = master.bnn_findChildren(types=[OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface], recursive=True)
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape', '|master|sphere|sphereShape'])
        
        nodes = master.bnn_findChildren(types=OpenMaya.MFn.kPointLight, recursive=True)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light|awesome:lightShape'])
    
    def test_bnn_findChildren_6(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        nodes = master.bnn_findChildren(pattern='awesome:*', recursive=True)
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light', '|master|awesome:light|awesome:lightShape'])
    
    def test_bnn_findChildren_7(self):
        underworld = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1')
        nodes = underworld.bnn_findChildren(pattern='*Shape*', recursive=True)
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MDagPath)
        names = [node.fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
    
    def test_bnn_findShape_1(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        self.assertIsNone(master.bnn_findShape(pattern=''))
        self.assertIsNone(master.bnn_findShape(pattern='', recursive=True))
    
    def test_bnn_findShape_2(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        shape = master.bnn_findShape(pattern='*|cubeShape', recursive=True)
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|cube|cubeShape')
        
        shape = master.bnn_findShape(pattern='*|sphereShape', recursive=True)
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|sphere|sphereShape')
        
        shape = master.bnn_findShape(pattern='cubeShape', recursive=True)
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|cube|cubeShape')
        
        shape = master.bnn_findShape(pattern='sphereShape', recursive=True)
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|sphere|sphereShape')
    
    def test_bnn_findShape_3(self):
        node = OpenMaya.MDagPath.bnn_get('|master|cube')
        shape = node.bnn_findShape()
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|cube|cubeShape')
        
        node = OpenMaya.MDagPath.bnn_get('|master|sphere')
        shape = node.bnn_findShape()
        self.assertIsInstance(shape, OpenMaya.MDagPath)
        self.assertEqual(shape.fullPathName(), '|master|sphere|sphereShape')
    
    def test_bnn_findShapes_1(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        self.assertEqual(master.bnn_findShapes(), [])
    
    def test_bnn_findShapes_2(self):
        master = OpenMaya.MDagPath.bnn_get('|master')
        
        shapes = master.bnn_findShapes(recursive=True)
        self.assertEqual(len(shapes), 4)
        for shape in shapes:
            self.assertIsInstance(shape, OpenMaya.MDagPath)
        names = [shape.fullPathName() for shape in shapes]
        self.assertEqual(sorted(names), ['|master|awesome:light|awesome:lightShape', '|master|circle|circleShape', '|master|cube|cubeShape', '|master|sphere|sphereShape'])
    
    def test_bnn_findShapes_3(self):
        node = OpenMaya.MDagPath.bnn_get('|master|cube')
        shapes = node.bnn_findShapes()
        self.assertEqual(len(shapes), 1)
        for shape in shapes:
            self.assertIsInstance(shape, OpenMaya.MDagPath)
        names = [shape.fullPathName() for shape in shapes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
        
        node = OpenMaya.MDagPath.bnn_get('|master|sphere')
        shapes = node.bnn_findShapes()
        self.assertEqual(len(shapes), 1)
        for shape in shapes:
            self.assertIsInstance(shape, OpenMaya.MDagPath)
        names = [shape.fullPathName() for shape in shapes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape'])
        
        node = OpenMaya.MDagPath.bnn_get('|master|awesome:light')
        shapes = node.bnn_findShapes()
        self.assertEqual(len(shapes), 1)
        for shape in shapes:
            self.assertIsInstance(shape, OpenMaya.MDagPath)
        names = [shape.fullPathName() for shape in shapes]
        self.assertEqual(sorted(names), ['|master|awesome:light|awesome:lightShape'])
    
    def test_bnn_findShapes_4(self):
        underworld = OpenMaya.MDagPath.bnn_get('|master|sphere|sphereShape->|projectionCurve1')
        shapes = underworld.bnn_findShapes(recursive=True)
        self.assertEqual(len(shapes), 2)
        for shape in shapes:
            self.assertIsInstance(shape, OpenMaya.MDagPath)
        names = [shape.fullPathName() for shape in shapes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
    
    def test_bnn_parent(self):
        self.assertIsNone(OpenMaya.MDagPath.bnn_get('|master').bnn_parent())
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|node').bnn_parent().fullPathName(), '|master')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_1').bnn_parent().fullPathName(), '|master')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_1|child_1').bnn_parent().fullPathName(), '|master|root_1')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_1|child_1|node').bnn_parent().fullPathName(), '|master|root_1|child_1')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_2').bnn_parent().fullPathName(), '|master')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_2|child_2').bnn_parent().fullPathName(), '|master|root_2')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_2|child_2|grandchild').bnn_parent().fullPathName(), '|master|root_2|child_2')
        self.assertEqual(OpenMaya.MDagPath.bnn_get('|master|root_2|child_2|grandchild|node').bnn_parent().fullPathName(), '|master|root_2|child_2|grandchild')


if __name__ == '__main__':
    unittest.main()

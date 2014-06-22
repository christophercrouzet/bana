import unittest

import banana.maya
import maya.standalone
from maya import OpenMaya, cmds


maya.standalone.initialize()
banana.maya.patch()


class MObjectTest(unittest.TestCase):
    
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
        self.assertIsNone(OpenMaya.MObject.bnn_get('node'))
        self.assertIsNone(OpenMaya.MObject.bnn_get('|node'))
        self.assertIsNone(OpenMaya.MObject.bnn_get('*|node'))
        self.assertIsNone(OpenMaya.MObject.bnn_get('*node'))
        self.assertIsNone(OpenMaya.MObject.bnn_get('node*'))
        self.assertIsNone(OpenMaya.MObject.bnn_get('n*de'))
    
    def test_bnn_get_2(self):
        node = OpenMaya.MObject.bnn_get('|master|node')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|node')
        
        node = OpenMaya.MObject.bnn_get('*|master|node')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|node')
        
        node = OpenMaya.MObject.bnn_get('master|node')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|node')
        
    def test_bnn_get_3(self):
        node = OpenMaya.MObject.bnn_get('|master|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MObject.bnn_get('|master|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_2|child_2')
    
        node = OpenMaya.MObject.bnn_get('*|root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MObject.bnn_get('*|root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_2|child_2')
    
        node = OpenMaya.MObject.bnn_get('root_1|child_1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_1|child_1')
        
        node = OpenMaya.MObject.bnn_get('root_2|child_2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_2|child_2')
    
    def test_bnn_get_4(self):
        node = OpenMaya.MObject.bnn_get('|master|root_1|child_*|node')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_1|child_1|node')
        
        node = OpenMaya.MObject.bnn_get('|master|root_2|child_*|*|node')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|root_2|child_2|grandchild|node')
    
    def test_bnn_get_5(self):
        node = OpenMaya.MObject.bnn_get('|master|awesome:light')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MObject.bnn_get('*|awesome:light')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MObject.bnn_get('awesome:light')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|awesome:light')
        
        node = OpenMaya.MObject.bnn_get('*:light')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|awesome:light')
    
    def test_bnn_get_6(self):
        node = OpenMaya.MObject.bnn_get('|master|sphere|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')
        
        node = OpenMaya.MObject.bnn_get('|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MObject.bnn_get('|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MObject.bnn_get('*|sphereShape->|projectionCurve1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1')
        
        node = OpenMaya.MObject.bnn_get('*|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MObject.bnn_get('*|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MObject.bnn_get('sphereShape->|*|projectionCurve1_1|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MObject.bnn_get('sphereShape->|*|projectionCurve1_2|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
        
        node = OpenMaya.MObject.bnn_get('sphereShape->|*|projectionCurve1_Shape1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1')
        
        node = OpenMaya.MObject.bnn_get('sphereShape->|*|projectionCurve1_Shape2')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDagNode(node).fullPathName(), '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2')
    
    def test_bnn_get_7(self):
        node = OpenMaya.MObject.bnn_get('time1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(node).name(), 'time1')
        
        node = OpenMaya.MObject.bnn_get('*time1')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(node).name(), 'time1')
        
        node = OpenMaya.MObject.bnn_get('time1*')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(node).name(), 'time1')
        
        node = OpenMaya.MObject.bnn_get('time*')
        self.assertIsInstance(node, OpenMaya.MObject)
        self.assertEqual(OpenMaya.MFnDependencyNode(node).name(), 'time1')
    
    def test_bnn_find_1(self):
        nodes = OpenMaya.MObject.bnn_find(pattern='child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
        nodes = OpenMaya.MObject.bnn_find(pattern='*|child_*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|root_1|child_1', '|master|root_2|child_2'])
    
    def test_bnn_find_2(self):
        nodes = OpenMaya.MObject.bnn_find(pattern='node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MObject.bnn_find(pattern='*|node')
        self.assertEqual(len(nodes), 3)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
        nodes = OpenMaya.MObject.bnn_find(pattern='*node')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome_node', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MObject.bnn_find(pattern='node*')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|node', '|master|node_awesome', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
        
        nodes = OpenMaya.MObject.bnn_find(pattern='n*de')
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|n0de', '|master|node', '|master|root_1|child_1|node', '|master|root_2|child_2|grandchild|node'])
    
    def test_bnn_find_3(self):
        selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName('*', selection)

        nodes = OpenMaya.MObject.bnn_find()
        self.assertEqual(len(nodes), selection.length())
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
    
    def test_bnn_find_4(self):
        nodes = OpenMaya.MObject.bnn_find(types=OpenMaya.MFn.kMesh)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
    
        nodes = OpenMaya.MObject.bnn_find(types=OpenMaya.MFn.kNurbsSurface)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape'])
    
        nodes = OpenMaya.MObject.bnn_find(types=[OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface])
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape', '|master|sphere|sphereShape'])
    
        nodes = OpenMaya.MObject.bnn_find(pattern='*|cube*', types=[OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface])
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|cube|cubeShape'])
    
    def test_bnn_find_5(self):
        nodes = OpenMaya.MObject.bnn_find(pattern='*|awesome:*')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light'])
    
        nodes = OpenMaya.MObject.bnn_find(pattern='*|awesome:*|awesome:*')
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|awesome:light|awesome:lightShape'])
    
    def test_bnn_find_6(self):
        nodes = OpenMaya.MObject.bnn_find(pattern='*|sphereShape->|*')
        self.assertEqual(len(nodes), 5)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
        
        nodes = OpenMaya.MObject.bnn_find(pattern='*|sphereShape->|*Shape*')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDagNode(node).fullPathName() for node in nodes]
        self.assertEqual(sorted(names), ['|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_1|projectionCurve1_Shape1', '|master|sphere|sphereShape->|projectionCurve1|projectionCurve1_2|projectionCurve1_Shape2'])
    
    def test_bnn_find_7(self):
        nodes = OpenMaya.MObject.bnn_find(pattern='default*Set')
        self.assertEqual(len(nodes), 2)
        for node in nodes:
            self.assertIsInstance(node, OpenMaya.MObject)
        names = [OpenMaya.MFnDependencyNode(node).name() for node in nodes]
        self.assertEqual(sorted(names), ['defaultLightSet', 'defaultObjectSet'])
    
    def test_bnn_getFunctionSet(self):
        node = OpenMaya.MObject.bnn_get('time1')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnDependencyNode)
        
        node = OpenMaya.MObject.bnn_get(pattern='defaultObjectSet')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnSet)
        
        node = OpenMaya.MObject.bnn_get(pattern='master')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnTransform)
        
        node = OpenMaya.MObject.bnn_get(pattern='cubeShape')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnMesh)
        
        node = OpenMaya.MObject.bnn_get(pattern='sphereShape')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnNurbsSurface)
        
        node = OpenMaya.MObject.bnn_get(pattern='circleShape')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnNurbsCurve)
        
        node = OpenMaya.MObject.bnn_get(pattern='awesome:lightShape')
        self.assertIs(node.bnn_getFunctionSet(), OpenMaya.MFnPointLight)
    
    def test_bnn_asFunctionSet(self):
        node = OpenMaya.MObject.bnn_get('time1')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnDependencyNode)
        self.assertEqual(functionSet.name(), 'time1')
        
        node = OpenMaya.MObject.bnn_get('defaultObjectSet')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnSet)
        self.assertEqual(functionSet.name(), 'defaultObjectSet')
        
        node = OpenMaya.MObject.bnn_get(pattern='master')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnTransform)
        self.assertEqual(functionSet.fullPathName(), '|master')
        
        node = OpenMaya.MObject.bnn_get(pattern='cubeShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnMesh)
        self.assertEqual(functionSet.fullPathName(), '|master|cube|cubeShape')
        
        node = OpenMaya.MObject.bnn_get(pattern='sphereShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnNurbsSurface)
        self.assertEqual(functionSet.fullPathName(), '|master|sphere|sphereShape')
        
        node = OpenMaya.MObject.bnn_get(pattern='circleShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnNurbsCurve)
        self.assertEqual(functionSet.fullPathName(), '|master|circle|circleShape')
        
        node = OpenMaya.MObject.bnn_get(pattern='awesome:lightShape')
        functionSet = node.bnn_asFunctionSet()
        self.assertIsInstance(functionSet, OpenMaya.MFnPointLight)
        self.assertEqual(functionSet.fullPathName(), '|master|awesome:light|awesome:lightShape')


if __name__ == '__main__':
    unittest.main()

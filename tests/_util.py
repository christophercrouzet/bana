from maya import OpenMaya


_NULL_OBJ = OpenMaya.MObject().kNullObj


class Context(object):

    def __init__(self):
        self.dg = OpenMaya.MDGModifier()
        self.dag = OpenMaya.MDagModifier()


def _createPrimitive(context, type, shapeType, outPlug, inPlug, name, parent):
    oParent = _NULL_OBJ if parent is None else parent.object()
    oGenerator = context.dg.createNode(type)
    oTransform = context.dag.createNode('transform', oParent)
    oShape = context.dag.createNode(shapeType, oTransform)

    generator = OpenMaya.MFnDependencyNode(oGenerator)
    transform = OpenMaya.MFnTransform(oTransform)
    shape = OpenMaya.MFnDagNode(oShape)

    context.dg.connect(generator.findPlug(outPlug), shape.findPlug(inPlug))
    if name is not None:
        transform.setName(name)
        shape.setName('%sShape' % (name,))

    return (transform, shape)


def createDagNode(context, type, name=None, parent=None):
    oParent = (context.dag.createNode('transform') if parent is None
               else parent.object())
    oNode = context.dag.createNode(type, oParent)
    node = OpenMaya.MFnDagNode(oNode)
    if name is not None:
        node.setName(name)

    return node


def createTransform(context, name=None, parent=None):
    oParent = _NULL_OBJ if parent is None else parent.object()
    oTransform = context.dag.createNode('transform', oParent)
    transform = OpenMaya.MFnTransform(oTransform)
    if name is not None:
        transform.setName(name)

    return transform


def createNurbsCircle(context, name=None, parent=None):
    return _createPrimitive(
        context, 'makeNurbCircle', 'nurbsCurve', 'outputCurve', 'create',
        name=name, parent=parent)


def createNurbsSphere(context, name=None, parent=None):
    return _createPrimitive(
        context, 'makeNurbSphere', 'nurbsSurface', 'outputSurface', 'create',
        name=name, parent=parent)


def createPolyCube(context, name, parent=None):
    return _createPrimitive(
        context, 'polyCube', 'mesh', 'output', 'inMesh',
        name=name, parent=parent)

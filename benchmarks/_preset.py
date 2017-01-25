import revl
from maya import OpenMaya


def _createPrimitive(context, intermediate=False, template=False, **kwargs):
    primitive = revl.createPrimitive(context, **kwargs)
    for oShape in primitive.shapes:
        shape = OpenMaya.MFnDependencyNode(oShape)
        context.dg.newPlugValueBool(shape.findPlug('intermediateObject'),
                                    intermediate)
        context.dg.newPlugValueBool(shape.findPlug('template'),
                                    template)


DEEP = [
    (50, revl.createPrimitive, (), {'parent': True}),
    (20, revl.createTransform, (), {'parent': True}),
    (15, revl.createDgNode, ('addDoubleLinear',)),
    (15, revl.createDgNode, ('clamp',)),
    (15, revl.createDagNode, ('pointConstraint',), {'parent': True}),
    (5, _createPrimitive, (), {'parent': True, 'intermediate': True}),
    (5, _createPrimitive, (), {'parent': True, 'template': True}),
    (5, _createPrimitive, (), {'parent': True, 'intermediate': True, 'template': True}),
    (5, revl.createDgNode, ('lambert',)),
    (1, revl.unparent),
]

FLAT = [
    (50, revl.createPrimitive),
    (20, revl.createTransform),
    (15, revl.createDgNode, ('addDoubleLinear',)),
    (15, revl.createDgNode, ('clamp',)),
    (15, revl.createDagNode, ('pointConstraint',)),
    (5, _createPrimitive, (), {'intermediate': True}),
    (5, _createPrimitive, (), {'template': True}),
    (5, _createPrimitive, (), {'intermediate': True, 'template': True}),
    (5, revl.createDgNode, ('lambert',)),
]

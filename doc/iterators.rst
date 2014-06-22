.. _iterators:

Iterators
=========

.. module:: banana.maya.extensions.OpenMaya.iterators

Set of additional iterators to traverse Maya objects.

.. autosummary::
   :nosignatures:
   
   bnn_MItDependencyNode
   bnn_MItDagNode
   bnn_MItDagHierarchy

It's possible to use those iterators the Maya way:

   >>> import banana.maya
   >>> banana.maya.patch()
   >>> from maya import OpenMaya
   >>> iterator = OpenMaya.bnn_MItDagHierarchy()
   >>> while not iterator.isDone():
   ...    node = iterator.currentItem()
   ...    print(node.fullPathName())
   ...    iterator.next()


But it's also possible to use them the Python way:

   >>> import banana.maya
   >>> banana.maya.patch()
   >>> from maya import OpenMaya
   >>> for node in OpenMaya.bnn_MItDagHierarchy():
   ...    print(node.fullPathName())


bnn_MItDependencyNode
---------------------

.. autoclass:: bnn_MItDependencyNode
   :members:
   
   .. automethod:: __init__


bnn_MItDagNode
--------------

.. autoclass:: bnn_MItDagNode
   :members:
   
   .. automethod:: __init__


bnn_MItDagHierarchy
-------------------

.. autoclass:: bnn_MItDagHierarchy
   :members:
   
   .. automethod:: __init__

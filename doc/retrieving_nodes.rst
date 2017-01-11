.. currentmodule:: bana

.. _retrieving_nodes:

Retrieving Nodes
================

Out of the box, the Maya API is a bit cumbersome when it comes to retrieving
DG and DAG nodes from a scene. This usually leads each TD to write their own
code for the task, and this is also something that Bana aims to provide.

The goal here is to offer a higher-level set of methods allowing to retrieve
nodes with enough flexibility to cover most of a TD's needs while remaining as
fast as possible.

Since these methods are in fact iterators, it is easy to build on top of them
in the case where more filtering options are required, such as for example
skipping the DAG shapes that are templated.

But what sets this library apart from the usual implementations is its
well-defined :ref:`pattern matching specification <pattern_matching>`. When
Maya's interpretation of the wildcard character ``*`` is everyone's guess, Bana
offers both precise and predictable results.


.. _rn_design:

Design
------

In Bana, there are 2 groups of classes from where the scene nodes can be
retrieved:

    * the function set classes :class:`~OpenMaya.MFnDependencyNode` and
      :class:`~OpenMaya.MFnDagNode`.
    * the lower-level classes :class:`~OpenMaya.MObject` and
      :class:`~OpenMaya.MDagPath`.


The former group represents the most common use case while the second can be
used to slightly speed things up when the extra functionalities brought by the
``MFn*`` classes are not required.

For each of these classes, two types of methods are then exposed as the API:

    * the methods starting with ``bnFind`` which return an iterator over a
      collection of nodes matching the input filters.
    * the methods starting with ``bnGet`` which return a single object matching
      the input filters. If zero or more nodes are found, then ``None`` is
      returned.


When using the lower-level family of classes, it is possible to explictely pass
a node type to match through the ``fnType`` parameter but in the case of the
function set classes, no ``fnType`` parameter is defined. Instead the node type
to match is deduced from the calling class. In other words, a call to
``maya.OpenMaya.MFnDagNode.bnFind()`` will match any node of type
``maya.OpenMaya.kDagNode`` while calling
``maya.OpenMaya.MFnTransform.bnFind()`` will only match transform nodes.


.. note::

   Node names are available from the ``maya.OpenMaya.MFnDependencyNode`` class
   but not directly from the ``maya.OpenMaya.MObject`` one. As a result,
   retrieving ``maya.OpenMaya.MObject`` objects from a pattern will internally
   convert them to ``maya.OpenMaya.MFnDependencyNode``, in which case there
   won't be much benefits from using the
   :meth:`MObject.bnFind() <OpenMaya.MObject.MObject.bnFind>` method in place
   of
   :meth:`MFnDependencyNode.bnFind() <OpenMaya.MFnDependencyNode.MFnDependencyNode.bnFind>`.


.. _rn_dg_vs_dag_nodes:

DG vs DAG Nodes
---------------

Although it is possible to iterate over all DG or DAG nodes using the methods
exposed within the :class:`~OpenMaya.MFnDependencyNode` and
:class:`~OpenMaya.MObject` classes, it is not possible to filter DAG nodes this
way using a *path* pattern. Indeed, these methods only accept *name* patterns.

Hence it is recommended to use instead the methods defined in the classes
:class:`~OpenMaya.MFnDagNode` and :class:`~OpenMaya.MDagPath` whenever DAG
nodes are to be retrieved. Furthermore, these offer a boost in performances,
especially when only a specific branch of DAG nodes needs to be traversed
through the use of the ``bnFindChildren()`` and ``bnGetChild()`` methods.


.. _rn_examples:

Examples
--------

.. code-block:: python

   >>> import bana
   >>> bana.initialize()
   >>> from maya import OpenMaya
   >>> # Retrieve a transform node named 'root'.
   >>> root = OpenMaya.MFnTransform.bnGet(pattern='*|root')
   >>> # Recursively iterate over all the DAG nodes child of 'root'.
   >>> for node in root.bnFindChildren():
   ...     print(node)
   >>> # Find all the mesh nodes in the scene containing the word 'Shape' but
   ... # not belonging to any namespace.
   >>> for node in OpenMaya.MFnMesh.bnFind(pattern='*|*Shape*'):
   ...     print(node)

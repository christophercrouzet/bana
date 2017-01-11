.. currentmodule:: bana

.. _pattern_matching:

Pattern Matching
================

The API of Maya has a well-defined syntax to describe DG names and DAG paths
but the solution offered to match wildcard patterns, through the use of
methods such as ``maya.OpenMaya.MGlobal.getSelectionListByName()``, can
sometimes lead to unexpected results.

As an example, Maya defines the pattern ``|*`` as matching only the DAG nodes
of depth 1, that is the nodes directly parented under the world. Therefore,
when using a similar pattern applied to the underworld, for instance
``node|shape->|*``, one would intuitively expect that only the nodes located
directly beneath the underworld are to be matched. Instead, Maya's
implementation leads to match all the nodes at any depth below the underworld,
which is inconsistent.

To alleviate this lack of predictability and to add a whole new set of
possibilities loosely borrowed from Python's |re|_ module, a new specification
dedicated to matching name and path patterns is being used across the Bana
extensions, mostly through the ``bnFind*()`` and ``bnGet*()`` methods (see
:ref:`retrieving_nodes`).

This pattern matching specification introduces:

    * a new :ref:`syntax <pm_syntax>` built upon Maya's DG names and DAG paths
      syntaxes, with support for four wildcard operators ``*``, ``+``, ``?``,
      and ``.``.
    * a well-defined set of :ref:`matching rules <pm_matching_rules>`
      describing the expected behaviour when using these wildcards in each
      possible scenario.


.. _pm_syntax:

Syntax
------

The standard syntax defined by Maya, and recognized by Bana, describes DG names
and DAG paths as they are expected to be returned by methods like
``maya.OpenMaya.MFnDependencyNode.name()`` and
``maya.OpenMaya.MFnDagNode.fullPathName()``:

.. productionlist::
   alpha      : "a"..."z" | "A"..."Z" | "_"
   character  : `alpha` | "0"..."9"
   name       : `alpha` `character`*
   full_name  : (`name` ":")* `name`
   path       : ("|" `full_name`)+
   full_path  : `path` ("->" `path`)* "->"?


The library Bana extends the standard syntax by adding support for the four
wildcard operators:

.. productionlist::
   wcard            : "*" | "+" | "?" | "."
   wcard_name       : (`alpha` | `wcard`+) (`character` | `wcard`+)*
   wcard_full_name  : (":" `wcard`+ | `wcard_name`) (":" `wcard_name`)* 
   wcard_path       : ("|" `wcard_full_name` | `wcard`+)+
   wcard_full_path  : `wcard_path` ("->" `wcard_path`)* "->"?


.. note::

   The syntax groups are listed in ascending precedence order. In other words:
   *character* < *name* < *full name* < *path* < *full path*. This is useful
   for determining the :ref:`context <pm_matching_rules_context>`.


.. _pm_syntax_english:

In English
^^^^^^^^^^

:token:`Names <name>` can identify DG nodes, excluding the ones carrying any
namespace or hierarchy information. They are made of :token:`character`
elements, that is *alphanumeric characters*, *underscores*, and *wildcards*.

:token:`Full names <full_name>` can fully identify any DG node. They are
composed by one or more :token:`name` elements, each separated by the namespace
delimiter ``:``.

:token:`Paths <path>` can identify DAG nodes, excluding the ones carrying any
underworld information. They are composed by one or more
:token:`full name <full_name>` elements, each starting with the hierarchy
delimiter ``|``.

:token:`Full paths <full_path>` can fully identify any DAG node. They are
composed by one or more :token:`path` elements, each separated by the
underworld delimiter ``->``.

Patterns can be checked against any of these syntax groups using the
corresponding ``bana.OpenMaya.MGlobal.bnIsValid*()`` method:

.. code-block:: python

   >>> import bana
   >>> bana.initialize()
   >>> from maya import OpenMaya
   >>> OpenMaya.MGlobal.bnIsValidName('node')
   True
   >>> OpenMaya.MGlobal.bnIsValidName('node_*', allowWildcards=True)
   True
   >>> OpenMaya.MGlobal.bnIsValidName('ns:node')
   False
   >>> OpenMaya.MGlobal.bnIsValidFullName('ns:node')
   True
   >>> OpenMaya.MGlobal.bnIsValidFullName('*:node', allowWildcards=True)
   True
   >>> OpenMaya.MGlobal.bnIsValidFullName('|node')
   False
   >>> OpenMaya.MGlobal.bnIsValidPath('|node')
   True
   >>> OpenMaya.MGlobal.bnIsValidPath('*|node', allowWildcards=True)
   True
   >>> OpenMaya.MGlobal.bnIsValidPath('|root->|node')
   False
   >>> OpenMaya.MGlobal.bnIsValidFullPath('|root->|node')
   True
   >>> OpenMaya.MGlobal.bnIsValidFullPath('*->|node', allowWildcards=True)
   True


.. _pm_syntax_tldr:

TL;DR
^^^^^

The composition of *names*, *full names*, *paths*, and *full paths*, can
approximately be summed up as follows:

    * a :token:`name` is composed of one or more :token:`character` elements.
    * a :token:`full name <full_name>` is composed of one or more :token:`name`
      elements separated by the ``:`` symbol.
    * a :token:`path` is composed of one or more :token:`full name <full_name>`
      elements separated by the ``|`` symbol.
    * a :token:`full path <full_path>` is composed of one or more :token:`path`
      elements separated by the ``->`` symbol.


.. _pm_matching_rules:

Matching Rules
--------------

Depending on where a wildcard operator is located within a pattern, it might
end up matching a certain number of occurrences of either one of the
:token:`character`, :token:`name`, :token:`full name <full_name>`, or
:token:`path` syntax groups. For example the wildcard in the pattern
``|node_*`` matches a *name* formed by any number of *characters*, but the same
wildcard in the pattern ``*|node`` matches a *path* composed by any number of
*full names* (e.g.: ``|root|parent|node``).

In order to understand what a wildcard, or a combination of wildcards, will
precisely match, there are two aspects to take into consideration:

    * the :ref:`context <pm_matching_rules_context>` in which the wildcards are
      defined.
    * the :ref:`number of occurrences <pm_matching_rules_occurrences>` that the
      wildcards describe.


.. _pm_matching_rules_context:

Context
^^^^^^^

The context represents the syntax group to be matched. It can be determined by
looking at the delimiters surrounding the wildcards, picking the one with the
highest precedence, and retrieving the syntax group associated with it as
defined in this table sorted in descending precedence order:

+---------------+------------------+
|  delimiter    |  syntax group    |
+===============+==================+
|  *character*  +  *name*          |
+---------------+------------------+
|  ``:``        +  *full name*     |
+---------------+------------------+
|  ``|``        +  *path*          |
+---------------+------------------+
|  ``->``       +  *full path*     |
+---------------+------------------+


For example, the wildcard in the pattern ``|ns:*|leaf`` is surrounded by the
delimiters ``:`` and ``|``, respectively representing the *full name* and
*path* syntax groups, hence the context is *full name* since it has a higher
precedence than *path*.

When the wildcards are located at the beginning or the end of a string, then
the only delimiter found is used to define the context. For example, the
context for the wildcard in the pattern ``*->|leaf`` is *full path*, as per the
``->`` delimiter.

If one of the delimiters is a *character*, then the context is bound to be
*name*. The pattern ``|node*->leaf`` is an example of such a case.

Finally, if a pattern is only composed of wildcards, then the global context
defined by the matching method called is used. For example the method
:meth:`MGlobal.bnMatchFullPath() <OpenMaya.MGlobal.MGlobal.bnMatchFullPath>`
defines the global context *full path*.


.. _pm_matching_rules_occurrences:

Number of Occurrences
^^^^^^^^^^^^^^^^^^^^^

Remember how, according to the rules of
:ref:`syntax composition <pm_syntax_tldr>`, a syntax group might be made of
one or more elements of another syntax group. With this in mind, the number of
occurences specifies how many elements of a context needs to be matched.

The special characters ``*``, ``+``, ``?``, and ``.`` all carry the same
purpose of matching a context element but a different number of times. The
quantity being described by these wildcards is the same as their regular
expression language counterparts, meaning that:

    * ``*`` matches 0 or more occurrences of a context element.
    * ``+`` matches 1 or more occurrences of a context element.
    * ``?`` matches 0 or 1 occurrences of a context element.
    * ``.`` matches 1 occurrence of a context element.


As an example, if the context is :token:`full name <full_name>`, then the
quantifier defines how many :token:`name` elements needs to be matched: the
wildcard in the pattern ``|ns:+|leaf`` will match 1 or more *names* separated
by the ``:`` delimiter, thus forming in the end a *full name*.


.. _pm_matching_rules_nothing:

Matching Nothing
^^^^^^^^^^^^^^^^

It sometimes makes sense to allow a wildcard to match zero occurrences.
This is especially useful when performing recursive searches where the pattern
``*|leaf`` can match any node named ``leaf``, including the one directly
parented under the world, and where the pattern ``|ns:*:leaf`` can match nodes
such as ``|ns:ns2:ns3:leaf`` and ``|ns:leaf``.

In some other cases, this doesn't make too much sense. For example the pattern
``|ns:*`` cannot match any node named ``|ns:`` because this isn't a valid
pattern.

To check if a wildcard is allowed to match zero occurrences or not, see
the :ref:`pm_matching_rules_tldr` table.


.. _pm_matching_rules_tldr:

TL;DR
^^^^^

The table below regroups all the possible valid uses of wildcard operators
located between two adjacent delimiters.

.. admonition:: Reminder

   If the occurrence of wildcard is not listed in this table, it is bound to
   belong to the *name* context.


.. role:: green
.. role:: red

+-------------+-----------------------+--------------------------------+---------------------+
|  pattern    |  example              |  context                       |  can match nothing  |
+=============+=======================+================================+=====================+
|  ``^@$``    |  ``@``                |  same as the global context    |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``^@:``    |  ``@:leaf``           |  *full name*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``^@|``    |  ``@|leaf``           |  *path*                        |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``^@->``   |  ``@->|leaf``         |  *full path*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``:@$``    |  ``|ns:@``            |  *full name*                   |  :red:`no`          |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``:@:``    |  ``|ns:@:leaf``       |  *full name*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``:@|``    |  ``|ns:@|leaf``       |  *full name*                   |  :red:`no`          |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``:@->``   |  ``|ns:@->|leaf``     |  *full name*                   |  :red:`no`          |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``|@$``    |  ``|root|@``          |  *path*                        |  :red:`no`          |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``|@:``    |  ``|root|@:leaf``     |  *full name*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``|@|``    |  ``|root|@|leaf``     |  *path*                        |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``|@->``   |  ``|root|@->|leaf``   |  *path*                        |  :red:`no`          |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``->@$``   |  ``|root->@``         |  *full path*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``->@|``   |  ``|root->@|leaf``    |  *path*                        |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+
|  ``->@->``  |  ``|root->@->|leaf``  |  *full path*                   |  :green:`yes`       |
+-------------+-----------------------+--------------------------------+---------------------+


.. note::

   The characters ``^`` and ``$`` used in the table respectively refer to the
   start and the end of a string. As for the character ``@``, it is to be
   replaced by one or more wildcards.


.. _pm_combining_wildcards:

Combining Wildcards
-------------------

If needed, it is possible to come up with some fancy patterns by successively
writing multiple wildcard operators that will combine to define a specific
number of occurrences. For example, the pattern ``...`` matches 3 occurrences
of the context element, while ``.+`` matches at least 2 occurrences, and
``..??`` matches from 2 to 4 occurrences.

The number of occurrences to match resulting from such a combination is easy to
figure out. Let's consider the regular expression notation ``{m,n}`` describing
``from m to n occurrences``, and ``{m,}`` that specifies ``at least m
occurrences``. Rewriting the four wildcard operators following this notation
gives:

    - ``*`` -> ``{0,}``
    - ``+`` -> ``{1,}``
    - ``?`` -> ``{0,1}``
    - ``.`` -> ``{1,1}``

Combining wildcard operators is equivalent to adding their range of
occurrences. From the previous example, the pattern ``.+`` equals to
``{1,1} + {1,}``, that is ``{2,}``, and the pattern ``..??`` equals to
``{1,1} + {1,1} + {0,1} + {0,1}``, that is ``{2,4}``.


.. _pm_namespace:

Namespace Construct
-------------------

The pattern ``|root|.`` allows matching any node which has ``root`` as direct
parent but it is not enough if filtering namespaces is also required. This
is why, as per the :ref:`syntax rules <pm_syntax>`, a special construct has
been added to allow a full name to start with the ``:`` delimiter if it is
followed by one or more wildcards. With this addition, the pattern ``|root|:.``
makes it possible to match any node directly parented under ``root`` that does
not belong to any namespce.


.. _pm_examples:

Examples
--------

Matching DG Nodes
^^^^^^^^^^^^^^^^^

.. code-block:: python

   >>> import bana
   >>> bana.initialize()
   >>> from maya import OpenMaya
   >>> # Match the nodes named 'leaf' belonging to any namespace.
   >>> OpenMaya.MGlobal.bnMatchFullName('*:leaf', 'leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchFullName('*:leaf', 'ns:leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchFullName('*:leaf', 'nsa:nsb:leaf')
   True
   >>> # Match the nodes directly nested under a namespace 'ns'.
   >>> OpenMaya.MGlobal.bnMatchFullName('ns:.', 'ns:leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchFullName('ns:.', 'ns:nsa:leaf')
   False
   >>> # Match the nodes recursively nested under a namespace 'ns'.
   >>> OpenMaya.MGlobal.bnMatchFullName('ns:+', 'ns:leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchFullName('ns:+', 'ns:nsa:leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchFullName('ns:+', 'ns:nsa:nsb:leaf')
   True


Matching DAG Nodes
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   >>> import bana
   >>> bana.initialize()
   >>> from maya import OpenMaya
   >>> # Match the nodes directly parented under the world.
   >>> OpenMaya.MGlobal.bnMatchPath('|.', '|leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('|.', '|ns:leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('|.', '|root|leaf')
   False
   >>> # Match the nodes directly parented under the world but not belonging to
   ... # any namespace.
   >>> OpenMaya.MGlobal.bnMatchPath('|:.', '|leaf')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('|:.', '|ns:leaf')
   False
   >>> OpenMaya.MGlobal.bnMatchPath('|:.', '|root|leaf')
   False
   >>> # Match the nodes containing 'Shape' anywhere in the hierarchy but not
   ... # belonging to any namespace.
   >>> OpenMaya.MGlobal.bnMatchPath('+|*Shape*', '|cube|cubeShape')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('+|*Shape*', '|root|sphere|sphereShape1')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('+|*Shape*', '|cube|ns:cubeShape')
   False
   >>> # Match the nodes containing 'Shape' anywhere in the hierarchy.
   >>> OpenMaya.MGlobal.bnMatchPath('+|*:*Shape*', '|cube|cubeShape')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('+|*:*Shape*', '|root|sphere|sphereShape1')
   True
   >>> OpenMaya.MGlobal.bnMatchPath('+|*:*Shape*', '|cube|ns:cubeShape')
   True


.. |character| replace:: *character*
.. |re| replace:: ``re``

.. _re: https://docs.python.org/library/re.html

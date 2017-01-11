.. currentmodule:: bana

.. _tutorial:

Tutorial
========

One cool thing with these extensions is that there isn't much to know to
get rolling—you'll be using the same old Maya's Python API as you've always
done, only with a few extra methods at your disposal that have been injected
here and there.

All there is to make these extensions available as part of Maya's API is to
initialize them:

.. code-block:: python

   >>> import bana
   >>> bana.initialize()


Done! Now you can head over to the :ref:`reference` section and make use of any
of the extensions listed in there.

.. note::

   Feel free to check out the :ref:`pattern_matching` and
   :ref:`retrieving_nodes` sections for guides about some core features
   included with Bana.

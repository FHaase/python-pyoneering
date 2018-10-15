===============
Getting started
===============

Configuration
=============

In order to provide a module-wide configuration for the decorators :func:`deprecated` and
:func:`refactored` include the following code-snippet in your module.

.. _default-configuration:
.. literalinclude:: /../tests/example/utils.py

Then these functions are accessible from anywhere in your module.

.. literalinclude:: /../tests/example/example.py
    :lines: 3

Examples
========

The examples are generated with :attr:`__version__='1.0'`.

.. py:currentmodule:: tests

deprecated class
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: DeprecatedClass

.. autoclass:: example.DeprecatedClass

deprecated method
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: deprecated_method

.. automethod:: example.deprecated_method

renamed parameter
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: renamed_parameter

.. automethod:: example.renamed_parameter

merged parameter
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: _merged_parameters
.. literalinclude:: /../tests/example/example.py
    :pyobject: merged_parameter

.. automethod:: example.merged_parameter

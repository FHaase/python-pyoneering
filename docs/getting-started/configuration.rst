Configuration
=============

In order to provide a module-wide configuration for the decorators :func:`deprecated` and
:func:`refactored` include the following code-snippet in your module.

.. _default-configuration:
.. literalinclude:: /../tests/example/utils.py

Then these functions are accessible from anywhere in your module.

.. literalinclude:: /../tests/example/example.py
    :lines: 3


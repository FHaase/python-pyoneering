Examples
========

The examples are generated using class :class:`DeprecationDecorators` with :attr:`current_version='1.0'`.

deprecated class
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: DeprecatedClass

.. autoclass:: tests.example.DeprecatedClass

deprecated method
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: deprecated_method

.. automethod:: tests.example.deprecated_method

renamed parameter
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: renamed_parameter

.. automethod:: tests.example.renamed_parameter

merged parameter
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: _merged_parameters
.. literalinclude:: /../tests/example/example.py
    :pyobject: merged_parameter

.. automethod:: tests.example.merged_parameter
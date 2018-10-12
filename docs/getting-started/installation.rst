Installation
============

.. |pipenv| replace:: ``pipenv``
.. _pipenv : https://pipenv.readthedocs.io/en/latest/

.. |pip| replace:: ``pip``
.. _pip : https://pip.pypa.io/en/stable/

You can install |project| with |pip|_ or |pipenv|_.

.. code-block:: console

    $ pip install pyoneering

.. code-block:: console

    $ pipenv install pyoneering

------------

In order to provide a module-wide configuration for the decorators :func:`deprecated` and
:func:`refactored` include the following code-snippet in your module.

.. _default-configuration:
.. literalinclude:: /../tests/example/utils.py

Then these functions are accessible from anywhere in your module.

.. literalinclude:: /../tests/example/example.py
    :lines: 3



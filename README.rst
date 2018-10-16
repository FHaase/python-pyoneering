========
Overview
========

.. start-badges

|codacy-grade| |codacy-coverage| |requires|

|docs| |travis| |appveyor|

|version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-pyoneering/badge/?style=flat
    :target: https://readthedocs.org/projects/python-pyoneering
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/FHaase/python-pyoneering.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/FHaase/python-pyoneering

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/FHaase/python-pyoneering?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/FHaase/python-pyoneering

.. |requires| image:: https://requires.io/github/FHaase/python-pyoneering/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/FHaase/python-pyoneering/requirements/?branch=master

.. |codacy-grade| image:: https://api.codacy.com/project/badge/Grade/eb62084e3ff6444f9a7d0c4c17d4d117
   :alt: Codacy Grade
   :target: https://app.codacy.com/app/FHaase/python-pyoneering?utm_source=github.com&utm_medium=referral&utm_content=FHaase/python-pyoneering&utm_campaign=Badge_Grade_Settings

.. |codacy-coverage| image:: https://api.codacy.com/project/badge/Coverage/eb62084e3ff6444f9a7d0c4c17d4d117
   :alt: Codacy Covarage
   :target: https://app.codacy.com/app/FHaase/python-pyoneering?utm_source=github.com&utm_medium=referral&utm_content=FHaase/python-pyoneering&utm_campaign=Badge_Grade_Settings

.. |version| image:: https://img.shields.io/pypi/v/pyoneering.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pyoneering

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyoneering.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pyoneering

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyoneering.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pyoneering

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pyoneering.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pyoneering


.. end-badges

Decorators for deprecating and refactoring

* Free software: Apache Software License 2.0

Installation
============

::

    pip install pyoneering

Documentation
=============


https://python-pyoneering.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

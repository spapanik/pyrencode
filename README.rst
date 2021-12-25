=================================
pyrencode: rencode in pure python
=================================

.. image:: https://github.com/spapanik/pyrencode/actions/workflows/build.yml/badge.svg
  :alt: Build
  :target: https://github.com/spapanik/pyrencode/actions/workflows/build.yml
.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pyrencode.svg
  :alt: Total alerts
  :target: https://lgtm.com/projects/g/spapanik/pyrencode/alerts/
.. image:: https://img.shields.io/github/license/spapanik/pyrencode
  :alt: License
  :target: https://github.com/spapanik/pyrencode/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/pyrencode
  :alt: PyPI
  :target: https://pypi.org/project/pyrencode
.. image:: https://pepy.tech/badge/pyrencode
  :alt: Downloads
  :target: https://pepy.tech/project/pyrencode
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style
  :target: https://github.com/psf/black

``pyrencode`` is a python rewrite of the original `rencode`_ by aresch, avoiding  the cython dependency, so that it can be used with PyPy.

In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use `poetry`_ to manage your dependencies and add *pyrencode* to them.

.. code-block:: toml

    [tool.poetry.dependencies]
    pyrencode = "*"

Usage
^^^^^

``pyrencode`` provides exactly the same interface as `rencode`_

.. _rencode: https://github.com/aresch/rencode
.. _poetry: https://python-poetry.org/


Links
-----

- `Documentation`_
- `Changelog`_


.. _Changelog: https://github.com/spapanik/pyrencode/blob/main/CHANGELOG.rst
.. _Documentation: https://pyrencode.readthedocs.io/en/latest/

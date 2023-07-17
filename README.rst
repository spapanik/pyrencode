=================================
pyrencode: rencode in pure python
=================================

.. image:: https://github.com/spapanik/pyrencode/actions/workflows/tests.yml/badge.svg
  :alt: Tests
  :target: https://github.com/spapanik/pyrencode/actions/workflows/tests.yml
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
  :alt: code style: black
  :target: https://github.com/psf/black
.. image:: https://img.shields.io/badge/build%20automation-yamk-success
  :alt: build automation: yam
  :target: https://github.com/spapanik/yamk
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
  :alt: Lint: ruff
  :target: https://github.com/charliermarsh/ruff

``pyrencode`` is a python rewrite of the original `rencode`_ by aresch, avoiding  the cython dependency, so that it can be used with PyPy.
Even though there in no cython code, the performance is comparable to the original, and in many cases it's even better.


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

Links
-----

- `Documentation`_
- `Changelog`_


.. _rencode: https://github.com/aresch/rencode
.. _poetry: https://python-poetry.org/
.. _Changelog: https://github.com/spapanik/pyrencode/blob/main/CHANGELOG.rst
.. _Documentation: https://pyrencode.readthedocs.io/en/latest/

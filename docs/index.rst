.. plaid documentation master file, created by
   sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

    <br>

.. image:: https://plaid-lib.github.io/assets/images/plaid-ops-logo.png
   :align: center
   :width: 300px

+-------------+-----------------------------------------------------------------------------------------------+
| **Testing** | |CI Status| |Docs| |Coverage| |Last Commit|                                                   |
+-------------+-----------------------------------------------------------------------------------------------+
| **Package** | |PyPI Version| |PyPi Downloads| |Platform| |Python Version|                                   |
+-------------+-----------------------------------------------------------------------------------------------+
| **Meta**    | |License| |GitHub Stars|                                                                      |
+-------------+-----------------------------------------------------------------------------------------------+


.. |CI Status| image:: https://github.com/PLAID-lib/plaid-ops/actions/workflows/testing.yml/badge.svg
   :target: https://github.com/PLAID-lib/plaid-ops/actions/workflows/testing.yml

.. |Docs| image:: https://readthedocs.org/projects/plaid-ops/badge/?version=latest
   :target: https://plaid-ops.readthedocs.io/en/latest/?badge=latest

.. |Coverage| image:: https://codecov.io/gh/plaid-lib/plaid-ops/branch/main/graph/badge.svg
   :target: https://app.codecov.io/gh/plaid-lib/plaid-ops/tree/main?search=&displayType=list

.. |Last Commit| image:: https://img.shields.io/github/last-commit/PLAID-lib/plaid-ops/main
   :target: https://github.com/PLAID-lib/plaid-ops/commits/main

.. |PyPI Version| image:: https://img.shields.io/pypi/v/plaid-ops.svg
   :target: https://pypi.org/project/plaid-ops/

.. |Platform| image:: https://img.shields.io/badge/platform-any-blue
   :target: https://github.com/PLAID-lib/plaid-ops

.. |Python Version| image:: https://img.shields.io/pypi/pyversions/plaid-ops
   :target: https://github.com/PLAID-lib/plaid-ops

.. |PyPi Downloads| image:: https://static.pepy.tech/badge/plaid-ops
   :target: https://pepy.tech/projects/plaid-ops

.. |License| image:: https://anaconda.org/conda-forge/plaid/badges/license.svg
   :target: https://github.com/PLAID-lib/plaid-ops/blob/main/LICENSE.txt

.. |GitHub Stars| image:: https://img.shields.io/github/stars/PLAID-lib/plaid-ops?style=social
   :target: https://github.com/PLAID-lib/plaid-ops


.. warning::

   The code is still in its initial configuration stages; interfaces may change. Use with care.

Plaid-ops offers standardized operations on PLAID (Physics Learning AI Datamodel) samples and datasets.
It has been developed at SafranTech, the research center of `Safran group <https://www.safran-group.com/>`_.

The code is hosted on `GitHub <https://github.com/PLAID-lib/plaid-ops>`_ and the Python package is published as ``plaid-ops``.

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Overview

   source/quickstart.md

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Advanced

   source/contributing.md

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Documentation

   API Reference <autoapi/plaid_ops/index>
   Examples & Tutorials <source/notebooks.rst>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

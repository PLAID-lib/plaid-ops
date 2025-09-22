<div align="center">
<img src="https://plaid-lib.github.io/assets/images/plaid-ops-logo.png" width="300">
</div>

| | |
| --- | --- |
| Testing | [![CI Status](https://github.com/PLAID-lib/plaid-ops/actions/workflows/testing.yml/badge.svg)](https://github.com/PLAID-lib/plaid-ops/actions/workflows/testing.yml) [![Documentation Status](https://readthedocs.org/projects/plaid-ops/badge/?version=latest)](https://plaid-ops.readthedocs.io/en/latest/?badge=latest) [![Coverage](https://codecov.io/gh/plaid-lib/plaid-ops/branch/main/graph/badge.svg)](https://app.codecov.io/gh/plaid-lib/plaid-ops/tree/main?search=&displayType=list) ![Last Commit](https://img.shields.io/github/last-commit/PLAID-lib/plaid-ops/main) |
| Package | [![PyPI Latest Release](https://img.shields.io/pypi/v/plaid-ops.svg)](https://pypi.org/project/plaid-ops/) [![PyPI Downloads](https://static.pepy.tech/badge/plaid-ops)](https://pepy.tech/projects/plaid-ops) ![Platform](https://img.shields.io/badge/platform-any-blue) ![Python Version](https://img.shields.io/pypi/pyversions/plaid-ops)  |
| Other | [![License - BSD 3-Clause](https://anaconda.org/conda-forge/plaid/badges/license.svg)](https://github.com/PLAID-lib/plaid-ops/blob/main/LICENSE.txt) ![GitHub stars](https://img.shields.io/github/stars/PLAID-lib/plaid-ops?style=social)|


# plaid-ops

Standardized operations on PLAID (Physics Learning AI Datamodel) samples and datasets.

> [!WARNING]
> The code is still in its initial configuration stages; interfaces may change. Use with care.


## 1 Using the library

First create an environment using conda/mamba:

```bash
mamba create -n plaid-ops python=3.11 hdf5 "vtk>=9.4" pycgns-core muscat-core=2.5 -c conda-forge
mamba activate plaid-ops
```

### User mode

Relies on the published PyPi package:

```bash
pip install plaid-ops
```

### Developper mode

Installing from the sources:

```bash
pip install -e .[dev]
```

Note: this will install the last stable version of [PLAID](https://github.com/PLAID-lib/plaid-ops).

## 2 Core concepts

plaid-ops provides high-level utilities to manipulate meshes and fields in PLAID datasets:
- Compute dataset-wide properties (e.g., bounding boxes)
- Project fields between unstructured meshes and regular rectilinear grids
- Transfer fields from one dataset to another with consistent sample/time alignment
- Perform mesh-based feature engineering (e.g., signed-distance function)
- Visualize results with simple helpers

It builds on top of PLAID and uses Muscat FE operators under the hood for accurate interpolations.

## 3 Going further

See the documentation for a concise getting started guide and end-to-end examples:
- [Getting Started](https://plaid-ops.readthedocs.io/en/latest/source/getting_started.html)
- [Examples & Tutorials](https://plaid-ops.readthedocs.io/en/latest/source/notebooks.html)
- [API reference](https://plaid-ops.readthedocs.io/en/latest/autoapi/plaid_ops/index.html)

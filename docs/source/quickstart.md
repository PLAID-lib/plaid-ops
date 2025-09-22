# Quickstart

Everything you need to start using plaid-ops and contributing effectively.

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

Note: this will install the last stable version of PLAID.

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
- [Examples & Tutorials](https://plaid-ops.readthedocs.io/en/latest/source/notebooks.html)
- [API reference](https://plaid-ops.readthedocs.io/en/latest/autoapi/plaid_ops/index.html)
"""This file defines shared pytest fixtures and test configurations."""

import numpy as np
import pytest
from Muscat.Bridges.CGNSBridge import MeshToCGNS
from Muscat.MeshTools import MeshCreationTools as MCT
from plaid.containers.sample import Sample
from plaid.types import CGNSTree


@pytest.fixture()
def nodes():
    return np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0],
            [0.5, 1.5],
        ]
    )


@pytest.fixture()
def triangles():
    return np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [2, 4, 3],
        ]
    )


@pytest.fixture()
def mesh(nodes, triangles):
    return MCT.CreateMeshOfTriangles(nodes, triangles)


@pytest.fixture()
def tree(mesh):
    return MeshToCGNS(mesh)


@pytest.fixture()
def sample():
    return Sample()


@pytest.fixture()
def sample_with_tree(tree: CGNSTree) -> Sample:
    """Generate a Sample objects with a tree."""
    sample = Sample()
    sample.add_tree(tree)
    return sample

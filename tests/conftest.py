"""This file defines shared pytest fixtures and test configurations."""

import numpy as np
import pytest
from Muscat.Bridges.CGNSBridge import MeshToCGNS
from Muscat.MeshTools import MeshCreationTools as MCT
from plaid.containers.dataset import Dataset
from plaid.containers.sample import Sample
from plaid.types import CGNSTree

# from plaid.examples import datasets, samples

# @pytest.fixture()
# def dataset():
#     return datasets.tensile2d

# @pytest.fixture()
# def sample():
#     return samples.tensile2d


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
    mesh = MCT.CreateMeshOfTriangles(nodes, triangles)
    mesh.nodeFields["test"] = np.arange(5)
    return mesh


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
    sample.add_scalar("a", 1.0)
    sample.add_time_series("b", [0.0, 1.0], [3.0, 4.0])
    return sample


@pytest.fixture()
def dataset(sample_with_tree: Sample) -> Dataset:
    """Generate a Sample objects with a tree."""
    return Dataset.from_list_of_samples([sample_with_tree, sample_with_tree])

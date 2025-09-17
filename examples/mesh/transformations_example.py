# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: plaid-ops
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Transformation examples
#
# ## Introduction
# This notebook illustrates some transformation capabilities provided by plaid-ops.

# %%
import pyvista as pv
pv.set_jupyter_backend('static')

import logging
logging.disable(logging.CRITICAL)

import numpy as np
from datasets import load_dataset
from IPython.display import Image as IPyImage
from IPython.display import display
from PIL import Image as PILImage
from plaid.bridges.huggingface_bridge import (
    huggingface_dataset_to_plaid,
    huggingface_description_to_problem_definition,
)

from plaid_ops.common.visualization import plot_field, plot_sample_field
from plaid_ops.mesh.transformations import (
    compute_bounding_box,
    project_on_other_dataset,
    project_on_regular_grid,
)

hf_dataset = load_dataset(
    "PLAID-datasets/2D_Multiscale_Hyperelasticity", split="all_samples"
)

pb_def = huggingface_description_to_problem_definition(hf_dataset.info.description)
ids = pb_def.get_split("DOE_train")[:2]
dataset, _ = huggingface_dataset_to_plaid(hf_dataset, ids=ids, processes_number=2)

# %% [markdown]
# ## Dataset-wide projection on a constant rectilinear mesh
#
# We start by illustrating the `u1` field from the first sample:

# %%
plot_sample_field(
    dataset[ids[0]],
    "u1",
    title="Unstructured mesh",
    show_edges=True,
    scalar_bar_args={"title": "u1"},
    interactive = False
)

# %% [markdown]
# Then, we project all the dataset meshes onto a constant rectilinear mesh. The process works seamlessly for 2D and 3D meshes, and relies on finite element interpolation, that exploit the order of the underlying finite element representation of the solution:

# %%
bbox = compute_bounding_box(dataset)
dims = [101, 101]
projected_dataset = project_on_regular_grid(
    dataset, dimensions=dims, bbox=bbox, verbose=True
)

plot_sample_field(
    projected_dataset[ids[0]],
    "u1",
    title="Projection on regular grid mesh",
    show_edges=True,
    scalar_bar_args={"title": "u1"},
    interactive = False
)

# %% [markdown]
# We can easily project back to the initial meshes of the dataset, using again finite element interpolation:

# %%
inv_projected_dataset = project_on_other_dataset(
    projected_dataset, dataset, verbose=True
)

plot_sample_field(
    inv_projected_dataset[ids[0]],
    "u1",
    title="Projection back to inital mesh",
    show_edges=True,
    scalar_bar_args={"title": "u1"},
    interactive = False
)

# %% [markdown]
# We compute the error made by both projections, and illustrate it:

# %%
error_1 = inv_projected_dataset[ids[0]].get_field("u1") - dataset[ids[0]].get_field(
    "u1"
)

plot_field(
    dataset[ids[0]],
    field=error_1,
    title="u1 error from projection and inverse projection",
    show_edges=True,
    scalar_bar_args={"title": "u1 error"},
    interactive = False
)

# %% [markdown]
# We compute the norm of the error made by the direct and inverse projections:

# %%
print(
    f"u1 error norm from projection and inverse projection = {np.linalg.norm(error_1)}"
)

# %% [markdown]
# Now, we compare our approach with a more naive one that relies on the value of the field on the nearest node in the input mesh:

# %%
from Muscat.Bridges.CGNSBridge import CGNSToMesh, MeshToCGNS
from Muscat.MeshTools.ConstantRectilinearMeshTools import CreateConstantRectilinearMesh
from plaid.containers.sample import Sample
from scipy.spatial import KDTree

# %% [markdown]
# Computation of the direct projection:

# %%
spacing = np.divide(bbox[1] - bbox[0], np.array(dims) - 1)
background_mesh = CreateConstantRectilinearMesh(
    dimensions=dims, origin=bbox[0], spacing=spacing
)
naive_proj_sample = Sample()
naive_proj_sample.add_tree(MeshToCGNS(background_mesh))

mesh = CGNSToMesh(dataset[ids[0]].get_mesh())
u1 = dataset[ids[0]].get_field("u1")

kdtree = KDTree(mesh.nodes)
_, id_bg_nodes = kdtree.query(background_mesh.nodes)

naive_proj_u1 = u1[id_bg_nodes]

# %% [markdown]
# Computation of the inverse projection and illustration of the error:

# %%
kdtree = KDTree(background_mesh.nodes)
_, id_origin_nodes = kdtree.query(mesh.nodes)

naive_inv_proj_u1 = naive_proj_u1[id_origin_nodes]

error_2 = naive_inv_proj_u1 - dataset[ids[0]].get_field("u1")

plot_field(
    dataset[ids[0]],
    field=error_2,
    title="u1 error from naive projection and inverse projection",
    show_edges=True,
    scalar_bar_args={"title": "u1 error"},
    clim=[min(error_1), max(error_1)],
    interactive = False
)

# %% [markdown]
# We compute the norm of the error made by the naive direct and inverse projections:

# %%
print(
    f"u1 error norm from projection and inverse projection = {np.linalg.norm(error_2)}"
)

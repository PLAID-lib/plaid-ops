# ---
# jupyter:
#   jupytext:
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: plaid-ops
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Feature engineering examples
#
# ## Introduction
# This notebook illustrates some feature engineering capabilities provided by plaid-ops.

# %%
import logging
logging.disable(logging.CRITICAL)

from plaid_ops.common.visualization import plot_field
from plaid_ops.mesh.feature_engineering import (
    compute_sdf,
    update_dataset_with_sdf,
    update_sample_with_sdf,
)

import numpy as np

from datasets.utils.logging import disable_progress_bar
from datasets import load_dataset

from plaid.bridges.huggingface_bridge import (
    huggingface_dataset_to_plaid,
    huggingface_description_to_problem_definition,
)

disable_progress_bar()

# %%
hf_dataset = load_dataset(
    "PLAID-datasets/2D_Multiscale_Hyperelasticity", split="all_samples"
)
pb_def = huggingface_description_to_problem_definition(hf_dataset.info.description)
ids = pb_def.get_split("DOE_train")[:2]
dataset, _ = huggingface_dataset_to_plaid(hf_dataset, ids=ids, processes_number=2, verbose=False)


# %% [markdown]
# ## Dataset-wide signed-distance function computation

# %%
sample = dataset[ids[0]]

print("[before update] 'sdf' in sample fields ?", "sdf" in sample.get_field_names())
updated_sample = update_sample_with_sdf(sample)
print(
    "[after update] 'sdf' in sample fields ?", "sdf" in updated_sample.get_field_names()
)

# %%
print(
    "[before update] 'sdf' in dataset fields ?",
    "sdf" in dataset[ids[0]].get_field_names(),
)
updated_dataset = update_dataset_with_sdf(dataset)
print(
    "[after update] 'sdf' in dataset fields ?",
    "sdf" in updated_dataset[ids[0]].get_field_names(),
)

# %%
sample = dataset[ids[0]]
computed_sdf = compute_sdf(sample)

array_img = plot_field(
    sample,
    field=computed_sdf,
    title="SDF illustration",
    scalar_bar_args={"title": "sdf"},
    interactive = False
)

# %% [markdown]
# This computation relies on the finite element engine provided by Muscat. It computes the exact distance from each node to the boundary, i.e., to the surface elements that define the mesh boundary (for both 2D and 3D meshes seamlessly).
#
# We now illustrate the error introduced by using a naive computation of the SDF, which measures the distance to the nearest point on the boundary.

# %%
from Muscat.Bridges.CGNSBridge import CGNSToMesh
from scipy.spatial import KDTree

mesh = CGNSToMesh(dataset[ids[0]].get_mesh())

ids_holes = mesh.GetNodalTag("Holes").GetIds()
ids_ext_boundary = mesh.GetNodalTag("Ext_bound").GetIds()

kdtree = KDTree(mesh.nodes[np.hstack((ids_holes, ids_ext_boundary))])

naive_sdf, _ = kdtree.query(mesh.nodes)

difference_sdf = computed_sdf - naive_sdf

array_img = plot_field(
    sample,
    field=difference_sdf,
    title="SDF error computation",
    scalar_bar_args={"title": "sdf error"},
    interactive = False
)
"""Module that implements some feature engineering functions on meshes."""

from typing import Optional

from Muscat.Bridges.CGNSBridge import CGNSToMesh
from Muscat.MeshTools.MeshTools import ComputeSignedDistance
from plaid.containers.dataset import Dataset
from plaid.containers.sample import Sample
from plaid.types import Field
from tqdm import tqdm


def compute_sdf(
    sample: Sample,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
) -> Field:
    """Compute the signed distance function (SDF) for a mesh extracted from a Sample.

    This function extracts the mesh from the given Sample (optionally at a specific time,
    base, or zone), converts it to a working Muscat mesh, and computes the signed distance
    function (SDF) at each mesh node.

    Args:
        sample (Sample): The input Sample containing the mesh and fields.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        time (Optional[float]): Simulation time to extract the mesh. If None, uses default.

    Returns:
        Field: The computed signed distance function values at mesh nodes.
    """
    baseNames = [base_name] if base_name is not None else None
    zoneNames = [zone_name] if zone_name is not None else None
    mesh = CGNSToMesh(sample.get_mesh(time), baseNames=baseNames, zoneNames=zoneNames)
    return ComputeSignedDistance(mesh, mesh.nodes)


def update_sample_with_sdf(
    sample: Sample,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    in_place: Optional[bool] = False,
    time: Optional[float] = None,
) -> Sample:
    """Update a Sample by computing and adding the signed distance function (SDF) field.

    Computes the SDF for the mesh in the given Sample and adds it as a new field named "sdf"
    at the vertex location for the specified base and zone. Optionally operates in-place.

    Args:
        sample (Sample): The input Sample to update.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        in_place (Optional[bool]): If True, modifies the Sample in-place. If False, works on a copy.
        time (Optional[float]): Simulation time to extract the mesh. If None, uses default.

    Returns:
        Sample: The Sample with the new "sdf" field added.
    """
    if not in_place:
        sample = sample.copy()
    sdf = compute_sdf(sample, base_name, zone_name, time)
    sample.add_field(
        "sdf",
        sdf,
        zone_name=zone_name,
        base_name=base_name,
        location="Vertex",
        time=time,
        warning_overwrite=False,
    )
    return sample


def update_dataset_with_sdf(
    dataset: Dataset,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    in_place: Optional[bool] = False,
    verbose: Optional[bool] = False,
) -> Dataset:
    """Update a dataset by computing and adding the Signed Distance Function (SDF) field for each sample and mesh time.

    Args:
        dataset (Dataset): The dataset to update. If `in_place` is False, a copy will be modified and returned.
        base_name (Optional[str], optional): The base name to use when computing the SDF. If None, all bases are used. The SDF is computed using the `compute_sdf` function for each sample and mesh time.
        zone_name (Optional[str], optional): The zone name to use when computing the SDF. If None, all zones are used.
        in_place (Optional[bool], optional): If True, modifies the dataset in place. If False, works on a copy. Defaults to False.
        verbose (Optional[bool], optional): If True, displays a progress bar during processing. Defaults to False.

    Returns:
        Dataset: The updated dataset with the SDF field (named "sdf" at the "Vertex" location) added to each sample for each mesh time. Existing fields are not overwritten (`warning_overwrite=False`).
    """
    if not in_place:
        dataset = dataset.copy()
    for sample in tqdm(dataset, total=len(dataset), disable=not verbose):
        for time in sample.meshes.get_all_mesh_times():
            sdf = compute_sdf(sample, base_name, zone_name, time)
            sample.add_field(
                "sdf",
                sdf,
                zone_name=zone_name,
                base_name=base_name,
                location="Vertex",
                time=time,
                warning_overwrite=False,
            )

    return dataset

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
    """Compute the signed distance function (SDF) on a mesh extracted from a Sample.

    This function converts a CGNS mesh into a working mesh, optionally selecting
    specific bases or zones, and then computes the signed distance function on it.

    Args:
        sample (Sample): The input Sample containing the mesh and fields.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        time (Optional[float]): Simulation time to extract the mesh. If None, use default.

    Returns:
        Field: The computed signed distance function field.
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

    This function computes the SDF for the given Sample and attaches it as a new field
    named "sdf" on the selected base/zone and vertices.

    Args:
        sample (Sample): The input Sample to update.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        in_place (Optional[bool]): If True, .
        time (Optional[float]): Simulation time to extract the mesh. If None, use default.

    Returns:
        Sample: The updated Sample containing the new "sdf" field.
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
    """Function to update a dataset with a computed signed distancs function."""
    if not in_place:
        dataset = dataset.copy()
    for sample in tqdm(dataset, total=len(dataset), disable=not verbose):
        for time in sample.get_all_mesh_times():
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

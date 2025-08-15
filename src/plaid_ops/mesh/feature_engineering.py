"""Module that implements some feature engineering functions on meshes."""

from typing import Optional

from Muscat.Bridges.CGNSBridge import CGNSToMesh
from Muscat.MeshTools.MeshTools import ComputeSignedDistance
from plaid.containers.sample import Sample
from plaid.types import FieldType


def compute_sdf(
    sample: Sample,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
) -> FieldType:
    """Compute the signed distance function (SDF) on a mesh extracted from a Sample.

    This function converts a CGNS mesh into a working mesh, optionally selecting
    specific bases or zones, and then computes the signed distance function on it.

    Args:
        sample (Sample): The input Sample containing the mesh and fields.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        time (Optional[float]): Simulation time to extract the mesh. If None, use default.

    Returns:
        FieldType: The computed signed distance function field.
    """
    baseNames = [base_name] if base_name is not None else None
    zoneNames = [zone_name] if zone_name is not None else None
    mesh = CGNSToMesh(sample.get_mesh(time), baseNames=baseNames, zoneNames=zoneNames)
    return ComputeSignedDistance(mesh, mesh.nodes)


def update_sample_with_sdf(
    sample: Sample,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
) -> Sample:
    """Update a Sample by computing and adding the signed distance function (SDF) field.

    This function computes the SDF for the given Sample and attaches it as a new field
    named "sdf" on the selected base/zone and vertices.

    Args:
        sample (Sample): The input Sample to update.
        base_name (Optional[str]): Name of the base to select. If None, all bases are used.
        zone_name (Optional[str]): Name of the zone to select. If None, all zones are used.
        time (Optional[float]): Simulation time to extract the mesh. If None, use default.

    Returns:
        Sample: The updated Sample containing the new "sdf" field.
    """
    sdf = compute_sdf(sample, base_name, zone_name, time)
    sample.add_field(
        "sdf",
        sdf,
        zone_name=zone_name,
        base_name=base_name,
        location="Vertex",
        time=time,
    )
    return sample

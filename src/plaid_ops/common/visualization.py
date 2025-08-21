"""Visualization module."""

from typing import Optional

from Muscat.Bridges.CGNSBridge import CGNSToMesh
from Muscat.Bridges.PyVistaBridge import MeshToPyVista
from plaid.containers.sample import Sample
from plaid.types import FieldType


def _generate_pyvista_mesh(
    sample: Sample,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
):
    baseNames = [base_name] if base_name is not None else None
    zoneNames = [zone_name] if zone_name is not None else None

    muscat_mesh = CGNSToMesh(sample.get_mesh())

    muscat_mesh = CGNSToMesh(
        sample.get_mesh(time), baseNames=baseNames, zoneNames=zoneNames
    )
    return MeshToPyVista(muscat_mesh)


def plot_sample_field(
    sample: Sample,
    field_name: str,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
    **kwargs,
) -> None:
    """Plot a sample field."""
    field = sample.get_field(
        name=field_name, base_name=base_name, zone_name=zone_name, time=time
    )
    plot_field(sample, field, base_name, zone_name, **kwargs)


def plot_field(
    sample: Sample,
    field: FieldType,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    time: Optional[float] = None,
    **kwargs,
) -> None:
    """Plot a given field using a sample geometrical support."""
    sample_ = sample.copy()
    sample_.del_all_fields()
    pv_mesh = _generate_pyvista_mesh(sample_, base_name, zone_name, time)
    pv_mesh.plot(cpos="xy", scalars=field, **kwargs)

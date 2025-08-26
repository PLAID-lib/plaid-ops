"""Visualization module."""

from typing import Optional

import pyvista as pv
from Muscat.Bridges.CGNSBridge import CGNSToMesh
from Muscat.Bridges.PyVistaBridge import MeshToPyVista
from plaid.containers.sample import Sample
from plaid.types import Field

pv.OFF_SCREEN = True


def _generate_pyvista_mesh(
    sample: Sample,
    time: Optional[float] = None,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
):
    zoneNames = [zone_name] if zone_name is not None else None
    baseNames = [base_name] if base_name is not None else None
    time = time if time is not None else 0.0

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
    title: Optional[str] = None,
    **kwargs,
) -> pv.pyvista_ndarray:
    """Plot a sample field."""
    field = sample.get_field(
        name=field_name, base_name=base_name, zone_name=zone_name, time=time
    )
    return plot_field(sample, field, base_name, zone_name, time, title, **kwargs)


def plot_field(
    sample: Sample,
    field: Field,
    time: Optional[float] = None,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    title: Optional[str] = None,
    pytest: Optional[bool] = False,
    **kwargs,
) -> pv.pyvista_ndarray:
    """Plot a given field using a sample geometrical support."""
    sample_ = sample.copy()
    sample_.del_all_fields()
    pv_mesh = _generate_pyvista_mesh(sample_, time, base_name, zone_name)

    plotter = pv.Plotter()
    plotter.view_xy()
    plotter.add_mesh(pv_mesh, scalars=field, **kwargs)
    plotter.reset_camera()
    plotter.camera.Zoom(1.0)

    if title:
        plotter.add_text(title, font_size=12, color="black", position="upper_edge")

    if pytest:
        img_array = 0.0
    else:  # pragma: no cover
        img_array = plotter.screenshot(return_img=True)
    plotter.close()

    return img_array

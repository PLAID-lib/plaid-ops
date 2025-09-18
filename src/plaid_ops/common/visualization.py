"""Visualization module."""

from typing import Optional

import pyvista as pv
from Muscat.Bridges.CGNSBridge import CGNSToMesh
from Muscat.Bridges.PyVistaBridge import MeshToPyVista
from plaid.containers.sample import Sample
from plaid.types import Field


def _generate_pyvista_mesh(
    sample: Sample,
    time: Optional[float] = None,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
) -> pv.PolyData:
    """Generate a PyVista mesh from a Sample.

    Args:
        sample (Sample): The input Sample containing the mesh data.
        time (Optional[float], optional): The simulation time to extract the mesh. Defaults to None.
        base_name (Optional[str], optional): The base name to use when extracting the mesh. Defaults to None.
        zone_name (Optional[str], optional): The zone name to use when extracting the mesh. Defaults to None.

    Returns:
        pv.PolyData: The generated PyVista mesh.
    """
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
    interactive: bool = True,
    **kwargs,
) -> Optional[pv.pyvista_ndarray]:
    """Plot a field from a sample using PyVista.

    Args:
        sample (Sample): The input Sample containing mesh and field data.
        field_name (str): The name of the field to plot.
        base_name (Optional[str], optional): The base name for mesh extraction. Defaults to None.
        zone_name (Optional[str], optional): The zone name for mesh extraction. Defaults to None.
        time (Optional[float], optional): The simulation time to extract the field. Defaults to None.
        title (Optional[str], optional): The title for the plot. Defaults to None.
        interactive (bool): If True, make the plot persist on the screen. Defaults to True.
        **kwargs: Additional keyword arguments passed to `plot_field`.

    Returns:
        Optional[pv.pyvista_ndarray]: Screenshot image as a NumPy array if ``interactive=False``,
        otherwise ``None``.
    """
    field = sample.get_field(
        name=field_name, base_name=base_name, zone_name=zone_name, time=time
    )
    plot_field(sample, field, base_name, zone_name, time, title, interactive, **kwargs)


def plot_field(
    sample: Sample,
    field: Field,
    time: Optional[float] = None,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    title: Optional[str] = None,
    interactive: bool = True,
    **kwargs,
) -> Optional[pv.pyvista_ndarray]:
    """Plot a given field using a sample geometrical support.

    Args:
        sample (Sample): The input Sample containing mesh and field data.
        field (Field): The field to plot.
        time (Optional[float], optional): The simulation time to extract the field. Defaults to None.
        base_name (Optional[str], optional): The base name for mesh extraction. Defaults to None.
        zone_name (Optional[str], optional): The zone name for mesh extraction. Defaults to None.
        title (Optional[str], optional): The title for the plot. Defaults to None.
        interactive (bool): If True, make the plot persist on the screen. Defaults to True.
        **kwargs: Additional keyword arguments passed to `pv.Plotter.meshes.add_tree`.

    Returns:
        Optional[pv.pyvista_ndarray]: Screenshot image as a NumPy array if ``interactive=False``,
        otherwise ``None``.
    """
    if not interactive:
        import platform

        if (
            platform.system() != "Linux"
        ):  # pragma: no cover (coverage computed on Linux CI only)
            print("Offscreen rendering is only supported on Linux with vtk-osmesa.")
            return None

    sample_ = sample.copy()
    sample_.del_all_fields()
    pv_mesh = _generate_pyvista_mesh(sample_, time, base_name, zone_name)

    plotter = pv.Plotter(off_screen=not interactive)
    plotter.view_xy()
    plotter.add_mesh(pv_mesh, scalars=field, **kwargs)
    plotter.reset_camera()
    plotter.camera.Zoom(1.0)

    if title:
        plotter.add_text(title, font_size=12, color="black", position="upper_edge")

    if interactive:  # pragma: no cover (cannot run in CI)
        plotter.show()
        return None

    # Offscreen rendering → return screenshot
    img = plotter.show(screenshot=True)
    plotter.close()
    return img

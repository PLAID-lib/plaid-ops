"""Module implementing some transformations on datasets."""

from typing import Optional, Sequence, Tuple

import numpy as np
from Muscat.Bridges.CGNSBridge import CGNSToMesh, MeshToCGNS
from Muscat.FE.FETools import PrepareFEComputation
from Muscat.FE.Fields.FEField import FEField
from Muscat.MeshContainers.Filters.FilterObjects import ElementFilter
from Muscat.MeshTools.ConstantRectilinearMeshTools import CreateConstantRectilinearMesh
from Muscat.MeshTools.MeshFieldOperations import GetFieldTransferOp
from plaid.containers.dataset import Dataset
from plaid.containers.sample import Sample
from plaid.types import Array
from plaid.utils.stats import OnlineStatistics
from tqdm import tqdm


def compute_bounding_box(
    dataset: Dataset,
    times: Optional[Sequence] = None,
    base_names: Optional[Sequence[str]] = None,
    zone_names: Optional[Sequence[str]] = None,
) -> Tuple[Array, Array]:
    """Compute the axis-aligned bounding box over all nodes in all samples of a dataset.

    Args:
        dataset (Dataset): The dataset containing samples with mesh nodes.
        times (Optional[Sequence], optional): Specific times to consider. If None, uses all available times.
        base_names (Optional[Sequence[str]], optional): The base names of the meshes to use. If None, uses all available bases.
        zone_names (Optional[Sequence[str]], optional): The zone names of the meshes to use. If None, uses all available zones.

    Returns:
        Tuple[Array, Array]: A tuple (mins, maxs) where mins is the minimum coordinate values and maxs is the maximum coordinate values across all nodes in the dataset.
    """
    stats = OnlineStatistics()
    for sample in dataset:
        mesh_times = times if times is not None else sample.get_all_mesh_times()
        for time in mesh_times:
            base_names_iter = base_names or sample.get_base_names(time=time)
            for base_name in base_names_iter:
                zone_names_iter = zone_names or sample.get_zone_names(
                    time=time, base_name=base_name, unique=True
                )
                for zone_name in zone_names_iter:
                    nodes = sample.get_nodes(
                        time=time, base_name=base_name, zone_name=zone_name
                    )
                    stats.add_samples(nodes)
    mins = stats.min.squeeze()
    maxs = stats.max.squeeze()
    return (mins, maxs)


def project_on_regular_grid(
    dataset: Dataset,
    dimensions: Sequence[int],
    bbox: Sequence[Array],
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    method: Optional[str] = "Interp/Clamp",
    verbose: Optional[bool] = False,
) -> Dataset:
    """Project all samples of a dataset onto a regular rectilinear grid.

    This function creates a regular grid defined by the given dimensions and bounding box,
    and projects all fields from each sample in the dataset onto this grid using the specified method.

    The available projection methods are:
        - "Interp/Nearest"
        - "Nearest/Nearest"
        - "Interp/Clamp"
        - "Interp/Extrap"
        - "Interp/ZeroFill"

    Args:
        dataset (Dataset): The dataset containing samples to project.
        dimensions (Sequence[int]): Number of grid points along each axis (e.g., [nx, ny, nz]).
        bbox (Sequence[Array]): Bounding box as (mins, maxs), where each is an array of coordinates.
        base_name (Optional[str], optional): Name of the mesh base to use. If None, uses all bases.
        zone_name (Optional[str], optional): Name of the mesh zone to use. If None, uses all zones.
        method (Optional[str], optional): Projection method. Defaults to "Interp/Clamp".
        verbose (Optional[bool], optional): If True, shows progress bar. Defaults to False.

    Returns:
        Dataset: A new dataset with all samples projected onto the regular grid.
    """
    dims = tuple(dimensions)

    mins = bbox[0]
    maxs = bbox[1]

    assert len(dims) == len(mins), (
        "`len(dimensions)` should be the same as the dimension of the bounding box of the dataset"
    )
    assert len(dims) == len(maxs), (
        "`len(dimensions)` should be the same as the dimension of the bounding box of the dataset"
    )

    spacing = np.divide(maxs - mins, np.array(dims) - 1)

    background_mesh = CreateConstantRectilinearMesh(
        dimensions=dims, origin=mins, spacing=spacing
    )

    baseNames = [base_name] if base_name is not None else None
    zoneNames = [zone_name] if zone_name is not None else None

    projected_samples = []

    for sample in tqdm(dataset, total=len(dataset), disable=not verbose):
        projected_sample = Sample()

        for sn in sample.get_scalar_names():
            projected_sample.add_scalar(sn, sample.get_scalar(sn))

        for tn in sample.get_time_series_names():
            ts = sample.get_time_series(tn)
            projected_sample.add_time_series(tn, ts[0], ts[1])

        for time in sample.get_all_mesh_times():
            projected_sample.add_tree(
                MeshToCGNS(background_mesh, exportOriginalIDs=False)
            )

            mesh = CGNSToMesh(
                sample.get_mesh(time=time), baseNames=baseNames, zoneNames=zoneNames
            )

            space, numberings, _, _ = PrepareFEComputation(mesh, numberOfComponents=1)
            field = FEField("", mesh=mesh, space=space, numbering=numberings[0])
            op, _, _ = GetFieldTransferOp(
                field,
                background_mesh.nodes,
                method=method,
                verbose=False,
                elementFilter=ElementFilter(),
            )

            for fn in sample.get_field_names():
                field = sample.get_field(
                    fn, base_name=base_name, zone_name=zone_name, time=time
                )
                if field is not None:
                    projected_sample.add_field(
                        fn,
                        op.dot(field),
                        base_name=base_name,
                        zone_name=zone_name,
                        time=time,
                        warning_overwrite=False,
                    )

        projected_samples.append(projected_sample)

    projected_dataset = Dataset()
    projected_dataset.add_samples(projected_samples, dataset.get_sample_ids())

    return projected_dataset


def project_on_other_dataset(
    dataset_source: Dataset,
    dataset_target: Dataset,
    base_name: Optional[str] = None,
    zone_name: Optional[str] = None,
    method: Optional[str] = "Interp/Clamp",
    verbose: Optional[bool] = False,
    in_place: Optional[bool] = False,
) -> Dataset:
    """Project all samples of a source dataset onto the mesh geometry of a target dataset.

    For each sample (with matching sample id and time) in `dataset_source` and `dataset_target`,
    this function transfers all nodal fields from the source mesh to the target mesh using the specified method.
    The mesh geometry of the target dataset is preserved, but its nodal fields are replaced by the projected fields from the source.

    The available projection methods are:
        - "Interp/Nearest"
        - "Nearest/Nearest"
        - "Interp/Clamp"
        - "Interp/Extrap"
        - "Interp/ZeroFill"

    Args:
        dataset_source (Dataset): The dataset providing the source fields and meshes.
        dataset_target (Dataset): The dataset providing the target mesh geometry.
        base_name (Optional[str], optional): Name of the mesh base to use. If None, uses all bases.
        zone_name (Optional[str], optional): Name of the mesh zone to use. If None, uses all zones.
        method (Optional[str], optional): Projection method. Defaults to "Interp/Clamp".
        verbose (Optional[bool], optional): If True, shows progress bar. Defaults to False.
        in_place (Optional[bool], optional): If True, modifies `dataset_target` in place. If False, works on a copy.

    Returns:
        Dataset: The target dataset with nodal fields replaced by the projected fields from the source dataset.
    """
    assert np.allclose(
        dataset_source.get_sample_ids(), dataset_target.get_sample_ids()
    ), "`dataset_source` and `dataset_target` should have same sample ids"

    if not in_place:
        dataset_target = dataset_target.copy()

    baseNames = [base_name] if base_name is not None else None
    zoneNames = [zone_name] if zone_name is not None else None

    for sample_source, sample_target in tqdm(
        zip(dataset_source, dataset_target),
        total=len(dataset_source),
        disable=not verbose,
    ):
        assert np.allclose(
            sample_source.get_all_mesh_times(), sample_target.get_all_mesh_times()
        ), "`sample_source` and `sample_target` should have same time steps"

        for time in sample_source.get_all_mesh_times():
            mesh_source = CGNSToMesh(
                sample_source.get_mesh(time=time),
                baseNames=baseNames,
                zoneNames=zoneNames,
            )
            mesh_target = CGNSToMesh(
                sample_target.get_mesh(time=time),
                baseNames=baseNames,
                zoneNames=zoneNames,
            )
            mesh_target.nodeFields = {}
            mesh_target.elemFields = {}

            sample_target.del_tree(time)

            space, numberings, _, _ = PrepareFEComputation(
                mesh_source, numberOfComponents=1
            )
            field = FEField("", mesh=mesh_source, space=space, numbering=numberings[0])
            op, _, _ = GetFieldTransferOp(
                field,
                mesh_target.nodes,
                method=method,
                verbose=False,
                elementFilter=ElementFilter(),
            )

            for fn, field in mesh_source.nodeFields.items():
                mesh_target.nodeFields[fn] = op.dot(field)

            sample_target.add_tree(MeshToCGNS(mesh_target, exportOriginalIDs=False))

    return dataset_target

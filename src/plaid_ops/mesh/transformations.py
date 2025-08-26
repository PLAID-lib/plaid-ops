"""Module implmenting some transformations on datasets."""

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
from tqdm import tqdm


def compute_bounding_box(
    dataset: Dataset,
    base_name: Optional[str] = None,
) -> Tuple[Array, Array]:
    """Compute a bonding box over all the samples of a dataset."""
    _id = dataset.get_sample_ids()[0]
    first_nodes = dataset[_id].get_nodes(base_name=base_name)
    mins = np.min(first_nodes, axis=0)
    maxs = np.max(first_nodes, axis=0)
    for sample in dataset:
        for time in sample.get_all_mesh_times():
            nodes = sample.get_nodes(base_name=base_name, time=time)
            mins = np.minimum(mins, nodes.min(axis=0))
            maxs = np.maximum(maxs, nodes.max(axis=0))
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
    """Project all the samples of a dataset on a regular grid.

    The available methods are:

    - "Interp/Nearest"
    - "Nearest/Nearest"
    - "Interp/Clamp"
    - "Interp/Extrap"
    - "Interp/ZeroFill".
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

            space, numberings, offset, NGauss = PrepareFEComputation(
                mesh, numberOfComponents=1
            )
            field = FEField("", mesh=mesh, space=space, numbering=numberings[0])
            op, status, entities = GetFieldTransferOp(
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
    """Project all the samples of a dataset on the geometrical supports from another dataset.

    The available methods are:

    - "Interp/Nearest"
    - "Nearest/Nearest"
    - "Interp/Clamp"
    - "Interp/Extrap"
    - "Interp/ZeroFill".
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

            space, numberings, offset, NGauss = PrepareFEComputation(
                mesh_source, numberOfComponents=1
            )
            field = FEField("", mesh=mesh_source, space=space, numbering=numberings[0])
            op, status, entities = GetFieldTransferOp(
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

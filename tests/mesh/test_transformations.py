from plaid_ops.mesh.transformations import (
    compute_bounding_box,
    project_on_other_datset,
    project_on_regular_grid,
)


class Test_Transformations:
    def test_compute_bounding_box(self, dataset):
        compute_bounding_box(dataset)

    def test_project_on_regular_grid(self, dataset):
        bbox = compute_bounding_box(dataset)
        project_on_regular_grid(dataset, (3, 3), bbox)

    def test_project_on_other_datset(self, dataset):
        project_on_other_datset(dataset, dataset)

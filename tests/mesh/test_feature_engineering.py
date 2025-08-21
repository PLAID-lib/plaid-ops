from plaid_ops.mesh.feature_engineering import (
    compute_sdf,
    update_dataset_with_sdf,
    update_sample_with_sdf,
)


class Test_Feature_Engineering:
    def test_compute_sdf(self, sample_with_tree):
        compute_sdf(sample_with_tree)

    def test_update_sample_with_sdf(self, sample_with_tree):
        update_sample_with_sdf(sample_with_tree)

    def test_update_dataset_with_sdf(self, dataset):
        update_dataset_with_sdf(dataset)

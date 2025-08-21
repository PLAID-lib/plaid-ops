from contextlib import contextmanager

import numpy as np
import pyvista as pv

from plaid_ops.common.visualization import (
    plot_field,
    plot_sample_field,
)


@contextmanager
def nogui():
    old_state = pv.OFF_SCREEN
    pv.OFF_SCREEN = True
    try:
        yield
    finally:
        pv.OFF_SCREEN = old_state


class Test_Visualization:
    def test_plot_sample_field(self, sample_with_tree):
        with nogui():
            plot_sample_field(sample_with_tree, "test")

    def test_plot_field(self, sample_with_tree):
        with nogui():
            plot_field(sample_with_tree, 1.0 + np.arange(5))

import os

import numpy as np
import pyvista as pv

from plaid_ops.common.visualization import (
    plot_field,
    plot_sample_field,
)

pv.set_jupyter_backend("static")

os.environ["PYVISTA_OFF_SCREEN"] = "true"

if os.name != "nt" and "DISPLAY" not in os.environ:
    try:
        pv.start_xvfb()
    except Exception as e:
        print("Could not start Xvfb:", e)


class Test_Visualization:
    def test_plot_sample_field(self, sample_with_tree):
        plot_sample_field(sample_with_tree, "test", interactive=False)

    def test_plot_field(self, sample_with_tree):
        plot_field(sample_with_tree, 1.0 + np.arange(5), interactive=False)

    def test_plot_field_with_title(self, sample_with_tree):
        plot_field(
            sample_with_tree, 1.0 + np.arange(5), title="test_title", interactive=False
        )

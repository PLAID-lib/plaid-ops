"""Module that implements PLAID common ops."""


def _in_notebook():
    try:
        from IPython import get_ipython

        return "IPKernelApp" in get_ipython().config
    except Exception:
        return False


if _in_notebook():  # pragma: no cover (not computed in CI)
    import os

    import pyvista as pv

    pv.set_jupyter_backend("static")

    os.environ["PYVISTA_OFF_SCREEN"] = "true"

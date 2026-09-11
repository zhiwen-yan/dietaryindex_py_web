"""Reference data for FISI/FII calculations."""

from functools import lru_cache
from importlib import resources

import pandas as pd


FISI_FLAVONOID_COMPONENTS = (
    "Flavan_3_ols",
    "Flavanones",
    "Flavones",
    "Flavonols",
    "Isoflavones",
)


@lru_cache(maxsize=2)
def load_fisi_nrv(version="usda"):
    """Load FISI nutrient reference values.

    Parameters
    ----------
    version : {"usda", "china"}
        The NRV reference standard. China NRVs are supplemented with USDA rows
        for components not present in the China table, matching the R package.
    """
    version = str(version).lower()
    if version not in {"usda", "china"}:
        raise ValueError('version must be either "usda" or "china".')

    filename = "nrvs_china.csv" if version == "china" else "nrvs_usda.csv"
    with resources.files("dietaryindex.data").joinpath(filename).open(
        "r", encoding="utf-8"
    ) as handle:
        nrv = pd.read_csv(handle)

    nrv.columns = [str(col).strip() for col in nrv.columns]
    missing = {"Variable", "TIS", "NRVs"} - set(nrv.columns)
    if missing:
        raise ValueError(f"NRV file missing expected columns: {sorted(missing)}")

    nrv = nrv.copy()
    nrv["Variable"] = nrv["Variable"].astype(str).str.strip().str.replace(" ", "_")
    nrv["TIS"] = pd.to_numeric(nrv["TIS"], errors="coerce")
    nrv["NRVs"] = pd.to_numeric(nrv["NRVs"], errors="coerce")

    if version == "china":
        usda = load_fisi_nrv("usda")
        usda_only = usda[~usda["Variable"].isin(nrv["Variable"])]
        if not usda_only.empty:
            nrv = pd.concat([nrv, usda_only], ignore_index=True)

    return nrv.reset_index(drop=True)


def fisi_component_names(version="usda", include_flavonoids=False):
    """Return component names used by a FISI calculation."""
    nrv = load_fisi_nrv(version)
    variables = nrv["Variable"].tolist()
    if not include_flavonoids:
        variables = [
            variable
            for variable in variables
            if variable not in FISI_FLAVONOID_COMPONENTS
        ]
    return variables

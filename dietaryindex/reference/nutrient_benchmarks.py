"""Shared nutrient benchmark tables for extended dietary indices."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from dietaryindex.reference.fisi_nrv import load_fisi_nrv


_SUPPLEMENTAL_BENCHMARKS = {
    "usda": {
        "Calcium": 1300.0,
        "Potassium": 4700.0,
        "Sodium": 2300.0,
        "Phosphorus": 700.0,
        "Added_sugar": 50.0,
        "Total_carotenoids": 6000.0,
    },
    "china": {
        "Calcium": 800.0,
        "Potassium": 2000.0,
        "Sodium": 2000.0,
        "Phosphorus": 700.0,
        "Added_sugar": 50.0,
        "Total_carotenoids": 6000.0,
    },
}


# Fulgoni, Keast, and Drewnowski (J Nutr. 2009;139:1549-1554),
# doi:10.3945/jn.108.101360. The original table reports vitamin A as
# 5,000 IU and vitamin E as 30 IU. The public API uses NHANES-compatible
# metric units, so these are represented as 1,500 ug RAE and 20 mg
# alpha-tocopherol, respectively. This table is deliberately independent
# of FISI NRVs and of the configurable NAR/MAR/INQ benchmark profiles.
NRF9_3_2009_METRIC_BENCHMARKS = {
    "Protein": 50.0,
    "Fiber": 25.0,
    "Vitamin_A": 1500.0,
    "Vitamin_C": 60.0,
    "Vitamin_E": 20.0,
    "Calcium": 1000.0,
    "Iron": 18.0,
    "Magnesium": 400.0,
    "Potassium": 3500.0,
    "Saturated_fat": 20.0,
    "Added_sugar": 50.0,
    "Sodium": 2400.0,
}

NRF9_3_DEFAULT_VERSION = "nrf9.3_2009_metric_capped_lim"
NRF9_3_UNCAPPED_LIM_VERSION = "nrf9.3_2009_metric_uncapped_lim"


def normalize_nrf_version(version: str) -> str:
    """Return an explicit NRF9.3 cap-policy version identifier.

    The pre-0.2.1 identifier did not state how LIM3 values above 100% MRV
    were handled.  It is retained as a compatibility alias for the corrected
    capped-LIM default, while the former uncapped behavior remains available
    only through an explicit version name.
    """

    normalized = str(version).strip().lower().replace("-", "_")
    aliases = {
        "nrf9.3_2009_metric": NRF9_3_DEFAULT_VERSION,
        "nrf9_3_2009_metric": NRF9_3_DEFAULT_VERSION,
        "nrf9.3_2009_metric_capped_lim": NRF9_3_DEFAULT_VERSION,
        "nrf9_3_2009_metric_capped_lim": NRF9_3_DEFAULT_VERSION,
        "nrf9.3_2009_metric_uncapped_lim": NRF9_3_UNCAPPED_LIM_VERSION,
        "nrf9_3_2009_metric_uncapped_lim": NRF9_3_UNCAPPED_LIM_VERSION,
    }
    try:
        return aliases[normalized]
    except KeyError as exc:
        allowed = f'"{NRF9_3_DEFAULT_VERSION}" or "{NRF9_3_UNCAPPED_LIM_VERSION}"'
        raise ValueError(f"NRF version must be {allowed}.") from exc


@lru_cache(maxsize=2)
def load_nutrient_benchmarks(version: str = "usda") -> pd.DataFrame:
    """Return a simple nutrient benchmark table keyed by nutrient name."""

    version = str(version).lower()
    if version not in {"usda", "china"}:
        raise ValueError('version must be either "usda" or "china".')

    base = load_fisi_nrv(version)[["Variable", "NRVs"]].rename(
        columns={"Variable": "nutrient", "NRVs": "benchmark"}
    )
    extra = pd.DataFrame(
        {
            "nutrient": list(_SUPPLEMENTAL_BENCHMARKS[version].keys()),
            "benchmark": list(_SUPPLEMENTAL_BENCHMARKS[version].values()),
        }
    )

    merged = pd.concat([base, extra], ignore_index=True)
    merged["nutrient"] = merged["nutrient"].astype(str).str.strip().str.replace(" ", "_")
    merged["benchmark"] = pd.to_numeric(merged["benchmark"], errors="coerce")
    merged = merged.dropna(subset=["benchmark"]).drop_duplicates(subset=["nutrient"], keep="last")
    return merged.reset_index(drop=True)


def get_benchmark_lookup(version: str = "usda") -> dict[str, float]:
    table = load_nutrient_benchmarks(version)
    return dict(zip(table["nutrient"], table["benchmark"]))


def get_nrf_benchmark_lookup(edition: str = NRF9_3_DEFAULT_VERSION) -> dict[str, float]:
    """Return the fixed published NRF9.3 benchmark profile.

    ``edition`` is explicit to prevent an NRF calculation from silently
    falling back to the separate FISI/NAR benchmark tables.
    """

    normalize_nrf_version(edition)
    return NRF9_3_2009_METRIC_BENCHMARKS.copy()

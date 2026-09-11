"""China Dietary Inflammatory Index (CHINA-DII)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from dietaryindex.reference.china_dii import CHINA_DII_REFERENCE, CHINA_DII_VARIABLE_ORDER


def _resolve_n_rows(data, respondent_id, kwargs) -> int:
    if data is not None:
        return len(data)
    if respondent_id is not None and not isinstance(respondent_id, str):
        return len(np.asarray(respondent_id))
    for value in kwargs.values():
        if value is not None:
            if isinstance(value, pd.DataFrame):
                return len(value)
            if isinstance(value, (pd.Series, np.ndarray, list, tuple)):
                return len(value)
    raise ValueError("Unable to infer the number of observations for CHINA-DII.")


def _normalize_id(data, respondent_id, n_rows: int):
    if respondent_id is None:
        return pd.Series(range(1, n_rows + 1), name="RESPONDENTID")
    if isinstance(respondent_id, str):
        if data is None:
            raise ValueError("String respondent_id requires `data` to be a DataFrame.")
        return data[respondent_id].reset_index(drop=True).rename("RESPONDENTID")
    return pd.Series(np.asarray(respondent_id), name="RESPONDENTID").reset_index(drop=True)


def compute_china_dii(
    data,
    respondent_id=None,
    **kwargs,
):
    """Compute CHINA-DII using the published Chinese adult reference table."""

    n_rows = _resolve_n_rows(data, respondent_id, kwargs)
    rid = _normalize_id(data, respondent_id, n_rows)

    records = []
    for i in range(n_rows):
        rec = {"RESPONDENTID": rid.iloc[i]}
        for key in CHINA_DII_VARIABLE_ORDER:
            if key in kwargs and kwargs[key] is not None:
                val = kwargs[key]
                if isinstance(val, pd.DataFrame):
                    rec[key] = val.iloc[i, 0]
                elif isinstance(val, pd.Series):
                    rec[key] = val.iloc[i]
                elif isinstance(val, (np.ndarray, list, tuple)):
                    rec[key] = val[i]
                else:
                    rec[key] = float(val)
            else:
                rec[key] = np.nan
        records.append(rec)

    long_df = pd.DataFrame(records)
    melted = long_df.melt(
        id_vars=["RESPONDENTID"],
        value_vars=list(CHINA_DII_VARIABLE_ORDER),
        var_name="Variable",
        value_name="Value",
    )

    ref_df = pd.DataFrame(
        {
            "Variable": key,
            "Overall_inflammatory_score": ref["inflammatory_score"],
            "China_mean": ref["china_mean"],
            "China_sd": ref["china_sd"],
        }
        for key, ref in CHINA_DII_REFERENCE.items()
    )

    merged = melted.merge(ref_df, on="Variable", how="left")
    merged["Z_SCORE"] = np.where(
        merged["China_sd"] > 0,
        (merged["Value"] - merged["China_mean"]) / merged["China_sd"],
        0.0,
    )
    merged["PERCENTILE"] = norm.cdf(merged["Z_SCORE"]) * 2 - 1
    merged["IND_SCORE"] = merged["PERCENTILE"] * merged["Overall_inflammatory_score"]

    # There is exactly one record per respondent/component.  ``pivot`` keeps
    # an observed missing intake as missing; ``pivot_table(..., aggfunc='sum')``
    # would silently turn an all-missing cell into a zero contribution.
    wide = merged.pivot(
        index="RESPONDENTID",
        columns="Variable",
        values="IND_SCORE",
    ).reset_index()

    ordered_component_cols = []
    for key in CHINA_DII_VARIABLE_ORDER:
        source_col = key if key in wide.columns else None
        output_col = f"CHINADII_{key}"
        if source_col is None:
            wide[output_col] = 0.0
        else:
            wide[output_col] = pd.to_numeric(wide[source_col], errors="coerce")
        ordered_component_cols.append(output_col)

    coverage = (
        long_df.groupby("RESPONDENTID", dropna=False)[list(CHINA_DII_VARIABLE_ORDER)]
        .apply(lambda frame: int(frame.notna().any(axis=0).sum()))
        .rename("Components_Used")
        .reset_index()
    )
    wide = wide.merge(coverage, on="RESPONDENTID", how="left")
    wide["CHINADII_ALL"] = wide[ordered_component_cols].sum(axis=1, min_count=1)
    wide.loc[wide["Components_Used"].eq(0), "CHINADII_ALL"] = np.nan

    ordered_cols = ["RESPONDENTID", "CHINADII_ALL", "Components_Used"] + ordered_component_cols
    return wide[ordered_cols].reset_index(drop=True)


__all__ = ["compute_china_dii"]

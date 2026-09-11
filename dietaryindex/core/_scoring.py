"""General scoring utilities shared across dietary indices.

This module now exposes two layers of helpers:

1. Direct scoring helpers used by the existing translated indices.
2. A reusable reference-cutoff engine for future indices that depend on
   sample medians, quantiles, or sex-specific reference distributions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd


REFERENCE_METHOD_PROBABILITIES = {
    "median": (0.5,),
    "quartile": (0.0, 0.25, 0.5, 0.75, 1.0),
    "quintile": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    "decile": tuple(np.linspace(0.0, 1.0, 11)),
}

REFERENCE_METADATA_COLUMNS = {
    "variable",
    "method",
    "rank",
    "prob",
    "cutoff",
    "n_non_missing",
}


def _safe_nanquantile(a, q):
    """Safely calculate nanquantiles when the input contains infinite values."""
    a = np.asarray(a, dtype=float)
    is_inf = np.isinf(a)
    is_pos_inf = is_inf & (a > 0)
    is_neg_inf = is_inf & (a < 0)
    if not is_inf.any():
        return np.nanquantile(a, q)
    finite_a = a[~is_inf & ~np.isnan(a)]
    if len(finite_a) == 0:
        return np.nanquantile(a, q)
    max_val = np.nanmax(finite_a)
    min_val = np.nanmin(finite_a)
    huge_pos = max_val + 1e15
    huge_neg = min_val - 1e15
    a_mapped = np.where(is_pos_inf, huge_pos, np.where(is_neg_inf, huge_neg, a))
    quantiles = np.nanquantile(a_mapped, q)
    threshold_pos = max_val + 1e14
    threshold_neg = min_val - 1e14
    return np.where(
        quantiles > threshold_pos,
        np.inf,
        np.where(quantiles < threshold_neg, -np.inf, quantiles),
    )


def _normalize_probabilities(method: str, probs: Sequence[float] | None = None) -> np.ndarray:
    method = str(method).lower()
    if probs is None:
        if method not in REFERENCE_METHOD_PROBABILITIES:
            raise ValueError(f"Unsupported reference method: {method}")
        probs = REFERENCE_METHOD_PROBABILITIES[method]
    probs_arr = np.asarray(probs, dtype=float)
    if probs_arr.ndim != 1 or probs_arr.size == 0:
        raise ValueError("Reference probabilities must be a one-dimensional sequence.")
    if np.any(np.diff(probs_arr) < 0):
        raise ValueError("Reference probabilities must be sorted in ascending order.")
    if probs_arr[0] < 0 or probs_arr[-1] > 1:
        raise ValueError("Reference probabilities must fall within [0, 1].")
    return probs_arr


def _normalize_group_columns(groupby) -> list[str]:
    if groupby is None:
        return []
    if isinstance(groupby, str):
        return [groupby]
    return [str(col) for col in groupby]


def _coerce_numeric_series(actual, name: str = "value") -> pd.Series:
    if isinstance(actual, pd.Series):
        series = actual.reset_index(drop=True)
        if series.name is None:
            series.name = name
    else:
        series = pd.Series(actual, name=name)
    return pd.to_numeric(series, errors="coerce")


def fit_reference_cutoffs(
    data,
    columns: Sequence[str] | None = None,
    *,
    method: str = "quintile",
    groupby=None,
    probs: Sequence[float] | None = None,
) -> pd.DataFrame:
    """Fit reusable reference cutoffs from a dataset.

    Parameters
    ----------
    data:
        A DataFrame or Series containing the variables used to estimate the
        reference distribution.
    columns:
        Variable columns to fit. When omitted, all non-group columns are used.
    method:
        One of ``median``, ``quartile``, ``quintile``, ``decile`` or a custom
        method name when ``probs`` is explicitly supplied.
    groupby:
        Optional grouping column(s), such as ``gender``. Separate reference
        tables are generated for each stratum.
    probs:
        Optional explicit probabilities. This is useful for custom reference
        grids while still preserving the same export format.

    Returns
    -------
    pandas.DataFrame
        A long-format table with one row per cutoff. The table is deliberately
        tidy so it can be exported to CSV and reused later.
    """

    method = str(method).lower()
    probabilities = _normalize_probabilities(method, probs=probs)
    group_cols = _normalize_group_columns(groupby)

    if isinstance(data, pd.Series):
        series_name = data.name or "value"
        df = data.to_frame(name=series_name)
        if columns is None:
            columns = [series_name]
    else:
        df = pd.DataFrame(data).copy()
        if columns is None:
            columns = [col for col in df.columns if col not in group_cols]

    columns = list(dict.fromkeys(columns or []))
    if not columns:
        raise ValueError("At least one variable column is required to fit references.")

    missing_cols = [col for col in [*group_cols, *columns] if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing columns for reference fitting: {missing_cols}")

    rows = []
    work_df = df[group_cols + columns].copy()
    if group_cols:
        grouped = work_df.groupby(group_cols, dropna=False, sort=True)
        iterator = grouped
    else:
        iterator = [((), work_df)]

    for group_key, frame in iterator:
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        base = dict(zip(group_cols, group_key)) if group_cols else {}

        for column in columns:
            values = pd.to_numeric(frame[column], errors="coerce").to_numpy(dtype=float)
            cutoff_values = np.asarray(_safe_nanquantile(values, probabilities), dtype=float).reshape(-1)
            valid_count = int(np.sum(~np.isnan(values)))

            for rank, (prob, cutoff) in enumerate(zip(probabilities, cutoff_values)):
                rows.append(
                    {
                        **base,
                        "variable": column,
                        "method": method,
                        "rank": rank,
                        "prob": float(prob),
                        "cutoff": float(cutoff),
                        "n_non_missing": valid_count,
                    }
                )

    result_columns = group_cols + [
        "variable",
        "method",
        "rank",
        "prob",
        "cutoff",
        "n_non_missing",
    ]
    return pd.DataFrame(rows, columns=result_columns)


def get_reference_group_columns(reference) -> list[str]:
    """Return grouping columns carried by a reference-cutoff table."""
    reference_df = pd.DataFrame(reference)
    return [col for col in reference_df.columns if col not in REFERENCE_METADATA_COLUMNS]


def get_reference_cutoffs(
    reference,
    variable: str,
    *,
    method: str | None = None,
    filters: Mapping[str, object] | None = None,
) -> pd.DataFrame:
    """Filter a long-format reference table down to one variable/stratum."""
    reference_df = pd.DataFrame(reference).copy()
    subset = reference_df.loc[reference_df["variable"] == variable].copy()
    if method is not None:
        subset = subset.loc[subset["method"] == str(method).lower()].copy()
    for key, value in (filters or {}).items():
        if key not in subset.columns:
            raise KeyError(f"Reference filter column not found: {key}")
        if pd.isna(value):
            subset = subset.loc[subset[key].isna()].copy()
        else:
            subset = subset.loc[subset[key] == value].copy()
    if subset.empty:
        raise KeyError(f"No reference cutoffs found for variable={variable!r}, filters={filters!r}")
    methods = subset["method"].dropna().unique().tolist()
    if len(methods) != 1:
        raise ValueError(
            "Reference subset must resolve to exactly one method before scoring. "
            f"Found methods: {methods}"
        )
    group_cols = get_reference_group_columns(subset)
    if group_cols and len(subset[group_cols].drop_duplicates()) != 1:
        raise ValueError(
            "Reference subset resolves to multiple strata. "
            "Please pass group filters so that one stratum remains."
        )
    return subset.sort_values("rank").reset_index(drop=True)


def reference_table_to_wide(reference) -> pd.DataFrame:
    """Convert a long reference table into a CSV-friendly wide format."""
    reference_df = pd.DataFrame(reference).copy()
    group_cols = get_reference_group_columns(reference_df)
    index_cols = group_cols + ["variable", "method", "n_non_missing"]
    wide = (
        reference_df.pivot_table(
            index=index_cols,
            columns="rank",
            values="cutoff",
            aggfunc="first",
        )
        .reset_index()
        .rename(columns=lambda col: f"cutoff_{col}" if isinstance(col, (int, np.integer)) else col)
    )
    return wide


def _resolve_scores(bin_count: int, direction: str, scores: Sequence[float] | None) -> np.ndarray:
    if scores is None:
        base = np.arange(1, bin_count + 1, dtype=float)
        if direction == "unhealthy":
            base = base[::-1]
        return base
    scores_arr = np.asarray(scores, dtype=float)
    if scores_arr.shape != (bin_count,):
        raise ValueError(f"Expected {bin_count} scores, got shape {scores_arr.shape}.")
    return scores_arr


def score_quantile_with_cutoffs(
    actual,
    cutoffs,
    *,
    direction: str = "healthy",
    scores: Sequence[float] | None = None,
    zero_as_lowest: bool = True,
):
    """Score an array against a set of ordered cutoffs.

    ``scores`` is interpreted from low intake to high intake. When it is not
    supplied, the helper defaults to 1..N for ``healthy`` and N..1 for
    ``unhealthy``.
    """

    direction = str(direction).lower()
    if direction not in {"healthy", "unhealthy"}:
        raise ValueError("direction must be either 'healthy' or 'unhealthy'.")

    values = np.asarray(actual, dtype=float)
    thresholds = np.asarray(cutoffs, dtype=float).reshape(-1)
    if thresholds.size < 2:
        raise ValueError("At least two cutoff values are required.")
    if np.any(np.diff(thresholds) < 0):
        raise ValueError("Cutoff values must be sorted in ascending order.")

    bin_count = thresholds.size - 1
    score_values = _resolve_scores(bin_count, direction, scores)
    inner_thresholds = thresholds[1:-1]
    bin_index = np.searchsorted(inner_thresholds, values, side="right")
    if zero_as_lowest:
        bin_index = np.where(values == 0, 0, bin_index)
    result = score_values[np.clip(bin_index, 0, bin_count - 1)]
    result = np.asarray(result, dtype=float)
    result[np.isnan(values)] = np.nan
    return result


def score_median_with_cutoff(actual, median, *, direction: str = "healthy"):
    """Score an array using a binary median cutoff."""
    direction = str(direction).lower()
    if direction not in {"healthy", "unhealthy"}:
        raise ValueError("direction must be either 'healthy' or 'unhealthy'.")

    values = np.asarray(actual, dtype=float)
    if direction == "healthy":
        result = np.where((values < median) | (values == 0), 0.0, 1.0)
    else:
        result = np.where((values < median) | (values == 0), 1.0, 0.0)
    result[np.isnan(values)] = np.nan
    return result


def _normalize_group_frame(group, group_cols: list[str], length: int) -> pd.DataFrame:
    if not group_cols:
        return pd.DataFrame(index=range(length))
    if group is None:
        raise ValueError(f"Group values are required for grouped references: {group_cols}")

    if isinstance(group, pd.Series):
        frame = group.to_frame(name=group.name or group_cols[0]).reset_index(drop=True)
    elif isinstance(group, pd.DataFrame):
        frame = group.reset_index(drop=True).copy()
    elif isinstance(group, Mapping):
        frame = pd.DataFrame(group).reset_index(drop=True)
    else:
        raise TypeError("group must be a pandas Series, DataFrame, or mapping of arrays/Series.")

    missing_group_cols = [col for col in group_cols if col not in frame.columns]
    if missing_group_cols:
        raise KeyError(f"Missing group columns for reference scoring: {missing_group_cols}")
    if len(frame) != length:
        raise ValueError(
            "Group values must have the same length as the data being scored. "
            f"Got {len(frame)} rows for {length} observations."
        )
    return frame[group_cols]


def _score_with_reference_subset(
    actual: pd.Series,
    subset: pd.DataFrame,
    *,
    direction: str,
    scores: Sequence[float] | None,
    zero_as_lowest: bool,
) -> np.ndarray:
    subset = subset.sort_values("rank").reset_index(drop=True)
    method = subset.loc[0, "method"]
    cutoffs = subset["cutoff"].to_numpy(dtype=float)
    if method == "median":
        if cutoffs.size != 1:
            raise ValueError("Median references must contain exactly one cutoff row.")
        return score_median_with_cutoff(actual, cutoffs[0], direction=direction)
    return score_quantile_with_cutoffs(
        actual,
        cutoffs,
        direction=direction,
        scores=scores,
        zero_as_lowest=zero_as_lowest,
    )


def score_series_with_reference(
    actual,
    reference,
    *,
    variable: str,
    direction: str = "healthy",
    group=None,
    scores: Sequence[float] | None = None,
    zero_as_lowest: bool = True,
):
    """Apply a reusable reference table back to a series of observations."""

    actual_series = _coerce_numeric_series(actual, name=variable)
    reference_df = pd.DataFrame(reference).copy()
    reference_df = reference_df.loc[reference_df["variable"] == variable].copy()
    if reference_df.empty:
        raise KeyError(f"Reference table does not contain variable: {variable}")

    group_cols = get_reference_group_columns(reference_df)
    if not group_cols:
        return _score_with_reference_subset(
            actual_series,
            reference_df,
            direction=direction,
            scores=scores,
            zero_as_lowest=zero_as_lowest,
        )

    group_frame = _normalize_group_frame(group, group_cols, len(actual_series))
    result = np.full(len(actual_series), np.nan, dtype=float)

    for _, combo in group_frame.drop_duplicates().iterrows():
        mask = pd.Series(True, index=group_frame.index)
        subset = reference_df
        filter_dict = {}
        for column in group_cols:
            value = combo[column]
            filter_dict[column] = value
            if pd.isna(value):
                mask &= group_frame[column].isna()
            else:
                mask &= group_frame[column].eq(value)
        subset = get_reference_cutoffs(reference_df, variable, filters=filter_dict)
        result[mask.to_numpy()] = _score_with_reference_subset(
            actual_series.loc[mask],
            subset,
            direction=direction,
            scores=scores,
            zero_as_lowest=zero_as_lowest,
        )
    return result


def score_healthy(actual, min_val, max_val, min_score=0.0, max_score=5.0):
    """Linear score for healthy components where higher intake is better."""
    actual = np.asarray(actual, dtype=float)
    result = np.where(
        actual >= max_val,
        max_score,
        np.where(
            actual <= min_val,
            min_score,
            min_score + (actual - min_val) * max_score / (max_val - min_val),
        ),
    )
    return result


def score_unhealthy(actual, min_val, max_val, min_score=0.0, max_score=10.0):
    """Linear score for unhealthy components where lower intake is better."""
    actual = np.asarray(actual, dtype=float)
    result = np.where(
        actual >= min_val,
        min_score,
        np.where(
            actual <= max_val,
            max_score,
            min_score + (actual - min_val) * max_score / (max_val - min_val),
        ),
    )
    return result


def score_quintile_healthy(actual):
    """Positive quintile scoring derived from the sample distribution."""
    cutoffs = _safe_nanquantile(np.asarray(actual, dtype=float), np.linspace(0, 1, 6))
    return score_quantile_with_cutoffs(actual, cutoffs, direction="healthy")


def score_quintile_unhealthy(actual):
    """Reverse quintile scoring derived from the sample distribution."""
    cutoffs = _safe_nanquantile(np.asarray(actual, dtype=float), np.linspace(0, 1, 6))
    return score_quantile_with_cutoffs(actual, cutoffs, direction="unhealthy")


def score_median_healthy(actual):
    """Positive median scoring derived from the sample median."""
    median_val = np.nanmedian(np.asarray(actual, dtype=float))
    return score_median_with_cutoff(actual, median_val, direction="healthy")


def score_median_unhealthy(actual):
    """Reverse median scoring derived from the sample median."""
    median_val = np.nanmedian(np.asarray(actual, dtype=float))
    return score_median_with_cutoff(actual, median_val, direction="unhealthy")


def score_quartile_healthy(actual, score_values=(0.0, 0.25, 0.5, 0.75)):
    """Positive quartile scoring derived from the sample distribution."""
    cutoffs = np.nanquantile(np.asarray(actual, dtype=float), np.linspace(0, 1, 5))
    return score_quantile_with_cutoffs(actual, cutoffs, scores=score_values)


def score_quartile_unhealthy(actual, score_values=(0.0, 1.0, 2.0, 3.0)):
    """Reverse quartile scoring derived from the sample distribution."""
    cutoffs = np.nanquantile(np.asarray(actual, dtype=float), np.linspace(0, 1, 5))
    return score_quantile_with_cutoffs(actual, cutoffs, scores=list(reversed(score_values)))


def score_decile_sodium(sodium_serv):
    """AHEI sodium scoring using sample-derived deciles."""
    deciles = _safe_nanquantile(np.asarray(sodium_serv, dtype=float), np.linspace(0, 1, 12))
    return score_quantile_with_cutoffs(
        sodium_serv,
        deciles,
        scores=list(range(10, -1, -1)),
    )

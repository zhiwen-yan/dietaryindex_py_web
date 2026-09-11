"""Food Inflammatory Score Index (FISI)."""

from pathlib import Path

import numpy as np
import pandas as pd

from dietaryindex.reference.fisi_nrv import (
    FISI_FLAVONOID_COMPONENTS,
    load_fisi_nrv,
)

FISI26_COMPONENTS = (
    "Protein",
    "Total_fat",
    "Carbohydrate",
    "Energy",
    "Fiber",
    "Iron",
    "Magnesium",
    "Zinc",
    "Selenium",
    "Vitamin_A",
    "Carotene_alpha",
    "Vitamin_E",
    "Vitamin_C",
    "Thiamin",
    "Riboflavin",
    "Niacin",
    "Cholesterol",
    "Saturated_fat",
    "PUFA_18_2",
    "PUFA_18_3",
    "PUFA_20_4",
    "DHA",
    "EPA",
    "DPA",
    "total_monounsaturated",
    "total_polyunsaturated",
)

FISI34_COMPONENTS = (
    "Protein",
    "Total_fat",
    "Carbohydrate",
    "Energy",
    "Alcohol",
    "Caffeine",
    "Fiber",
    "Iron",
    "Magnesium",
    "Zinc",
    "Selenium",
    "Vitamin_A",
    "Carotene_alpha",
    "Vitamin_E",
    "Vitamin_D",
    "Vitamin_C",
    "Thiamin",
    "Riboflavin",
    "Niacin",
    "Vitamin_B6",
    "Vitamin_B12",
    "Folic_acid",
    "Vitamin_E_added",
    "Vitamin_B_12_added",
    "Cholesterol",
    "Saturated_fat",
    "PUFA_18_2",
    "PUFA_18_3",
    "PUFA_20_4",
    "DHA",
    "EPA",
    "DPA",
    "total_monounsaturated",
    "total_polyunsaturated",
)


def compute_fisi(
    data,
    id_col=None,
    respondent_id=None,
    version="usda",
    include_flavonoids=False,
    col_map=None,
    quiet=True,
    components=None,
):
    """Calculate Food Inflammatory Score Index from nutrient intake data.

    FISI is computed as ``sum(TIS_i * Intake_i / NRV_i)``. More negative
    scores indicate a more anti-inflammatory dietary profile.
    """
    version = str(version).lower()
    if version not in {"usda", "china"}:
        raise ValueError('version must be either "usda" or "china".')

    df = _read_fisi_input(data)
    if df.empty:
        raise ValueError("data has zero rows.")

    if id_col is not None and id_col not in df.columns:
        raise ValueError(f'Column "{id_col}" not found in data.')

    nrv = load_fisi_nrv(version).rename(columns={"NRVs": "NRV"})
    if not include_flavonoids:
        nrv = nrv[~nrv["Variable"].isin(FISI_FLAVONOID_COMPONENTS)].copy()
    if components is not None:
        components = tuple(str(component) for component in components)
        unknown_components = sorted(set(components) - set(nrv["Variable"]))
        if unknown_components:
            raise ValueError(
                "Unknown FISI components for the selected NRV version: "
                + ", ".join(unknown_components)
            )
        nrv = (
            nrv.set_index("Variable")
            .loc[list(components)]
            .reset_index()
        )

    col_lookup = {variable: variable for variable in nrv["Variable"]}
    if col_map is not None:
        if not isinstance(col_map, dict):
            raise ValueError("col_map must be a dictionary mapping standard names to data columns.")
        unknown = sorted(set(col_map) - set(col_lookup))
        if unknown and not quiet:
            print(f"Ignoring unknown FISI nutrient names in col_map: {', '.join(unknown)}")
        for standard, actual in col_map.items():
            if standard in col_lookup:
                col_lookup[standard] = actual

    available = [
        variable
        for variable in nrv["Variable"]
        if col_lookup.get(variable) in df.columns
    ]
    if not available:
        standards = ", ".join(nrv["Variable"].tolist())
        raise ValueError(
            "No recognised nutrient columns found in data. "
            "Use col_map to map your columns to standard FISI nutrient names. "
            f"Standard names: {standards}"
        )

    ids = _resolve_ids(df, id_col=id_col, respondent_id=respondent_id)
    nutrient_df = pd.DataFrame({"ID": ids})
    for variable in available:
        nutrient_df[variable] = pd.to_numeric(
            df[col_lookup[variable]], errors="coerce"
        ).reset_index(drop=True)

    long_df = nutrient_df.melt(
        id_vars=["ID"],
        value_vars=available,
        var_name="Variable",
        value_name="Intake",
    )
    long_df = long_df.merge(
        nrv[["Variable", "TIS", "NRV"]],
        on="Variable",
        how="left",
    )
    long_df["FISI_component"] = np.where(
        long_df["NRV"].notna() & (long_df["NRV"] > 0),
        long_df["TIS"] * long_df["Intake"] / long_df["NRV"],
        np.nan,
    )

    totals = (
        long_df.groupby("ID", sort=False)
        .agg(
            FISI_Total=("FISI_component", lambda s: s.sum(skipna=True)),
            Components_Used=(
                "FISI_component",
                lambda s: int((s.notna() & long_df.loc[s.index, "Intake"].notna()).sum()),
            ),
        )
        .reset_index()
    )
    # A zero-component row is unknown, not an inflammation score of zero.
    totals.loc[totals["Components_Used"].eq(0), "FISI_Total"] = np.nan

    component_wide = long_df.pivot_table(
        index="ID",
        columns="Variable",
        values="FISI_component",
        aggfunc="first",
    ).add_prefix("FISI_")
    intake_wide = long_df.pivot_table(
        index="ID",
        columns="Variable",
        values="Intake",
        aggfunc="first",
    ).add_prefix("Intake_")

    result = (
        totals.set_index("ID")
        .join(component_wide, how="left")
        .join(intake_wide, how="left")
        .reset_index()
    )

    if not quiet:
        print(
            "FISI calculation complete. "
            f"n = {len(result)} | components = {len(available)} | version = {version.upper()}"
        )

    return result


def _read_fisi_input(data):
    if isinstance(data, pd.DataFrame):
        return data.reset_index(drop=True).copy()

    if isinstance(data, (str, Path)):
        path = Path(data)
        ext = path.suffix.lower()
        if ext == ".csv":
            return pd.read_csv(path)
        if ext in {".tsv", ".txt"}:
            return pd.read_csv(path, sep="\t")
        if ext in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        if ext == ".xpt":
            return pd.read_sas(path, format="xport")
        raise ValueError(
            f'Unsupported FISI input file type "{ext}". '
            "Use CSV, TSV, Excel, XPT, or pass a DataFrame."
        )

    raise ValueError("data must be a pandas DataFrame or a supported file path.")


def _resolve_ids(df, id_col=None, respondent_id=None):
    if respondent_id is not None:
        if isinstance(respondent_id, str):
            if respondent_id not in df.columns:
                raise ValueError(f'Column "{respondent_id}" not found in data.')
            return df[respondent_id].reset_index(drop=True)
        values = pd.Series(np.asarray(respondent_id)).reset_index(drop=True)
        if len(values) != len(df):
            raise ValueError("respondent_id length must match data rows.")
        return values

    if id_col is not None:
        return df[id_col].reset_index(drop=True)

    return pd.Series(np.arange(1, len(df) + 1), name="ID")

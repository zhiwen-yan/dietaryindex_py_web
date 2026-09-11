"""Unified computation entrypoints for API usage."""

from __future__ import annotations

import inspect
from pathlib import Path

import numpy as np
import pandas as pd

from dietaryindex import (
    compute_acs2020_v1,
    compute_acs2020_v2,
    compute_ahei,
    compute_ahei_block,
    compute_ahei_dhq3,
    compute_ahei_nhanes_fped,
    compute_ahei_nhanes_mped,
    compute_aheip,
    compute_aheip_block,
    compute_cdai,
    compute_chei,
    compute_china_dii,
    compute_dash,
    compute_dash_nhanes_fped,
    compute_dash_nhanes_mped,
    compute_dashi,
    compute_dashi_nhanes_fped,
    compute_dashi_nhanes_mped,
    compute_dbi,
    compute_di_gm,
    compute_di_gm_nhanes_fped,
    compute_di_gm_nhanes_mped,
    compute_dii,
    compute_dii_asa24,
    compute_dii_block,
    compute_dii_dhq3,
    compute_dii_nhanes_fped,
    compute_dii_nhanes_mped,
    compute_dqii,
    compute_edii,
    compute_fisi,
    compute_fisi_nhanes,
    compute_gdqs,
    compute_hei2015,
    compute_hei2015_nhanes_fped,
    compute_hei2015_nhanes_mped,
    compute_hei2020,
    compute_hei2020_nhanes_fped,
    compute_hei2020_nhanes_mped,
    compute_hei2020_v2,
    compute_hpdi,
    compute_inq,
    compute_mar,
    compute_med,
    compute_med_nhanes_fped,
    compute_med_nhanes_mped,
    compute_medi,
    compute_medi_nhanes_fped,
    compute_medi_nhanes_mped,
    compute_medi_v2,
    compute_mind,
    compute_nar,
    compute_neap,
    compute_nrf,
    compute_obs,
    compute_pdi,
    compute_phdi,
    compute_phdi_asa24,
    compute_phdi_block,
    compute_phdi_dhq3,
    compute_phdi_nhanes_fped,
    compute_phdi_nhanes_mped,
    compute_phdi_v2,
    compute_pral,
    compute_updi,
    compute_wish,
)
from dietaryindex.service.files import load_dataframe_from_path
from dietaryindex.service.registry import get_index_detail, get_mode_requirements
from dietaryindex.service.results import build_result_payload
from dietaryindex.core.fisi import FISI26_COMPONENTS, FISI34_COMPONENTS
from dietaryindex.adapters.fisi import compute_fisi1_nhanes, compute_fisi26_nhanes
from dietaryindex.service.source_modes import (
    auto_map_fields,
    prepare_source_dataframe,
    summarize_asa24,
    validate_auto_mapping,
)


GENERAL_FUNCTION_MAP = {
    "compute_dii": compute_dii,
    "compute_hei2015": compute_hei2015,
    "compute_hei2020": compute_hei2020,
    "compute_hei2020_v2": compute_hei2020_v2,
    "compute_ahei": compute_ahei,
    "compute_aheip": compute_aheip,
    "compute_dash": compute_dash,
    "compute_dashi": compute_dashi,
    "compute_med": compute_med,
    "compute_medi": compute_medi,
    "compute_medi_v2": compute_medi_v2,
    "compute_acs2020_v1": compute_acs2020_v1,
    "compute_acs2020_v2": compute_acs2020_v2,
    "compute_phdi": compute_phdi,
    "compute_phdi_v2": compute_phdi_v2,
    "compute_di_gm": compute_di_gm,
    "compute_fisi": compute_fisi,
    "compute_pdi": compute_pdi,
    "compute_hpdi": compute_hpdi,
    "compute_updi": compute_updi,
    "compute_mind": compute_mind,
    "compute_dqii": compute_dqii,
    "compute_chei": compute_chei,
    "compute_dbi": compute_dbi,
    "compute_gdqs": compute_gdqs,
    "compute_wish": compute_wish,
    "compute_obs": compute_obs,
    "compute_edii": compute_edii,
    "compute_china_dii": compute_china_dii,
    "compute_nrf": compute_nrf,
    "compute_nar": compute_nar,
    "compute_mar": compute_mar,
    "compute_inq": compute_inq,
    "compute_pral": compute_pral,
    "compute_neap": compute_neap,
    "compute_cdai": compute_cdai,
}


ADAPTER_MAP = {
    ("DII", "asa24"): compute_dii_asa24,
    ("PHDI", "asa24"): compute_phdi_asa24,
    ("DII", "dhq3"): compute_dii_dhq3,
    ("AHEI", "dhq3"): compute_ahei_dhq3,
    ("PHDI", "dhq3"): compute_phdi_dhq3,
    ("DII", "block"): compute_dii_block,
    ("AHEI", "block"): compute_ahei_block,
    ("AHEIP", "block"): compute_aheip_block,
    ("PHDI", "block"): compute_phdi_block,
    ("DII", "nhanes_fped"): compute_dii_nhanes_fped,
    ("HEI2015", "nhanes_fped"): compute_hei2015_nhanes_fped,
    ("HEI2020", "nhanes_fped"): compute_hei2020_nhanes_fped,
    ("MED", "nhanes_fped"): compute_med_nhanes_fped,
    ("DASHI", "nhanes_fped"): compute_dashi_nhanes_fped,
    ("DASH", "nhanes_fped"): compute_dash_nhanes_fped,
    ("AHEI", "nhanes_fped"): compute_ahei_nhanes_fped,
    ("MEDI", "nhanes_fped"): compute_medi_nhanes_fped,
    ("DI_GM", "nhanes_fped"): compute_di_gm_nhanes_fped,
    ("PHDI", "nhanes_fped"): compute_phdi_nhanes_fped,
    ("DII", "nhanes_mped"): compute_dii_nhanes_mped,
    ("HEI2015", "nhanes_mped"): compute_hei2015_nhanes_mped,
    ("HEI2020", "nhanes_mped"): compute_hei2020_nhanes_mped,
    ("MED", "nhanes_mped"): compute_med_nhanes_mped,
    ("DASHI", "nhanes_mped"): compute_dashi_nhanes_mped,
    ("DASH", "nhanes_mped"): compute_dash_nhanes_mped,
    ("AHEI", "nhanes_mped"): compute_ahei_nhanes_mped,
    ("MEDI", "nhanes_mped"): compute_medi_nhanes_mped,
    ("DI_GM", "nhanes_mped"): compute_di_gm_nhanes_mped,
    ("PHDI", "nhanes_mped"): compute_phdi_nhanes_mped,
}


SINGLE_FILE_PARAM_CANDIDATES = ("data_path", "raw_data", "file_path")
AUTO_SOURCE_MODES = {"asa24", "dhq3", "block"}
NHANES_CYCLES = {
    "nhanes_fped": {"2005-2006", "2007-2008", "2009-2010", "2011-2012", "2013-2014", "2015-2016", "2017-2018"},
    "nhanes_mped": {"1999-2000", "2001-2002", "2003-2004"},
}


def _nhanes_cycle_sort_key(cycle: dict) -> tuple[int, int, str]:
    """Return a chronological key for an already validated NHANES cycle."""
    label = str(cycle.get("label") or "").strip()
    try:
        start, end = (int(part) for part in label.split("-", maxsplit=1))
    except (TypeError, ValueError):
        return (10_000, 10_000, label)
    return (start, end, label)


FISI_VARIANTS = {
    "fisi34": {"version": "usda", "components": FISI34_COMPONENTS},
    "fisi26_china": {"version": "china", "components": FISI26_COMPONENTS},
    "fisi26_usda": {"version": "usda", "components": FISI26_COMPONENTS},
    "fisi1": {"kind": "food"},
}


def _resolve_fisi_variant(fisi_variant="fisi34"):
    key = str(fisi_variant or "fisi34").strip().lower()
    if key not in FISI_VARIANTS:
        supported = ", ".join(FISI_VARIANTS)
        raise ValueError(f"Unsupported FISI algorithm version '{fisi_variant}'. Choose one of: {supported}.")
    return key, FISI_VARIANTS[key]


def _compute_fisi_nhanes_files(
    nutrient_path=None,
    nutrient_path2=None,
    nutrient_ind_path=None,
    nutrient_ind_path2=None,
    demo_path=None,
    fisi_variant="fisi34",
    exclude_extremes=True,
    include_flavonoids=False,
):
    """Expose the FISI NHANES adapter through the shared NHANES file keys."""
    if nutrient_path is None:
        raise ValueError("Day 1 nutrient totals are required for FISI NHANES computation.")
    variant_key, variant = _resolve_fisi_variant(fisi_variant)
    if variant_key == "fisi1":
        if nutrient_ind_path is None:
            raise ValueError("FISI1 requires the Day 1 NHANES individual-food file.")
        if (nutrient_path2 is None) != (nutrient_ind_path2 is None):
            raise ValueError(
                "FISI1 Day 2 nutrient totals and individual-food files must be provided together."
            )
        fii_csv = Path(__file__).resolve().parents[1] / "data" / "fii_food_usda.csv"
        return compute_fisi1_nhanes(
            iff_day1=nutrient_ind_path,
            tot_day1=nutrient_path,
            fii_csv=fii_csv,
            iff_day2=nutrient_ind_path2,
            tot_day2=nutrient_path2,
            demo_path=demo_path,
            exclude_extremes=exclude_extremes,
        )
    if variant_key == "fisi34":
        return compute_fisi_nhanes(
            nutrient_path1=nutrient_path,
            nutrient_path2=nutrient_path2,
            demo_path=demo_path,
            exclude_extremes=exclude_extremes,
            include_flavonoids=include_flavonoids,
        )
    return compute_fisi26_nhanes(
        nutrient_path1=nutrient_path,
        nutrient_path2=nutrient_path2,
        demo_path=demo_path,
        version=variant["version"],
        components=variant["components"],
        exclude_extremes=exclude_extremes,
        include_flavonoids=include_flavonoids,
    )


ADAPTER_MAP[("FISI", "nhanes_fped")] = _compute_fisi_nhanes_files
ADAPTER_MAP[("FISI", "nhanes_mped")] = _compute_fisi_nhanes_files


def _get_param_order(func):
    sig = inspect.signature(func)
    return [
        name
        for name, param in sig.parameters.items()
        if param.kind != inspect.Parameter.VAR_KEYWORD
    ]


def _accepts_var_keyword(func):
    sig = inspect.signature(func)
    return any(param.kind == inspect.Parameter.VAR_KEYWORD for param in sig.parameters.values())


def _resolve_mapped_value(df, mapped):
    if isinstance(mapped, str) and mapped in df.columns:
        return df[mapped].values
    return mapped


def _signature_params(func) -> set[str]:
    return set(inspect.signature(func).parameters.keys())


def _invoke_adapter(func, *, file_path=None, file_paths=None, options=None):
    options = dict(options or {})
    params = _signature_params(func)
    kwargs = {}

    if file_paths:
        for key, value in file_paths.items():
            if key in params and value is not None:
                kwargs[key] = value

    if file_path is not None:
        for candidate in SINGLE_FILE_PARAM_CANDIDATES:
            if candidate in params and candidate not in kwargs:
                kwargs[candidate] = file_path
                break

    for key, value in options.items():
        if key in params and key not in kwargs:
            kwargs[key] = value

    return func(**kwargs)


def _validate_mode_inputs(
    *,
    index_key: str,
    mode: str,
    file_path: str | Path | None,
    file_paths: dict[str, str | Path] | None,
) -> None:
    requirements = get_mode_requirements(index_key, mode)
    if requirements.get("single_file"):
        if file_path is None:
            raise ValueError(
                f"{index_key} in mode '{mode}' requires one uploaded input file. "
                f"{requirements.get('notes_en', '')}".strip()
            )
        return

    provided = set((file_paths or {}).keys())
    missing = [key for key in requirements.get("required_file_keys", []) if key not in provided]
    if missing:
        note = requirements.get("notes_en", "")
        raise ValueError(
            f"{index_key} in mode '{mode}' is missing required files: {', '.join(missing)}."
            + (f" {note}" if note else "")
        )


def _run_general_compute_from_df(
    *,
    index_key: str,
    detail: dict,
    df,
    mapping: dict,
    options: dict | None = None,
    output_dir: str | Path | None = None,
    mode: str = "general",
) -> dict:
    cfg_fields = detail["fields"]
    func = GENERAL_FUNCTION_MAP[detail["function_name"]]

    respondent_id_val = None
    extra_vals = {}
    for field in cfg_fields:
        mapped = mapping.get(field["name"])
        if field["field_type"] == "extra":
            if field["name"] == "respondent_id":
                respondent_id_val = _resolve_mapped_value(df, mapped)
            else:
                if mapped not in (None, ""):
                    extra_vals[field["name"]] = _resolve_mapped_value(df, mapped)
                elif field.get("default") is not None:
                    extra_vals[field["name"]] = field["default"]

    if respondent_id_val is None:
        respondent_id_val = np.arange(1, len(df) + 1)

    if index_key == "DII":
        kwargs = {"respondent_id": respondent_id_val, "repeat_num": extra_vals.get("repeat_num", 1)}
        for field in cfg_fields:
            if field["field_type"] != "input":
                continue
            mapped = mapping.get(field["name"])
            if mapped in (None, ""):
                continue
            kwargs[field["name"]] = _resolve_mapped_value(df, mapped)
        result = func(data=df, **kwargs)
    elif index_key == "FISI":
        variant_key, variant = _resolve_fisi_variant((options or {}).get("fisi_variant", "fisi34"))
        if variant_key == "fisi1":
            raise ValueError(
                "FISI1 is a food-level NHANES workflow. Use NHANES FPED/MPED mode "
                "with total nutrient and individual-food files."
            )
        nutrient_map = {}
        for field in cfg_fields:
            if field["field_type"] != "input":
                continue
            mapped = mapping.get(field["name"])
            if isinstance(mapped, str) and mapped in df.columns:
                nutrient_map[field["name"]] = mapped
        result = func(
            data=df,
            respondent_id=respondent_id_val,
            col_map=nutrient_map,
            version=variant["version"],
            include_flavonoids=False,
            components=variant["components"],
        )
    else:
        args = {}
        param_order = _get_param_order(func)
        accepts_var_keyword = _accepts_var_keyword(func)

        for param_name in param_order:
            if param_name == "data":
                args["data"] = df
            elif param_name == "respondent_id":
                args["respondent_id"] = respondent_id_val
            elif param_name in extra_vals:
                args[param_name] = extra_vals[param_name]
            else:
                mapped = mapping.get(param_name)
                if mapped not in (None, ""):
                    args[param_name] = _resolve_mapped_value(df, mapped)

        if accepts_var_keyword:
            for field in cfg_fields:
                if field["field_type"] != "input":
                    continue
                if field["name"] in args:
                    continue
                mapped = mapping.get(field["name"])
                if mapped not in (None, ""):
                    args[field["name"]] = _resolve_mapped_value(df, mapped)

        result = func(**args)

    return build_result_payload(
        index_key=index_key,
        mode=mode,
        result=result,
        output_dir=output_dir,
        primary_output_column=(detail["output_cols"][0] if detail["output_cols"] else None),
        mapping=mapping,
    )


def _run_general_compute(
    index_key: str,
    file_path: str | Path,
    mapping: dict,
    options: dict | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    detail = get_index_detail(index_key)
    df = prepare_source_dataframe(load_dataframe_from_path(file_path))
    return _run_general_compute_from_df(
        index_key=index_key,
        detail=detail,
        df=df,
        mapping=mapping,
        options=options,
        output_dir=output_dir,
        mode="general",
    )


def _run_auto_source_compute(
    *,
    index_key: str,
    mode: str,
    file_path: str | Path,
    options: dict | None,
    output_dir: str | Path | None,
) -> dict:
    detail = get_index_detail(index_key)
    df = prepare_source_dataframe(load_dataframe_from_path(file_path))
    mapping = auto_map_fields(df, detail["fields"])

    if mode == "asa24":
        recall_summarize = bool((options or {}).get("recall_summarize", True))
        df, mapping = summarize_asa24(df, mapping, recall_summarize=recall_summarize)

    missing_required, unmapped, total = validate_auto_mapping(detail["fields"], mapping)
    if missing_required:
        raise ValueError(
            f"Auto-mapping for {mode} is missing required fields: {', '.join(missing_required)}. "
            "Use general mode with manual mapping if the source export uses nonstandard column names."
        )
    if total and unmapped > total * 0.55:
        raise ValueError(
            f"Auto-mapping for {mode} is too incomplete ({total - unmapped}/{total} mapped). "
            "Use general mode with manual mapping."
        )

    final_mapping = {key: value for key, value in mapping.items() if value is not None}
    return _run_general_compute_from_df(
        index_key=index_key,
        detail=detail,
        df=df,
        mapping=final_mapping,
        options=options,
        output_dir=output_dir,
        mode=mode,
    )


def _run_special_mode_compute(
    *,
    index_key: str,
    mode: str,
    file_path: str | Path | None,
    file_paths: dict[str, str | Path] | None,
    options: dict | None,
    output_dir: str | Path | None,
) -> dict:
    _validate_mode_inputs(index_key=index_key, mode=mode, file_path=file_path, file_paths=file_paths)
    detail = get_index_detail(index_key)
    func = ADAPTER_MAP.get((index_key, mode))
    if func is None:
        if mode in AUTO_SOURCE_MODES and file_path is not None:
            return _run_auto_source_compute(
                index_key=index_key,
                mode=mode,
                file_path=file_path,
                options=options,
                output_dir=output_dir,
            )
        raise NotImplementedError(f"{index_key} does not currently expose a package/API adapter for mode '{mode}'.")

    result = _invoke_adapter(func, file_path=file_path, file_paths=file_paths, options=options)
    primary_output_column = (
        "FISI1"
        if index_key == "FISI" and str((options or {}).get("fisi_variant", "")).lower() == "fisi1"
        else (detail["output_cols"][0] if detail["output_cols"] else None)
    )
    return build_result_payload(
        index_key=index_key,
        mode=mode,
        result=result,
        output_dir=output_dir,
        primary_output_column=primary_output_column,
        mapping=options or {},
    )


def run_multi_cycle_compute(
    *,
    index_key: str,
    mode: str,
    cycles: list[dict],
    options: dict | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    """Compute NHANES cycles independently and export one labelled result table.

    Each NHANES cycle needs its own set of files: identifiers such as SEQN are
    only unique within a cycle, and source-file suffixes change between cycles.
    Therefore files are never concatenated before an adapter runs.  The scored
    data frames are labelled and concatenated only after each independent run.
    """
    if mode not in {"nhanes_fped", "nhanes_mped"}:
        raise ValueError("Multi-cycle computation is currently available for NHANES FPED and MPED modes only.")
    if not cycles:
        raise ValueError("Provide at least one NHANES cycle.")

    labels = [str(cycle.get("label") or "").strip() for cycle in cycles]
    if any(not label for label in labels):
        raise ValueError("Every NHANES cycle must have a cycle label.")
    if len(labels) != len(set(labels)):
        raise ValueError("Duplicate NHANES cycles are not allowed.")
    unsupported = [label for label in labels if label not in NHANES_CYCLES[mode]]
    if unsupported:
        raise ValueError(f"Unsupported {mode} cycle(s): {', '.join(unsupported)}.")

    func = ADAPTER_MAP.get((index_key, mode))
    if func is None:
        raise NotImplementedError(f"{index_key} does not currently expose a package/API adapter for mode '{mode}'.")

    ordered_cycles = sorted(cycles, key=_nhanes_cycle_sort_key)

    frames: list[pd.DataFrame] = []
    for position, cycle in enumerate(ordered_cycles, start=1):
        label = str(cycle.get("label") or f"Cycle {position}").strip()
        file_paths = cycle.get("file_paths") or {}
        _validate_mode_inputs(index_key=index_key, mode=mode, file_path=None, file_paths=file_paths)
        result = _invoke_adapter(func, file_paths=file_paths, options=options)
        if not isinstance(result, pd.DataFrame):
            raise TypeError(f"{index_key} {mode} adapter returned {type(result).__name__}, expected DataFrame.")
        labelled = result.copy()
        labelled.insert(0, "NHANES_CYCLE", label)
        frames.append(labelled)

    combined = pd.concat(frames, ignore_index=True, sort=False)
    detail = get_index_detail(index_key)
    primary_output_column = (
        "FISI1"
        if index_key == "FISI" and str((options or {}).get("fisi_variant", "")).lower() == "fisi1"
        else (detail["output_cols"][0] if detail["output_cols"] else None)
    )
    return build_result_payload(
        index_key=index_key,
        mode=mode,
        result=combined,
        output_dir=output_dir,
        primary_output_column=primary_output_column,
        mapping={
            "cycles": [{"label": str(cycle.get("label") or f"Cycle {position}")} for position, cycle in enumerate(ordered_cycles, start=1)],
            **(options or {}),
        },
    )


def run_compute(
    *,
    index_key: str,
    mode: str,
    file_path: str | Path | None = None,
    file_paths: dict[str, str | Path] | None = None,
    mapping: dict | None = None,
    options: dict | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    if mode == "general":
        if file_path is None:
            raise ValueError("General mode requires file_path.")
        return _run_general_compute(
            index_key=index_key,
            file_path=file_path,
            mapping=mapping or {},
            options=options,
            output_dir=output_dir,
        )

    return _run_special_mode_compute(
        index_key=index_key,
        mode=mode,
        file_path=file_path,
        file_paths=file_paths,
        options=options or mapping or {},
        output_dir=output_dir,
    )

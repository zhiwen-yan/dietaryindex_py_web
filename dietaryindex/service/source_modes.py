"""Shared helpers for source-specific auto-mapping modes."""

from __future__ import annotations

import pandas as pd


COMMON_SYNONYMS = {
    "respondent_id": ["id", "seqn", "participant_id", "participantid", "subject_id", "subjectid", "username", "user_name", "respondentid"],
    "gender": ["sex", "riagendr"],
    "age": ["ridageyr"],
    "total_kcal": ["kcal", "energy", "totalenergy", "totalkcal", "dr1tkcal", "drxtkcal"],
    "kcal": ["energy", "totalenergy", "totalkcal"],
    "energy": ["kcal", "totalenergy", "totalkcal"],
    "total_fruit": ["fruit_total", "totalfruit", "totalfruits", "f_total"],
    "whole_fruit": ["wholefruit", "wholefruits", "wholefrt"],
    "total_vegetable": ["vegetable_total", "totalvegetable", "totalvegetables", "veg_total", "v_total"],
    "green_and_bean": ["greensandbeans", "greenbean", "greenbeans"],
    "total_protein": ["totalprotein"],
    "seafood_plant_protein": ["seafoodplantprotein", "seafoodplantproteins"],
    "whole_grain": ["wholegrain", "wholegrains", "g_whl"],
    "refined_grain": ["refinedgrain", "refinedgrains", "g_nwhl"],
    "fatty_acid": ["fattyacidratio"],
    "sodium": ["na", "sodi", "dr1tsodi", "drxtsodi"],
    "fiber": ["fibre", "dietaryfiber", "tfibe", "dr1tfibe", "drxtfibe"],
    "alcohol": ["alco", "dr1talco", "drxtalco"],
    "protein": ["prot", "dr1tprot", "drxtprot"],
    "carb": ["carbohydrate", "carbo", "dr1tcarb", "drxtcarb"],
    "carbohydrate": ["carb", "carbo", "dr1tcarb", "drxtcarb"],
    "totalfat": ["total_fat", "fat", "tfat", "dr1ttfat", "drxttfat"],
    "total_fat": ["totalfat", "fat", "tfat", "dr1ttfat", "drxttfat"],
    "satfat": ["saturatedfat", "sat_fat", "sfa", "sfat", "dr1tsfat", "drxtsfat"],
    "saturated_fat": ["saturatedfat", "satfat", "sat_fat", "sfa", "sfat", "dr1tsfat", "drxtsfat"],
    "pufa": ["poly_fat", "polyunsaturated"],
    "mufa": ["mono_fat", "monounsaturated"],
    "trans_fat": ["transfat", "transfattyacids"],
    "n3_fat": ["n3fat", "omega3", "omega_3"],
    "ssb_fruit_juice": ["ssb", "sweetenedbeverage", "fruitjuice", "ssbjuice"],
    "red_processed_meat": ["redmeat", "processedmeat", "redprocessedmeat"],
    "added_sugar": ["addedsugars", "asug", "added_sugars", "sugar"],
    "vitamin_a": ["vita_rae", "vitarae", "vita", "dr1tvara", "drxtvara"],
    "vitamin_c": ["vitc", "dr1tvitc", "drxtvitc"],
    "vitamin_e": ["vite", "atoc", "dr1tatoc", "drxtatoc"],
    "calcium": ["calc", "dr1tcalc", "drxtcalc"],
    "magnesium": ["mg", "magn", "dr1tmagn", "drxtmagn"],
    "potassium": ["pota", "dr1tpota", "drxtpota"],
    "phosphorus": ["phos", "dr1tphos", "drxtphos"],
    "zinc": ["zn", "dr1tzinc", "drxtzinc"],
    "selenium": ["sele", "se", "dr1tsele", "drxtsele"],
    "total_carotenoids": ["totalcarotenoids", "total_carotenoid", "carotenoids", "tcar"],
    "caffeine": ["caff", "dr1tcaff", "drxtcaff"],
    "carotene_alpha": ["acar", "alpha_carotene", "dr1tacar", "drxtacar"],
    "folic_acid": ["fola", "folac", "dr1tfa", "drxtfa"],
    "cholesterol": ["chole", "chol", "dr1tchol", "drxtchol"],
    "puFA_18_2".lower(): ["p182", "dr1tp182", "drxtp182"],
    "puFA_18_3".lower(): ["p183", "dr1tp183", "drxtp183"],
    "puFA_20_4".lower(): ["p204", "dr1tp204", "drxtp204"],
    "dha": ["p226", "dr1tp226", "drxtp226"],
    "epa": ["p205", "dr1tp205", "drxtp205"],
    "dpa": ["p225", "dr1tp225", "drxtp225"],
    "total_monounsaturated": ["mfat", "monofat", "mono_fat", "dr1tmfat", "drxtmfat"],
    "total_polyunsaturated": ["pfat", "polyfat", "poly_fat", "dr1tpfat", "drxtpfat"],
    "fruit": ["totalfruit", "fruit_total"],
    "vegetable": ["veg", "totalvegetable", "vegetable_total"],
    "legumes": ["legume"],
    "nuts": ["nut"],
    "olive_oil": ["oliveoil"],
    "fish_seafood": ["fishseafood"],
    "discret_fat": ["discretionaryfat"],
}


def prepare_source_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Add safe, unit-preserving derived fields used by source-mode indices."""
    prepared = df.copy()
    normalized = {_normalize_col(col): col for col in prepared.columns}
    if "totalcarotenoids" not in normalized:
        component_aliases = (
            ("acar", "alphacarotene", "carotenealpha"),
            ("bcar", "betacarotene", "carotenebeta"),
            ("cryp", "betacryptoxanthin", "cryptoxanthin"),
            ("lyco", "lycopene"),
            ("lutzea", "luteinzeaxanthin"),
        )
        component_columns = []
        for aliases in component_aliases:
            match = next((normalized[name] for name in aliases if name in normalized), None)
            if match is not None:
                component_columns.append(match)
        if component_columns:
            prepared["total_carotenoids"] = (
                prepared[component_columns]
                .apply(pd.to_numeric, errors="coerce")
                .sum(axis=1, min_count=1)
            )
    return prepared


def _normalize_col(name: str) -> str:
    return "".join(ch for ch in str(name).strip().lower() if ch.isalnum())


def _candidate_names(param_name: str) -> list[str]:
    base = [
        param_name,
        param_name.lower(),
        param_name.upper(),
        param_name.replace("_", ""),
        param_name.replace("_", " "),
    ]
    extras = COMMON_SYNONYMS.get(param_name.lower(), [])
    return list(dict.fromkeys(base + extras))


def _find_best_column(param_name: str, normalized_columns: dict[str, str]) -> str | None:
    for candidate in _candidate_names(param_name):
        normalized_candidate = _normalize_col(candidate)
        if normalized_candidate in normalized_columns:
            return normalized_columns[normalized_candidate]
    # Standard questionnaire exports often append units to compact nutrient
    # names (for example PROT_g or POTA_mg). Accept only one unambiguous
    # prefix match and avoid very short aliases such as ID, MG, or SE.
    for candidate in _candidate_names(param_name):
        normalized_candidate = _normalize_col(candidate)
        if len(normalized_candidate) < 4:
            continue
        matches = [
            original
            for normalized, original in normalized_columns.items()
            if normalized.startswith(normalized_candidate)
        ]
        if len(matches) == 1:
            return matches[0]
    return None


def auto_map_fields(df: pd.DataFrame, fields: list[dict]) -> dict[str, str | None]:
    normalized = {_normalize_col(col): col for col in df.columns}
    mapping: dict[str, str | None] = {}
    for field in fields:
        if field["name"] == "repeat_num":
            continue
        mapping[field["name"]] = _find_best_column(field["name"], normalized)
    if "respondent_id" not in mapping:
        mapping["respondent_id"] = _find_best_column("respondent_id", normalized)
    return mapping


def summarize_asa24(df: pd.DataFrame, mapping: dict[str, str | None], recall_summarize: bool = True) -> tuple[pd.DataFrame, dict[str, str | None]]:
    if not recall_summarize:
        return df, mapping

    id_col = None
    for candidate in ["UserName", "username", "USERNAME", "UserName"]:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col is None:
        return df, mapping

    mapped_cols = [value for value in mapping.values() if isinstance(value, str) and value in df.columns]
    agg_dict: dict[str, str] = {}
    for col in mapped_cols:
        numeric_series = pd.to_numeric(df[col], errors="coerce")
        agg_dict[col] = "mean" if numeric_series.notna().any() else "first"

    resp_col = mapping.get("respondent_id")
    if resp_col and resp_col in df.columns and resp_col != id_col:
        agg_dict[resp_col] = "first"

    if not agg_dict:
        return df, mapping

    summarized = df.groupby(id_col, as_index=False).agg(agg_dict)
    updated_mapping = dict(mapping)
    updated_mapping["respondent_id"] = id_col
    return summarized, updated_mapping


def validate_auto_mapping(fields: list[dict], mapping: dict[str, str | None]) -> tuple[list[str], int, int]:
    missing_required = []
    total = 0
    unmapped = 0
    for field in fields:
        if field["name"] == "repeat_num":
            continue
        total += 1
        if mapping.get(field["name"]) is None:
            unmapped += 1
            if field.get("required") and field["name"] != "respondent_id":
                missing_required.append(field["name"])
    return missing_required, unmapped, total

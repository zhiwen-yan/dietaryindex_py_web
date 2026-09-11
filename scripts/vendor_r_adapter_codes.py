"""Vendor NHANES FNDDS code lists used by the upstream R adapters.

Run this script from a source checkout and pass the upstream R package's
``R`` directory.  The generated CSV files make the Python package independent
of a sibling ``dietaryindex-main`` checkout at runtime.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EXPORTS = {
    "DASH_NHANES_FPED.R": {
        "dash_ssb_fndds_1718_codes.csv": ("COFFEE", "TEA", "DRINK"),
        "dash_skim_milk_fndds_1718_codes.csv": ("SKIM_MILK",),
        "dash_lowf_cheese_fndds_1718_codes.csv": ("LOWF_CHEESE",),
    },
    "MEDI_NHANES_FPED.R": {
        "medi_ssb_fndds_1718_codes.csv": ("COFFEE", "TEA", "DRINK"),
        "medi_sweets_fndds_1718_codes.csv": ("SWEETS",),
        "medi_fat_oil_fndds_1718_codes.csv": ("FAT_OIL",),
        "medi_olive_oil_fndds_1718_codes.csv": ("OLIVE_OIL",),
    },
    "DI_GM_NHANES_FPED.R": {
        "di_gm_avocado_fndds_1718_codes.csv": ("AVOCADO",),
        "di_gm_broccoli_fndds_1718_codes.csv": ("BROCCOLI",),
        "di_gm_chickpea_fndds_1718_codes.csv": ("CHICKPEA",),
        "di_gm_coffee_fndds_1718_codes.csv": ("COFFEE",),
        "di_gm_cranberry_fndds_1718_codes.csv": ("CRANBERRY",),
        "di_gm_fermented_dairy_fndds_1718_codes.csv": ("FERMENTED_DAIRY",),
        "di_gm_green_tea_fndds_1718_codes.csv": ("GREEN_TEA",),
        "di_gm_soybean_fndds_1718_codes.csv": ("SOYBEAN",),
    },
}


def extract_vector(source: str, symbol: str) -> list[int]:
    match = re.search(rf"\b{re.escape(symbol)}\s*=\s*c\((.*?)\)", source, re.S)
    if not match:
        raise ValueError(f"Could not find vector {symbol}")
    return [int(value) for value in re.findall(r"\b\d{7,8}\b", match.group(1))]


def unique(values: list[int]) -> list[int]:
    return list(dict.fromkeys(values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("r_source_dir", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "dietaryindex" / "data",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for script_name, outputs in EXPORTS.items():
        source = (args.r_source_dir / script_name).read_text(encoding="utf-8")
        for output_name, symbols in outputs.items():
            codes = unique([code for symbol in symbols for code in extract_vector(source, symbol)])
            output_path = args.output_dir / output_name
            with output_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["code"])
                writer.writerows((code,) for code in codes)
            print(f"{output_name}: {len(codes)} codes")


if __name__ == "__main__":
    main()

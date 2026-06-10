from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from figure_export_utils import save_figure_exports
from dietaryindex import (
    compute_ahei_nhanes_fped,
    compute_dash_nhanes_fped,
    compute_dashi_nhanes_fped,
    compute_di_gm_nhanes_fped,
    compute_dii_nhanes_fped,
    compute_hei2015_nhanes_fped,
    compute_hei2020_nhanes_fped,
    compute_med_nhanes_fped,
    compute_medi_nhanes_fped,
)


ROOT_DIR = Path(r"D:\项目\Python_Streamlit_web\NHANES")
OUT_DIR = ROOT_DIR / "_derived"

SCORES_PATH = OUT_DIR / "diet_scores_2007_2018_nhanes_python_raw.csv"
RAW_DEMO_WITH_SCORES_PATH = OUT_DIR / "demo_raw_2007_2018_with_nhanes_python_scores.csv"
COVERAGE_PATH = OUT_DIR / "diet_scores_2007_2018_nhanes_python_raw_coverage.csv"
CORR_PATH = OUT_DIR / "diet_scores_2007_2018_nhanes_python_raw_correlation_matrix.csv"
HEATMAP_PATH = OUT_DIR / "diet_scores_2007_2018_nhanes_python_raw_heatmap.png"

CYCLES = [
    {"label": "2007-2008", "suffix": "e", "fped_suffix": "0708"},
    {"label": "2009-2010", "suffix": "f", "fped_suffix": "0910"},
    {"label": "2011-2012", "suffix": "g", "fped_suffix": "1112"},
    {"label": "2013-2014", "suffix": "h", "fped_suffix": "1314"},
    {"label": "2015-2016", "suffix": "i", "fped_suffix": "1516"},
    {"label": "2017-2018", "suffix": "j", "fped_suffix": "1718"},
]

SCORE_COLS = [
    "dii",
    "hei_2015",
    "hei_2020",
    "ahei",
    "dash",
    "dashi",
    "med",
    "medi",
    "di_gm",
]

LABELS = {
    "dii": "DII",
    "hei_2015": "HEI-2015",
    "hei_2020": "HEI-2020",
    "ahei": "AHEI",
    "dash": "DASH",
    "dashi": "DASHI",
    "med": "MED",
    "medi": "MEDI",
    "di_gm": "DI-GM",
}


def cycle_paths(cycle: dict[str, str]) -> dict[str, str]:
    cycle_dir = ROOT_DIR / cycle["label"]
    suffix = cycle["suffix"]
    fped_suffix = cycle["fped_suffix"]
    return {
        "demo": str(cycle_dir / "Demographics" / f"demo_{suffix}.xpt"),
        "tot1": str(cycle_dir / "Dietary" / f"dr1tot_{suffix}.xpt"),
        "tot2": str(cycle_dir / "Dietary" / f"dr2tot_{suffix}.xpt"),
        "fped1": str(cycle_dir / "Dietary" / f"fped_dr1tot_{fped_suffix}.sas7bdat"),
        "fped2": str(cycle_dir / "Dietary" / f"fped_dr2tot_{fped_suffix}.sas7bdat"),
        "iff1": str(cycle_dir / "Dietary" / f"dr1iff_{suffix}.xpt"),
        "iff2": str(cycle_dir / "Dietary" / f"dr2iff_{suffix}.xpt"),
        "fpediff1": str(cycle_dir / "Dietary" / f"fped_dr1iff_{fped_suffix}.sas7bdat"),
        "fpediff2": str(cycle_dir / "Dietary" / f"fped_dr2iff_{fped_suffix}.sas7bdat"),
    }


def read_demo_xpt(path: str) -> pd.DataFrame:
    try:
        return pd.read_sas(path, format="xport")
    except Exception as exc:
        raise RuntimeError(f"Failed to read DEMO file: {path}") from exc


def build_raw_demo_stack() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for cycle in CYCLES:
        paths = cycle_paths(cycle)
        demo_df = read_demo_xpt(paths["demo"]).copy()
        demo_df["cycle"] = cycle["label"]
        frames.append(demo_df)
    return pd.concat(frames, ignore_index=True)


def compute_cycle_scores(cycle: dict[str, str]) -> pd.DataFrame:
    paths = cycle_paths(cycle)

    dii = compute_dii_nhanes_fped(
        fped_path=paths["fped1"],
        nutrient_path=paths["tot1"],
        demo_path=paths["demo"],
        fped_path2=paths["fped2"],
        nutrient_path2=paths["tot2"],
    )[["SEQN", "DII_ALL"]].rename(columns={"SEQN": "seqn", "DII_ALL": "dii"})

    hei2015 = compute_hei2015_nhanes_fped(
        fped_path=paths["fped1"],
        nutrient_path=paths["tot1"],
        demo_path=paths["demo"],
        fped_path2=paths["fped2"],
        nutrient_path2=paths["tot2"],
    )[["SEQN", "HEI2015_ALL"]].rename(columns={"SEQN": "seqn", "HEI2015_ALL": "hei_2015"})

    hei2020 = compute_hei2020_nhanes_fped(
        fped_path=paths["fped1"],
        nutrient_path=paths["tot1"],
        demo_path=paths["demo"],
        fped_path2=paths["fped2"],
        nutrient_path2=paths["tot2"],
    )[["SEQN", "HEI2020_ALL"]].rename(columns={"SEQN": "seqn", "HEI2020_ALL": "hei_2020"})

    ahei = compute_ahei_nhanes_fped(
        fped_ind_path=paths["fpediff1"],
        nutrient_ind_path=paths["iff1"],
        fped_ind_path2=paths["fpediff2"],
        nutrient_ind_path2=paths["iff2"],
        demo_path=paths["demo"],
    )[["SEQN", "AHEI_ALL"]].rename(columns={"SEQN": "seqn", "AHEI_ALL": "ahei"})

    dash = compute_dash_nhanes_fped(
        fped_ind_path=paths["fpediff1"],
        nutrient_ind_path=paths["iff1"],
        fped_ind_path2=paths["fpediff2"],
        nutrient_ind_path2=paths["iff2"],
        demo_path=paths["demo"],
    )[["SEQN", "DASH_ALL"]].rename(columns={"SEQN": "seqn", "DASH_ALL": "dash"})

    dashi = compute_dashi_nhanes_fped(
        nutrient_path=paths["tot1"],
        nutrient_path2=paths["tot2"],
        demo_path=paths["demo"],
    )[["SEQN", "DASHI_ALL"]].rename(columns={"SEQN": "seqn", "DASHI_ALL": "dashi"})

    med = compute_med_nhanes_fped(
        fped_path=paths["fped1"],
        nutrient_path=paths["tot1"],
        demo_path=paths["demo"],
        fped_path2=paths["fped2"],
        nutrient_path2=paths["tot2"],
    )[["SEQN", "MED_ALL"]].rename(columns={"SEQN": "seqn", "MED_ALL": "med"})

    medi = compute_medi_nhanes_fped(
        fped_ind_path=paths["fpediff1"],
        nutrient_ind_path=paths["iff1"],
        fped_ind_path2=paths["fpediff2"],
        nutrient_ind_path2=paths["iff2"],
        demo_path=paths["demo"],
    )[["SEQN", "MEDI_ALL"]].rename(columns={"SEQN": "seqn", "MEDI_ALL": "medi"})

    di_gm = compute_di_gm_nhanes_fped(
        fped_ind_path=paths["fpediff1"],
        nutrient_ind_path=paths["iff1"],
        fped_ind_path2=paths["fpediff2"],
        nutrient_ind_path2=paths["iff2"],
        demo_path=paths["demo"],
    )[["SEQN", "DI_GM_TOTAL"]].rename(columns={"SEQN": "seqn", "DI_GM_TOTAL": "di_gm"})

    merged = dii
    for frame in [hei2015, hei2020, ahei, dash, dashi, med, medi, di_gm]:
        merged = merged.merge(frame, on="seqn", how="outer")

    merged["cycle"] = cycle["label"]
    return merged


def build_heatmap(scores: pd.DataFrame) -> None:
    corr = scores[SCORE_COLS].corr(method="spearman")
    corr = corr.rename(index=LABELS, columns=LABELS)
    corr.to_csv(CORR_PATH, index=True)

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(10, 8), dpi=200)
    sns.heatmap(
        corr,
        cmap="RdBu_r",
        vmin=-1,
        vmax=1,
        center=0,
        annot=True,
        fmt=".2f",
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.85, "label": "Spearman r"},
        ax=ax,
    )
    ax.set_title("NHANES 2007-2018 Dietary Index Correlation Heatmap")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    save_figure_exports(fig, HEATMAP_PATH)
    plt.close(fig)


def main() -> None:
    raw_demo = build_raw_demo_stack()

    cycle_frames = [compute_cycle_scores(cycle) for cycle in CYCLES]
    raw_scores = pd.concat(cycle_frames, ignore_index=True)
    final_scores = raw_scores.copy()

    coverage = pd.DataFrame(
        {
            "score": SCORE_COLS,
            "non_missing_n": [int(final_scores[col].notna().sum()) for col in SCORE_COLS],
            "total_n": [len(final_scores)] * len(SCORE_COLS),
        }
    )

    raw_demo_with_scores = (
        raw_demo.rename(columns={"SEQN": "seqn"})
        .merge(final_scores, on=["seqn", "cycle"], how="left")
    )

    final_scores.to_csv(SCORES_PATH, index=False)
    raw_demo_with_scores.to_csv(RAW_DEMO_WITH_SCORES_PATH, index=False)
    coverage.to_csv(COVERAGE_PATH, index=False)
    build_heatmap(final_scores)

    print(SCORES_PATH)
    print(RAW_DEMO_WITH_SCORES_PATH)
    print(COVERAGE_PATH)
    print(CORR_PATH)
    print(HEATMAP_PATH)
    print(HEATMAP_PATH.with_suffix(".tiff"))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path

from docx import Document


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = REPO_ROOT / "Supplementary Material.docx"
OUTPUT_DIR = REPO_ROOT / "streamlit_app" / "final_products"

TABLE_OUTPUTS = {
    0: "table_s1_dii_reference_database.csv",
    1: "table_s2_scoring_algorithms.csv",
    2: "table_s3_fndds_mapping.csv",
    3: "table_s4_support_matrix_detailed.csv",
    4: "table_s5_public_api_inventory.csv",
}


def _clean(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def _extract_rows(table) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.rows:
        values = [_clean(cell.text) for cell in row.cells]
        if any(values):
            rows.append(values)
    return rows


def _write_csv(rows: list[list[str]], dst: Path) -> None:
    max_cols = max(len(row) for row in rows)
    normalized = [row + [""] * (max_cols - len(row)) for row in rows]
    with dst.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerows(normalized)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = Document(DOCX_PATH)

    for idx, filename in TABLE_OUTPUTS.items():
        rows = _extract_rows(doc.tables[idx])
        dst = OUTPUT_DIR / filename
        _write_csv(rows, dst)
        print(f"Wrote {dst}")


if __name__ == "__main__":
    main()

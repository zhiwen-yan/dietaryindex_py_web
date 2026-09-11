"""File preview and loading helpers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd


def load_dataframe_from_path(path: str | Path, *, sheet_name: str | int | None = 0) -> pd.DataFrame:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path)
    if suffix == ".xlsx":
        return pd.read_excel(file_path, engine="openpyxl", sheet_name=sheet_name)
    if suffix == ".xls":
        return pd.read_excel(file_path, engine="xlrd", sheet_name=sheet_name)
    if suffix == ".xpt":
        try:
            return pd.read_sas(file_path, format="xport")
        except Exception:
            import pyreadstat

            data_bytes = file_path.read_bytes()
            df, _ = pyreadstat.read_xport(BytesIO(data_bytes))
            return df
    if suffix == ".sas7bdat":
        import pyreadstat

        data_bytes = file_path.read_bytes()
        df, _ = pyreadstat.read_sas7bdat(BytesIO(data_bytes))
        return df

    raise ValueError(f"Unsupported file type: {file_path.name}")


def preview_file(path: str | Path, *, rows: int = 10, sheet_name: str | int | None = 0) -> dict:
    df = load_dataframe_from_path(path, sheet_name=sheet_name)
    # JSON does not permit NaN or +/-Infinity.  Convert the preview to object
    # dtype first; otherwise pandas keeps missing values as float NaN even
    # after replacing them with None.
    preview = df.head(rows).astype(object)
    preview = preview.replace([float("inf"), float("-inf")], None)
    preview = preview.where(pd.notna(preview), None)
    return {
        "rows": int(len(df)),
        "columns": [str(col) for col in df.columns],
        "dtypes": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        "preview": preview.to_dict(orient="records"),
    }

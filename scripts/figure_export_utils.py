from __future__ import annotations

from pathlib import Path

from matplotlib.figure import Figure


def save_figure_exports(
    fig: Figure,
    png_path: Path,
    *,
    bbox_inches: str = "tight",
    tiff_dpi: int = 600,
) -> tuple[Path, Path]:
    """
    Save a matplotlib figure as both PNG and TIFF from the same source figure.

    PNG keeps the figure's current export defaults.
    TIFF is written at high DPI for publication delivery.
    """
    png_path = Path(png_path)
    tiff_path = png_path.with_suffix(".tiff")

    fig.savefig(png_path, bbox_inches=bbox_inches)
    fig.savefig(
        tiff_path,
        bbox_inches=bbox_inches,
        format="tiff",
        dpi=tiff_dpi,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    return png_path, tiff_path

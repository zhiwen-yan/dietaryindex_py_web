from __future__ import annotations

import importlib.util
from io import BytesIO
from pathlib import Path

from PIL import Image

from generate_1718_mixed_figures import main as regenerate_mixed_figures


REPO_ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = REPO_ROOT / "streamlit_app" / "final_products" / "figures"
FIGURES_PAGE_PATH = REPO_ROOT / "streamlit_app" / "pages" / "14_figures.py"
DPI = 600

PLOTLY_EXPORT_SPECS = {
    "figure_s1_bland_altman_panel.tiff": {"fn": "_fig_s1_bland_altman_panel", "source_png": "figure_s1_bland_altman_panel.png", "scale": 2},
    "figure5_dii_validation.tiff": {"fn": "_fig5_dii_detail", "source_png": "figure5_dii_validation.png", "scale": 2},
    "figure7_hei2020_panel.tiff": {"fn": "_fig7_hei2020_components", "source_png": "figure7_hei2020_panel.png", "scale": 2},
    "figure9_correlation_heatmap_9indices.tiff": {"fn": "_fig9_correlation_heatmap", "source_png": "figure9_correlation_heatmap_9indices.png", "scale": 2},
}


def _load_figures_page_module():
    spec = importlib.util.spec_from_file_location("figures_page_export", FIGURES_PAGE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _png_bytes_to_tiff(png_bytes: bytes, dst: Path) -> None:
    with Image.open(BytesIO(png_bytes)) as img:
        if img.mode not in {"RGB", "RGBA"}:
            img = img.convert("RGB")

        img.save(dst, format="TIFF", dpi=(DPI, DPI), compression="tiff_lzw")


def _get_png_canvas_size(filename: str) -> tuple[int, int]:
    png_path = FIG_DIR / filename
    with Image.open(png_path) as img:
        return img.size


def _export_plotly_tiff(module, filename: str, cfg: dict[str, object]) -> Path:
    fig = getattr(module, cfg["fn"])()
    width, height = _get_png_canvas_size(str(cfg["source_png"]))
    png_bytes = fig.to_image(
        format="png",
        width=width,
        height=height,
        scale=int(cfg["scale"]),
    )
    dst = FIG_DIR / filename
    _png_bytes_to_tiff(png_bytes, dst)
    return dst


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Regenerate matplotlib-origin figures directly from code.
    regenerate_mixed_figures()

    # Regenerate Plotly-origin figures directly from figure objects.
    figures_page = _load_figures_page_module()
    for filename, cfg in PLOTLY_EXPORT_SPECS.items():
        dst = _export_plotly_tiff(figures_page, filename, cfg)
        print(f"Wrote {dst}")


if __name__ == "__main__":
    main()

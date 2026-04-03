"""Generate a CausalNex structure plot for study methods."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

from causalnex.plots import EDGE_STYLE, NODE_STYLE, plot_structure
from causalnex.structure import StructureModel

from playwright.sync_api import sync_playwright

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent


def main() -> None:
    edges = [
        ("study", "uses_digital_notes"),
        ("study", "uses_notebook"),
        ("study", "uses_flashcards"),
        ("uses_digital_notes", "understanding"),
        ("uses_notebook", "understanding"),
        ("uses_flashcards", "understanding"),
        ("understanding", "learning_outcome"),
    ]
    sm = StructureModel(edges)

    node_attributes = {
        "study": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
        "uses_digital_notes": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
        "uses_notebook": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
        "uses_flashcards": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
        "understanding": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
        "learning_outcome": {
            "shape": "hexagon",
            "color": {"background": "#0b1026", "border": "#2b2f5e"},
            "font": {"color": "#e5e7ff"},
        },
    }
    viz = plot_structure(
        sm,
        all_node_attributes=NODE_STYLE.WEAK,
        node_attributes=node_attributes,
        all_edge_attributes=EDGE_STYLE.WEAK,
    )
    layout_opts = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "LR",
                "sortMethod": "directed",
                "nodeSpacing": 180,
                "levelSeparation": 240,
            }
        }
    }
    viz.set_options(options=json.dumps(layout_opts))
    html_path = ROOT / "study_methods_bn.html"
    viz.generate_html()
    html_path.write_text(viz.html, encoding="utf-8")

    png_path = ROOT / "study_methods_bn.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1300, "height": 720})
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(png_path), full_page=True)
        browser.close()

    print(f"Wrote BN HTML (CausalNex plot_structure): {html_path}")
    print(f"Wrote BN PNG (screenshot of CausalNex HTML): {png_path}")
    print("Done (CausalNex structure + plot_structure).")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate README image assets for dsh-ifc-qto (docs/assets/).

Outputs (idempotent overwrite):
  dsh-ifc-qto-flow-light.svg / dsh-ifc-qto-flow-dark.svg
      Hero pipeline diagram. Two hand-written SVG files (vector - never
      rasterized to webp). Every label is a command/config token
      (input.ifc, ifc.ingest, ...), so all five README languages share the
      same pair. The pre-existing single-version docs/assets/dsh-ifc-qto-flow.svg
      is intentionally left untouched so old external links keep resolving.

No raster asset is produced: this repository has no benchmark/RESULTS.md, so
there is no evidence bar chart to draw. If one is added later, reuse the
family template's Pillow bar-chart block (Pillow, webp quality=90, explicit
CJK font probe) and keep the light/dark pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Python 3 (the SVG path needs no third-party package)
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

# --- palette: PerryLink family (accent) + GitHub page backgrounds ----------
FAMILY = "#4B67B4"   # family accent (badges use #2B3245 as labelColor)
GREEN = {"light": "#16a34a", "dark": "#3fb950"}
SKIN = {
    "light": dict(bg="#ffffff", box="#f6f8fa", border="#d0d7de",
                  text="#1f2328", sub="#57606a"),
    "dark": dict(bg="#0d1117", box="#161b22", border="#30363d",
                 text="#f0f6fc", sub="#8b949e"),
}

# The SVG text is ASCII/command tokens, so no font is embedded. The probe is
# kept so a future raster chart cannot silently render Chinese as tofu.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",      # Microsoft YaHei
    r"C:\Windows\Fonts\simhei.ttf",    # SimHei
    r"C:\Windows\Fonts\Deng.ttf",      # DengXian
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]


def probed_font() -> str:
    path = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
    if path is None:
        sys.exit("FATAL: no CJK font found (looked for msyh.ttc, simhei.ttf, "
                 "Deng.ttf, Noto Sans CJK, PingFang). Refusing to render a "
                 "future raster chart with tofu boxes; install one of the "
                 "probed fonts and re-run.")
    return path


# ---------------------------------------------------------------------------
# Hero pipeline SVG (light + dark)
# ---------------------------------------------------------------------------
# (label, line 1, line 2) - tokens only, no prose sentences.
FLOW_NODES = [
    ("input.ifc", "ISO-10303-21", "IFC4 \u00b7 UTF-8"),
    ("ifc.unit_check", "LENGTHUNIT", "AREAUNIT \u00b7 VOLUMEUNIT"),
    ("ifc.ingest", "model_id = ifc_&lt;sha16&gt;", "elements \u00b7 IfcQuantity*"),
    ("ifc.qto_summary", "length \u00b7 area \u00b7 volume", "count \u00b7 total \u00b7 min/max"),
    ("ifc.export_csv", "exports/*.csv", "rows \u00b7 sha256"),
]


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    w, h = 1200, 440
    nw, nh, gap = 188, 104, 38
    y0 = 156
    x0 = 60
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="dsh-ifc-qto pipeline">',
        '<title>dsh-ifc-qto pipeline</title>',
        f'<rect width="{w}" height="{h}" rx="18" fill="{s["bg"]}"/>',
        f'<text x="60" y="62" fill="{s["text"]}" font-family="ui-sans-serif,'
        f'system-ui,sans-serif" font-size="30" font-weight="700">dsh-ifc-qto</text>',
        f'<text x="60" y="94" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="15">input.ifc \u00b7 ISO-10303-21 \u2192 '
        f'elements + IfcQuantity* \u2192 CSV \u00b7 local only</text>',
        f'<line x1="60" y1="116" x2="1140" y2="116" stroke="{s["border"]}"/>',
    ]
    for i, (label, sub1, sub2) in enumerate(FLOW_NODES):
        x = x0 + i * (nw + gap)
        accent = GREEN[skin] if i == len(FLOW_NODES) - 1 else (
            FAMILY if i == 1 else s["border"])
        parts.append(
            f'<rect x="{x}" y="{y0}" width="{nw}" height="{nh}" rx="14" '
            f'fill="{s["box"]}" stroke="{accent}" stroke-width="2"/>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 36}" fill="{s["text"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="15" font-weight="700">{label}</text>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 62}" fill="{s["sub"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="11">{sub1}</text>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 82}" fill="{s["sub"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="11">{sub2}</text>')
        if i < len(FLOW_NODES) - 1:
            ax = x + nw + 4
            ay = y0 + nh // 2
            parts.append(
                f'<path d="M{ax} {ay}h{gap - 12}" stroke="{s["sub"]}" '
                f'stroke-width="3"/>')
            parts.append(
                f'<path d="M{ax + gap - 14} {ay - 7}l10 7-10 7" fill="none" '
                f'stroke="{s["sub"]}" stroke-width="3" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    # local store bar under ingest / summary / export
    by, bh = 300, 72
    for i in (2, 3, 4):
        cx = x0 + nw // 2 + i * (nw + gap)
        parts.append(
            f'<path d="M{cx} {y0 + nh}v{by - y0 - nh}" stroke="{FAMILY}" '
            f'stroke-width="2" stroke-dasharray="5 5"/>')
    parts.append(
        f'<rect x="60" y="{by}" width="1092" height="{bh}" rx="12" '
        f'fill="{s["box"]}" stroke="{FAMILY}" stroke-width="2"/>')
    parts.append(
        f'<text x="84" y="{by + 30}" fill="{s["text"]}" font-family='
        f'"ui-monospace,monospace" font-size="15" font-weight="700">'
        f'$DSH_HOME/storages/dsh-ifc-qto</text>')
    parts.append(
        f'<text x="84" y="{by + 55}" fill="{s["sub"]}" font-family='
        f'"ui-monospace,monospace" font-size="12">storage domain ifc \u00b7 '
        f'models \u00b7 exports/ \u00b7 DSH_IFC_HOME</text>')
    parts.append(
        f'<text x="60" y="418" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="13">no network \u00b7 no model call \u00b7 '
        f'source .ifc unchanged</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    print(f"fonts: {probed_font()}")
    for skin in ("light", "dark"):
        with open(os.path.join(OUT, f"dsh-ifc-qto-flow-{skin}.svg"),
                  "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
    print("wrote 2 SVG assets to docs/assets/")


if __name__ == "__main__":
    main()

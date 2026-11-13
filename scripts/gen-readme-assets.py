#!/usr/bin/env python3
"""README visuals for dsh-ifc-qto -- v5, read off the shipped pipeline.

Outputs (idempotent overwrite):
  docs/assets/dsh-ifc-qto-hero-{zh,en}-{light,dark}.webp   1440x576 (Pillow)
  docs/assets/dsh-ifc-qto-flow-v5-{light,dark}.svg         1100x660 (hand SVG)

Design notes
------------
* Hero: the left column is prose (kicker / title / two value lines / one
  subtitle / one meta / footer). The right column is this repository's own
  semantic object -- a six-line excerpt of the real STEP text from
  samples/quickstart/input/sample-building.ifc, each line annotated with the
  thing the plugin extracts from it (element type, quantity kind, the flagged
  zero, the unit assignment), plus the three real totals and the 11-row CSV.
* Flow: a take-off sheet, not a row of boxes. One local .ifc text fans into
  two readers (ifc_unit_check stamps the unit header, ifc_ingest fills the
  element-class matrix and the quantity rows), the sheet is keyed by
  model_id in the `ifc` storage domain, ifc_qto_summary computes
  count/total/min/max and the non-positive issue, and ifc_export_csv tears
  the bottom strip off as exports/ifc_<sha16>.csv. Grammar: matrix /
  take-off-sheet scoreboard.

Every number and token is taken from src/core/ifc.ts, src/plugin/tools.ts,
package.json or samples/quickstart/expected/result.json:
  6 elements, 5 types (WALL 2, SLAB 1, DOOR 1, WINDOW 1, COLUMN 1),
  6 quantities (length 3: 900/3000/4200 total 8100; area 2: 86.4/0 total
  86.4 min 0; volume 1: 25.92), 1 issue E_IFC_QUANTITY_NON_POSITIVE
  NetSideArea=0, 11 CSV rows, sha256 3e8f62d3e7fd6a56..., units
  MILLI|METRE / $|SQUARE_METRE / $|CUBIC_METRE, 1 718 B sample.

Run once:  python scripts/gen-readme-assets.py
Requires:  Python 3.10+ with Pillow; Windows fonts msyh.ttc / msyhbd.ttc /
           consola.ttf / segoeui.ttf / segoeuib.ttf.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_EN = r"C:\Windows\Fonts\segoeui.ttf"
FONT_EN_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_EN, FONT_EN_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

WARNINGS: list[str] = []

# Shapes are composited at 2x and downsampled: crisp cards and chips.
S = 2

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8", card="#ffffff",
        card_edge="#e4e1ee", zone="#f5f2fb", zone_edge="#e3def1",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent_soft="#ece7f9",
        good="#16a34a", warn="#c2410c", danger="#c02b2b",
        danger_soft="#fbe9ea", grid="#e7e4f0", pill="#ece7f9",
        dots="#d9d3ea", shadow=(34, 28, 66), shadow_a=26,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016", card="#1b2231",
        card_edge="#2e374b", zone="#171e2d", zone_edge="#2b3448",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent_soft="#242d42",
        good="#3fb950", warn="#d29922", danger="#f87171",
        danger_soft="#3a2026", grid="#2a3346", pill="#242d42",
        dots="#263049", shadow=(0, 0, 0), shadow_a=110,
    ),
}

# real quickstart fixture numbers (samples/quickstart/expected/result.json)
TYPES = [("WALL", 2), ("SLAB", 1), ("DOOR", 1), ("WINDOW", 1), ("COLUMN", 1),
         ("BEAM", 0), ("FOOTING", 0), ("STAIR", 0), ("RAILING", 0),
         ("RAMP", 0), ("PILE", 0), ("MEMBER", 0), ("PLATE", 0),
         ("COVERING", 0)]
KINDS = [
    ("length", "3", "8 100 mm", "900", "4 200"),
    ("area", "2", "86.4 m²", "0", "86.4"),
    ("volume", "1", "25.92 m³", "25.92", "25.92"),
]

# --------------------------------------------------------------- primitives


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD, "mono": FONT_MONO,
         "en": FONT_EN, "en_bold": FONT_EN_BOLD}[kind], int(round(size * S)))


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: str, b: str, t: float) -> tuple[int, int, int]:
    return tuple(int(x + (y - x) * t) for x, y in zip(hx(a), hx(b)))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = 0.20 * (y / h) + 0.80 * (y / h) ** 1.5
        d.line([(0, y), (w, y)], fill=mix(c1, c2, t))
    return base


def glow(img: Image.Image, cx: float, cy: float, r: float, color: str,
         alpha: int = 40) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(12, 0, -1):
        rr = r * i / 12
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (1 - i / 13)),))
    layer = layer.filter(ImageFilter.GaussianBlur(26))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def tw(s: str, size: float, kind: str = "cjk") -> float:
    return MEASURE.textlength(s, font=font(size, kind)) / S


def fit(s: str, kind: str, start: float, max_w: float,
        floor: float = 12) -> float:
    size = start
    while size > floor:
        if tw(s, size, kind) <= max_w:
            return size
        size -= 1
    return floor


class Layer:
    """Vector layer in design coordinates (1440x576), rasterised at 2x."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def refresh(self) -> None:
        self.d = ImageDraw.Draw(self.img)

    def rect(self, box, radius: float = 0, fill=None, outline=None,
             width: float = 1.0) -> None:
        self.d.rounded_rectangle([v * S for v in box], radius=radius * S,
                                 fill=fill, outline=outline,
                                 width=max(1, round(width * S)))

    def line(self, p1, p2, fill, width: float = 1.0) -> None:
        self.d.line([p1[0] * S, p1[1] * S, p2[0] * S, p2[1] * S],
                    fill=fill, width=max(1, round(width * S)))

    def shadow(self, box, radius: float = 22, blur: float = 16,
               color=(0, 0, 0), alpha: int = 30, dy: float = 10) -> None:
        sh = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        d.rounded_rectangle([box[0] * S, (box[1] + dy) * S, box[2] * S,
                             (box[3] + dy) * S], radius=radius * S,
                            fill=color + (alpha,))
        sh = sh.filter(ImageFilter.GaussianBlur(blur * S))
        self.img = Image.alpha_composite(self.img, sh)
        self.refresh()

    def text(self, xy, s: str, size: float, kind: str = "cjk",
             fill: str = "#000000", anchor: str = "la") -> None:
        self.d.text((xy[0] * S, xy[1] * S), s, font=font(size, kind),
                    fill=hx(fill), anchor=anchor)

    def flatten(self) -> Image.Image:
        return self.img.resize((self.w, self.h), Image.LANCZOS)


def write(layer: Layer, xy, s: str, skin, size: float, kind: str,
          color: str, max_w: float | None = None, min_size: float = 11,
          tag: str = "", anchor: str = "la") -> float:
    if max_w is not None:
        size = fit(s, kind, size, max_w, min_size)
        if tw(s, size, kind) > max_w:
            WARNINGS.append(f"{tag}: {s!r} wider than {max_w}px")
            print(f"WARN {tag}: {s!r} wider than {max_w}px")
    layer.text(xy, s, size, kind, skin[color], anchor)
    return size


# --------------------------------------------------------------- hero model

HERO = {
    "zh": dict(
        kicker="DeepSeek Harness · IFC 工程量清点插件",
        title="dsh-ifc-qto",
        value=["读本地 IFC，数清 14 类构件", "3 组工程量汇总，导出 CSV"],
        sub="读 .ifc → 数构件、查单位 → 导出 CSV",
        meta="R0 只读 / R1 本地写 · 无网络 · 不调模型",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        card_title="从 STEP 文本里取量",
        card_sub="ISO-10303-21 · IFC4 · 一行一条实体",
        csv_tag=["CSV · 11 行", "sha256 3e8f62d3…"],
        notes=["构件 · WALL", "构件 · DOOR", "工程量 · LENGTH",
               "工程量 · AREA", "E_IFC_QUANTITY_NON_POSITIVE",
               "单位声明 · 3 项"],
        tiles=[("长度合计 · mm", "8 100", "3 笔 · min 900 · max 4 200"),
               ("面积合计 · m²", "86.4", "2 笔 · min 0 · max 86.4"),
               ("体积合计 · m³", "25.92", "1 笔 · 25.92")],
        units="units  MILLI|METRE · $|SQUARE_METRE · $|CUBIC_METRE · assignment=true",
    ),
    "en": dict(
        kicker="DeepSeek Harness · IFC take-off plugin",
        title="dsh-ifc-qto",
        value=["14 element classes from one local IFC",
               "Three quantity kinds into one CSV"],
        sub="Local .ifc → count, check units → CSV",
        meta="R0 read-only / R1 local write · no network · no model",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        card_title="Reading the STEP text",
        card_sub="ISO-10303-21 · IFC4 · one entity per line",
        csv_tag=["CSV · 11 rows", "sha256 3e8f62d3…"],
        notes=["element · WALL", "element · DOOR", "quantity · LENGTH",
               "quantity · AREA", "E_IFC_QUANTITY_NON_POSITIVE",
               "unit assignment · 3 units"],
        tiles=[("length total · mm", "8 100", "3 rows · min 900 · max 4 200"),
               ("area total · m²", "86.4", "2 rows · min 0 · max 86.4"),
               ("volume total · m³", "25.92", "1 row · 25.92")],
        units="units  MILLI|METRE · $|SQUARE_METRE · $|CUBIC_METRE · assignment=true",
    ),
}

# six real lines from samples/quickstart/input/sample-building.ifc
CODE_ROWS = [
    [("#101=", "faint"), ("IFCWALL", "accent"),
     ("('0SAMPLEWALL0000000001',#20,…);", "sub")],
    [("#104=", "faint"), ("IFCDOOR", "accent"),
     ("('0SAMPLEDOOR0000000001',#20,…);", "sub")],
    [("#201=", "faint"), ("IFCQUANTITYLENGTH", "accent"),
     ("('Length',$,", "sub"), ("4200.", "text"), (",$);", "sub")],
    [("#204=", "faint"), ("IFCQUANTITYAREA", "accent"),
     ("('NetArea',$,", "sub"), ("86.4", "text"), (",$);", "sub")],
    [("#206=", "faint"), ("IFCQUANTITYAREA", "accent"),
     ("('NetSideArea',$,", "sub"), ("0.", "danger"), (",$);", "sub")],
    [("#10=", "faint"), ("IFCUNITASSIGNMENT", "accent"),
     ("((#11,#12,#13));", "sub")],
]


def hero(lang: str, skin_name: str) -> None:
    s = SKIN[skin_name]
    hm = HERO[lang]
    zh = lang == "zh"
    w, h = 1440, 576
    img = gradient(w, h, s["bg_from"], s["bg_to"])
    img = glow(img, 1170, 30, 430, hx(s["accent"]),
               20 if skin_name == "light" else 38)
    img = glow(img, 110, 566, 300, hx(s["accent"]),
               10 if skin_name == "light" else 16)

    L = Layer(w, h)
    m = 60

    # ---------------------------------------------------------- left column
    ksize = 20 if zh else 19
    kkind = "cjk_bold" if zh else "en_bold"
    kw = tw(hm["kicker"], ksize, kkind)
    L.rect((m, 62, m + kw + 40, 62 + ksize + 22), radius=(ksize + 22) / 2,
           fill=hx(s["pill"]))
    L.text((m + 20, 62 + 11), hm["kicker"], ksize, kkind, s["accent"])

    tsize = fit(hm["title"], "mono", 84, 540, 64)
    L.text((m, 124), hm["title"], tsize, "mono", s["text"])

    vkind = "cjk_bold" if zh else "en_bold"
    vsize = 38 if zh else 33
    for line in hm["value"]:
        vsize = min(vsize, fit(line, vkind, vsize, 540, 24))
    for i, line in enumerate(hm["value"]):
        L.text((m, 258 + i * (vsize + 14)), line, vsize, vkind, s["text"])

    write(L, (m + 2, 374), hm["sub"], s, 25, "cjk" if zh else "en", "sub",
          540, 24, f"hero.{lang}.sub")
    write(L, (m + 2, 436), hm["meta"], s, 20, "cjk" if zh else "en", "faint",
          540, 19, f"hero.{lang}.meta")

    L.line((m + 2, 474), (m + 542, 474), hx(s["grid"]), 1.6)
    write(L, (m + 2, 492), hm["foot"], s, 17, "en", "faint", 540, 14,
          f"hero.{lang}.foot")

    # ------------------------------------------------------- right: text card
    cb = (620, 44, 1380, 508)
    L.shadow(cb, radius=22, blur=18, color=s["shadow"], alpha=s["shadow_a"],
             dy=12)
    L.rect(cb, radius=22, fill=hx(s["card"]), outline=hx(s["card_edge"]),
           width=1.4)

    write(L, (652, 70), hm["card_title"], s, 22, "cjk_bold" if zh else "en_bold",
          "text", 420, 18, f"hero.{lang}.card_title")
    write(L, (652, 101), hm["card_sub"], s, 14, "cjk" if zh else "en", "faint",
          420, 12, f"hero.{lang}.card_sub")

    # CSV tag (tear-off receipt, top right)
    tag_box = (1178, 64, 1352, 120)
    L.rect(tag_box, radius=12, fill=hx(s["zone"]), outline=hx(s["zone_edge"]),
           width=1.2)
    write(L, (1192, 72), hm["csv_tag"][0], s, 12.5,
          "cjk_bold" if zh else "en_bold", "accent", 150, 11,
          f"hero.{lang}.csv0")
    write(L, (1192, 96), hm["csv_tag"][1], s, 10.5, "mono", "faint", 150, 9,
          f"hero.{lang}.csv1")

    L.line((630, 130), (1370, 130), hx(s["grid"]), 1.3)

    # code rows with per-row annotations
    row_y = [162, 204, 246, 288, 330, 372]
    code_size = 14
    for i, segs in enumerate(CODE_ROWS):
        y = row_y[i]
        if i % 2 == 0:
            L.rect((632, y - 27, 1368, y + 11), radius=8, fill=hx(s["zone"]))
        L.rect((638, y - 18, 642, y + 6), radius=2, fill=hx(s["accent"]))
        x = 656
        for text, key in segs:
            L.text((x, y - 13), text, code_size, "mono", s[key])
            x += tw(text, code_size, "mono")
        note = hm["notes"][i]
        if i == 4:
            write(L, (1356, y - 9), note, s, 11, "mono", "danger", 300, 9,
                  f"hero.{lang}.note4", anchor="ra")
        else:
            nsize = 13 if zh else 12.5
            nkind = "cjk" if zh else "en"
            write(L, (1356, y - 10), note, s, nsize, nkind,
                  "accent" if i in (2, 3, 5) else "sub", 296, 10,
                  f"hero.{lang}.note{i}", anchor="ra")

    # ------------------------------------------------------- totals + units
    L.line((630, 390), (1370, 390), hx(s["grid"]), 1.3)
    tile_x = [652, 888, 1124]
    for i, (label, value, note) in enumerate(hm["tiles"]):
        x = tile_x[i]
        L.rect((x, 396, x + 224, 466), radius=12, fill=hx(s["zone"]),
               outline=hx(s["zone_edge"]), width=1.0)
        write(L, (x + 14, 405), label, s, 11, "cjk" if zh else "en", "sub",
              196, 10, f"hero.{lang}.tile{i}label")
        L.text((x + 14, 423), value, 23, "mono", s["text"])
        write(L, (x + 14, 452), note, s, 10.5, "cjk" if zh else "en", "faint",
              196, 9, f"hero.{lang}.tile{i}note")

    L.line((630, 474), (1370, 474), hx(s["grid"]), 1.3)
    write(L, (652, 479), hm["units"], s, 11, "mono", "faint", 700, 9,
          f"hero.{lang}.units")

    out = os.path.join(OUT, f"dsh-ifc-qto-hero-{lang}-{skin_name}.webp")
    img = Image.alpha_composite(img.convert("RGBA"), L.flatten()).convert("RGB")
    img.save(out, "WEBP", quality=92)
    print(f"wrote {os.path.basename(out)}")


# ------------------------------------------------------------- flow diagram

MONO = ("ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', "
        "monospace")
SANS = ("ui-sans-serif, system-ui, -apple-system, 'Segoe UI', "
        "'Microsoft YaHei', 'PingFang SC', sans-serif")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_text(x: float, y: float, s: str, size: float, fill: str,
             family: str = SANS, weight: int | None = None,
             anchor: str | None = None, ls: float | None = None) -> str:
    a = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
         f'font-family="{family}"', f'font-size="{size}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    if ls:
        a.append(f'letter-spacing="{ls}"')
    return f'<text {" ".join(a)}>{esc(s)}</text>'


def svg_rect(x: float, y: float, w: float, h: float, r: float,
             fill: str, stroke: str | None = None,
             sw: float = 1.2, extra: str = "") -> str:
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill}"{st}{(" " + extra) if extra else ""}/>')


def svg_pill(x: float, y: float, w: float, h: float, label: str, s: dict,
             size: float = 11.5, mono: bool = True,
             fill: str | None = None, color: str | None = None) -> str:
    out = [svg_rect(x, y, w, h, h / 2, fill or s["accent_soft"])]
    out.append(svg_text(x + w / 2, y + h / 2 + size * 0.36, label, size,
                        color or s["accent"], MONO if mono else SANS,
                        anchor="middle"))
    return "".join(out)


def number_badge(cx: float, cy: float, n: str, s: dict) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="{s["accent"]}"/>'
            + svg_text(cx, cy + 3.6, n, 10.5, s["card"], MONO, 700,
                       anchor="middle"))


def arrow_head(x: float, y: float, dx: float, dy: float, color: str) -> str:
    """Small triangle pointing along (dx, dy)."""
    px, py = -dy, dx
    tip = (x + dx * 6, y + dy * 6)
    a = (x + px * 3.6, y + py * 3.6)
    b = (x - px * 3.6, y - py * 3.6)
    return (f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} '
            f'{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}" '
            f'fill="{color}"/>')


def check_mark(x: float, y: float, color: str) -> str:
    return (f'<path d="M{x} {y}l4 4 7-8" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def flow_svg(skin_name: str) -> str:
    s = SKIN[skin_name]
    W, H = 1100, 660
    el: list[str] = []

    el.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="dsh-ifc-qto structure: '
        f'one local .ifc text is read by ifc_unit_check for the unit '
        f'declaration and by ifc_ingest into 14 element classes and 3 '
        f'quantity kinds stored as model_id in the ifc domain models table; '
        f'ifc_qto_summary computes count, total and min/max plus the '
        f'non-positive issue, and ifc_export_csv writes '
        f'exports/ifc_92f1f2cfc519059a.csv with 11 rows and a sha256">')
    el.append('<title>dsh-ifc-qto: one take-off sheet, four local tools</title>')
    el.append('<defs>')
    el.append(
        '<linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">'
        f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
        f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    shadow_color = "#1b1735" if skin_name == "light" else "#000000"
    shadow_opacity = 0.10 if skin_name == "light" else 0.55
    el.append(
        '<filter id="soft" x="-25%" y="-25%" width="150%" height="170%">'
        f'<feDropShadow dx="0" dy="9" stdDeviation="12" '
        f'flood-color="{shadow_color}" flood-opacity="{shadow_opacity}"/>'
        '</filter>')
    el.append(
        f'<pattern id="dots" width="26" height="26" '
        f'patternUnits="userSpaceOnUse"><circle cx="1.4" cy="1.4" r="1.4" '
        f'fill="{s["dots"]}"/></pattern>')
    el.append('</defs>')

    el.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    el.append(f'<rect width="{W}" height="{H}" fill="url(#dots)" '
              f'opacity="{0.45 if skin_name == "light" else 0.5}"/>')

    # ------------------------------------------------------------- header
    el.append(svg_text(44, 52, "dsh-ifc-qto", 31, s["text"], MONO, 700))
    el.append(svg_text(
        44, 78,
        "one local .ifc text → take-off sheet → summary + CSV · "
        "text-level, no geometry take-off",
        14, s["sub"]))
    el.append(svg_rect(784, 28, 256, 32, 16, s["pill"]))
    el.append(svg_text(912, 49, "ISO-10303-21 · IFC4 · text only", 13,
                       s["accent"], MONO, anchor="middle"))
    el.append(f'<line x1="44" y1="94" x2="1056" y2="94" '
              f'stroke="{s["grid"]}" stroke-width="1.4"/>')

    # -------------------------------------------------------------- sheet
    el.append('<g filter="url(#soft)">')
    el.append(svg_rect(40, 104, 1020, 482, 20, s["card"], s["card_edge"],
                       1.4))
    el.append('</g>')

    # header: source pane + two readers + sheet identity
    el.append(svg_text(60, 132, "SOURCE · READ-ONLY · 1 718 B", 11,
                       s["accent"], MONO, 600, ls=1.1))
    for i, line in enumerate(("ISO-10303-21;", "FILE_SCHEMA(('IFC4'));",
                              "#101=IFCWALL('0SAMPLE…');")):
        el.append(svg_text(60, 152 + i * 17, line, 11, s["sub"], MONO))

    # fan-out: one text, two readers
    el.append(f'<path d="M300 157h6" stroke="{s["accent"]}" stroke-width="1.6"/>')
    el.append(f'<path d="M306 141v32" stroke="{s["accent"]}" stroke-width="1.6"/>')
    el.append(f'<path d="M306 141h6" stroke="{s["accent"]}" stroke-width="1.6"/>')
    el.append(f'<path d="M306 173h6" stroke="{s["accent"]}" stroke-width="1.6"/>')
    el.append(arrow_head(313, 141, 1, 0, s["accent"]))
    el.append(arrow_head(313, 173, 1, 0, s["accent"]))

    readers = [("1", "ifc_unit_check", "R0 · units"),
               ("2", "ifc_ingest", "R1 · types + quantities")]
    for i, (n, name, note) in enumerate(readers):
        y = 126 + i * 36
        el.append(svg_rect(320, y, 292, 28, 14, s["zone"], s["zone_edge"],
                           1.1))
        el.append(number_badge(338, y + 14, n, s))
        el.append(svg_text(352, y + 18, name, 13, s["text"], MONO, 700))
        el.append(svg_text(596, y + 18, note, 11, s["sub"], anchor="end"))

    el.append(svg_text(640, 140, "TAKE-OFF SHEET", 16, s["text"], SANS, 700,
                       ls=2.4))
    el.append(svg_text(640, 164, "model_id  ifc_92f1f2cfc519059a", 13,
                       s["sub"], MONO))
    el.append(svg_text(640, 184,
                       "key = 'ifc_' + sha256(text)[:16] · domain ifc · models",
                       11, s["faint"], MONO))
    el.append(f'<line x1="60" y1="200" x2="1040" y2="200" '
              f'stroke="{s["grid"]}" stroke-width="1.2"/>')

    # unit declaration strip
    el.append(number_badge(68, 224, "1", s))
    el.append(svg_text(84, 228, "UNIT DECLARATION · 3", 11, s["accent"],
                       MONO, 600, ls=1.1))
    el.append(svg_text(1040, 228, "ifc_unit_check · R0 · issues=0", 11,
                       s["faint"], anchor="end"))
    units = [("LENGTHUNIT", "MILLI|METRE"), ("AREAUNIT", "$|SQUARE_METRE"),
             ("VOLUMEUNIT", "$|CUBIC_METRE")]
    for i, (label, value) in enumerate(units):
        x = 60 + i * 332
        el.append(svg_rect(x, 238, 316, 38, 11, s["zone"], s["zone_edge"],
                           1.1))
        el.append(svg_text(x + 14, 253, label, 11, s["accent"], MONO, 600,
                           ls=0.9))
        el.append(svg_text(x + 14, 270, value, 13, s["text"], MONO))
        el.append(check_mark(x + 282, 256, s["good"]))

    # element class matrix
    el.append(number_badge(68, 298, "2", s))
    el.append(svg_text(84, 302, "ELEMENT CLASSES · 14", 11, s["accent"],
                       MONO, 600, ls=1.1))
    el.append(svg_text(1040, 302,
                       "ifc_ingest · R1 · 5 of 14 present · elements=6", 11,
                       s["faint"], anchor="end"))
    for i, (name, count) in enumerate(TYPES):
        x = 60 + i * 70
        present = count > 0
        el.append(svg_rect(x, 310, 64, 60, 12,
                           s["card"] if present else s["zone"],
                           s["accent"] if present else s["zone_edge"],
                           1.4 if present else 1.0))
        el.append(svg_text(x + 32, 333, name, 13,
                           s["text"] if present else s["faint"], MONO,
                           anchor="middle"))
        el.append(svg_text(x + 32, 357, str(count), 18,
                           s["accent"] if present else s["faint"], MONO, 700,
                           anchor="middle"))

    # measurement kinds + issue
    el.append(number_badge(68, 392, "3", s))
    el.append(svg_text(84, 396, "MEASUREMENT KINDS · 3", 11, s["accent"],
                       MONO, 600, ls=1.1))
    el.append(svg_text(750, 396, "ifc_qto_summary · R0 · quantities=6", 11,
                       s["faint"], anchor="end"))

    cols = [("kind", 60, "start"), ("qty", 310, "end"), ("total", 480, "end"),
            ("min", 610, "end"), ("max", 750, "end")]
    for label, x, anchor in cols:
        el.append(svg_text(x, 418, label, 11, s["faint"], MONO,
                           anchor=anchor))
    el.append(f'<line x1="60" y1="426" x2="750" y2="426" '
              f'stroke="{s["grid"]}" stroke-width="1.2"/>')
    for i, (kind, qty, total, mn, mx) in enumerate(KINDS):
        y = 446 + i * 30
        el.append(svg_text(60, y, kind, 13.5, s["text"], MONO, 700))
        el.append(svg_text(310, y, qty, 13, s["sub"], MONO, anchor="end"))
        el.append(svg_text(480, y, total, 13.5, s["text"], MONO,
                           anchor="end"))
        el.append(svg_text(610, y, mn, 13.5,
                           s["danger"] if mn == "0" else s["sub"], MONO,
                           anchor="end"))
        el.append(svg_text(750, y, mx, 13.5, s["sub"], MONO, anchor="end"))
        if i < 2:
            el.append(f'<line x1="60" y1="{y + 10}" x2="750" y2="{y + 10}" '
                      f'stroke="{s["grid"]}" stroke-width="0.9" '
                      f'opacity=".7"/>')

    # issue card
    el.append(svg_rect(790, 390, 250, 122, 14, s["danger_soft"], s["danger"],
                       1.2))
    el.append(svg_text(808, 414, "DATA QUALITY · 1", 11, s["danger"], MONO,
                       600, ls=1.1))
    el.append(svg_text(808, 436, "E_IFC_QUANTITY_NON_POSITIVE", 11,
                       s["danger"], MONO))
    el.append(svg_text(808, 458, "NetSideArea = 0", 13, s["text"], MONO, 700))
    el.append(svg_text(808, 480, "flagged, not dropped:", 11, s["sub"]))
    el.append(svg_text(808, 496, "the other rows still total", 11,
                       s["sub"]))

    # tear-off CSV strip
    el.append(f'<line x1="60" y1="520" x2="1040" y2="520" '
              f'stroke="{s["grid"]}" stroke-width="1.6" '
              f'stroke-dasharray="7 7"/>')
    el.append(svg_rect(60, 534, 192, 32, 16, s["accent_soft"]))
    el.append(number_badge(78, 550, "4", s))
    el.append(svg_text(92, 554, "ifc_export_csv · R1", 11.5, s["accent"],
                       MONO, 700))
    el.append(svg_text(268, 554, "exports/ifc_92f1f2cfc519059a.csv", 13,
                       s["text"], MONO))
    el.append(svg_text(534, 554, "11 rows", 13, s["sub"], MONO))
    el.append(svg_text(600, 554, "sha256 3e8f62d3e7fd6a56…", 12, s["faint"],
                       MONO))
    el.append(svg_text(1040, 554, "same text → same model_id", 11,
                       s["faint"], anchor="end"))

    # ------------------------------------------------------------- footer
    el.append(svg_text(
        44, 630,
        "no network · no model call · source .ifc unchanged · writes only "
        "under $DSH_IFC_HOME", 11.5, s["faint"]))
    el.append(svg_text(1056, 630,
                       "sample: samples/quickstart/input/sample-building.ifc",
                       11.5, s["faint"], anchor="end"))

    el.append('</svg>')
    return "\n".join(el) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"dsh-ifc-qto-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {os.path.basename(path)}")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s)")
    else:
        print("no width warnings")


if __name__ == "__main__":
    main()

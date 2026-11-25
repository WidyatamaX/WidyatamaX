#!/usr/bin/env python3
"""
OMORI Dark Headspace & RPG Box SVG generator for @WidyatamaX.
Produces responsive desktop (1200px) and mobile (480px) GitHub-safe SVGs
using pure SVG + CSS animations (no external fonts, no JavaScript).
"""

from __future__ import annotations

import html
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# --- OMORI Dark Headspace & RPG Palette ---
C = {
    "void": "#0b0a12",
    "deep": "#110f1d",
    "panel": "#151226",
    "card": "#1b1730",
    "white": "#f5f2eb",
    "muted": "#9b97b8",
    "dim": "#4c4669",
    "grid": "#2a2444",
    "lavender": "#a78bfa",
    "periwinkle": "#8b80f9",
    "sky": "#7dd3fc",
    "rose": "#f472b6",
    "crimson": "#fb7185",
    "mint": "#86efac",
    "amber": "#fcd34d",
}

FONT_MONO = "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
FONT_SANS = "'Plus Jakarta Sans', 'Segoe UI', system-ui, -apple-system, sans-serif"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def svg_wrap(width: int, height: int, label: str, defs: str, styles: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">\n'
        f"  <title>{esc(label)}</title>\n"
        f"  <defs>\n{defs}\n  </defs>\n"
        f"  <style>\n"
        f"    text {{ font-family: {FONT_MONO}; }}\n"
        f"    .sans {{ font-family: {FONT_SANS}; }}\n"
        f"    @media (prefers-reduced-motion: reduce) {{\n"
        f"      * {{ animation: none !important; transition: none !important; }}\n"
        f"    }}\n"
        f"{styles}\n"
        f"  </style>\n"
        f"{body}\n"
        f"</svg>\n"
    )


def common_bg_defs(uid: str) -> str:
    return f"""    <linearGradient id="{uid}-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0a12"/>
      <stop offset="55%" stop-color="#131024"/>
      <stop offset="100%" stop-color="#0d0b17"/>
    </linearGradient>
    <radialGradient id="{uid}-nebula-l" cx="22%" cy="28%" r="55%">
      <stop offset="0%" stop-color="{C['lavender']}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="{C['void']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{uid}-nebula-r" cx="84%" cy="76%" r="50%">
      <stop offset="0%" stop-color="{C['sky']}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{C['void']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="{uid}-dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1" fill="{C['white']}" opacity="0.065"/>
    </pattern>"""


def rpg_box(
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str = C["void"],
    border: str = C["white"],
    outer_w: float = 2.5,
    inset: float = 5.0,
    radius: float = 2.0,
    fill_opacity: float = 0.94,
) -> str:
    """Signature OMORI double-bordered RPG dialogue box."""
    return (
        f'  <g class="rpg-box">\n'
        f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" fill-opacity="{fill_opacity}" stroke="{border}" stroke-width="{outer_w}"/>\n'
        f'    <rect x="{x + inset}" y="{y + inset}" width="{w - inset * 2}" height="{h - inset * 2}" '
        f'rx="{max(0.0, radius - 1)}" fill="none" stroke="{border}" stroke-width="1" opacity="0.65"/>\n'
        f"  </g>"
    )


def star4(cx: float, cy: float, r: float, fill: str = C["white"], opacity: float = 0.9, cls: str = "") -> str:
    """Hand-drawn 4-point Headspace sparkle star."""
    ir = r * 0.28
    pts = [
        (cx, cy - r),
        (cx + ir, cy - ir),
        (cx + r, cy),
        (cx + ir, cy + ir),
        (cx, cy + r),
        (cx - ir, cy + ir),
        (cx - r, cy),
        (cx - ir, cy - ir),
    ]
    pstr = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    c_attr = f' class="{cls}"' if cls else ""
    return f'<polygon points="{pstr}" fill="{fill}" opacity="{opacity}"{c_attr}/>'


def black_lightbulb(cx: float, top_y: float, cord_len: float, scale: float = 1.0, sway_cls: str = "sway") -> str:
    """Original vector black lightbulb hanging on a thin wire (OMORI homage)."""
    by = top_y + cord_len
    return f"""  <g class="{sway_cls}" style="transform-origin: {cx}px {top_y}px;">
    <line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{by}" stroke="{C['white']}" stroke-width="{1.6 * scale:.2f}" opacity="0.72"/>
    <g transform="translate({cx}, {by}) scale({scale})">
      <!-- Subtle eerie white-lavender aura -->
      <circle cx="0" cy="34" r="34" fill="{C['lavender']}" opacity="0.13"/>
      <circle cx="0" cy="34" r="24" fill="{C['white']}" opacity="0.09"/>
      <!-- Screw socket -->
      <rect x="-7" y="0" width="14" height="10" rx="2" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.8"/>
      <line x1="-6" y1="4" x2="6" y2="4" stroke="{C['white']}" stroke-width="1" opacity="0.7"/>
      <line x1="-6" y1="7.5" x2="6" y2="7.5" stroke="{C['white']}" stroke-width="1" opacity="0.7"/>
      <!-- Black glass bulb -->
      <path d="M -8 10 C -19 15 -22 28 -18 40 C -14 50 -7 54 0 54 C 7 54 14 50 18 40 C 22 28 19 15 8 10 Z"
            fill="#06050a" stroke="{C['white']}" stroke-width="2.2" stroke-linejoin="round"/>
      <!-- Inner white sketchy filament -->
      <path d="M -4 14 L -3 28 L 0 24 L 3 28 L 4 14" fill="none" stroke="{C['white']}" stroke-width="1.2" opacity="0.82" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Tiny highlight ink stroke -->
      <path d="M -12 24 C -13 30 -11 36 -8 40" fill="none" stroke="{C['white']}" stroke-width="1.3" opacity="0.45" stroke-linecap="round"/>
    </g>
  </g>"""


def pill(x: float, y: float, text: str, accent: str, height: float = 28, font_size: float = 12.5) -> tuple[str, float]:
    """RPG-bordered pill badge with accurate width calculation."""
    w = max(68.0, len(text) * (font_size * 0.63) + 34.0)
    svg = (
        f'  <g>\n'
        f'    <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{height}" rx="2" '
        f'fill="{C["void"]}" stroke="{C["white"]}" stroke-width="1.2" stroke-opacity="0.72"/>\n'
        f'    <circle cx="{x + 12:.1f}" cy="{y + height / 2:.1f}" r="3.4" fill="{accent}"/>\n'
        f'    <text x="{x + 22:.1f}" y="{y + height / 2 + 4.2:.1f}" fill="{C["white"]}" '
        f'font-size="{font_size}" font-weight="600">{esc(text)}</text>\n'
        f"  </g>"
    )
    return svg, w


# =====================================================================
# 1. HEADER BANNER (Desktop 1200x340 & Mobile 480x560)
# =====================================================================
def build_header_desktop() -> str:
    defs = common_bg_defs("hdr")
    styles = """    .sway { animation: sway 5.4s ease-in-out infinite; }
    .tw1 { animation: tw 3.2s ease-in-out infinite; }
    .tw2 { animation: tw 4.4s ease-in-out infinite 1.1s; }
    .tw3 { animation: tw 3.8s ease-in-out infinite 0.5s; }
    .blink { animation: blink 1.15s steps(2, start) infinite; }
    @keyframes sway { 0%, 100% { transform: rotate(-2.4deg); } 50% { transform: rotate(2.4deg); } }
    @keyframes tw { 0%, 100% { opacity: 0.95; } 50% { opacity: 0.25; } }
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0.12; } }"""

    stars = [
        (82, 62, 7.5, C["white"], "tw1"),
        (145, 275, 5.5, C["lavender"], "tw2"),
        (292, 74, 5.0, C["sky"], "tw3"),
        (980, 56, 6.5, C["white"], "tw2"),
        (1060, 128, 8.5, C["lavender"], "tw1"),
        (1126, 78, 5.5, C["rose"], "tw3"),
        (1095, 255, 6.5, C["sky"], "tw2"),
        (1018, 286, 4.8, C["amber"], "tw1"),
        (56, 198, 4.5, C["rose"], "tw3"),
    ]
    star_svg = "\n  ".join(star4(x, y, r, col, 0.92, cls) for x, y, r, col, cls in stars)

    # Subtle constellation on right side
    constellation = f"""  <g opacity="0.38" stroke="{C['lavender']}" stroke-width="1" stroke-dasharray="3 4" fill="none">
    <path d="M 980 56 L 1060 128 L 1126 78 M 1060 128 L 1095 255 L 1018 286"/>
  </g>
  <!-- Dream crescent moon -->
  <g transform="translate(1078, 178)" opacity="0.72">
    <path d="M 10 -24 A 24 24 0 1 0 24 14 A 19 19 0 1 1 10 -24 Z" fill="none" stroke="{C['white']}" stroke-width="1.8"/>
  </g>"""

    body = f"""  <rect width="1200" height="340" rx="10" fill="url(#hdr-bg)"/>
  <rect width="1200" height="340" rx="10" fill="url(#hdr-nebula-l)"/>
  <rect width="1200" height="340" rx="10" fill="url(#hdr-nebula-r)"/>
  <rect width="1200" height="340" rx="10" fill="url(#hdr-dots)"/>
  <rect x="8" y="8" width="1184" height="324" rx="6" fill="none" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="4 6" opacity="0.65"/>

  {constellation}
  {star_svg}

  <!-- Hanging Black Lightbulb -->
  {black_lightbulb(165, 0, 96, 1.15, "sway")}

  <!-- Tiny sketchy floor shadow under lightbulb -->
  <ellipse cx="165" cy="272" rx="46" ry="7" fill="{C['lavender']}" opacity="0.12"/>
  <text x="165" y="294" text-anchor="middle" fill="{C['muted']}" font-size="11" letter-spacing="2.2">WHITE SPACE</text>

  <!-- Main OMORI RPG Dialogue Box -->
  {rpg_box(280, 92, 680, 188, fill=C['void'], border=C['white'], outer_w=2.8, inset=6)}

  <!-- Floating Speaker Name Tag -->
  {rpg_box(304, 62, 204, 40, fill=C['void'], border=C['white'], outer_w=2.4, inset=4)}
  <text x="406" y="87" text-anchor="middle" fill="{C['white']}" font-size="15" font-weight="700" letter-spacing="2.6">WIDYATAMAX</text>

  <!-- Dialogue Content -->
  <text x="316" y="148" fill="{C['white']}" font-size="38" font-weight="800" letter-spacing="2.2" class="sans">REZA WIDYA UTAMA</text>
  <text x="318" y="182" fill="{C['lavender']}" font-size="16" font-weight="600" letter-spacing="0.6">Offline-First Software Builder  ·  Web · Desktop · Android</text>
  <line x1="316" y1="201" x2="924" y2="201" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
  <text x="318" y="232" fill="{C['white']}" font-size="14.5" opacity="0.9">▸ Welcome to my headspace. Building calm, local-first tools</text>
  <text x="336" y="254" fill="{C['sky']}" font-size="13.5" opacity="0.92">OpenFormu (HiGHS WASM)  ·  Defisit Harian  ·  Gemini &amp; Antigravity</text>

  <!-- Blinking RPG Continue Triangle -->
  <polygon points="928,248 942,248 935,260" fill="{C['white']}" class="blink"/>"""

    return svg_wrap(1200, 340, "Reza Widya Utama — @WidyatamaX OMORI Headspace Header", defs, styles, body)


def build_header_mobile() -> str:
    defs = common_bg_defs("hdrm")
    styles = """    .sway { animation: sway 5.4s ease-in-out infinite; }
    .tw1 { animation: tw 3.2s ease-in-out infinite; }
    .tw2 { animation: tw 4.4s ease-in-out infinite 1.1s; }
    .blink { animation: blink 1.15s steps(2, start) infinite; }
    @keyframes sway { 0%, 100% { transform: rotate(-2.5deg); } 50% { transform: rotate(2.5deg); } }
    @keyframes tw { 0%, 100% { opacity: 0.95; } 50% { opacity: 0.25; } }
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0.12; } }"""

    stars = [
        (56, 62, 6.5, C["white"], "tw1"),
        (418, 76, 7.5, C["lavender"], "tw2"),
        (92, 168, 5.0, C["sky"], "tw2"),
        (392, 182, 5.5, C["rose"], "tw1"),
        (68, 514, 5.0, C["amber"], "tw1"),
        (414, 520, 6.0, C["sky"], "tw2"),
    ]
    star_svg = "\n  ".join(star4(x, y, r, col, 0.92, cls) for x, y, r, col, cls in stars)

    body = f"""  <rect width="480" height="540" rx="10" fill="url(#hdrm-bg)"/>
  <rect width="480" height="540" rx="10" fill="url(#hdrm-nebula-l)"/>
  <rect width="480" height="540" rx="10" fill="url(#hdrm-nebula-r)"/>
  <rect width="480" height="540" rx="10" fill="url(#hdrm-dots)"/>
  <rect x="8" y="8" width="464" height="524" rx="6" fill="none" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="4 6" opacity="0.65"/>

  {star_svg}
  {black_lightbulb(240, 0, 82, 1.15, "sway")}
  <ellipse cx="240" cy="186" rx="44" ry="6" fill="{C['lavender']}" opacity="0.14"/>

  <!-- Main Mobile RPG Box -->
  {rpg_box(24, 240, 432, 250, fill=C['void'], border=C['white'], outer_w=2.6, inset=5.5)}
  {rpg_box(42, 212, 194, 38, fill=C['void'], border=C['white'], outer_w=2.2, inset=4)}
  <text x="139" y="236" text-anchor="middle" fill="{C['white']}" font-size="14" font-weight="700" letter-spacing="2.2">WIDYATAMAX</text>

  <text x="48" y="294" fill="{C['white']}" font-size="30" font-weight="800" letter-spacing="1.2" class="sans">REZA WIDYA</text>
  <text x="48" y="330" fill="{C['white']}" font-size="30" font-weight="800" letter-spacing="1.2" class="sans">UTAMA</text>
  <text x="48" y="362" fill="{C['lavender']}" font-size="13.5" font-weight="600">Offline-First Software Builder</text>
  <text x="48" y="382" fill="{C['sky']}" font-size="13" font-weight="600">Web (PWA) · Desktop · Android</text>
  <line x1="48" y1="400" x2="432" y2="400" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
  <text x="48" y="428" fill="{C['white']}" font-size="13" opacity="0.92">▸ Welcome to my headspace.</text>
  <text x="64" y="450" fill="{C['muted']}" font-size="12.5">OpenFormu · Defisit Harian</text>
  <text x="64" y="470" fill="{C['muted']}" font-size="12.5">Gemini &amp; Antigravity workflow</text>

  <polygon points="424,462 438,462 431,474" fill="{C['white']}" class="blink"/>"""

    return svg_wrap(480, 540, "Reza Widya Utama — Mobile OMORI Header", defs, styles, body)


# =====================================================================
# 2. SOCIAL / ACTION BUTTONS (OMORI RPG Menu Buttons)
# =====================================================================
def build_social_btn(filename: str, width: int, label: str, accent: str, icon_svg: str) -> str:
    styles = ""
    body = f"""  {rpg_box(2, 2, width - 4, 44, fill=C['void'], border=C['white'], outer_w=2, inset=4, radius=2)}
  <rect x="7" y="39" width="{width - 14}" height="2.2" fill="{accent}" opacity="0.85"/>
  <text x="16" y="29" fill="{accent}" font-size="13" font-weight="700">▸</text>
  <g transform="translate(32, 13)">{icon_svg}</g>
  <text x="58" y="28.5" fill="{C['white']}" font-size="12.5" font-weight="700" letter-spacing="0.4">{esc(label)}</text>"""
    return svg_wrap(width, 48, label, "", styles, body)


# =====================================================================
# 3. SECTION HEADERS & DIVIDERS
# =====================================================================
def build_section_header(title: str, chapter: str, accent: str, mobile: bool = False) -> str:
    w = 480 if mobile else 1200
    h = 64 if mobile else 74
    box_w = min(295, max(180, len(title) * 14 + 72)) if mobile else max(240, len(title) * 16 + 96)
    box_y = 10 if mobile else 12
    box_h = 44 if mobile else 50
    mid_y = h / 2
    fs = 15 if mobile else 17

    styles = """    .cur { animation: cur 1.3s steps(2, start) infinite; }
    @keyframes cur { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0.25; } }"""

    line_x1 = 18 + box_w + 14
    line_x2 = w - (88 if mobile else 126)

    body = f"""  <rect width="{w}" height="{h}" fill="none"/>
  {rpg_box(16, box_y, box_w, box_h, fill=C['void'], border=C['white'], outer_w=2.2, inset=4.5)}
  <rect x="21" y="{box_y + box_h - 6.5}" width="{box_w - 10}" height="2" fill="{accent}" opacity="0.9"/>
  <text x="34" y="{mid_y + 5.5:.1f}" fill="{accent}" font-size="{fs}" font-weight="700" class="cur">▸</text>
  <text x="54" y="{mid_y + 5.5:.1f}" fill="{C['white']}" font-size="{fs}" font-weight="800" letter-spacing="2.2">{esc(title)}</text>

  <line x1="{line_x1}" y1="{mid_y:.1f}" x2="{line_x2}" y2="{mid_y:.1f}" stroke="{C['dim']}" stroke-width="1.5" stroke-dasharray="5 5"/>
  {star4(line_x1 + 10, mid_y, 5.5, accent, 0.95)}
  {star4(line_x2 - 8, mid_y, 5.0, C['white'], 0.85)}

  <text x="{w - 20}" y="{mid_y + 4.5:.1f}" text-anchor="end" fill="{C['muted']}" font-size="12" font-weight="700" letter-spacing="1.8">{esc(chapter)}</text>"""

    return svg_wrap(w, h, title, "", styles, body)


def build_divider(mobile: bool = False) -> str:
    w = 480 if mobile else 1200
    h = 28 if mobile else 34
    mid_x = w / 2
    mid_y = h / 2
    body = f"""  <line x1="28" y1="{mid_y}" x2="{mid_x - 36}" y2="{mid_y}" stroke="{C['dim']}" stroke-width="1.2" stroke-dasharray="4 6"/>
  <line x1="{mid_x + 36}" y1="{mid_y}" x2="{w - 28}" y2="{mid_y}" stroke="{C['dim']}" stroke-width="1.2" stroke-dasharray="4 6"/>
  {star4(mid_x - 20, mid_y, 4.2, C['lavender'], 0.85)}
  {star4(mid_x, mid_y, 7.2, C['white'], 0.95)}
  {star4(mid_x + 20, mid_y, 4.2, C['sky'], 0.85)}"""
    return svg_wrap(w, h, "Section Divider", "", "", body)


# =====================================================================
# 4. WHITE SPACE × HEADSPACE CODING DESK (assets/desk.svg, 420x290)
# =====================================================================
def build_desk() -> str:
    defs = common_bg_defs("desk")
    styles = """    .sway { animation: sway 5.2s ease-in-out infinite; }
    .steam1 { animation: steam 2.8s ease-in-out infinite; }
    .steam2 { animation: steam 2.8s ease-in-out infinite 1.1s; }
    .zzz1 { animation: zzz 3.2s ease-in-out infinite; }
    .zzz2 { animation: zzz 3.2s ease-in-out infinite 0.9s; }
    .zzz3 { animation: zzz 3.2s ease-in-out infinite 1.8s; }
    .cur { animation: cur 1.1s steps(2, start) infinite; }
    @keyframes sway { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }
    @keyframes steam { 0% { opacity: 0; transform: translateY(4px); } 50% { opacity: 0.7; } 100% { opacity: 0; transform: translateY(-8px); } }
    @keyframes zzz { 0% { opacity: 0; transform: translate(0px, 4px); } 45% { opacity: 0.9; } 100% { opacity: 0; transform: translate(6px, -10px); } }
    @keyframes cur { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }"""

    body = f"""  <rect width="420" height="290" rx="8" fill="url(#desk-bg)"/>
  <rect width="420" height="290" rx="8" fill="url(#desk-nebula-l)"/>
  <rect width="420" height="290" rx="8" fill="url(#desk-dots)"/>
  {rpg_box(6, 6, 408, 278, fill=C['void'], border=C['white'], outer_w=2.4, inset=5, fill_opacity=0.65)}

  <!-- Top scene bar -->
  <line x1="14" y1="36" x2="406" y2="36" stroke="{C['white']}" stroke-width="1" opacity="0.45"/>
  <text x="26" y="26" fill="{C['muted']}" font-size="10.5" letter-spacing="1.6">▸ WHITE_SPACE // DESK.SCENE</text>
  <text x="394" y="26" text-anchor="end" fill="{C['lavender']}" font-size="10.5">✦ FOCUSED</text>

  <!-- Headspace Window on Wall -->
  <rect x="268" y="54" width="110" height="82" rx="2" fill="#0d0a1a" stroke="{C['white']}" stroke-width="1.6"/>
  <line x1="323" y1="54" x2="323" y2="136" stroke="{C['white']}" stroke-width="1" opacity="0.5"/>
  <line x1="268" y1="95" x2="378" y2="95" stroke="{C['white']}" stroke-width="1" opacity="0.5"/>
  {star4(290, 74, 4.2, C['white'], 0.9)}
  {star4(352, 72, 3.5, C['lavender'], 0.85)}
  {star4(300, 118, 3.0, C['sky'], 0.8)}
  <path d="M 350 105 A 11 11 0 1 0 358 122 A 8.5 8.5 0 1 1 350 105 Z" fill="{C['amber']}" opacity="0.85"/>

  <!-- Mini Hanging Black Lightbulb -->
  {black_lightbulb(206, 36, 34, 0.56, "sway")}

  <!-- Desk Surface -->
  <rect x="24" y="206" width="372" height="14" rx="2" fill="{C['card']}" stroke="{C['white']}" stroke-width="1.8"/>
  <rect x="38" y="220" width="12" height="50" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.4"/>
  <rect x="370" y="220" width="12" height="50" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.4"/>

  <!-- Open Laptop -->
  <g transform="translate(46, 120)">
    <!-- Screen glow -->
    <rect x="2" y="2" width="114" height="74" rx="4" fill="{C['lavender']}" opacity="0.14"/>
    <rect x="6" y="6" width="106" height="68" rx="3" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.8"/>
    <rect x="12" y="12" width="94" height="56" rx="1" fill="#090714" stroke="{C['dim']}" stroke-width="1"/>
    <!-- Code lines -->
    <rect x="18" y="19" width="32" height="3.5" rx="1" fill="{C['lavender']}"/>
    <rect x="54" y="19" width="22" height="3.5" rx="1" fill="{C['sky']}"/>
    <rect x="24" y="28" width="46" height="3.5" rx="1" fill="{C['white']}" opacity="0.8"/>
    <rect x="24" y="37" width="28" height="3.5" rx="1" fill="{C['mint']}"/>
    <rect x="56" y="37" width="34" height="3.5" rx="1" fill="{C['rose']}"/>
    <rect x="18" y="46" width="40" height="3.5" rx="1" fill="{C['sky']}"/>
    <rect x="18" y="55" width="18" height="3.5" rx="1" fill="{C['lavender']}"/>
    <rect x="40" y="54" width="6" height="6" fill="{C['white']}" class="cur"/>
    <!-- Keyboard base -->
    <path d="M 0 74 L 118 74 L 128 86 L -10 86 Z" fill="{C['card']}" stroke="{C['white']}" stroke-width="1.8" stroke-linejoin="round"/>
  </g>

  <!-- Red Sketchbook (OMORI nod) -->
  <g transform="translate(184, 188)">
    <rect x="0" y="5" width="48" height="13" rx="1.5" fill="{C['crimson']}" stroke="{C['white']}" stroke-width="1.5"/>
    <line x1="6" y1="5" x2="6" y2="18" stroke="{C['white']}" stroke-width="1.2"/>
    <line x1="12" y1="11" x2="38" y2="11" stroke="{C['white']}" stroke-width="1" opacity="0.7"/>
  </g>

  <!-- Coffee Mug + Steam -->
  <g transform="translate(246, 174)">
    <path d="M 7 -4 C 4 -10 10 -14 7 -20" fill="none" stroke="{C['white']}" stroke-width="1.3" stroke-linecap="round" class="steam1"/>
    <path d="M 15 -2 C 12 -9 18 -13 15 -19" fill="none" stroke="{C['sky']}" stroke-width="1.3" stroke-linecap="round" class="steam2"/>
    <rect x="0" y="4" width="22" height="28" rx="3" fill="{C['void']}" stroke="{C['white']}" stroke-width="1.8"/>
    <path d="M 22 10 C 30 10 30 24 22 24" fill="none" stroke="{C['white']}" stroke-width="1.8"/>
    <rect x="4" y="13" width="14" height="5" fill="{C['lavender']}" opacity="0.7"/>
  </g>

  <!-- Sleeping Black Cat (Mewo-inspired original vector) -->
  <g transform="translate(292, 166)">
    <!-- Soft cushion -->
    <ellipse cx="42" cy="38" rx="42" ry="6" fill="{C['lavender']}" opacity="0.22"/>
    <!-- Curled body -->
    <path d="M 12 38 C 8 22 22 12 42 12 C 62 12 74 22 72 38 Z" fill="#06050a" stroke="{C['white']}" stroke-width="1.9" stroke-linejoin="round"/>
    <!-- Cat head -->
    <circle cx="24" cy="24" r="13" fill="#06050a" stroke="{C['white']}" stroke-width="1.9"/>
    <!-- Ears -->
    <polygon points="14,15 16,5 22,12" fill="#06050a" stroke="{C['white']}" stroke-width="1.7" stroke-linejoin="round"/>
    <polygon points="26,12 32,5 34,15" fill="#06050a" stroke="{C['white']}" stroke-width="1.7" stroke-linejoin="round"/>
    <!-- Sleeping happy eyes -->
    <path d="M 17 24 Q 20 21 22 24" fill="none" stroke="{C['white']}" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 26 24 Q 29 21 31 24" fill="none" stroke="{C['white']}" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Tiny mouth -->
    <circle cx="24" cy="28" r="1.2" fill="{C['rose']}"/>
    <!-- Curled tail -->
    <path d="M 70 34 C 84 32 86 20 76 18" fill="none" stroke="{C['white']}" stroke-width="2" stroke-linecap="round"/>
    <!-- Floating Zzz -->
    <text x="38" y="4" fill="{C['white']}" font-size="10" font-weight="700" class="zzz1">z</text>
    <text x="48" y="-5" fill="{C['lavender']}" font-size="11.5" font-weight="700" class="zzz2">z</text>
    <text x="58" y="-14" fill="{C['sky']}" font-size="13" font-weight="700" class="zzz3">Z</text>
  </g>

  <!-- Subtle floor caption -->
  <text x="210" y="254" text-anchor="middle" fill="{C['muted']}" font-size="11">waiting for something to ship...</text>"""

    return svg_wrap(420, 290, "White Space coding desk with sleeping black cat, laptop, sketchbook and coffee", defs, styles, body)


# =====================================================================
# 5. OMORI STATUS WINDOW / NEOFETCH (Desktop 1200x430 & Mobile 480x850)
# =====================================================================
NEO_ROWS = [
    ("NAME", "Reza Widya Utama", C["white"]),
    ("HANDLE", "@WidyatamaX", C["lavender"]),
    ("FOCUS", "Offline-First & Cross-Platform Software", C["sky"]),
    ("PLATFORMS", "Web (PWA) · Windows (Tauri v2) · Android (Capacitor)", C["white"]),
    ("SHIPPING", "OpenFormu (LP Engine) · Defisit Harian (Finance)", C["mint"]),
    ("LANGUAGES", "TypeScript · JavaScript · Python · Rust · Java", C["white"]),
    ("CORE STACK", "React · Vite · Tailwind · HiGHS WASM · Dexie", C["lavender"]),
    ("AI COPILOT", "Google Gemini · Antigravity", C["rose"]),
    ("LOCATION", "Indonesia", C["amber"]),
    ("STATUS", "Building & Open to Collab ✦", C["mint"]),
]

NEO_ROWS_MOBILE = [
    ("NAME", "Reza Widya Utama", C["white"]),
    ("HANDLE", "@WidyatamaX", C["lavender"]),
    ("FOCUS", "Offline-First & Cross-Platform", C["sky"]),
    ("PLATFORMS", "PWA · Tauri v2 · Capacitor", C["white"]),
    ("SHIPPING", "OpenFormu · Defisit Harian", C["mint"]),
    ("LANGUAGES", "TS · JS · Python · Rust · Java", C["white"]),
    ("STACK", "React · Vite · Tailwind · WASM", C["lavender"]),
    ("AI", "Google Gemini · Antigravity", C["rose"]),
    ("LOCATION", "Indonesia", C["amber"]),
    ("STATUS", "Open to Collab ✦", C["mint"]),
]


def status_card_svg(x: float, y: float, w: float, h: float) -> str:
    """OMORI Battle-Style Character Card."""
    cx = x + w / 2
    bar_w = w - 68
    return f"""  <g>
    {rpg_box(x, y, w, h, fill=C['void'], border=C['white'], outer_w=2.4, inset=5)}
    <!-- Emotion header bar -->
    <rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="32" rx="1" fill="#1e2246" stroke="{C['sky']}" stroke-width="1.3"/>
    <text x="{cx}" y="{y + 33}" text-anchor="middle" fill="{C['sky']}" font-size="13.5" font-weight="800" letter-spacing="2.4">FOCUSED</text>

    <!-- Portrait frame -->
    <rect x="{x + 18}" y="{y + 54}" width="{w - 36}" height="178" rx="2" fill="#0d0b1a" stroke="{C['white']}" stroke-width="1.8"/>
    <rect x="{x + 23}" y="{y + 59}" width="{w - 46}" height="168" fill="none" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
    {star4(x + 48, y + 86, 5.0, C['white'], 0.9, 'tw1')}
    {star4(x + w - 48, y + 92, 6.0, C['lavender'], 0.9, 'tw2')}
    {star4(x + 62, y + 188, 4.0, C['sky'], 0.85, 'tw2')}
    {star4(x + w - 58, y + 182, 4.5, C['rose'], 0.85, 'tw1')}

    <!-- Lightbulb + Horizon emblem inside portrait -->
    {black_lightbulb(cx, y + 59, 34, 0.86, "sway")}
    <!-- Floating pixel island + tiny cat silhouette -->
    <path d="M {cx - 64} {y + 194} Q {cx} {y + 182} {cx + 64} {y + 194} L {cx + 46} {y + 210} L {cx - 46} {y + 210} Z"
          fill="{C['card']}" stroke="{C['white']}" stroke-width="1.4"/>
    <circle cx="{cx + 22}" cy="{y + 181}" r="6.5" fill="#06050a" stroke="{C['white']}" stroke-width="1.3"/>
    <polygon points="{cx + 16},{y + 177} {cx + 18},{y + 170} {cx + 21},{y + 175}" fill="#06050a" stroke="{C['white']}" stroke-width="1.1"/>
    <polygon points="{cx + 23},{y + 175} {cx + 26},{y + 170} {cx + 28},{y + 177}" fill="#06050a" stroke="{C['white']}" stroke-width="1.1"/>
    <text x="{cx - 24}" y="{y + 186}" fill="{C['lavender']}" font-size="10.5" font-weight="700">&lt;/&gt;</text>

    <!-- HEART bar -->
    <path d="M {x + 26} {y + 258} C {x + 26} {y + 253} {x + 33} {y + 253} {x + 33} {y + 258} C {x + 33} {y + 253} {x + 40} {y + 253} {x + 40} {y + 258} C {x + 40} {y + 264} {x + 33} {y + 268} {x + 33} {y + 268} C {x + 33} {y + 268} {x + 26} {y + 264} {x + 26} {y + 258} Z" fill="{C['crimson']}"/>
    <rect x="{x + 48}" y="{y + 250}" width="{bar_w}" height="18" rx="1" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.5"/>
    <rect x="{x + 50}" y="{y + 252}" width="{bar_w - 4}" height="14" fill="{C['crimson']}" opacity="0.88"/>
    <text x="{x + 56}" y="{y + 263}" fill="{C['void']}" font-size="10.5" font-weight="800">HEART</text>
    <text x="{x + 44 + bar_w}" y="{y + 263}" text-anchor="end" fill="{C['void']}" font-size="10.5" font-weight="800">100/100</text>

    <!-- JUICE bar -->
    <path d="M {x + 33} {y + 280} C {x + 33} {y + 280} {x + 40} {y + 289} {x + 40} {y + 293} A 7 7 0 0 1 {x + 26} {y + 293} C {x + 26} {y + 289} {x + 33} {y + 280} {x + 33} {y + 280} Z" fill="{C['sky']}"/>
    <rect x="{x + 48}" y="{y + 280}" width="{bar_w}" height="18" rx="1" fill="{C['deep']}" stroke="{C['white']}" stroke-width="1.5"/>
    <rect x="{x + 50}" y="{y + 282}" width="{bar_w - 4}" height="14" fill="{C['sky']}" opacity="0.88"/>
    <text x="{x + 56}" y="{y + 293}" fill="{C['void']}" font-size="10.5" font-weight="800">JUICE</text>
    <text x="{x + 44 + bar_w}" y="{y + 293}" text-anchor="end" fill="{C['void']}" font-size="10.5" font-weight="800">99/99</text>

    <!-- Footer tag -->
    <line x1="{x + 18}" y1="{y + 314}" x2="{x + w - 18}" y2="{y + 314}" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
    <text x="{x + 22}" y="{y + 338}" fill="{C['muted']}" font-size="11.5" font-weight="700">LVL. 2026</text>
    <text x="{x + w - 22}" y="{y + 338}" text-anchor="end" fill="{C['lavender']}" font-size="11.5" font-weight="700">BUILDER</text>
  </g>"""


def build_neofetch_desktop() -> str:
    defs = common_bg_defs("neo")
    styles = """    .sway { animation: sway 5.4s ease-in-out infinite; }
    .tw1 { animation: tw 3.1s ease-in-out infinite; }
    .tw2 { animation: tw 4.2s ease-in-out infinite 1s; }
    @keyframes sway { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }
    @keyframes tw { 0%, 100% { opacity: 0.95; } 50% { opacity: 0.25; } }"""

    rows_svg = []
    for i, (k, v, col) in enumerate(NEO_ROWS):
        ry = 110 + i * 26.5
        rows_svg.append(
            f'  <text x="412" y="{ry:.1f}" fill="{C["lavender"]}" font-size="13.5" font-weight="700">{esc(k)}</text>\n'
            f'  <text x="536" y="{ry:.1f}" fill="{C["dim"]}" font-size="13.5">:</text>\n'
            f'  <text x="556" y="{ry:.1f}" fill="{col}" font-size="13.5" font-weight="600">{esc(v)}</text>'
        )

    swatches = [C["white"], C["lavender"], C["periwinkle"], C["sky"], C["mint"], C["amber"], C["rose"], C["crimson"]]
    swatch_svg = "\n  ".join(
        f'<rect x="{412 + idx * 34}" y="382" width="26" height="12" rx="1.5" fill="{col}"/>'
        for idx, col in enumerate(swatches)
    )

    body = f"""  <rect width="1200" height="430" rx="10" fill="url(#neo-bg)"/>
  <rect width="1200" height="430" rx="10" fill="url(#neo-nebula-l)"/>
  <rect width="1200" height="430" rx="10" fill="url(#neo-nebula-r)"/>
  <rect width="1200" height="430" rx="10" fill="url(#neo-dots)"/>

  {status_card_svg(26, 26, 332, 378)}

  <!-- Right Terminal Status Panel -->
  {rpg_box(380, 26, 794, 378, fill=C['void'], border=C['white'], outer_w=2.4, inset=5)}
  <text x="412" y="62" fill="{C['sky']}" font-size="14" font-weight="700">▸ reza@widyatamax</text>
  <text x="582" y="62" fill="{C['muted']}" font-size="13.5">~  status --all</text>
  <text x="1146" y="62" text-anchor="end" fill="{C['muted']}" font-size="11.5" letter-spacing="1.5">[HEADSPACE OS]</text>
  <line x1="406" y1="78" x2="1148" y2="78" stroke="{C['dim']}" stroke-width="1.2" stroke-dasharray="4 4"/>

  {"".join(rows_svg)}

  <!-- Headspace color swatch strip -->
  {swatch_svg}
  <text x="1146" y="392" text-anchor="end" fill="{C['muted']}" font-size="11">OMORI // HEADSPACE THEME</text>"""

    return svg_wrap(1200, 430, "OMORI Status Window and Neofetch for Reza Widya Utama", defs, styles, body)


def build_neofetch_mobile() -> str:
    defs = common_bg_defs("neom")
    styles = """    .sway { animation: sway 5.4s ease-in-out infinite; }
    .tw1 { animation: tw 3.1s ease-in-out infinite; }
    .tw2 { animation: tw 4.2s ease-in-out infinite 1s; }
    @keyframes sway { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }
    @keyframes tw { 0%, 100% { opacity: 0.95; } 50% { opacity: 0.25; } }"""

    rows_svg = []
    for i, (k, v, col) in enumerate(NEO_ROWS_MOBILE):
        ry = 486 + i * 28.5
        rows_svg.append(
            f'  <text x="42" y="{ry:.1f}" fill="{C["lavender"]}" font-size="12.5" font-weight="700">{esc(k)}</text>\n'
            f'  <text x="138" y="{ry:.1f}" fill="{C["dim"]}" font-size="12.5">:</text>\n'
            f'  <text x="152" y="{ry:.1f}" fill="{col}" font-size="12.5" font-weight="600">{esc(v)}</text>'
        )

    swatches = [C["white"], C["lavender"], C["periwinkle"], C["sky"], C["mint"], C["amber"], C["rose"], C["crimson"]]
    swatch_svg = "\n  ".join(
        f'<rect x="{42 + idx * 32}" y="776" width="24" height="11" rx="1.5" fill="{col}"/>'
        for idx, col in enumerate(swatches)
    )

    body = f"""  <rect width="480" height="820" rx="10" fill="url(#neom-bg)"/>
  <rect width="480" height="820" rx="10" fill="url(#neom-nebula-l)"/>
  <rect width="480" height="820" rx="10" fill="url(#neom-dots)"/>

  {status_card_svg(24, 22, 432, 368)}

  {rpg_box(24, 410, 432, 390, fill=C['void'], border=C['white'], outer_w=2.4, inset=5)}
  <text x="42" y="444" fill="{C['sky']}" font-size="13" font-weight="700">▸ reza@widyatamax ~ status</text>
  <line x1="40" y1="458" x2="440" y2="458" stroke="{C['dim']}" stroke-width="1.1" stroke-dasharray="4 4"/>
  {"".join(rows_svg)}
  {swatch_svg}"""

    return svg_wrap(480, 820, "Mobile OMORI Status Window for Reza Widya Utama", defs, styles, body)


# =====================================================================
# 6. JOURNEY TIMELINE (Desktop 1200x300 & Mobile 480x610)
# =====================================================================
JOURNEY = [
    ("2026 · Q2", "Entered GitHub", "Started @WidyatamaX & explored", "offline-first web engineering.", C["sky"]),
    ("2026 · NOV", "Shipped OpenFormu", "LP feed formulation engine with", "HiGHS WASM, Tauri v2 & Capacitor.", C["mint"]),
    ("2026 · NOV", "Built Defisit Harian", "Zero-cloud Android finance app", "using React, Dexie & OHLC charts.", C["lavender"]),
    ("NEXT", "Keep Building", "Scaling cross-platform tools &", "Gemini / Antigravity workflows.", C["rose"]),
]


def build_timeline_desktop() -> str:
    defs = common_bg_defs("tl")
    cards = []
    xs = [36, 326, 616, 906]
    cw = 258
    line_y = 66

    for idx, (date, title, l1, l2, col) in enumerate(JOURNEY):
        x = xs[idx]
        cx = x + cw / 2
        cards.append(f"""  <g>
    <circle cx="{cx:.1f}" cy="{line_y}" r="12" fill="{C['void']}" stroke="{col}" stroke-width="2.2"/>
    {star4(cx, line_y, 5.5, col, 1.0)}
    <line x1="{cx:.1f}" y1="{line_y + 12}" x2="{cx:.1f}" y2="108" stroke="{col}" stroke-width="1.5" stroke-dasharray="3 3"/>
    {rpg_box(x, 108, cw, 160, fill=C['void'], border=C['white'], outer_w=2.1, inset=4.5)}
    <rect x="{x + 14}" y="122" width="106" height="22" rx="2" fill="{C['card']}" stroke="{col}" stroke-width="1.2"/>
    <text x="{x + 67}" y="137" text-anchor="middle" fill="{col}" font-size="11" font-weight="700">{esc(date)}</text>
    <text x="{x + 16}" y="174" fill="{C['white']}" font-size="16" font-weight="800" class="sans">{esc(title)}</text>
    <text x="{x + 16}" y="204" fill="{C['muted']}" font-size="12">{esc(l1)}</text>
    <text x="{x + 16}" y="224" fill="{C['muted']}" font-size="12">{esc(l2)}</text>
    <rect x="{x + 14}" y="251" width="{cw - 28}" height="2.4" fill="{col}" opacity="0.8"/>
  </g>""")

    body = f"""  <rect width="1200" height="296" rx="10" fill="url(#tl-bg)"/>
  <rect width="1200" height="296" rx="10" fill="url(#tl-nebula-l)"/>
  <rect width="1200" height="296" rx="10" fill="url(#tl-dots)"/>
  <line x1="165" y1="{line_y}" x2="1035" y2="{line_y}" stroke="{C['lavender']}" stroke-width="2.2" stroke-dasharray="6 5" opacity="0.72"/>
  <text x="36" y="34" fill="{C['muted']}" font-size="11.5" letter-spacing="1.8">▸ MEMORY LOG // CHAPTER CHECKPOINTS</text>
  {"".join(cards)}"""

    return svg_wrap(1200, 296, "Journey timeline for Reza Widya Utama", defs, "", body)


def build_timeline_mobile() -> str:
    defs = common_bg_defs("tlm")
    cards = []
    lx = 46
    for idx, (date, title, l1, l2, col) in enumerate(JOURNEY):
        y = 58 + idx * 134
        cy = y + 56
        cards.append(f"""  <g>
    <circle cx="{lx}" cy="{cy}" r="11" fill="{C['void']}" stroke="{col}" stroke-width="2"/>
    {star4(lx, cy, 4.8, col, 1.0)}
    <line x1="{lx + 11}" y1="{cy}" x2="78" y2="{cy}" stroke="{col}" stroke-width="1.4" stroke-dasharray="3 3"/>
    {rpg_box(78, y, 378, 114, fill=C['void'], border=C['white'], outer_w=2.0, inset=4)}
    <text x="96" y="{y + 28}" fill="{col}" font-size="11.5" font-weight="700">[{esc(date)}]</text>
    <text x="96" y="{y + 52}" fill="{C['white']}" font-size="15.5" font-weight="800" class="sans">{esc(title)}</text>
    <text x="96" y="{y + 76}" fill="{C['muted']}" font-size="12">{esc(l1)}</text>
    <text x="96" y="{y + 95}" fill="{C['muted']}" font-size="12">{esc(l2)}</text>
  </g>""")

    body = f"""  <rect width="480" height="608" rx="10" fill="url(#tlm-bg)"/>
  <rect width="480" height="608" rx="10" fill="url(#tlm-dots)"/>
  <text x="26" y="34" fill="{C['muted']}" font-size="11" letter-spacing="1.6">▸ MEMORY LOG // CHECKPOINTS</text>
  <line x1="{lx}" y1="114" x2="{lx}" y2="516" stroke="{C['lavender']}" stroke-width="2" stroke-dasharray="5 5" opacity="0.7"/>
  {"".join(cards)}"""

    return svg_wrap(480, 608, "Mobile Journey timeline for Reza Widya Utama", defs, "", body)


# =====================================================================
# 7. TECH STACK MARQUEE (Desktop 1200x76 & Mobile 480x68)
# =====================================================================
MARQUEE_ITEMS = [
    ("TypeScript", C["sky"]),
    ("React 19", C["sky"]),
    ("Vite", C["lavender"]),
    ("Tailwind CSS", C["sky"]),
    ("Tauri v2", C["amber"]),
    ("Capacitor", C["mint"]),
    ("Offline-First PWA", C["mint"]),
    ("HiGHS WASM", C["rose"]),
    ("IndexedDB / Dexie", C["lavender"]),
    ("Rust", C["crimson"]),
    ("Python", C["amber"]),
    ("Vitest", C["mint"]),
    ("GitHub Actions", C["lavender"]),
    ("Google Gemini", C["sky"]),
    ("Antigravity", C["rose"]),
]


def build_marquee(mobile: bool = False) -> str:
    w = 480 if mobile else 1200
    h = 68 if mobile else 76
    ph = 30 if mobile else 32
    py = (h - ph) / 2
    gap = 12.0

    # Measure one complete track
    cursor = 0.0
    one_track = []
    for label, col in MARQUEE_ITEMS:
        p_svg, pw = pill(cursor, py, label, col, height=ph, font_size=12.5)
        one_track.append(p_svg)
        cursor += pw + gap
    track_w = cursor

    # Duplicate track for seamless wrap
    track_html = "\n".join(one_track)
    dur = 28 if not mobile else 24

    defs = f"""    <linearGradient id="mq-fade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="black"/>
      <stop offset="8%" stop-color="white"/>
      <stop offset="92%" stop-color="white"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
    <mask id="mq-mask">
      <rect width="{w}" height="{h}" fill="url(#mq-fade)"/>
    </mask>"""

    styles = f"""    .track {{ animation: scroll {dur}s linear infinite; }}
    @keyframes scroll {{
      0% {{ transform: translateX(0px); }}
      100% {{ transform: translateX(-{track_w:.1f}px); }}
    }}"""

    body = f"""  {rpg_box(2, 2, w - 4, h - 4, fill=C['void'], border=C['white'], outer_w=2.0, inset=4, radius=4)}
  <g mask="url(#mq-mask)">
    <g class="track">
      <g>{track_html}</g>
      <g transform="translate({track_w:.1f}, 0)">{track_html}</g>
    </g>
  </g>"""

    return svg_wrap(w, h, "Tech stack and AI marquee", defs, styles, body)


# =====================================================================
# 8. TECH STACK INVENTORY GRID (Desktop 1200x380 & Mobile 480x760)
# =====================================================================
STACK_CATEGORIES = [
    ("LANGUAGES", C["lavender"], ["TypeScript", "JavaScript", "Python", "Rust", "Java", "HTML5", "CSS3"]),
    ("FRONTEND & UI", C["sky"], ["React 18 / 19", "Vite", "Tailwind CSS", "Motion", "Lucide", "Lightweight Charts"]),
    ("CROSS-PLATFORM & OFFLINE", C["mint"], ["Tauri v2", "Capacitor", "PWA", "IndexedDB", "Dexie", "HiGHS WASM"]),
    ("TOOLING & QA", C["rose"], ["Vitest", "Testing Library", "ESLint", "Prettier", "GitHub Actions", "Git"]),
]


def render_pill_flow(x0: float, y0: float, max_w: float, items: list[str], accent: str) -> str:
    out = []
    cx = x0
    cy = y0
    for item in items:
        est_w = max(68.0, len(item) * (12.5 * 0.63) + 34.0)
        if cx > x0 and (cx - x0 + est_w) > max_w:
            cx = x0
            cy += 38.0
        p_svg, pw = pill(cx, cy, item, accent, height=28, font_size=12.5)
        out.append(p_svg)
        cx += pw + 10.0
    return "\n".join(out)


def build_stack_desktop() -> str:
    defs = common_bg_defs("stk")
    positions = [(26, 24), (612, 24), (26, 204), (612, 204)]
    cw, ch = 562, 162

    cards = []
    for (title, col, items), (x, y) in zip(STACK_CATEGORIES, positions):
        pills_svg = render_pill_flow(x + 22, y + 66, cw - 44, items, col)
        cards.append(f"""  <g>
    {rpg_box(x, y, cw, ch, fill=C['void'], border=C['white'], outer_w=2.2, inset=4.5)}
    <text x="{x + 22}" y="{y + 38}" fill="{col}" font-size="14" font-weight="800" letter-spacing="1.6">▸ {esc(title)}</text>
    <text x="{x + cw - 22}" y="{y + 38}" text-anchor="end" fill="{C['muted']}" font-size="11">{len(items)} ITEMS</text>
    <line x1="{x + 20}" y1="{y + 50}" x2="{x + cw - 20}" y2="{y + 50}" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
    {pills_svg}
  </g>""")

    body = f"""  <rect width="1200" height="390" rx="10" fill="url(#stk-bg)"/>
  <rect width="1200" height="390" rx="10" fill="url(#stk-nebula-l)"/>
  <rect width="1200" height="390" rx="10" fill="url(#stk-nebula-r)"/>
  <rect width="1200" height="390" rx="10" fill="url(#stk-dots)"/>
  {"".join(cards)}"""

    return svg_wrap(1200, 390, "Tech stack inventory: Languages, Frontend, Cross-Platform, Tooling", defs, "", body)


def build_stack_mobile() -> str:
    defs = common_bg_defs("stkm")
    cw = 432
    cards = []
    cy = 20
    for title, col, items in STACK_CATEGORIES:
        # Estimate row count for dynamic card height
        rx, rows = 0.0, 1
        for it in items:
            ew = max(68.0, len(it) * (12.5 * 0.63) + 34.0)
            if rx > 0 and rx + ew > cw - 40:
                rx = 0.0
                rows += 1
            rx += ew + 10.0
        ch = 74 + rows * 38
        pills_svg = render_pill_flow(44, cy + 62, cw - 40, items, col)
        cards.append(f"""  <g>
    {rpg_box(24, cy, cw, ch, fill=C['void'], border=C['white'], outer_w=2.1, inset=4.5)}
    <text x="44" y="{cy + 35}" fill="{col}" font-size="13.5" font-weight="800" letter-spacing="1.4">▸ {esc(title)}</text>
    <line x1="42" y1="{cy + 47}" x2="{24 + cw - 18}" y2="{cy + 47}" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="3 4"/>
    {pills_svg}
  </g>""")
        cy += ch + 16

    total_h = cy + 6
    body = f"""  <rect width="480" height="{total_h}" rx="10" fill="url(#stkm-bg)"/>
  <rect width="480" height="{total_h}" rx="10" fill="url(#stkm-dots)"/>
  {"".join(cards)}"""

    return svg_wrap(480, total_h, "Mobile tech stack inventory", defs, "", body)


# =====================================================================
# 9. AI TOOLBOX ORBIT (Desktop 1200x360 & Mobile 480x620)
# =====================================================================
def orbit_emblem_svg(cx: float, cy: float) -> str:
    nodes = [
        (0, -112, "Architecture", C["sky"]),
        (134, -8, "Agentic Code", C["lavender"]),
        (0, 112, "Testing & QA", C["mint"]),
        (-134, -8, "Automation", C["rose"]),
    ]
    node_svgs = []
    for dx, dy, lbl, col in nodes:
        nx, ny = cx + dx, cy + dy
        bw = len(lbl) * 7.8 + 26
        node_svgs.append(
            f'  <g>\n'
            f'    <line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{col}" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>\n'
            f'    <rect x="{nx - bw/2:.1f}" y="{ny - 15:.1f}" width="{bw:.1f}" height="30" rx="2" fill="{C["void"]}" stroke="{C["white"]}" stroke-width="1.4"/>\n'
            f'    <circle cx="{nx - bw/2 + 10:.1f}" cy="{ny:.1f}" r="3.2" fill="{col}"/>\n'
            f'    <text x="{nx + 5:.1f}" y="{ny + 4:.1f}" text-anchor="middle" fill="{C["white"]}" font-size="11.5" font-weight="700">{esc(lbl)}</text>\n'
            f"  </g>"
        )

    return f"""  <g>
    <!-- Soft dream glow -->
    <circle cx="{cx}" cy="{cy}" r="118" fill="{C['lavender']}" opacity="0.08"/>
    <!-- Rotating dashed orbit rings -->
    <g class="spin-slow" style="transform-origin: {cx}px {cy}px;">
      <circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="{C['lavender']}" stroke-width="1.3" stroke-dasharray="6 7" opacity="0.65"/>
      <circle cx="{cx + 112}" cy="{cy}" r="3.5" fill="{C['sky']}"/>
      <circle cx="{cx - 112}" cy="{cy}" r="3.5" fill="{C['rose']}"/>
    </g>
    <g class="spin-rev" style="transform-origin: {cx}px {cy}px;">
      <circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{C['sky']}" stroke-width="1.2" stroke-dasharray="4 6" opacity="0.6"/>
      {star4(cx, cy - 74, 5.5, C['amber'], 0.9)}
    </g>

    <!-- Core Star Emblem -->
    <circle cx="{cx}" cy="{cy}" r="48" fill="{C['void']}" stroke="{C['white']}" stroke-width="2.2"/>
    <circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="{C['lavender']}" stroke-width="1" opacity="0.7"/>
    {star4(cx, cy - 12, 13, C['sky'], 0.95, 'pulse')}
    <text x="{cx}" y="{cy + 14}" text-anchor="middle" fill="{C['white']}" font-size="11.5" font-weight="800" letter-spacing="1.2">GEMINI</text>
    <text x="{cx}" y="{cy + 28}" text-anchor="middle" fill="{C['lavender']}" font-size="9.5" font-weight="700">ANTIGRAVITY</text>

    {"".join(node_svgs)}
  </g>"""


def build_ai_desktop() -> str:
    defs = common_bg_defs("ai")
    styles = """    .spin-slow { animation: spin 36s linear infinite; }
    .spin-rev { animation: spinr 24s linear infinite; }
    .pulse { animation: pulse 3s ease-in-out infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes spinr { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.55; } }"""

    skills = [
        ("✦ Google Gemini", "Deep reasoning, system design & multimodal problem solving", C["sky"]),
        ("✦ Antigravity", "Agentic coding, multi-file refactors & automated verification", C["lavender"]),
        ("▸ Core Loop", "Spec-first planning → strict TypeScript → Vitest verification", C["mint"]),
        ("▸ Principle", "AI accelerates shipping; offline-first craft owns reliability", C["rose"]),
    ]
    rows = []
    for i, (t, desc, col) in enumerate(skills):
        ry = 114 + i * 64
        rows.append(
            f'  <rect x="596" y="{ry - 20}" width="552" height="52" rx="2" fill="{C["deep"]}" stroke="{C["dim"]}" stroke-width="1.2"/>\n'
            f'  <rect x="596" y="{ry - 20}" width="4" height="52" fill="{col}"/>\n'
            f'  <text x="614" y="{ry}" fill="{col}" font-size="14" font-weight="800">{esc(t)}</text>\n'
            f'  <text x="614" y="{ry + 21}" fill="{C["muted"]}" font-size="12.5">{esc(desc)}</text>'
        )

    body = f"""  <rect width="1200" height="366" rx="10" fill="url(#ai-bg)"/>
  <rect width="1200" height="366" rx="10" fill="url(#ai-nebula-l)"/>
  <rect width="1200" height="366" rx="10" fill="url(#ai-nebula-r)"/>
  <rect width="1200" height="366" rx="10" fill="url(#ai-dots)"/>

  {rpg_box(26, 24, 518, 318, fill=C['void'], border=C['white'], outer_w=2.2, inset=5)}
  {orbit_emblem_svg(285, 183)}

  {rpg_box(568, 24, 606, 318, fill=C['void'], border=C['white'], outer_w=2.2, inset=5)}
  <text x="596" y="60" fill="{C['white']}" font-size="15" font-weight="800" letter-spacing="2">▸ EQUIPPED AI SKILLS</text>
  <text x="1146" y="60" text-anchor="end" fill="{C['lavender']}" font-size="11.5">ACTIVE LOADOUT</text>
  <line x1="596" y1="74" x2="1148" y2="74" stroke="{C['dim']}" stroke-width="1.1" stroke-dasharray="4 4"/>
  {"".join(rows)}"""

    return svg_wrap(1200, 366, "AI Toolbox featuring Google Gemini and Antigravity", defs, styles, body)


def build_ai_mobile() -> str:
    defs = common_bg_defs("aim")
    styles = """    .spin-slow { animation: spin 36s linear infinite; }
    .spin-rev { animation: spinr 24s linear infinite; }
    .pulse { animation: pulse 3s ease-in-out infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes spinr { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.55; } }"""

    skills = [
        ("✦ Google Gemini", "Reasoning, design & multimodal workflows", C["sky"]),
        ("✦ Antigravity", "Agentic coding & automated verification", C["lavender"]),
        ("▸ Core Loop", "Spec-first → strict TS → Vitest checks", C["mint"]),
        ("▸ Principle", "AI speeds shipping; local-first owns reliability", C["rose"]),
    ]
    rows = []
    for i, (t, desc, col) in enumerate(skills):
        ry = 416 + i * 62
        rows.append(
            f'  <rect x="44" y="{ry - 18}" width="392" height="50" rx="2" fill="{C["deep"]}" stroke="{C["dim"]}" stroke-width="1.1"/>\n'
            f'  <rect x="44" y="{ry - 18}" width="4" height="50" fill="{col}"/>\n'
            f'  <text x="60" y="{ry}" fill="{col}" font-size="13.5" font-weight="800">{esc(t)}</text>\n'
            f'  <text x="60" y="{ry + 20}" fill="{C["muted"]}" font-size="11.5">{esc(desc)}</text>'
        )

    body = f"""  <rect width="480" height="678" rx="10" fill="url(#aim-bg)"/>
  <rect width="480" height="678" rx="10" fill="url(#aim-dots)"/>

  {rpg_box(24, 22, 432, 300, fill=C['void'], border=C['white'], outer_w=2.2, inset=4.5)}
  {orbit_emblem_svg(240, 172)}

  {rpg_box(24, 340, 432, 316, fill=C['void'], border=C['white'], outer_w=2.2, inset=4.5)}
  <text x="44" y="372" fill="{C['white']}" font-size="14" font-weight="800" letter-spacing="1.6">▸ EQUIPPED AI SKILLS</text>
  <line x1="44" y1="384" x2="436" y2="384" stroke="{C['dim']}" stroke-width="1" stroke-dasharray="4 4"/>
  {"".join(rows)}"""

    return svg_wrap(480, 678, "Mobile AI Toolbox featuring Google Gemini and Antigravity", defs, styles, body)


# =====================================================================
# 10. FOOTER (Desktop 1200x176 & Mobile 480x220)
# =====================================================================
def build_footer(mobile: bool = False) -> str:
    w = 480 if mobile else 1200
    h = 216 if mobile else 176
    uid = "ftm" if mobile else "ft"
    defs = common_bg_defs(uid)
    styles = """    .blink { animation: blink 1.15s steps(2, start) infinite; }
    .tw1 { animation: tw 3.4s ease-in-out infinite; }
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0.12; } }
    @keyframes tw { 0%, 100% { opacity: 0.95; } 50% { opacity: 0.25; } }"""

    if not mobile:
        body = f"""  <rect width="1200" height="176" rx="10" fill="url(#ft-bg)"/>
  <rect width="1200" height="176" rx="10" fill="url(#ft-nebula-l)"/>
  <rect width="1200" height="176" rx="10" fill="url(#ft-nebula-r)"/>
  <rect width="1200" height="176" rx="10" fill="url(#ft-dots)"/>
  {star4(74, 48, 6.0, C['white'], 0.9, 'tw1')}
  {star4(1124, 52, 6.5, C['lavender'], 0.9, 'tw1')}
  {star4(104, 134, 4.5, C['sky'], 0.85)}
  {star4(1092, 136, 4.8, C['rose'], 0.85)}

  {rpg_box(160, 42, 880, 110, fill=C['void'], border=C['white'], outer_w=2.4, inset=5)}
  {rpg_box(184, 18, 168, 34, fill=C['void'], border=C['white'], outer_w=2.0, inset=3.5)}
  <text x="268" y="39.5" text-anchor="middle" fill="{C['sky']}" font-size="12.5" font-weight="800" letter-spacing="2">SAVE POINT</text>

  <text x="600" y="92" text-anchor="middle" fill="{C['white']}" font-size="17" font-weight="700" class="sans">"Thanks for visiting. You've been coding here for as long as you can remember."</text>
  <text x="600" y="124" text-anchor="middle" fill="{C['muted']}" font-size="13">Made with ☕ &amp; offline-first craft  ·  Reza Widya Utama (@WidyatamaX)</text>
  <polygon points="1008,124 1020,124 1014,134" fill="{C['white']}" class="blink"/>"""
    else:
        body = f"""  <rect width="480" height="216" rx="10" fill="url(#ftm-bg)"/>
  <rect width="480" height="216" rx="10" fill="url(#ftm-nebula-l)"/>
  <rect width="480" height="216" rx="10" fill="url(#ftm-dots)"/>
  {star4(42, 26, 4.5, C['white'], 0.9, 'tw1')}
  {star4(438, 28, 5.0, C['lavender'], 0.9, 'tw1')}

  {rpg_box(22, 46, 436, 148, fill=C['void'], border=C['white'], outer_w=2.2, inset=4.5)}
  {rpg_box(40, 22, 152, 32, fill=C['void'], border=C['white'], outer_w=2.0, inset=3.5)}
  <text x="116" y="42.5" text-anchor="middle" fill="{C['sky']}" font-size="12" font-weight="800" letter-spacing="1.8">SAVE POINT</text>

  <text x="240" y="94" text-anchor="middle" fill="{C['white']}" font-size="14.5" font-weight="700" class="sans">"Thanks for visiting. You've been</text>
  <text x="240" y="116" text-anchor="middle" fill="{C['white']}" font-size="14.5" font-weight="700" class="sans">coding here as long as you remember."</text>
  <text x="240" y="152" text-anchor="middle" fill="{C['muted']}" font-size="11.5">Made with ☕ &amp; offline-first craft</text>
  <text x="240" y="170" text-anchor="middle" fill="{C['lavender']}" font-size="11.5">@WidyatamaX · Indonesia</text>
  <polygon points="426,170 438,170 432,180" fill="{C['white']}" class="blink"/>"""

    return svg_wrap(w, h, "Save Point Footer — WidyatamaX", defs, styles, body)


def write_and_validate(rel_path: str, content: str) -> None:
    # Validate strict XML well-formedness before writing
    ET.fromstring(content.encode("utf-8"))
    out = ASSETS / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def main() -> None:
    files: dict[str, str] = {
        "header.svg": build_header_desktop(),
        "m/header.svg": build_header_mobile(),
        "desk.svg": build_desk(),
        "neofetch.svg": build_neofetch_desktop(),
        "m/neofetch.svg": build_neofetch_mobile(),
        "timeline.svg": build_timeline_desktop(),
        "m/timeline.svg": build_timeline_mobile(),
        "marquee.svg": build_marquee(mobile=False),
        "m/marquee.svg": build_marquee(mobile=True),
        "stack.svg": build_stack_desktop(),
        "m/stack.svg": build_stack_mobile(),
        "ai-orbit.svg": build_ai_desktop(),
        "m/ai-orbit.svg": build_ai_mobile(),
        "divider.svg": build_divider(mobile=False),
        "m/divider.svg": build_divider(mobile=True),
        "footer.svg": build_footer(mobile=False),
        "m/footer.svg": build_footer(mobile=True),
    }

    sections = [
        ("about", "ABOUT ME", "CH.01", C["lavender"]),
        ("journey", "JOURNEY", "CH.02", C["sky"]),
        ("stack", "TECH STACK", "CH.03", C["mint"]),
        ("ai", "AI TOOLBOX", "CH.04", C["rose"]),
        ("stats", "GITHUB STATS", "CH.05", C["amber"]),
    ]
    for slug, title, ch, col in sections:
        files[f"sections/{slug}.svg"] = build_section_header(title, ch, col, mobile=False)
        files[f"m/section-{slug}.svg"] = build_section_header(title, ch, col, mobile=True)

    # Social / Contact RPG menu buttons
    icon_mail = (
        f'<rect x="0" y="3" width="18" height="13" rx="1.5" fill="none" stroke="{C["white"]}" stroke-width="1.6"/>'
        f'<path d="M 1 4 L 9 11 L 17 4" fill="none" stroke="{C["rose"]}" stroke-width="1.6" stroke-linejoin="round"/>'
    )
    icon_gh = (
        f'<circle cx="9" cy="10" r="7.5" fill="none" stroke="{C["white"]}" stroke-width="1.6"/>'
        f'<path d="M 5.5 11.5 L 7.5 9.5 L 5.5 7.5 M 9.5 12.5 L 13 12.5" fill="none" stroke="{C["lavender"]}" stroke-width="1.6" stroke-linecap="round"/>'
    )
    icon_app = (
        f'<rect x="1" y="2" width="16" height="15" rx="2" fill="none" stroke="{C["white"]}" stroke-width="1.6"/>'
        f'<path d="M 5 12 L 8 8 L 10.5 10.5 L 13.5 6" fill="none" stroke="{C["mint"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    files["social/email.svg"] = build_social_btn("email.svg", 296, "rezawidyautama567@gmail.com", C["rose"], icon_mail)
    files["social/github.svg"] = build_social_btn("github.svg", 184, "@WidyatamaX", C["lavender"], icon_gh)
    files["social/openformu.svg"] = build_social_btn("openformu.svg", 206, "OpenFormu Live", C["mint"], icon_app)

    for rel, content in files.items():
        write_and_validate(rel, content)

    print(f"Generated and XML-validated {len(files)} OMORI SVG assets in {ASSETS}")


if __name__ == "__main__":
    main()

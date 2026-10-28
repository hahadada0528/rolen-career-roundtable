"""Board HTML writer with 睿览 (rolen) branding overlay."""
from __future__ import annotations

import base64
import re
from pathlib import Path
from typing import Any

from src.collab._board_stock import *  # noqa: F403
from src.collab import _board_stock as _stock

_LOGO_CACHE: str | None = None

_FONTS_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Newsreader:opsz,wght@6..72,500;6..72,600;6..72,700&"
    "family=Figtree:wght@400;500;600;700&"
    "family=IBM+Plex+Mono:wght@400;500&display=swap"
)

_SKIN_CSS = r"""
/* —— 睿览 skin —— */
:root {
  --bg: #e9eef4;
  --bg-wash: #f2f5f9;
  --paper: #fcfdff;
  --paper-2: #f4f7fb;
  --ink: #132033;
  --muted: #5a6a7c;
  --line: #d5dde8;
  --line-soft: #e6ecf3;
  --accent: #0b2b4a;
  --accent-soft: #ebf1f8;
  --accent-deep: #071e36;
  --amber: #9a7340;
  --amber-soft: #f7f1e7;
  --wait: #3d6f8f;
  --wait-bg: #eaf3f8;
  --shadow: 0 12px 36px rgba(11, 43, 74, 0.07);
  --shadow-soft: 0 2px 10px rgba(11, 43, 74, 0.04);
  --radius: 16px;
  --radius-sm: 12px;
  --font-display: "Newsreader", "Songti SC", "Noto Serif SC", serif;
  --font-body: "Figtree", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Consolas, monospace;
}
body {
  font: 15px/1.55 var(--font-body);
  background:
    radial-gradient(1100px 480px at 0% -10%, rgba(11,43,74,0.10), transparent 58%),
    radial-gradient(800px 420px at 100% 0%, rgba(61,111,143,0.08), transparent 52%),
    linear-gradient(180deg, var(--bg-wash) 0%, var(--bg) 55%, #e4eaf1 100%);
  letter-spacing: 0.005em;
}
.app { padding: 16px 18px 14px; gap: 0; }

header.top {
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.98), rgba(252,253,255,0.94));
  border: 1px solid rgba(213,221,232,0.95);
  box-shadow: var(--shadow-soft), var(--shadow);
  padding: 16px 18px 12px;
  margin-bottom: 14px;
  animation: rolen-header-in .45s ease both;
}
header.top::before {
  content: "";
  position: absolute; left: 0; right: 0; top: 0; height: 3px;
  background: linear-gradient(90deg, #071e36 0%, #0b2b4a 42%, #3d6f8f 100%);
}
.top-bar { margin-bottom: 12px; align-items: center; }

.brand-row { display: flex; align-items: center; gap: 16px; min-width: 0; }
.brand-logo {
  height: 48px; width: auto; max-width: min(210px, 46vw);
  flex: 0 0 auto; object-fit: contain; display: block;
  filter: drop-shadow(0 1px 0 rgba(255,255,255,0.4));
}
.brand-mark { display: none !important; }
.brand-text {
  min-width: 0;
  padding-left: 16px;
  border-left: 1px solid rgba(11,43,74,0.12);
}
.brand-kicker {
  margin: 0;
  font-family: var(--font-body);
  font-size: 12px; letter-spacing: 0.08em; text-transform: none;
  color: #3d6f8f; font-weight: 700;
}
h1 {
  margin: 3px 0 0;
  font-family: var(--font-display);
  font-size: 28px; font-weight: 600; letter-spacing: -0.01em;
  color: var(--accent-deep); line-height: 1.12;
}

.stage-chip {
  border-radius: 999px;
  background: linear-gradient(180deg, #fff, var(--accent-soft));
  border: 1px solid #c8d4e4;
  box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset;
  padding: 7px 13px;
}
.meta { font-size: 12px; letter-spacing: 0.01em; }

.flow-bar { gap: 8px; margin: 0 0 12px; padding-bottom: 2px; }
.flow-group {
  border-radius: 13px;
  padding: 9px 11px;
  background: rgba(244,247,251,0.9);
  box-shadow: none;
}
.flow-group.on {
  border-color: transparent;
  background:
    linear-gradient(165deg, #ffffff 0%, var(--accent-soft) 100%);
  box-shadow:
    0 0 0 1px rgba(11,43,74,0.18),
    0 8px 20px rgba(11,43,74,0.08);
  position: relative;
}
.flow-group.on::before {
  content: "";
  position: absolute; left: 0; top: 10px; bottom: 10px; width: 3px;
  border-radius: 0 3px 3px 0;
  background: linear-gradient(180deg, #0b2b4a, #3d6f8f);
}
.flow-group.done { background: #eef2f7; }
.flow-num {
  font-variant-numeric: tabular-nums;
  color: #3d6f8f;
}
.flow-group.on .flow-num { color: var(--accent); }

.wait-banner {
  border-radius: 13px;
  border-color: #b7cede;
  background: linear-gradient(135deg, #eef6fb, var(--wait-bg));
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}

.rail, .stage-shell {
  border-color: rgba(213,221,232,0.95);
  box-shadow: var(--shadow-soft);
}
.rail-label {
  letter-spacing: 0.12em;
  color: #6a7a8c;
}
.seat {
  border-radius: 12px;
  background: linear-gradient(180deg, #fff, var(--paper-2));
}
.seat.working {
  border-color: #b7c8dc;
  background: linear-gradient(165deg, #fff, var(--accent-soft));
}
.seat:hover {
  border-color: #aebcd0;
  box-shadow: 0 4px 12px rgba(11,43,74,0.06);
}

nav.tabs {
  background: linear-gradient(180deg, #fff 0%, #f6f8fb 100%);
  padding: 10px 14px 0;
}
.tab {
  border-radius: 10px 10px 0 0;
  letter-spacing: 0.01em;
}
.tab.on {
  color: var(--accent-deep);
  border-bottom-color: var(--accent);
  background: linear-gradient(180deg, rgba(11,43,74,0.04), transparent);
}

.card {
  border-radius: 13px;
  background: linear-gradient(180deg, #fff, var(--paper-2));
  box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset;
}
.card.you {
  border-color: #c2d0e2;
  background: linear-gradient(155deg, #ffffff 0%, #eef3f9 100%);
}
.card header {
  font-family: var(--font-display);
  font-weight: 600;
  letter-spacing: -0.01em;
}

#talk-composer {
  border-radius: 14px;
  border: 1px solid #c7d3e0;
  box-shadow: 0 -4px 24px rgba(11,43,74,0.05);
  background: linear-gradient(180deg, #fff, #fafcfe);
  padding: 12px 12px 10px;
}
button, #talk-composer button, .upload-box button {
  border-radius: 10px;
  letter-spacing: 0.02em;
  box-shadow: 0 1px 0 rgba(255,255,255,0.18) inset;
}
button:not(.secondary):not(.tab),
#talk-composer button:not(.secondary),
.upload-box button:not(.secondary) {
  background: linear-gradient(180deg, #14385c 0%, #0b2b4a 100%);
}
button:not(.secondary):hover,
#talk-composer button:not(.secondary):hover {
  filter: brightness(1.08);
}
button.secondary,
#talk-composer button.secondary,
.upload-box button.secondary,
.duty-box button.secondary {
  border-radius: 10px;
  border-color: #b8c6d6;
  background: #fff;
}

.duty-box, .upload-box {
  border-radius: 14px;
  box-shadow: var(--shadow-soft);
}
.duty-box {
  border-color: #c5d2e3;
  background: linear-gradient(165deg, #fff, var(--accent-soft));
}
.upload-box header, .duty-box header {
  font-family: var(--font-display);
  font-weight: 600;
}

.ingest-progress {
  border-color: #b7c8dc;
  background: linear-gradient(165deg, #fff, var(--accent-soft));
  color: #24384f;
}
.ingest-progress .bar { background: #d8e2ee; }
.ingest-progress .ingest-current { color: #3d556e; }
.file-hint { color: #3d556e; }

::-webkit-scrollbar-thumb {
  background: #b8c4d4;
  border: 2px solid transparent;
  background-clip: padding-box;
}

@keyframes rolen-header-in {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) {
  header.top { animation: none; }
}
@media (max-width: 960px) {
  h1 { font-size: 23px; }
  .brand-logo { height: 40px; }
}
"""


def _logo_data_uri(project_root: Path) -> str:
    global _LOGO_CACHE
    if _LOGO_CACHE is not None:
        return _LOGO_CACHE
    logo = Path(project_root) / "assets" / "rolen-logo.png"
    if not logo.is_file():
        _LOGO_CACHE = ""
        return _LOGO_CACHE
    raw = logo.read_bytes()
    mime = "image/jpeg" if raw[:3] == b"\xff\xd8\xff" else "image/png"
    _LOGO_CACHE = f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")
    return _LOGO_CACHE


def _apply_rolen_brand(html: str, project_root: Path) -> str:
    logo = _logo_data_uri(project_root)

    # Fonts
    html = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet">',
        f'<link href="{_FONTS_HREF}" rel="stylesheet">',
        html,
        count=1,
    )

    # Legacy teal → navy (stock template leftovers)
    html = html.replace("--accent: #2f6f6a;", "--accent: #0b2b4a;")
    html = html.replace("--accent-soft: #e5f1ef;", "--accent-soft: #ebf1f8;")
    html = html.replace("--accent-deep: #245853;", "--accent-deep: #071e36;")
    html = html.replace("rgba(47,111,106,", "rgba(11,43,74,")
    html = html.replace("#c7ddd9", "#c5d0e0")
    html = html.replace("#4d726c", "#4a6178")
    html = html.replace("#6a7f78", "#6a7a8a")
    html = html.replace("#c5d9d0", "#c5d0dc")
    html = html.replace("#f3faf6", "#f3f6fa")
    html = html.replace("#9ec4bf", "#b7c8dc")
    html = html.replace("#d7e6e3", "#d8e2ee")
    html = html.replace("#2f4f4b", "#24384f")
    html = html.replace("#3d5f59", "#3d556e")

    # Brand block CSS (stock header marks)
    brand_css = """
    .brand-row { display: flex; align-items: center; gap: 16px; min-width: 0; }
    .brand-logo {
      height: 48px; width: auto; max-width: min(210px, 46vw);
      flex: 0 0 auto; object-fit: contain; display: block;
    }
    .brand-mark { display: none !important; }
    .brand-text { min-width: 0; padding-left: 16px; border-left: 1px solid rgba(11,43,74,0.12); }
    .brand-kicker {
      margin: 0;
      font-size: 12px; letter-spacing: 0.08em; text-transform: none;
      color: #3d6f8f; font-weight: 700;
    }
"""
    html = re.sub(
        r"\.brand-row \{ display: flex; align-items: center; gap: 12px; min-width: 0; \}\s*"
        r"\.brand-mark \{.*?\}\s*"
        r"@keyframes ring-spin \{ to \{ transform: rotate\(360deg\); \} \}\s*"
        r"\.brand-text \{ min-width: 0; \}\s*"
        r"\.brand-kicker \{.*?\}",
        brand_css.strip(),
        html,
        count=1,
        flags=re.S,
    )

    logo_tag = (
        f'<img class="brand-logo" src="{logo}" alt="睿览 rolen" width="168" height="56" />'
        if logo
        else '<div class="brand-logo-fallback" aria-hidden="true">睿览</div>'
    )
    new_brand = f"""<div class="brand-row">
        {logo_tag}
        <div class="brand-text">
          <p class="brand-kicker">职业工作手册 · 圆桌</p>
          <h1>"""
    html = re.sub(
        r'<div class="brand-row">\s*'
        r'<div class="brand-mark" aria-hidden="true"></div>\s*'
        r'<div class="brand-text">\s*'
        r'<p class="brand-kicker">职业工作手册 · 圆桌</p>\s*'
        r"<h1>",
        new_brand,
        html,
        count=1,
    )

    html = html.replace("<title>圆桌 · ", "<title>睿览 · 圆桌 · ")
    html = html.replace('document.title = "圆桌 · "', 'document.title = "睿览 · 圆桌 · "')
    html = html.replace(
        'document.title = "圆桌 · 职业工作手册";',
        'document.title = "睿览 · 职业工作手册";',
    )
    html = html.replace(
        ".seat.working header::before,\n      .brand-mark,\n",
        ".seat.working header::before,\n",
    )

    # Inject full skin once
    if "/* —— 睿览 skin —— */" not in html:
        html = html.replace("</style>", _SKIN_CSS + "\n  </style>", 1)

    return html


def write_board(project_root: Any, topic: Any, history: Any, *args: Any, **kwargs: Any):
    path = _stock.write_board(project_root, topic, history, *args, **kwargs)
    try:
        p = Path(path)
        html = p.read_text(encoding="utf-8")
        branded = _apply_rolen_brand(html, Path(project_root))
        if branded != html:
            p.write_text(branded, encoding="utf-8")
    except OSError:
        pass
    return path

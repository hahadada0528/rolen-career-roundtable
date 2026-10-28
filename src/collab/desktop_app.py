"""Native desktop window for the roundtable board (pywebview / macOS WebKit)."""
from __future__ import annotations


def open_board_window(url: str) -> None:
    """Block until the user closes the app window."""
    try:
        import webview
    except ImportError as exc:
        raise RuntimeError(
            "未安装 pywebview。请执行：pip install pywebview\n然后重新运行：python main.py app"
        ) from exc
    webview.create_window(
        "睿览 · 职业工作手册",
        url,
        width=1440,
        height=900,
        min_size=(960, 640),
    )
    webview.start()

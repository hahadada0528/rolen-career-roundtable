"""Mac / source-style entry: launch the roundtable desktop app."""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _mac_defaults() -> None:
    """Fill env defaults that the Windows build assumed."""
    desktop = Path.home() / "Desktop"
    os.environ.setdefault("CAREER_DESKTOP", str(desktop))
    # Skills template: this package already ships .agents/skills
    os.environ.setdefault("AI_DATABASE_PATH", str(ROOT))
    os.environ.setdefault("ROUNDTABLE_DATA_ROOT", str(ROOT / "data"))


def _load_impl():
    pyc = ROOT / "_roundtable_main.pyc"
    if not pyc.is_file():
        raise RuntimeError(f"缺少 {_roundtable_main_name()}: 请重新从 Windows 包提取 main.pyc")
    spec = importlib.util.spec_from_file_location("_roundtable_main", pyc)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 _roundtable_main.pyc")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _roundtable_main_name() -> str:
    return "_roundtable_main.pyc"


def main() -> None:
    _mac_defaults()
    os.chdir(ROOT)
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from src.collab.app_paths import ensure_runtime_dirs

    ensure_runtime_dirs()

    # Match frozen app_entry: default subcommand is desktop "app"
    if len(sys.argv) == 1:
        sys.argv.append("app")

    mod = _load_impl()
    raise SystemExit(mod.app())


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as exc:
        log = ROOT / "圆桌App-错误日志.txt"
        try:
            import traceback

            log.write_text(
                "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
                encoding="utf-8",
            )
        except OSError:
            pass
        print(f"启动失败，详见：{log}", file=sys.stderr)
        raise

#!/bin/bash
cd "$(dirname "$0")"
export PATH="$PWD/.venv/bin:$PATH"
if [[ ! -x .venv/bin/python ]]; then
  echo "未找到 .venv，请先运行：uv venv --python 3.12 .venv && uv pip install -r requirements-mac.txt -p .venv/bin/python"
  read -r -p "按回车关闭…"
  exit 1
fi
exec .venv/bin/python main.py

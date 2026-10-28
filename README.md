# 睿览 · 职业工作手册圆桌

> 多智能体「圆桌」产品：你说出一个职业，主 agent 点兵、分阶段推进背调 / 调研 / 知识库 / 分解 / 人机分工，**每一步都等人批准**，最后交出可复检的职业工作手册。

<p align="center">
  <img src="assets/rolen-logo.png" alt="睿览 rolen" width="220" />
</p>

**角色**：产品工程 / Mac 客户端适配 / 品牌化看板 UI  
**形态**：桌面 App（pywebview）+ 本地看板 + LLM 多智能体流水线  
**栈**：Python 3.12 · LangChain / LangGraph · Deep Agents · Obsidian LLM Wiki · pywebview

---

## 作品集摘要

| 维度 | 说明 |
|------|------|
| 问题 | 职业学习资料散落在招聘站、标准文件和个人笔记里，缺少「可批准、可复检、可沉淀」的流程 |
| 方案 | 把流程拆成固定席位与阶段门禁；产出进本地知识库；链接必须可打开 |
| 我的工作 | ① Windows 独立包 → **macOS 可运行时** ② 看板 **睿览品牌化**与视觉体系 ③ 启动脚本 / 依赖 / 说明文档 |
| 亮点 | 人在环（Human-in-the-loop）批准门；席位分工清晰；知识库「compile, don't retrieve」 |

---

## 产品怎么跑

```text
你说职业名
    ↓
建库骨架（知识库席）
    ↓
职业背调 → 你录入 JD → 归纳 → 你批准
    ↓
全网行业调研 → 你批准链接 → 知识库核实入库
    ↓
你上传素材 → 蒸馏切片
    ↓
目标分解 → 复检 → 你批准
    ↓
人机分工（tools.md）→ 复检 → 交稿
```

| 席位 | 职责 |
|------|------|
| 主 agent | 理解意图、点兵、等人批准、终审交稿 |
| 知识库 | Obsidian + LLM Wiki；切片带原文链接 |
| 职业背调 | 求职网站职责归纳 |
| 行业调研 | 规范 / 岗位 / KPI 类公开资料（交链接，不直入库） |
| 分解 | 第一性原理拆工作事项 |
| 人机分工 | 工具学习 / AI 可替代 / 必须人工 |
| 复检 | Reality Checker：链接与结构 |

详细规则见 [`AGENTS.md`](AGENTS.md)。

---

## 架构一览

```text
┌─────────────────────────────────────────────┐
│  Desktop shell (pywebview / Mac WebKit)     │
│  board.html  ← 本地 HTTP 看板 :8765          │
└──────────────────┬──────────────────────────┘
                   │ task / upload / status
┌──────────────────▼──────────────────────────┐
│  RoundTable runtime                         │
│  orchestrator → seats (LangChain agents)    │
│  pipeline.json · workspace · data/{职业}/   │
└──────────────────┬──────────────────────────┘
                   │
         AGICTO OpenAI-compatible API
```

**Mac 适配要点**

- 从 Windows PyInstaller 包抽出应用字节码，用 Python 3.12 + 原生依赖运行
- `main.py` 补齐 macOS 路径（`CAREER_DESKTOP` / `AI_DATABASE_PATH`）
- `src/collab/board.py` 在每次写看板时注入睿览视觉皮肤（logo、海军蓝、字体）
- `启动圆桌App.command` 一键启动

---

## 界面

看板顶栏使用睿览 logo，主色对齐品牌海军蓝（`#0b2b4a`），字体 Newsreader + Figtree，流程条与席位卡统一冷色纸面层级。

本地打开 `board.html` 或启动 App 后即可预览。

---

## 在 macOS 上运行

**要求**：Python 3.12+（推荐 [uv](https://github.com/astral-sh/uv)）、AGICTO API Key

```bash
# 1. 克隆
git clone https://github.com/hahadada0528/rolen-career-roundtable.git
cd rolen-career-roundtable

# 2. 虚拟环境与依赖
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements-mac.txt

# 3. 配置
cp .env.example .env
# 编辑 .env，填入 AGICTO_API_KEY

# 4. 启动
./启动圆桌App.command
# 或
python main.py
```

在「圆桌对话」里发送职业名即可开始。产物在 `outputs/` 与 `data/{职业名}/`。

> 仓库不含 Windows 的 `圆桌App.exe` / `_internal`（体积过大）。Mac 运行依赖本仓库的 `src/` + `requirements-mac.txt`。

---

## 仓库结构

```text
├── main.py                 # Mac / 源码式入口
├── board.html              # 看板（运行时也会重写）
├── assets/rolen-logo.png   # 品牌
├── src/                    # 圆桌核心（含 Mac 覆盖层 board.py / desktop_app.py）
├── .agents/skills/         # 行业调研、人机分工、LLM Wiki 等技能
├── playbook/               # 工具与行业目录、产品进化记忆
├── workspace/              # 会话工作区（运行时写入）
├── AGENTS.md               # 圆桌工作手册
└── requirements-mac.txt
```

---

## 安全说明

- **不要**提交 `.env`。示例见 `.env.example`。
- API Key 泄露后请到 AGICTO 控制台轮换。

---

## 许可与声明

本仓库用于作品集展示与本机运行。若你二次分发，请自行确认依赖包与模型服务条款。品牌「睿览 / rolen」用于本产品界面标识。

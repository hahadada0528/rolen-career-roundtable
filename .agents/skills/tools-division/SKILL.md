---
name: tools-division
description: >
  Roundtable tools stage: human-machine division of labor for the tools-division seat.
  Use when pipeline stage is tools / review_tools, user approved analysis.md,
  or when implementing workspace/tools.md, run_inline_tools, and per-item web search.
  Requires internet_search per work item from analysis.md — no catalog filler.
  Output must answer: tools to learn, what AI can replace, what must stay human.
---

# 人机分工（tools · specialist / 专业调研）

你是 **本席 agent** 在 **tools** 阶段的执行规范。系统内联入口：`src/collab/tools_phase.py` → `run_inline_tools()`。
本技能由 `src/collab/skill_inject.py` 注入本席；内联路径也会 `record_applied_skills(specialist)`。

## 用户要的结果（交稿形态）

对 **analysis.md 每一条工作事项**，必须回答三件事：

1. **需要学会的工具** — 网上检索到的具体产品/平台/文档；写清工具名、官网、学什么、证明摘录
2. **AI可替代** — 起草、汇总、提醒、初筛等可由 AI/工具代劳的部分
3. **必须人工** — 审批、当面沟通、法律责任、不可逆人事决策

## 前置门禁

1. `read_pipeline` → **profession**；stage 须为 `tools` 或 `review_tools`（返工）。
2. **analysis.md 已批准**（用户发「批准/继续」后系统会 `reset_tools_from_analysis`）。
3. **禁止** wiki_ingest / 改 vault；只写 `workspace/tools.md`。
4. **禁止** @scout；**禁止**把本阶段交给知识库席。
5. **禁止**不检索就秒交旧稿 / 目录万能工具。

## 核心原则

| 必须 | 禁止 |
|------|------|
| 对照 **analysis.md** 子目标 → 工作事项 **逐条** 写 | 不检索就填钉钉/飞书/北森等「万能工具」 |
| 每条 **internet_search** 后再写入 | 编造 URL、编造摘录 |
| 引用含 **https + 摘录 + 检索来源标注** | 目录/catalog 兜底冒充完成 |
| 工具须 **服务该条工作事项** | 同一链接刷全篇、招聘站首页糊弄无关事项 |

## 检索与深研流程（每条工作事项 · 慢而真）

1. `parse_work_item_specs` → `(子目标, 工作事项)`。
2. **多组 internet_search**（职业 + 事项 + 产品名 / `site:官网`）。
3. **`open_page` 打开产品页**，摘「页面摘录」。
4. **调用模型**根据页面正文写：需要学会的工具 / AI可替代 / 必须人工（禁止 `division_of_labor` 套话秒填）。
5. 写入 `tools.md`，标注：
   - `检索来源：internet_search · 查询词：…`
   - `页面核实：open_page … · 写法：模型深研`
6. 检索/开页/模型失败 → 「搜索失败/缺口」，不得用目录秒交。

单批默认 **1 条**工作事项（`_ITEMS_PER_TURN=1`），看板会显示「检索 / 打开产品页 / 撰写分工」进度。

## tools.md 结构（每条工作事项）

```
#### 工作事项：{事项名}
> 对应子目标：…
> **检索来源**：internet_search · **查询词**：…
> **本项工具数**：1～5（尽量收录检索到的不同产品；禁止同品凑数）

**需要学会的工具**
- **工具**：…（可连续写多个工具块，每个都有官网/学什么/摘录；同一产品只写一次）
- **解决**：…
- **官网/文档**：https://…
- **学什么**：…
- **页面摘录**：…（open_page）
- **证明摘录**：…
- **工具**：…（第二个不同产品，若有）
- …
```

若用户修改意见要求「多项多个工具 / 能搜到的都要」：尽量列不同产品（上限 5），**禁止**用同一工具的不同链接凑数；只找到 1 个也可用。

**找不到可用软件/AI 工具**：写明「检索结论：没有可用的 AI/软件工具」+ AI可替代写「无」+ 必须人工写清本事项仍靠人做；**禁止**为凑链接空转重搜。

（兼容旧稿标题 `可用工具/平台` + `AI/工具可做`。）

## 交稿门槛

- 工作事项全部完成；每条含检索来源 + 需要学会的工具 + AI可替代 + 必须人工（无工具结论也算完成）
- 唯一 https 数达标；同一 host 不得刷屏
- 与当前 analysis.md 指纹一致
- 内联跑满后 `set_pipeline_stage("review_tools")` → @critic

## 返工

1. 只改 critique「需改清单」点名条目；其余原样保留。
2. 对被点条目重新 internet_search。
3. 改完 → review_tools → @critic。

## 本地验证

```bash
.venv/Scripts/python.exe scripts/run_live_tools.py
```

期望：真实联网检索；`has_search_markers=true`；每条有「需要学会的工具」。

## 相关文件

| 文件 | 用途 |
|------|------|
| `workspace/analysis.md` | 已批准分解 |
| `workspace/tools.md` | 人机分工正文 |
| `src/collab/skill_inject.py` | 技能注入 |
| `src/collab/tools_phase.py` | 内联检索与写稿 |
| `src/collab/tools_quality.py` | 交稿门槛 |

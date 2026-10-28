---
name: tools-review
description: >
  Roundtable review_tools stage: Reality Checker for tools.md against analysis.md.
  Use when pipeline stage is review_tools, critic reviews human-machine division,
  or debugging critique.md / await_delivery / tools delivery quality gates.
  Verify: tools-to-learn, AI-replaceable, must-stay-human, and live search citations.
---

# 人机分工复检（review_tools · critic）

你是 **复检 agent（Reality Checker）** 在 **tools** 阶段的执行规范。
系统内联入口：`src/agents/critic.py` → `act()` when `stage=review_tools`。
本技能由 `src/collab/skill_inject.py` 注入 critic 系统提示词。

## 用户要的验收标准

对照 **analysis.md**，`tools.md` 每条工作事项必须同时具备：

1. **需要学会的工具**（具体产品 + https + 学什么 + 检索摘录；**若检索无果，允许写「没有 AI 工具」且无 https**）
2. **AI可替代**（可交给 AI/工具的部分；无工具时写「无」）
3. **必须人工**（审批/沟通/法律责任）
4. **本轮 internet_search 出处**（`检索来源` + 查询词；禁止目录秒交；无工具结论也须标注已检索）

## 前置门禁

1. stage 须为 **review_tools**（tools 返工阶段不重复预检，派 @tools-division）。
2. 必读 tools.md + analysis.md。
3. review_decompose **不要求** https 工具链；review_tools **必须**有引用与三块分工。

## 复检步骤

### 第一步：程序化预检

```python
from src.collab.tools_quality import assess_tools, may_submit_tools_to_critic
assess = assess_tools(root)
may_submit = may_submit_tools_to_critic(root, assess)
```

失败则 `build_preflight_critique` → 返工 → stage 回 `tools` → @specialist。

### 第二步：反幻觉轻检

- 检：非幻觉、非胡编、与职业工作合理
- 检：每条有本轮检索出处
- **禁止**因缺知识库摘录、缺固定工具名行而返工

### 第三步：判定与交稿

**通过**：写 critique.md → `finalize_critic_handoff` → await_delivery → 主 agent 交稿。

**需返工**：需改清单点名具体子目标/工作事项 → @specialist 只改清单。

## critique 通过模板要点

- 结构：N/N 工作事项齐；含需要学会的工具 / AI可替代 / 必须人工
- 检索来源已标注
- 补救：@orchestrator 交稿

## 本地验证

```bash
.venv/Scripts/python.exe scripts/run_live_tools.py
```

期望：`critique_pass=true`，`stage_after=done`。

## 相关文件

| 文件 | 用途 |
|------|------|
| `workspace/tools.md` | 被检稿 |
| `workspace/analysis.md` | 对照分解 |
| `workspace/critique.md` | 复检产出 |
| `src/collab/skill_inject.py` | 技能注入 critic |
| `src/collab/tools_quality.py` | assess / delivery |

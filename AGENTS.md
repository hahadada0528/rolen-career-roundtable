# 职业工作手册圆桌（Agency Agents · NEXUS-Micro）

用户的话先交给主 agent。主 agent 像项目经理一样理解自然语言、必要时追问你拍板，再判断职业、点兵、等人批准，并做终审后再把文件交给用户。

**各席共性**：每人都有独立理解力与分析力——先弄清本轮任务、成功标准与用户约束，再动手；证据优先；自检不过先改再交。改 skill 极谨慎：默认只落实本轮产出，持久规则才补丁。

## 席位

| 圆桌席 | 职责 | 产出 |
|--------|------|------|
| orchestrator | Agents Orchestrator（对话经理） | `workspace/brief.md`；听懂 prompt、追问澄清；把复检通过的稿交给用户；等人批准 |
| researcher | 知识库 agent | `data/{职业}/知识库`（Obsidian + LLM Wiki）；建库；整理上传切片 |
| industry-survey | 行业调研 agent | 交 URL（**禁止直接入库**）；`professional-survey.md` + `survey-links.md`；技能：`industry-survey` |
| tools-division | 人机分工 agent | `workspace/tools.md` + 每轮 `research-report.md`；技能：`tools-division` |
| scout | 职业背调 | `workspace/background.md`（用户录入职责 + 统计归纳） |
| browser | 本地浏览器 agent | **已暂时关闭**（默认不用 Chrome 自动化） |
| critic | Reality Checker 复检 | `critique.md` + `kb-pending.md` → 主 agent 协调入库与返工；技能：`tools-review` |
| analyst | Workflow Architect 分解 | `workspace/analysis.md`（第一性原理） |

## 顺序（分解/工具仍经 critic；第一轮背调由用户录入并自行复检）

1. 用户给出职业 → 主 agent 判定，在程序目录 `data/{职业}/` 建库与持久数据
2. 知识库 agent 按 LLM Wiki / Obsidian 技能搭库骨架
3. **第一轮背调**：主 agent 点兵 @scout → 求职网站清单 → **背调传送窗口**录入 → **交给背调分析**（scout 逐条去杂音归纳，非词频统计）→ **归纳稿交给你批准** → 满意后发「批准」或「继续」
4. **全网行业调研**：@industry-survey 写调研稿 + **调研链接汇总** → **你批准** → @researcher 逐条 open_page 核实入库
5. 交给用户「需要自行传入的素材」及原因。用户上传后由 **知识库** agent 整理进库。
6. 用户说**继续** → 分解 → 复检 → 批准。
7. **人机分工** @tools-division 按 analysis.md 写 tools.md；**复检** 产出 critique + kb-pending → **主 agent** → 若有待入库则 **知识库先入** → 再派人机分工改稿（若需返工）。
8. 通过后交给你。

用户说不满意或给修改建议时，回到主 agent，由他判断打回哪一席。

专家遇到不懂的、或需要你拍板的问题，必须交回主 agent；主 agent 在「圆桌对话」里向你汇报并提问，等你回复后再继续。主 agent 也会在目标/范围不清时主动问你 1～3 个问题，而不是猜着推进。

职业持久数据建在程序目录：`data/{职业}/`（含知识库、背调、调研、上传等；compile, don't retrieve）。模板技能来自 LLM Wiki。不使用 OneDrive。

点名：`@orchestrator` / `@agents-orchestrator`、`@researcher` / 知识库、`@industry-survey` / 行业调研 / `@pro-researcher`、`@tools-division` / 人机分工 / `@tool-researcher`、`@scout` / `@background-checker`、`@browser` / `@local-browser`、`@analyst` / `@workflow-architect`、`@critic` / `@reality-checker`。（旧名 `@specialist` 兼容映射到行业调研）

每人一份私有记忆（`workspace/memory/{席位}.md`），同事读不到。

**产品进化（跨轮自动优化）**：系统把用户批准/入库/交稿的链接与检索词写入 `playbook/learned/product.json`，下一轮 collect/tools 自动复用；打回/删链会降权。无需手改 catalog。

人先把圆桌跑起来，再在「圆桌对话」里把职业发给主 agent。生成的文件在看板「生成的文件」标签。素材用对话里的传入文件窗口。

**本地浏览器 agent 已暂时关闭**（默认）。背调靠看板「背调传送窗口」录入 + scout 分析；资料收集用 HTTP 搜索。若要重新启用 Chrome 自动化：设置 `ROUNDTABLE_LOCAL_BROWSER=1` 后重启圆桌。

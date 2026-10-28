---
name: industry-survey
description: >
  Roundtable collect stage: industry-intelligence survey for the industry-survey seat
  (separated from tools-division). Use when stage is collect / await_survey,
  user says 重新全网调研 / 重做全网调研 / 重做专业调研 / 行业调研, or when writing
  professional-survey.md, survey-links.md, source-urls.md.
  Goal: industry norms — laws/regulations, national occupational standards, role specs,
  acceptance/KPI criteria — NOT news portals, gov homepages, language tutorials, or downloads.
---

# 行业情报调研（collect · specialist · industry-survey）

你是 **行业调研 agent** 在 **collect** 阶段的**唯一**规范。  
系统入口：`src/collab/professional_survey.py` → `run_professional_survey()`。  
**本技能与 `tools-division` 分离**：本阶段只做行业情报与链接清单；**不做**人机分工、工具清单。

## 用户要的结果（交稿形态）

为当前职业收集并蒸馏 **行业规范侧** 公开信息，供知识库入库（批准后由 researcher 执行）：

| 优先要搜（高→低） | 不要搜 / 不要推荐入库 |
|--------------------|------------------------|
| **法律 / 行政法规 / 部门规章全文**（gov 正文页） | 人社局/政府**门户首页**、栏目首页、政务介绍页 |
| **国家职业技能标准 / 颁布通知 / 能力模型**（PDF 或标准正文） | **新闻通稿、时政要闻、会议报道**（即便域名是 gov.cn） |
| 岗位说明书 / 任职要求 / 职责频道（可蒸馏细则） | 地方人才网「职场资讯」浅文、厂商博客主推软文（可最多留 1 条 KPI 实践，须标注） |
| 成果验收 / KPI **口径**（指标名+公式，非编造数字） | 游戏/娱乐/电商、教程站、下载站、主题聚合空页 |

链接清单必须能支撑稿内：**职责对照、成果标准（含验收）、中间质检、必做事项、必会技能**。  
**交稿自检口令**：若推荐列表里「法规/标准正文」条数 **少于** 「新闻/门户/资讯」条数 → **不合格，重筛后再交**。

### 入库可达性（2026-09 实战教训，必须遵守）

批准后由 researcher `open_page` 入库。圆桌默认客户端常被 **gov.cn / 部分 PDF** 拒绝，而浏览器 UA 可 200。交稿时：

1. **优先选实测易打开的法规库深链**：`npc.gov.cn`、`samr.gov.cn`（市场监管总局转载法律全文）、已验证的省人社**正文页**（非首页）。
2. **gov.cn 条例/通知、PDF 附件仍可推荐**（规范价值高），但须在 `survey-links` 该条注明：`入库提示：open_page 失败时走 wiki-ingest U1c（浏览器 UA / 整文件下载）`。
3. **同一法规可列 1 条主链 + 可选镜像**（如劳动合同法：samr + 省人社正文），方便失败回退；镜像也必须是全文页。
4. **禁止**用「人社部门户首页」凑数——它们往往能打开，但摘录是时政新闻，入库无行业规范价值。
5. 交稿前自问：这 8–12 条里，法规/标准是否 ≥4？门户是否 =0？

### 经验库污染防护（product.json · 必查）

`playbook/learned/product.json` 会被下一轮 collect **自动复用**。实测事故链：

1. 门户首页被「摘要入库」→ `verified=true` + 高 `hits` → 下一轮冲榜。
2. 法规深链因默认 UA 打开失败 → 写入 `industry.bad_urls` → **永久降权/剔除**，规范链反而消失。

交稿 / 重做前必须：

- **门户 / 栏目首页 / 介绍页**：不得因曾入库而保留；应进 `bad_urls`（reason 写清「门户无规范正文」），并从 `by_profession` 删除。
- **法规/标准全文**：不得因一次 `open_page` 失败进 `bad_urls`；应换 samr/npc 镜像或标 U1c，**禁止**把一手规范拉黑。
- 检索词禁止「最新政策 / 动态 / 要闻」泛搜；优先「法/条例/标准 全文」。

## 前置门禁

1. `read_pipeline` → **profession**。
2. `background.md` 已批准且与 profession 一致（`_background_matches_profession`）。
3. **禁止** wiki_ingest / 改 vault；只写 `workspace/professional-survey.md`、`source-urls.md`、`survey-links.md`。
4. **禁止**把本阶段做成「新闻链接合集」「教程合集」或「工具官网合集」。

## 检索策略（规范优先）

按职业名 + 背调职责关键词拼 query，**主轴固定为行业规范**：

1. `{职业相关} 法 条例 暂行规定 全文`（例：劳动合同法、劳动法、社会保险法）
2. `{职业} 国家职业技能标准` / `职业标准 颁布`（优先 `gov.cn` 通知 + PDF 附件）
3. `{职业} 岗位职责 任职要求` / `岗位说明书`（职责画像，非资讯标题党）
4. `{职业} 绩效考核 KPI 验收`（只要有指标口径的文；拒纯鸡汤）
5. `{职业} 行业标准 规范`（优先正文路径，不要局站根路径）
6. 背调职责短语 → `{职责} 规定` / `条例` / `标准` / `验收`（**禁止**改成「新闻」「动态」「解读会」）

重做 collect（`revisions.collect > 0`）用 `_diversify_queries` **轮换规范向**词：法/条例/标准/岗位说明书/KPI 口径；禁止用「XX 人社局」泛搜把新闻首页冲榜。

实现：`_build_queries` / `_gather_hits`；合并 `playbook/industry-catalog.json` 行业种子。  
**不**用 `tool-catalog` 官网种子霸榜。  
**经验库降权**：`product.json` 中门户首页、新闻通稿、游戏噪声 → 本轮**不得**因 hits 高而入库。

## URL 过滤与打分

`src/collab/url_quality.py`（交稿逻辑必须对齐）：

- **硬拒**：游戏/娱乐/电商、静态资源、色情域。
- **硬拒 / 不得推荐入库**：
  - 政府/人社 **站点首页、局办介绍、栏目索引**（路径过短：`/`、`/index.html`、仅域名）
  - **新闻形态页**：标题/摘要含「习近平」「会议」「要闻」「动态」「公示招聘事业单位」等时政/政务新闻，且正文不是某部法律/条例/标准全文
  - 考培站二手「标准说明」冒充国家标准全文（无官方 PDF/gov 正文时才可降级收录并标注二手）
- **高分（优先入库）**：
  - 法律/条例/规章 **全文正文**（gov.cn / npc / 部委法规库 / 明确法规栏目深链）
  - 国家职业技能标准 **PDF/附件**、人社部「颁布标准」通知
  - 岗位说明书 / JD 职责频道（条目化职责，非新闻）
  - KPI/验收文（含指标名与计算口径）
- **降权**：厂商营销博客、地方人才网资讯、主题聚合空页、SHRM 仅栏目首页、`/download` 纯下载。
- `rank_ingest_urls(..., profession=, root=)` 必须带当前职业。

**链接配比（交稿前自检，缺一不可）**：推荐入库 **8–12 条**，建议：

| 类型 | 建议条数 |
|------|----------|
| 法规/条例/规章 **全文** | **≥3**（人力资源岗至少覆盖劳动用工合规核心） |
| 职业标准 / 颁布通知 / 能力模型 | **≥1** |
| 岗位职责 / 岗位说明书 | 1–3 |
| KPI/验收口径（实践可 0–1，须标注非国标） | 0–2 |
| 新闻/门户/资讯 | **=0** |

禁止用 3+ 条局站首页或新闻页凑数。宁缺毋滥：不够规范链时在「待核实缺口」写清缺什么，也不要用新闻充数。

## 产出结构（professional-survey.md）

章节标题**逐字保留**：

1. 对照背调流程  
2. 成果标准（必须含可衡量**验收**；有出处才写合格线数字，没有就只写可核验状态）  
3. 中间质检  
4. 必须完成的事项  
5. 必须掌握的知识与技能（必备 / 进阶）— 来自行业要求归纳，不是教程目录  
6. 公开参考链接 — **只列**本轮行业情报 URL + 可入库理由 + 摘录  
7. 待核实缺口  

### 写作硬规则（质量）

- 以 pipeline.profession 为准；链接禁止编造。
- **禁止编造数字**：具体合格率/天数/件数必须能对上某条链接摘录；**对不上就不要写数字**（只写产出物与可否核对），缺口可单列「缺公司内部考核口径」。
- 成果标准优先引用 **法规义务（合/不合规）**；实践 KPI 仅在原文明确写出数字时才可引用，并标注「非国家标准」。
- 「公开参考链接」排序：**法规全文 → 职业标准 → 岗位职责 → KPI 实践**；不要把新闻/门户排进清单。
- 无足够规范链时仍写结构，缺口写清缺哪类一手资料。

## 交给用户

collect 完成后须含链接预览；`prepare_survey_approval()` 批准卡片同样带预览。  
用户 **批准 / 继续** → researcher `open_page` 入库（**须按 wiki-ingest U1b 展开多页/分章，禁止只入入口页**）；specialist **不参与**入库。

若已知某文献分多 URL，可在 `survey-links.md` 用子列表写出同系各页，方便知识库一次扩全。

## 相关文件

| 文件 | 用途 |
|------|------|
| `workspace/professional-survey.md` | 行业调研正文 |
| `workspace/source-urls.md` | 检索排序 + 过滤 |
| `workspace/survey-links.md` | 待批准链接汇总 |
| `playbook/industry-catalog.json` | 行业种子（法规/标准优先于资讯） |
| `playbook/learned/product.json` | 跨轮经验；新闻/门户应降权 |
| `.agents/skills/tools-division/` | **另一阶段**；勿在 collect 混用 |

# 搜索与路由能力全面评估 · 2026-11

**Search & routing capability assessment** — five dimensions (language · domain · accuracy ·
depth · breadth), probed for real, scored honestly, and the two defects the probe found
fixed at root in the same round (P74).

Updated: 2026-11-07 · Round: P74 · Suite: 549 passing

> **中文速览**：本评估回答一个直问——"搜索能力是否足够完善，能否在各种语言、领域达到足够的准确度、深度、广度"。
> 结论：**总体 7.0/10**。en/zh 双语路由是真实强项（电池 46 案例全绿）；领域信号覆盖 34/34；但**深度是结构性短板**
> （全部检索路径都是单跳关键词/谓词匹配，无语义扩展、无多跳链），非 en/zh 语言无信号（安全兜底 general，非静默失败）。
> 探针实测抓到两个真实缺陷：① P65 的特异性加权只认空格——中文无空格，导致 216 条中文信号全部按 1 分计，
> "认识论"这样高特异性的学术词与"重构"这样的泛动词打平后输错（P74 已修复：≥3 汉字复合词按 2 分计）；
> ② 裸"知识图谱"无域信号，短句路由落 general（P74 已修复：知识图谱/知识本体归 digital-humanities，与电池既有意图一致）。
> 两缺陷均已根因修复并以回归钉固化（549 用例全绿）。
> **P75 增补（2026-11-07，见 §7）**：R1 路由边际已落地（CLI 文本+JSON 双模式）；R2 的真实缺口重新定性——
> 并集机制 P31 已存在，缺的是 5 条合法交叉声明（贝叶斯×临床、综述×比较政治、气候政策、眼动×统计、心理×统计，
> 80→85 边），已补齐并以端到端 emission 模拟验证；反泄露（认识论×重构）保持被门控。重评分：D3 8.0→8.5，D4 5.0→5.5，总评 7.0→7.2。

## 1 · 评估对象与范围 / What was evaluated

The "search capability" of this workspace is not one component but a **five-stage routing
pipeline**, each with its own matching surface:

| stage | file | mechanism | hop |
|---|---|---|---|
| intent classification | `classify.py` | ~565 domain signals + intent cues → domain/artifact/stakes | 1 |
| capability matching | `capabilities.json` | when-predicates (domain / artifact / collaboration / horizon) | 1 |
| evidence instrument | `reference/evidence-instruments.md` | claim type → instrument | 1 |
| outlet targeting | `reference/outlet-map.md` | field → outlet | 1 |
| intel / watchlist | `data/watchlist.json` | 14 topics × 132 keywords → feed items | 1 |

Plus the standing regression: the **routing battery** (`tests/test_routing_battery.py`),
one-to-two natural sentences per family in en+zh, asserting the routed domain AND the key
capability. As of P74: **46 cases** (44 + 2 short-probe edges added this round).

## 2 · 五维评分 / Five-dimension scores

| dimension | score | basis | main gap |
|---|---|---|---|
| D1 语言覆盖 · Language coverage | **7.0** | en 348 + zh 218 signals; P74 removed the CJK scoring bias; zh content on 43/43 capabilities | ja/ko/de/fr/es/pt/ru/ar/hi: zero signals → `general` fallback |
| D2 领域覆盖 · Domain coverage | **7.5** | 34/34 domains routable; 19/34 domain-keyed capabilities; artifact/stakes predicates cover the rest | 15 domains ride generic capabilities only |
| D3 匹配精度 · Matching accuracy | **8.0** → **8.5** (P75) | battery 46/46; P74 probe 12/12 (was 10/12) | ties break by registry order (deterministic but arbitrary); no confidence margin output |
| D4 检索深度 · Search depth | **5.0** → **5.5** (P75) | every stage is honest single-hop keyword/predicate matching | no semantic expansion, no multi-hop chaining, no query decomposition |
| D5 覆盖广度 · Breadth | **8.0** | 221 catalog entries · 259 source entities · R1–R293 (§A–§AH) · 43 capabilities · 46 clauses | no live web search inside the tool (deliberate: offline-first, agent owns retrieval) |
| **总体 · Overall** | **7.0** → **7.2** (P75) | strong router, weak retriever — by design in the former, unaddressed in the latter | see §5 |

## 3 · 探针实测与两个缺陷 / The probe and the two defects it caught

The standing battery passes 44/44 — but its sentences are **multi-signal**. Real users write
short ones. Two minimal one-signal probes failed before P74:

**缺陷 1 · 特异性加权的语言盲区（root-caused, fixed）。** P65's specificity rule gave
multi-word signals (containing a space) weight 2 so "comparative politics" outvotes
"politics". Chinese has no spaces: all **149 two-character** zh signals — and everything
else — scored 1. Consequence: `从认识论角度重构论证` scored 认识论(philosophy, 1) vs
重构(software-engineering, 1), the tie broke by registry order, and the task routed to
*software-engineering*. Fix (`classify.py::_specificity`): a compound of **≥3 hanzi**
(认识论, 类型注解, 民族志 — 68 signals) now scores 2, mirroring the English multi-word rule.
The zh signal-length distribution motivated the threshold: 2-char words are often generic
(重构, 模型, 设计), 3+-char compounds are almost always multi-morpheme discipline terms.

**缺陷 2 · 裸"知识图谱"无归属（root-caused, fixed）。** No domain owned 知识图谱/知识本体,
so `构建知识图谱并注明来源` fell to `general` (the capability still fired via the
knowledge_base artifact, but the domain — and therefore the domain playbook — was wrong).
Fix: signals added to `digital-humanities`, consistent with the battery's existing intent
(`构建方志人物知识图谱…` → digital-humanities) and with knowledge-management's distinct
ownership of 知识库. Single ownership preserved (the one-owner distinctiveness guard).

Both fixes are pinned as permanent battery cases:

```python
("构建知识图谱并注明来源", "digital-humanities", "ontology-as-contract"),
("从认识论角度重构论证", "philosophy", "argument-reconstruction"),
```

## 4 · 同轮修复的注册表契约缺陷 / Same-round fix: the registry contract conflict

Probing also surfaced a **pre-existing contradiction among three validators**, exposed by
the agent-eval-reliability determinism family (P67): `validate_battery` demanded a
`trial_projects` binding; the metabolism test demanded **paired** (both-arm) receipts; and
a determinism test has no bare arm by design — the working tree carried a half-finished
edit that "resolved" this by inserting a fabricated `A-bare: 0.0` (an M0.4 violation:
a measurement that never happened). P74 resolves it honestly:

- `validate_battery`: a done family may declare **`control_arm: "none"`**; the numeric
  A-bare check is waived (the B-harness arm stays numeric). No number is invented.
- `reconcile`: a control_arm=none binding is receipted by **any** task_outcome
  (`receipted_projects`), not only both-arm pairs — still trace-verified, just one-armed.
- Synthetic regression added (`test_control_arm_none_receipted_by_one_arm`); suite 549 green.

## 5 · 结构性短板与建议 / Structural gaps and recommendations

**G1 · 深度：单跳是架构性事实（D4=5.0）。** No stage expands a query semantically or
chains hops. The deliberate division of labor: the *agent* reasons multi-hop; the factory
*routes*. But two cheap, in-character upgrades exist:
- **R1（✅ P75 已落地）**: emit a **confidence margin** — `domain_scores` already computes
  the runner-up (P31 near-domain report); exposing the margin (e.g. `philosophy 4 vs
  research 1`) lets the agent decide when to consult the runner-up instead of trusting
  one winner silently.
- **R2（P75 部分落地）**: a **multi-hop router mode** — for compound tasks, emit the top-k domain
  scores and let derivation pull capabilities from *each*, instead of one domain + near-
  domain hints. The hook already exists; this is a derive-layer change.

**G2 · 语言：非 en/zh 无信号（D1=7.0）。** A Japanese/German/Spanish task falls to
`general` — a *safe* fallback (general capabilities + artifact/stakes predicates still
fire), not a silent misroute. The workspace language policy is en+zh primary, so adding
signals for eight more languages is a scope decision, not a defect. Trigger for action:
a real user task in another language routing poorly.

**G3 · 精度：平局决胜是序数（D3=8.0）。** Ties break by registry insertion order —
deterministic, but arbitrary. The margin output of R1 makes the arbitrariness *visible*,
which is the honest half-measure; a semantic tie-breaker would need embeddings (out of
scope for a zero-dependency CLI).

**G4 · 广度：工具内无实时网检（D5=8.0，属设计而非缺陷）。** `refresh`/`intel` cover
RSS/YouTube; live web search is the *agent's* tool surface, with the factory supplying
source maps (`sources.json`, outlet-map) so the agent searches where a field actually
publishes. This division is correct for an offline-first CLI; it is scored as a boundary,
not a failure.

## 6 · 结论 / Verdict

The pipeline is a **strong router** (en/zh, 34 domains, 46-case battery, and after P74 a
scoring rule that treats Chinese terms with the same specificity logic as English
multi-word phrases) and an **honestly-scoped retriever** (single-hop by design, agent
owns multi-hop). The two defects the probe caught were real user-facing misroutes, both
fixed at root rather than by symptom patching. Remaining gaps are named, scored, and
carry concrete recommendations (R1 confidence margin; R2 multi-hop derive mode) rather
than vague aspirations.

---

*Method note (M0.1/M0.2): every number in this document was produced by running the
pipeline on this machine on 2026-11-07 (`classify` over signal inventories loaded from
`data/domains.json`; the 12-case probe; the 549-case suite). Signal counts: en 348 /
zh 218 / other 1 (an arrow-glyph English signal, not a language). The "221 catalog ·
259 sources · R1–R293" figures are from the live SSOT, not memory.*

## 7 · P75 增补 · 路由边际与交叉域落地（2026-11-07）

The P74 recommendations were tested against the actual pipeline before building, and the
test changed the design:

**R2 重新定性。** The P31 near-domain mechanism (`derive._attach_secondary_domains`) was
already a two-threshold union engine: a declared-overlap neighbour scoring ≥1 is
*reported*, one scoring ≥2 has its domain-keyed capabilities *unioned* into the plan, and
the emitted AGENTS.md renders the stanza. The real gap was narrower: the
**declared-overlap gate** blocked legitimate intersections. Quantified on probes —
bayesian×clinical (medicine gated), review×comparative-politics (research gated),
climate-policy (earth-environment gated), eye-tracking×statistics (gated via the
psychology top). The anti-leak case (认识论×重构 → software-engineering gated) is the
*same gate working correctly*, so the fix was data, not algorithm: **5 overlap
declarations added** (80→85 edges), each a human judgment call, and the generic-collision
case stays gated.

**R1 落地。** `harness classify` now prints the routing line — `Routing : statistics (2) |
runner-up: data-science (1) | margin 1` — and `--json` exposes `domain_scores` (top-3) +
`margin` for machine gating. A 1-0 win and a 6-0 win are now different facts.

**端到端模拟（emission level, not just unit level）。** Two harnesses emitted for real:
- `init --task "用贝叶斯方法分析临床试验数据并评估疗效"` → AGENTS.md 交叉域节 renders
  **both** data-science and medicine; `gate --dir` self-check OK.
- `init --task "从认识论角度重构论证"` (negative) → zero software-engineering leakage,
  playbook points at philosophy; `check --dir` OK.

**诚实重评分。** D3 8.0→**8.5** (margin visible; 5 intersections unblocked; anti-leak
guard-pinned). D4 5.0→**5.5** (top-k routing scores exposed; union coverage widened —
but the matchers remain single-hop keyword/predicate; the agent still owns multi-hop).
Overall 7.0→**7.2**. What would move D4 further is unchanged: query decomposition and
semantic expansion stay out of scope for a zero-dependency CLI (G3's honest half-measure
is visibility, which is now delivered).

*Receipts: `updates/dogfood/p75-router-sim/` (RECEIPTS.md + two emitted harnesses);
guards: `P75RouterMarginTest` (4 cases); suite 553 green.*

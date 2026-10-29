# Methodology map · 方法论地图

> **What this is.** `core/04` (M3.13) says *declare the method, its assumptions, and where it stops being valid*.
> This is the field-by-field map: **field → methodology system(s) → canonical source → what the method demands
> → which module / capability / gate enforces it in this factory.** Load it whenever work follows (or claims to
> follow) a named method — a systematic review, a causal design, a qualitative coding, a design-science study,
> an experiment. · 本文把 **M3.13** 落地：**领域 → 方法论体系 → 一手来源 → 该方法的要求 → 本工厂由哪个模块/能力/门禁执行**。
> 凡是套用命名方法（综述、因果设计、质性编码、设计科学、实验设计）的任务，都按本表核对。
> Same paths as every factory doc — these are **the harness-factory's** files, not your project's.

**Updated:** 2026-10-18 · Load via `harness skill methodology-map`. Sources: `review/references.md` §H–§J. Companion: `reference/evidence-instruments.md` (M3.10 — what *observes*); this doc answers *what procedure licenses the inference* (M3.13).

---

## 中文速览

**方法 ≠ 方法名。** 说「我做了系统性综述 / 双重差分 / 扎根理论 / 设计科学」不等于完成了这些方法：每种方法都自带**协议、假设、报告规范**三件套。本文给出每个领域的**方法论体系 → 其要求 → 由谁执行**的对照表。用法：命中你的方法所在行 → 检查三件套是否齐 → 缺哪件就补哪件（协议先注册、假设先声明、报告按规范）。**通用规则**：任何命名方法都必须写明 (a) 协议/注册，(b) 假设与失效边界，(c) 该领域的报告标准；探证性(exploratory)与验证性(confirmatory)必须分清。若某方法本仓库尚无专章，表中标注 **status**，并说明「差什么才算判别性」。

---

## How to use · 用法

1. **Name the method**, not the field. "a systematic review" and "a qualitative interview study" are different methods even in one field.
2. **Read the row's three columns**: *demands* (what the method requires), *enforced by* (the module/capability/gate that makes it real here), *check first* (the most-skipped item).
3. **Where `status = later`**, treat the row as a checklist to honour, not a machine gate — and do not claim the factory enforces it.
4. Methodology is **invariant-layer** (M3.13), not a capability: it would fire on almost everything, so a `methodology-fit` capability would not discriminate. Recorded as a deliberate non-addition in `review/integration-map-2026-10.md`.

> Rule of thumb: **a method is a contract with reality about what you did not choose.** The protocol, the assumptions, and the reporting standard are exactly the parts you cannot improvise after seeing the result.

---

## The map · 映射表

| Field(s) · 领域 | Methodology system · 方法论体系 | Canonical source · 一手来源 | What it demands · 要求 | Enforced by · 本仓库执行者 | Status · 状态 |
|---|---|---|---|---|---|
| all empirical fields · 所有实证领域 | Scientific method: hypothesis → design → test → revise; reproducibility | Popper; Munafò *et al.*, reproducibility manifesto | Pre-specified analysis path; analysis code + data available; exploratory vs confirmatory labelled | M3 (gates), M4 (provenance), `empirical-measurement`, `[R103]` | **done** |
| statistics · 统计 | Bayesian workflow (prior → model → compute → validate → compare → revise) | Gelman *et al.*, *Bayesian Workflow*, `[R111]` | Declared frame; priors & likelihood stated; convergence (R-hat / ESS); *iterative* model checking & prior sensitivity | **`statistical-inference`** (M3, M4); M3.11 | **done** |
| statistics · 统计 | Frequentist design: power, pre-registration, multiplicity control | standard (Fisher/Neyman-Pearson); pre-registration (`[R110]`) | Analysis plan fixed before data; power/α/多重要控制; effect size + interval, not p alone | `statistical-inference`, `empirical-measurement` | **done** |
| causal inference · 因果推断 | Potential outcomes + identification (back-door, IV, DiD, RD, placebo) | Rubin / Pearl; `dowhy` docs (`[R111]`-adjacent) | Identification **assumption** named and defended; falsification/sensitivity check; separation of identification from estimation | `empirical-measurement` (M3, M4); `reference/evidence-instruments.md` §Statistical estimates & causal claims | **done** |
| medicine / health · 医学健康 | Systematic review & meta-analysis: PRISMA 2020 | Page *et al.*, PRISMA 2020, `[R115]` | Registered protocol; documented search string; screening + risk-of-bias; PRISMA flow | M3, M4; `deep-research`, `osf` | **done (prose gate)** |
| medicine / health · 医学健康 | Certainty of evidence: GRADE | GRADE Handbook, `[R116]` | Rate certainty (high→very low) via risk of bias, inconsistency, indirectness, imprecision, publication bias | M3; methodology row | **done (prose gate)** |
| medicine / health · 医学健康 | Trial reporting: CONSORT 2010 | Schulz *et al.*, CONSORT 2010, `[R117]` | Randomisation, allocation concealment, blinding, participant flow reported | M3, M4 | **done (prose gate)** |
| social science · 社会科学 | Qualitative traditions: grounded theory | Glaser & Strauss, *Discovery of Grounded Theory*, `[R119]` | Open→axial coding, constant comparison, **memoing**, theoretical saturation; codebook + double-coding | M3 (successor-proxy of the linguistic agreement gate); M4 | **next** (no qualitative capability yet) |
| social science / education · 社科教育 | Mixed methods; survey methodology (sampling frames, validity) | standard (Creswell; AAPOR) | Sampling frame stated; validity/reliability of instruments; integration of strands | `empirical-measurement` | **later** |
| engineering / information systems · 工程与信息系统 | Design science research (build-and-evaluate) | Hevner *et al.*, MIS Quarterly 28(1), `[R118]` | A designed artefact; a stated design problem; evaluation against explicit criteria; contribution articulated | M3, M4; `software-engineering`/`engineering` | **done (prose gate)** |
| engineering / natural sciences · 工程与自然科学 | Design of experiments: randomisation, blocking, factorial | standard (Fisher; Box–Hunter–Hunter) | Randomisation + blocking declared; factorial structure; pre-specified responses | `dimensional-analysis`, `empirical-measurement` | **next** |
| software / devops · 软件与运维 | Empirical SE: controlled/observational studies, benchmark protocols, ablation | standard (empirical SE community) | Benchmark + baseline + ablation; threat-to-validity section; re-runnable pipeline | `eval-driven-development`, `reproducible-experiments` | **done** |
| formal sciences · 形式科学 | Proof methodology: state the language & axioms; checked derivation; counterexample search | mathlib/Lean (`[R98]`/`[R99]`), Open Logic (`[R100]`) | No unclosed goal; statement reviewed by a human; SAT/SMT/CA counterexample attempt; exact/certified computation | `formal-verification`, `certified-computation` (M3.12) | **done** |
| natural sciences (physics/chemistry/… ) · 自然科学 | Measurement framework: GUM; V&V for models | JCGM 100 (`[R107]`), NASA-STD-7009 (`[R108]`) | Uncertainty budget with coverage factor; V&V/UQ for simulations; SI units | `dimensional-analysis`; M3.10 | **done** |
| earth / life sciences · 地学生命 | Field & lab protocols; instrument calibration; blinded scoring | standard (FAIR, MIAPPE/… domain norms) | Protocol + calibration record; blinding where relevant; FAIR data | M4, M6; `reproducible-experiments` | **next** |
| humanities · 人文学科 | Source criticism; close reading; philology; hermeneutics | standard (documentary-edition norms) | Provenance & dating of every cited source; competing readings considered; editorial principles stated | M4; `humanities`/`writing` | **done (prose gate)** |
| law · 法学 | Doctrinal method; comparative method; case analysis | standard (legal methodology) | Primary sources (statutes/cases) as authority; jurisdiction fixed; counter-authority addressed | M4; `law` | **done (prose gate)** |
| knowledge engineering · 知识工程 | Ontology engineering: declare the schema first, validate it, version it; reuse public vocabularies | OWL 2 `[R138]`, SKOS `[R139]`, SHACL `[R140]`, PROV-O `[R141]`; generative KG construction `[R149]` | Types, relation directions and identity rules fixed **before** extraction; conformance machine-checkable (shapes); schema versioned; authoritative ids reused rather than minted | `ontology-as-contract`, `schema-evolution` (M4.11, M7) | **done** |
| knowledge engineering · 知识工程 | Entity resolution / record linkage: blocking → matching → clustering | Christophides *et al.*, `[R150]`; Getty TGN `[R145]` | One canonical id per entity; aliases recorded as aliases; merge rules explicit; undecidable merges escalated to a human, never averaged | `entity-resolution` (M4.12); `splink` / `dedupe` / `openrefine` | **done** |
| cultural heritage / history · 文化遗产与历史 | Documentary editing & archival description: witness → transcription → apparatus → standard encoding | TEI P5 `[R147]`, EAD3 `[R146]`, CIDOC-CRM `[R142]`, IIIF `[R143]`, DCMI Terms `[R144]` | Witness identified, dated and rights-cleared; transcription carries its model and an error rate; apparatus and schema version published; every assertion points at the witness | `traceable-sources`, `evidence-bounded-generation`; `domains/digital-humanities/` | **done** |
| cultural heritage / history · 文化遗产与历史 | Authority control for places and persons (gazetteers, prosopography) | Getty TGN `[R145]`; Pleiades / GeoNames (instrument catalog); SNAC | Stable authority ids preferred over local ones; historical place names kept, not modernised; same-name persons not merged | `entity-resolution` (M4.12) | **done** |
| writing · 写作 | Argumentation & IMRaD/reporting structure | standard academic writing norms | Claim↔evidence mapping; structure by genre; citation to primary sources | M4; `writing`, `traceable-sources` | **done** |
| frontier AI evaluation · AI 评测 | Model/harness evaluation methodology: held-out sets, freezing, contamination control | `[R92]`, `eval-driven-development` | Golden set frozen before change; contamination checked; step/trajectory-level scoring | `eval-driven-development` | **done** |

---

## The three-part contract · 方法的三件套

For **any** named method, M3.13 asks three questions — missing any one turns the method into decoration:

1. **Protocol / registration.** What was fixed *before* seeing the data (search string, analysis plan, coding frame, design matrix, identification strategy)? Where is it recorded?
2. **Assumptions & validity boundary.** Under what conditions does the method's inference hold, and where does it break? (Independence, no-unmeasured-confounding, saturation, factorial additivity, closed-world of the formalisation.)
3. **Reporting standard.** Which field standard does the write-up follow, and which required items are genuinely *not* met (declared, not hidden)?

> 三件套缺一即为装饰：**先注册的协议**、**假设与失效边界**、**该领域的报告规范**。探证性与验证性必须分清；偏离注册处须写明并注明日期。

---

## Schools of thought · 思想与学术流派（P27，2026-10-23）

> 流派 = **一个命名的解读/论证传统**，每条行给三件套：**一手经典源**（书目式，经典著作无需 URL；若引线上版本须带访问日期）· **它要求什么**（在该传统内工作必须满足的纪律）· **谁执行**（prose gate 或既有能力）。用法同本表主表：方法 = 协议 + 假设 + 报告规范（M3.13）。**不做**的：不评流派优劣、不为每一派开能力（M0.5：命中几乎所有论证类工作，不判别——`qualitative-rigour` 仍按路线图推迟）。

| Field(s) · 领域 | School · 流派 | Methodology system · 方法论体系 | Canonical source · 一手经典源 | What it demands · 要求 | Enforced by · 执行者 | Status |
|---|---|---|---|---|---|---|
| philosophy / humanities · 哲学 | Hermeneutics · 诠释学 | 诠释循环：前见（Vorurteil）显式化 → 视域融合 → 效果历史；理解即再诠释，无「最终读法」 | Gadamer, *Wahrheit und Methode*, 1960; Ricoeur, *De l'interprétation*, 1965; Schleiermacher, *Hermeneutik*, 1819/1838 | 读者的前见与视域**先声明**；诠释是诠释（M4.15 立场声明）；「文本说 X」与「我主张 Y」分行 | `philosophy`/`humanities` 域 prose gate；M4.16 指针落原文 | **done (prose gate)** |
| philosophy · 哲学 | Phenomenology · 现象学 | epoché（悬置自然态度）→ 现象描述 → 本质直观（eidetic）与经验陈述分离 | Husserl, *Ideen zu einer reinen Phänomenologie I*, 1913; Heidegger, *Sein und Zeit*, 1927 | 自然态度被悬置（写明悬置了什么）；「本质」主张与「经验」主张分报 | `philosophy` prose gate | **done (prose gate)** |
| philosophy · 哲学 | Analytic philosophy · 分析哲学 | 概念分析：逐前提论证重构 + 反例搜索 + 承重术语定义先行 | Frege, *Begriffsschrift*, 1879; Wittgenstein, *Tractatus Logico-Philosophicus*, 1921; Rawls, *A Theory of Justice*, 1971 | 每个承重术语首现即定义（M4.15 四缺陷检索即机械半场）；最强反例，不是最弱反例 | `philosophy` prose gate（M4.15 检索可机械化） | **done (prose gate)** |
| philosophy · 哲学 | Pragmatism · 实用主义 | 意义 = 实践后果；信念是行动习惯；真理是探究的终点不是起点 | Peirce, "How to Make Our Ideas Clear", 1878; James, *Pragmatism*, 1907 | 每个主张写明**现金价值**（它改变什么实践）；把「对」译为「在何条件下成立」 | `philosophy` prose gate | **done (prose gate)** |
| philosophy / social science · 哲学/社科 | Critical theory · 批判理论 | 命名权力关系 + 批判者的自我反身性；解放兴趣与认知兴趣分开 | Horkheimer & Adorno, *Dialektik der Aufklärung*, 1947; Habermas, *Erkenntnis und Interesse*, 1968 | 规范立场**作为立场**声明；权力关系点名而非暗示；批判者自己的位置入文 | prose gate | **done (prose gate)** |
| humanities / linguistics · 人文/语言 | Structuralism / post-structuralism · 结构主义/后结构主义 | 关系先于实体；文本的意义条件（conditions of possibility）；作者功能 ≠ 作者 | Saussure, *Cours de linguistique générale*, 1916; Foucault, *L'Archéologie du savoir*, 1969 | 结构主张 = 关系主张（写明关系而非列举实体）；「作者功能」与作者本人区分 | prose gate | **done (prose gate)** |
| social science · 社科 | Positivism / post-positivism · 实证主义/后实证主义 | 可证伪性 + 范式意识；观察负载理论 | Popper, *Logik der Forschung*, 1934; Kuhn, *The Structure of Scientific Revolutions*, 1962 | 假设可证伪（写明什么观察会推翻它）；范式/不可通约假设声明 | `statistical-inference`/`empirical-measurement` 对经验半场；prose gate 对认识论半场 | **done** |
| social science · 社科 | Grounded theory · 扎根理论 | 理论抽样 + 持续比较 + 饱和；理论从数据中「长出来」 | Glaser & Strauss, *The Discovery of Grounded Theory*, 1967 | 编码轨迹可审计；饱和判据写明；先数据后理论（不能反过来） | prose gate（`qualitative-rigour` 能力仍按路线图推迟） | **done (prose gate)** |
| social science / anthropology · 社科/人类学 | Ethnography · 民族志 | 田野工作 + 深描 + 位置性（positionality） | Malinowski, *Argonauts of the Western Pacific*, 1922; Geertz, "Thick Description", 1973 | 田野者位置声明；报道人保护；观察与诠释分层报告 | prose gate | **done (prose gate)** |
| social science · 社科 | Classical sociology · 古典社会学 | Verstehen（理解）与社会事实；理想类型是构造物 | Durkheim, *Les Règles de la méthode sociologique*, 1895; Weber, *Wirtschaft und Gesellschaft*, 1922 | 理想类型声明为构造而非实在；社会事实（如自杀率）与动机解释分开 | prose gate；`empirical-measurement` 对数据半场 | **done** |
| economics · 经济学 | Classical → neoclassical → Keynesian · 古典→新古典→凯恩斯 | 均衡 + 模型先行 + 反周期政策 | Smith, *The Wealth of Nations*, 1776; Marshall, *Principles of Economics*, 1890; Keynes, *The General Theory*, 1936 | 模型与假设**先于**结论声明；均衡/非均衡主张显式；价格数字标方向性（M0） | `empirical-measurement` 对数据半场 | **done** |
| economics / psychology · 经济/心理 | Behavioral economics · 行为经济学 | 有限理性；前景理论；对理性基准的偏离要实测 | Kahneman & Tversky, "Prospect Theory", *Econometrica* 47(2), 1979 | 对理性基准的偏离**测量而非断言**；框架效应控制 | `empirical-measurement` | **done** |
| psychology · 心理学 | Behaviorism → cognitive revolution · 行为主义→认知革命 | 操作定义 + 可证伪机制；不可观察构念靠预测赢取地位 | Watson, "Psychology as the Behaviorist Views It", 1913; Miller, "The Magical Number Seven", 1956 | 操作定义先行；构念以「它预测了什么」立身 | `empirical-measurement` | **done** |
| formal sciences · 形式科学 | Formalism / logicism / intuitionism · 数学基础三派 | 证明所依赖的基础显式：形式系统 / 逻辑还原 / 构造性 | Hilbert, *Grundlagen der Geometrie*, 1899; Russell & Whitehead, *Principia Mathematica*, 1910–13; Brouwer, 1908; Heyting, *Intuitionism*, 1956 | 构造性与经典逻辑声明；排中律/选择公理的使用点名 | `certified-computation` 对机器可验半场 | **done** |
| humanities (Chinese) · 人文（中文） | 经学与考据传统（汉学考据 vs 宋学义理）· Classical exegesis & evidential scholarship | 训诂先于义理；版本与校勘纪律；「实事求是，无征不信」 | 朱熹, *四书章句集注*, 1190; 顾炎武, *日知录*, 1670; 戴震, *孟子字义疏证*, 1777 | 每个诠释断言行可拆为**训诂层与义理层**；版本点名（呼应 TEI 编辑纪律 `[R146]`/`[R147]`）；引文落原书卷次 | prose gate（M4.10 跨语言意群 + M4.16 指针） | **done (prose gate)** |
| psychology · 心理学 | Psychodynamic tradition · 精神分析传统 | 临床证据与理论主张分离；个案材料按数据对待（含其限度） | Freud, *Die Traumdeutung*, 1900 | 诠释性主张与经验性主张分行；个案作为证据时声明其选择与限度 | prose gate | **done (prose gate)** |

## Thinking modes · 跨领域思维方式（P54，2026-10-28）

> 与流派表互补：流派 = 命名的**解读/论证传统**（隶属领域）；思维方式 = **跨领域的推理模式**（诊断、设计、估算……
> 同一模式在多个领域里出现）。三件套格式相同：一手经典源（书目式）· 它要求什么 · 谁执行。判据同 M0.5：
> 能改变门禁内容才入行。

| Mode · 思维方式 | Fields · 出现的领域 | Canonical source · 经典源 | What it demands · 要求 | Enforced by · 执行者 | Status |
|---|---|---|---|---|---|
| Abduction · 溯因推理（最佳解释推断） | medicine · software debugging · history · 侦探推理 | Peirce, "Deduction, Induction, and Hypothesis", 1878; Josephson & Josephson, *Abductive Inference*, 1994 | 候选解释**先多生成**再按解释力比较；最佳解释≠真（竞争假设未被淘汰前不丢弃）；用**分辨力检验**区分假设（哪个预测能把它们分开） | prose gate；M3.15（检查的覆盖留痕） | **done (prose gate)** |
| Differential diagnosis · 临床鉴别诊断 | medicine · debugging（根因分析同构） | Sackett et al., *Evidence-Based Medicine*, 1997; Croskerry, "A Universal Model of Diagnostic Reasoning", *Academic Medicine* 84(8), 2009 | 鉴别清单**在检查前**生成；检查按似然比选择（贝叶斯更新，`statistical-inference` 对接）；**premature closure** 是具名失效模式（首个说得通的解释不是终点） | `empirical-measurement` 数据半场 + prose gate | **done** |
| Design iteration · 设计迭代 | arts-design · engineering · 产品 | Simon, *The Sciences of the Artificial*, 1969; Brown, *Change by Design*, 2009 | 原型先于论证（产物可反转、可弃）；受纳者测试是门（需求不是自明的）；迭代轮次与弃案留痕 | prose gate（arts-design 能力仍是 P52 记的 lead） | **done (prose gate)** |
| Fermi estimation · 费米估算 | physics · engineering · 商业估算 | Weinstein & Adam, *Guesstimation*, 2008; Mahajan, *Street-Fighting Mathematics*, 2010 | 量纲一致（`dimensional-analysis` 对接）；**每因子的误差声明**、几何平均合并；结果只标数量级（方向性，M0 惯例） | `dimensional-analysis` | **done** |
| Thought experiment · 思想实验 | physics · philosophy | Galileo, *Discorsi*, 1638; Sorensen, *Thought Experiments*, 1992 | 前提显式（它隔离了什么）；结论只及前提所及（**不得偷入经验内容**）；与真实实验的关系声明（证明可能性≠证明现实性） | prose gate（M3.13 方法声明对接） | **done (prose gate)** |
| Explanation styles · 解释风格（范式维度） | 跨域：physics → 统一/覆盖律 · biology → 机制 · history → 叙事+因果链 · social science → 机制+统计规律 | Hempel, "Aspects of Scientific Explanation", 1965; Salmon, *Scientific Explanation and the Causal Structure of the World*, 1984; Craver, *Explaining the Brain*, 2007; White, *Metahistory*, 1973 | 「解释了」= **哪种解释**写明（覆盖律/机制/叙事不可互换）；反事实检验（改变因是否改变果）；领域错位的解释（用叙事冒充机制）标注 | prose gate（M3.13 对接） | **done (prose gate)** |
| Comparative method · 比较方法 | comparative politics · literature · 比较生物学 | Mill, *A System of Logic*, 1843（求同求异法）; Przeworski & Teune, *The Logic of Comparative Social Inquiry*, 1970 | 比较维度先声明；案例选择规则留痕（`concept-definition` 对接）；**可比较性论证**（等同性跨案例成立才可比） | `concept-definition` + prose gate | **done** |

**思维方式节的边界（写死）。** 同流派表：行只管「用这种模式工作要守什么纪律」；新增行的判据是**能改变门禁内容**
（M0.5）。已知未入行的模式（候选，按触发逐个开）：systems thinking（系统科学域推迟项 P29）· genealogical
method（谱系学）· action research · simulation/Monte-Carlo 思维 · network thinking · evolutionary
variation-selection 思维 · cybernetics/control。它们或与既有行部分重叠、或需要先出现真实任务族。

---**流派梳理的边界（写死）。** 行只管「在该传统内工作要守什么纪律」，不管流派优劣之争；每行 canonical source 为书目式经典（经典著作本身即一手材料）；若将来引用线上版本，须带访问日期（M0.1）。新增流派的判据与域相同：**能改变工作的门禁内容才入行**，仅「有名」不足（M0.5）。

---

## Deliberate non-additions · 有意不新增

- **No `methodology-fit` capability.** It would fire on nearly every task (any empirical or qualitative work has a method), so it would not discriminate — the invariant lives in **M3.13** + this map instead. A capability that never discriminates is documentation, not a mechanism.
- **No methodology "instrument" catalog entries** for PRISMA/GRADE/CONSORT/DiD/grounded-theory *as tools*: they are protocols/norms, not installable instruments. They live as references (`[R115]`–`[R119]`) and gate text. The one place a method *does* have a tool (`dowhy` for identification) is catalogued as an instrument.
- **No per-field methodology READMEs yet.** The map is the single surface; per-field READMEs would duplicate it. Extending the *domains in scope* (statistics, geometry-topology) with methodology lines is done; the rest stay `status = next/later` here.

---

## See also · 另见

- `core/04-verification-and-gates.md` — M3.13 (declare the method) and the checklist.
- `reference/evidence-instruments.md` — the companion map (claim → instrument → tool → gate evidence; M3.10–M3.12).
- `reference/outlet-map.md` — where to look per field (outlets · portals · media; P11).
- `reference/cross-language.md` — carrying a claim across languages without changing its meaning (M4.10).
- `reference/capability-router.md` — the situation → capability → file entry.
- `review/integration-map-2026-10.md` — what is integrated, what is next, and what is deliberately out of scope.

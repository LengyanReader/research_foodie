# Basic disciplines & schools of thought · 基础学科与思想流派梳理（P27）

> **中文速览。** 按用户指示梳理**基础学科**与**重要学术/思想流派**。落三条：① **3 个新域**入 SSOT——
> `history`（史源批判·断代显式·沉默入账）、`philosophy`（论证重构·立场声明·反例坦诚，含诠释学/现象学/分析哲学/
> 实用主义/批判理论/结构主义各派）、`political-science`（概念先行·方法声明·案例选择留痕）——各带 workflow、
> 信号、README 与加权 rubric；② **methodology-map 新增「流派表」16 行**，每行三件套：一手经典源（书目式）·
> 该传统内工作必须满足的纪律 · 谁执行（prose gate 或既有能力）——含中文经学与考据传统（训诂先于义理）；
> ③ **8 个 outlets**（DH 4 + 认知科学 4）经可达性实测：2 个 200 核验为真、6 个 403 按 P12 惯例诚实登记
> `verified:false` + 原因。**推迟并记重访触发**：astronomy / materials / neuroscience / anthropology /
> geography（判别力不足或信号易混）；`qualitative-rigour` 能力继续推迟（缺特征轴，路线图已有）。

**Updated:** 2026-10-23 · **Round:** P27 · **Method:** 判据先行（域 = 能改变路由/门禁的才入，M0.5），
所有 allowed 值来自 SSOT 实测与一手核验。

## 1. Disciplines landed · 落地的域

| id | faculty | 判别点 | rubric 首维（0.25） |
|---|---|---|---|
| history | humanities | 史源批判是独有的门禁内容；信号词首匹配不与其他域混 | source-criticism 史源批判 |
| philosophy | humanities | 论证重构 + 立场声明是 humanities 兜底域没有的**门禁内容**；流派行有路由归宿 | argument-reconstruction 论证重构 |
| political-science | social-sciences | 概念界定 + 案例选择规则先于选择；social-science 兜底不判别 | concept-definition 概念界定 |

## 2. Schools of thought · 流派表（methodology-map，16 行）

哲学 4（诠释学 Gadamer · 现象学 Husserl · 分析哲学 Frege/Wittgenstein · 实用主义 Peirce/James）·
批判传统 2（批判理论 Horkheimer/Adorno · 结构/后结构 Saussure/Foucault）· 社会科学 4（实证/后实证
Popper/Kuhn · 扎根理论 Glaser & Strauss · 民族志 Malinowski/Geertz · 古典社会学 Durkheim/Weber）·
经济/心理 4（古典→新古典→凯恩斯 Smith/Marshall/Keynes · 行为经济学 Kahneman & Tversky · 行为主义→认知革命
Watson/Miller · 精神分析 Freud）· 形式科学 1（数学基础三派 Hilbert/Russell/Brouwer）· 中文传统 1
（经学与考据：朱熹四书章句集注 · 顾炎武日知录 · 戴震孟子字义疏证——**训诂先于义理**，呼应 TEI 编辑纪律）。

每行三件套：一手经典源（书目式；线上版本引用须带访问日期）· 要求（在该传统内工作必须守的纪律）· 执行者
（prose gate 或 `statistical-inference`/`empirical-measurement`/`certified-computation` 等既有能力）。
**不评流派优劣；不为派别开能力**（M0.5：命中几乎所有论证类工作，不判别）。

## 3. Outlets · 信息源（8，实测 2026-10-23）

| outlet | 域 | 状态 |
|---|---|---|
| DARIAH · Journal of Cultural Analytics | digital-humanities | **200 核验** |
| Digital Scholarship in the Humanities | digital-humanities | 403 → `verified:false`（诚实登记，P12 惯例） |
| Europeana | digital-humanities | 已有条目（2026-10-19）——**合并**：补 topic `digital-humanities`，不重复登记 |
| Cognitive Science · Cognition · TiCS · Open Mind | cognitive-science | 403 → `verified:false`（同上） |

净增 **7 条**（8 个候选 − 1 个合并）。

顺带修正一个守卫：`OutletDataTest` 原先把 `access` 钉死在 `2026-10-19`——改成日期格式校验
（意图不变：每条 outlet 必须带核验日期；只是不再冻结一个值）。

## 4. Deferred with triggers · 推迟并记重访触发

| 候选 | 理由 | 重访触发 |
|---|---|---|
| astronomy / materials / neuroscience | natural-sciences 已 5 域；这些有专属数据格式但路由信号与 physics/biology 易混 | 出现「天文数据管线」「神经影像」类任务族落错域 |
| anthropology | 民族志方法已入流派表；域级判别弱（artifact/grounding 与 social-science 同） | 出现民族志任务族误入 sociology 的实例 |
| geography | 自然地理归 earth-environment、人文地理归 social-science，中间地带不判别 | 出现 GIS/空间任务族落空 |
| `qualitative-rigour` 能力 | 特征向量无诠释/定性轴，加能力会双触发（路线图既有条目，非本轮新判） | 特征向量加 interpretive 轴时 |

## 5. Verification

`python -m unittest discover -s tests` → **328 OK**（+2：P27 守卫）；`cycle audit` → **23 轮 · 0 硬 · 0 缺口**；
`catalog --write` 重生成（33 域 → CAPABILITIES / HARNESS-MAP / harness-index 同步）；P18 32 族路由回归全过。

**信号所有权记录（判别纪律的产物）。** 唯一性守卫（`test_signals_are_distinctive_enough`）强制每个信号只属一个域：
通用词（`history`/`philosophy`/`历史`/`哲学`/`诠释学`…）留在 `humanities`，新域持有**学科专属信号**
（`historiography`/`史学`/`编年`/`考据`；`metaphysics`/`形而上学`/`认识论`；`comparative politics`/`政治学`/`选举`…）。
后果写清：英文裸词「history」路由到 humanities（通用兜底），学科专属词才到新域——与 reading/humanities 的
分工同构。若将来需要「history」直通史学域，须先决定 humanities 是否让渡该词（重访触发）。
另：outlets 的 `topics` 必须注册进 `sources.json` 的 `topic_ids`——本轮把 `digital-humanities` 与
`cognitive-science` 两个 id 补入注册表。

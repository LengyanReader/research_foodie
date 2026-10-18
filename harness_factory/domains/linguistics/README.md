# Domain · Linguistics · 语言域
> Wiring `core/` modules into language description and annotation: an explicit scheme, measured agreement, and every cited form traceable.
> 把 `core/` 模块接线成语言描写与标注流程：方案显式、一致性可测、每个引例可溯源。
**Updated:** 2026-10-18

---

## 中文速览
语言域的目标是**让「语言事实」可复核**：先固定研究对象与理论框架（M0/M1），再写清标注方案与类别定义（M7）；标注样本并**测量标注者一致性**（κ/α，M3/M4）；用**可查证的例证 + 计数**支撑描写（M4）；主动寻找反例与跨语言差异（M3）；每个引用形式都带出处（语料库、版本、行号）。域特有风险：**类别定义漂移**、**单标注者即真理**、**只给结论不给例证**（英语中心偏差）、**把形态-句法框架当事实**、**语料版权与说话人隐私**。

---

## What this domain is for · 用途
Make a claim about language (*this construction behaves like X*, *this corpus shows Y*) re-runnable: a defined annotation scheme, a sample others can re-annotate, reliability reported rather than assumed, and glossed examples with provenance. Covers syntax, morphology, phonology, semantics/pragmatics, corpus work and computational-linguistic annotation.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Object & framework | M0, M1 | which variety, which theory, which data |
| L1 | Annotation scheme | M7, M1 | category definitions + decision rules, versioned |
| L2 | Annotate & measure agreement | M3, M4 | κ/α on a shared sample; disagreements analysed |
| L3 | Describe the pattern | M3, M4 | glossed examples + counts; no example-free claim |
| L4 | Counterexamples & variation | M3 | near-misses, typological and dialectal variation |
| L5 | Write up | M7, M4 | provenance for every form; data statement |

## Module combination · 模块组合
- **M0** — a theory-laden paraphrase is not a datum; separate observation from framework.
- **M1** — the scheme, the tagset and the guidelines live in context, versioned and citable.
- **M2** — corpora and annotation runs are checkpointed; a re-annotation is a resumable increment.
- **M3** — the gate is agreement measurement plus an explicit counterexample sweep.
- **M4** — every cited form carries source, version and location; corpora are provenance-bearing.
- **M6** — taggers, parsers and alignment tools are instruments: pinned versions, reported accuracy.
- **M7** — licensing, consent and speaker de-identification are release gates, not footnotes.

## Instruments · 仪器
- **Scheme & data** — `universal-dependencies` (guideline version + treebank release + validators).
- **Annotation** — `inception` (multi-layer, knowledge-base linking) · `elan` (tiered, time-aligned audio/video).
- **Agreement gate** — report κ/α on a double-annotated sample (`[R102]`); a model annotator is an *instrument with its own reliability*, not an oracle ("agrees with itself" ≠ agreement).
- **Rights gate** — the corpus licence and consent must permit the use claimed.
- Full map: `../reference/evidence-instruments.md#linguistic-data`.

## Discipline-specific risks · 领域特有风险
- **Scheme drift** (categories reinterpreted mid-annotation without a version bump).
- **Single annotator as ground truth** (no reliability measure reported).
- **Anecdotal authority** (a striking example replacing the distribution).
- **One-language overgeneralisation** (claims from English data stated as universal).
- **Framework reification** (treating UD-style analyses as theory-neutral facts).

## See also
`../reading/README.md` (close reading of texts) · `../humanities/README.md` · `../core/00-index.md` · `../sources/source-map.md` · `../review/disciplines-crosswalk-2026-10.md`.

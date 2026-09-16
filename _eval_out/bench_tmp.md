# DAS-Bench-style evaluation pilot — research_foodie preview

> Updated: 2026-09-16 · scorer = this repo's LLM judge (default `opencode/big-pickle`), NOT DAS-Bench's frozen ≥300B judge
>
> Status: **preview / directional only**. Full DAS-Bench compliance is out of reach in this env (see feasibility matrix at the end).

## Run summary

| id | kind | paper | candidates | papers | cited | out chars | pdf pg | L6 | internal judge | DAS-16 cov. |
|---|---|---|---|---|---|---|---|---|---|---|
| P-A | proxy | 2306.15666 | 2306.15666,1906.04043,2304.02819 | 3 | 3 | 15781 | 6 | 1.00 | pass@5.00 | 16/16 |
| P-B | proxy | 2304.02819 | 2304.02819 | 1 | 1 | 14759 | 6 | 1.00 | pass@4.00 | 16/16 |
| P-C | proxy | 1906.04043 | 1906.04043,2306.15666,2304.02819 | 3 | 3 | 11049 | 4 | 1.00 | pass@4.00 | 16/16 |
| 001 | das | - | 2409.13740 | 0 | 0 | 0 | - | 0.00 | - | - |
| 019 | das | - | - | 0 | 0 | 0 | - | 0.00 | - | - |
| QA-1 | qa | 1906.04043 | 1906.04043 | 1 | 1 | 12757 | 5 | 1.00 | QA 4/4 | gold 2/3 |
| QA-2 | qa | 2304.02819 | 2304.02819 | 1 | 1 | 9829 | 4 | 1.00 | QA 5/5 | gold 2/2 |
| QA-3 | qa | 2306.15666 | 2306.15666 | 1 | 1 | 15274 | 5 | 1.00 | QA 1/2 | gold 0/2 |
| QA-4 | qa | 2304.02819 | 2304.02819,1906.04043,2306.15666 | 3 | 3 | 20740 | 7 | 1.00 | QA 5/5 | gold 1/2 |
| QA-5 | qa | 1906.04043 | 1906.04043 | 1 | 1 | 18477 | 7 | 1.00 | QA 4/5 | gold 2/3 |
| QA-6 | qa | 1908.10084 | - | 1 | 0 | 128 | 1 | 0.00 | QA 4/4 | gold 0/2 |
| QA-7 | qa | 1611.03599 | - | 1 | 1 | 17099 | 6 | 1.00 | QA 1/5 | gold 0/2 |

## QA-1 · QA · GLTR — how the detector visualizes token likelihood

- question: What visualizations and statistics does GLTR use to expose machine-generated text?
- paper_id: 1906.04043 · evidence chars: 12757 · elapsed: 174.0s · **cached (vintage run)**
- QA judge: correctness **4/5** · groundedness **4/5** · gold-token hit **2/3**
   - judge feedback: The artifact answers the question well: it identifies GLTR's statistics (distributional/rank-based signals under a surrogate LM, e.g. top-100 vs out-of-vocabulary usage) and the annotation visualization (color-coded rank buckets top-10/top-100/top-1000/OOV) that makes the signal legible. It correctl

## QA-2 · QA · Liang — detector bias against non-native writers

- question: How does bias against non-native English writers manifest in GPT detectors?
- paper_id: 2304.02819 · evidence chars: 9829 · elapsed: 177.4s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **2/2**
   - judge feedback: The artifact answers the question precisely, reproducing the paper's specific quantitative findings: 61.22% average FPR across seven detectors on non-native TOEFL essays (n=91), enrichment reducing FPR to 11.77% (~49.45 pp drop), the self-edit prompt dropping detection of 31 counterfeit college essa

## QA-3 · QA · Weber-Wulff — families of AI-text detection

- question: What families of AI-generated-text detection methods does the Weber-Wulff survey cover?
- paper_id: 2306.15666 · evidence chars: 15274 · elapsed: 247.5s · **cached (vintage run)**
- QA judge: correctness **1/5** · groundedness **2/5** · gold-token hit **0/2**
   - judge feedback: The artifact never answers the question. Asked what families of AI-generated-text detection methods the Weber-Wulff survey covers, it instead delivers bibliographic-identity, authorship, and evidence-boundary commentary about arXiv:2306.15666. It also misidentifies the paper's nature: 2306.15666 is 

## QA-4 · QA · Liang — the human Turing-test protocol

- question: What human experiment protocol did Liang et al. use to test whether GPT detectors misjudge non-native writing?
- paper_id: 2304.02819 · evidence chars: 20740 · elapsed: 445.8s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **1/2**
   - judge feedback: The artifact directly and specifically answers the question: Liang et al. tested GPT detectors on 91 TOEFL essays written by non-native English speakers, using seven widely-used detectors, reporting an average 61.22% false-positive AI-labeling rate (arXiv:2304.02819). It also supplies corroborating 

## QA-5 · QA · GLTR — statistical cues behind detection

- question: Which token statistics make machine text detectable according to GLTR?
- paper_id: 1906.04043 · evidence chars: 18477 · elapsed: 303.3s · **cached (vintage run)**
- QA judge: correctness **4/5** · groundedness **5/5** · gold-token hit **2/3**
   - judge feedback: Correctly identifies the core GLTR token statistics: generated text concentrates probability mass on high-rank tokens because the model samples from its own predicted distribution, while human text favors high-rank, non-obvious words regardless of predicted entropy; it also grounds the signal in con

## QA-6 · Qasper · Sentence-BERT — STS evaluation metrics

- question: What metrics are used for the STS tasks?
- paper_id: 1908.10084 · evidence chars: 128 · elapsed: 0.1s
- QA judge: correctness **4/5** · groundedness **4/5** · gold-token hit **0/2**
   - judge feedback: Mock QA grader: correct answer with inline cites.

## QA-7 · Qasper · UTCNN — Chinese data size

- question: What is the size of the Chinese data?
- paper_id: 1611.03599 · evidence chars: 17099 · elapsed: 292.5s · **cached (vintage run)**
- QA judge: correctness **1/5** · groundedness **5/5** · gold-token hit **0/2**
   - judge feedback: The artifact never states the size of the Chinese data (e.g., number of posts or users). It only repeats that the corpus is highly skewed with roughly 20% of posts carrying a stance label, and it explicitly leaves the exact scale as an open gap ('leaving open the motivating question of the exact sca

## P-A · Proxy · AI-generated text detection (paper-anchored)

- paper_id: 2306.15666 · evidence chars: 15781 · elapsed: 309.1s · **cached (vintage run)**
- rendered manuscript (MAR): `_eval_out\manuscripts\P-A_manuscript.pdf` · **6 pages**
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@5.00
- **BSC** — Claim-Level Citation Support: 5 · Reference Faithfulness and Attribution Accuracy: 5 · Multi-Reference Synthesis Coverage and Quality: 4 · Citation Distribution Balance and Non-Redundancy: 3  (avg 4.25)
- **MAR** — Citation and Reference Presentation Integrity: 3 · Figure/Table Quality and Textual Integration: 3 · Layout and Formatting Professionalism: 3 · Manuscript Component Completeness: 3  (avg 3.00)
- **TSQ** — Research-Space Coverage: 3 · Taxonomy Clarity and Boundary Control: 3 · Survey Organization and Functional Coherence: 4 · Synthesis Insight and Gap Analysis: 5  (avg 3.75)
- **HDQ** — Multi-Level Goal Alignment: 4 · Paragraph Argument Progression: 5 · Atomic Claim Specificity and Technical Concreteness: 5 · Local Synthesis and Non-Enumerative Writing: 5  (avg 4.75)
- **Total Avg**: 3.94  (coverage 16/16, judge=opencode/big-pickle)

## P-B · Proxy · Detection-tool bias against non-native writers (paper-anchored)

- paper_id: 2304.02819 · evidence chars: 14759 · elapsed: 322.2s · **cached (vintage run)**
- rendered manuscript (MAR): `_eval_out\manuscripts\P-B_manuscript.pdf` · **6 pages**
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@4.00
- **BSC** — Claim-Level Citation Support: 3 · Reference Faithfulness and Attribution Accuracy: 4 · Multi-Reference Synthesis Coverage and Quality: 2 · Citation Distribution Balance and Non-Redundancy: 2  (avg 2.75)
- **MAR** — Citation and Reference Presentation Integrity: 3 · Figure/Table Quality and Textual Integration: 2 · Layout and Formatting Professionalism: 4 · Manuscript Component Completeness: 3  (avg 3.00)
- **TSQ** — Research-Space Coverage: 2 · Taxonomy Clarity and Boundary Control: 2 · Survey Organization and Functional Coherence: 4 · Synthesis Insight and Gap Analysis: 3  (avg 2.75)
- **HDQ** — Multi-Level Goal Alignment: 4 · Paragraph Argument Progression: 4 · Atomic Claim Specificity and Technical Concreteness: 4 · Local Synthesis and Non-Enumerative Writing: 3  (avg 3.75)
- **Total Avg**: 3.06  (coverage 16/16, judge=opencode/big-pickle)

## P-C · Proxy · Methods taxonomy: detect AIGC (statistical, watermark, human)

- paper_id: 1906.04043 · evidence chars: 11049 · elapsed: 434.6s · **cached (vintage run)**
- rendered manuscript (MAR): `_eval_out\manuscripts\P-C_manuscript.pdf` · **4 pages**
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@4.00
- **BSC** — Claim-Level Citation Support: 4 · Reference Faithfulness and Attribution Accuracy: 5 · Multi-Reference Synthesis Coverage and Quality: 3 · Citation Distribution Balance and Non-Redundancy: 4  (avg 4.00)
- **MAR** — Citation and Reference Presentation Integrity: 5 · Figure/Table Quality and Textual Integration: 4 · Layout and Formatting Professionalism: 4 · Manuscript Component Completeness: 3  (avg 4.00)
- **TSQ** — Research-Space Coverage: 3 · Taxonomy Clarity and Boundary Control: 4 · Survey Organization and Functional Coherence: 4 · Synthesis Insight and Gap Analysis: 4  (avg 3.75)
- **HDQ** — Multi-Level Goal Alignment: 4 · Paragraph Argument Progression: 4 · Atomic Claim Specificity and Technical Concreteness: 5 · Local Synthesis and Non-Enumerative Writing: 4  (avg 4.25)
- **Total Avg**: 4.00  (coverage 16/16, judge=opencode/big-pickle)

## QA pilot — evidence-grounded answers (preview)

| id | correctness (5) | groundedness (5) | gold-token hit | pdf pg |
|---|---|---|---|---|
| QA-1 | 4 | 4 | 2/3 | 5 |
| QA-2 | 5 | 5 | 2/2 | 4 |
| QA-3 | 1 | 2 | 0/2 | 5 |
| QA-4 | 5 | 5 | 1/2 | 7 |
| QA-5 | 4 | 5 | 2/3 | 7 |
| QA-6 | 4 | 4 | 0/2 | 1 |
| QA-7 | 1 | 5 | 0/2 | 6 |
| **mean (n=7)** | **3.43** | **4.29** | - | - |

## Family means across scored scenarios (preview)

| method | BSC | MAR | TSQ | HDQ | Total |
|---|---|---|---|---|---|
| research_foodie (preview, n=3) | 3.67 | 3.33 | 3.42 | 4.25 | 3.67 |
| Human (published) | 3.84 | 5.00 | 4.29 | 4.24 | 4.34 |
| Codex (published) | 2.80 | 4.19 | 2.99 | 2.75 | 3.18 |
| GPT Deep Research (published) | 3.32 | 4.14 | 3.48 | 3.76 | 3.68 |
| Gemini Deep Research (published) | 2.95 | 4.84 | 3.82 | 4.07 | 3.92 |
| Naive RAG (published) | 3.73 | 4.09 | 4.06 | 4.22 | 4.03 |
| AutoSurvey (published) | 3.81 | 3.67 | 3.74 | 3.69 | 3.73 |
| SurveyForge (published) | 3.73 | 3.83 | 3.81 | 3.74 | 3.78 |
| LiRA (published) | 3.63 | 3.07 | 3.72 | 4.06 | 3.62 |
| InteractiveSurvey (published) | 2.75 | 4.68 | 3.88 | 3.93 | 3.81 |
| DAS (published) | 3.85 | 5.00 | 4.22 | 4.28 | 4.34 |

> ⚠ Directional only: published rows used a multi-paper survey artifact, a ≥300B frozen judge, rendered pages (MAR) and DAS-2M pools; our preview artifacts are single-paper grounded summaries scored by the local judge. Not comparable head-to-head.

## Feasibility matrix — is DAS-Bench usable in this env?

| asset | status | notes |
|---|---|---|
| `benchmark/topics.json` (30 topics) | ✅ local | used verbatim (001, 019 probed) |
| `benchmark/evaluation_protocol.md` (16 criteria) | ✅ local | re-implemented here (frozen judge prompt is not public) |
| `results/main_results_30_topics.csv` | ✅ local | benchmark published scores (context only) |
| `evaluation/*.py` + `run_eval_all.sh` | ✅ local | full harness present (BSC/MAR/TSQ/HDQ) |
| DAS-2M candidate-paper metadata pool | ⛔ Hugging Face | not fetched (network); task pools are the benchmark input |
| gold source PDFs / reference surveys | ⛔ Hugging Face | not fetched |
| ≥300B-class frozen judge | ⛔ keys/GPU | config.json also supports a local OpenAI-compatible judge endpoint |
| MAR rendered-page scoring (dpi/binary) | ⛔ env | needs PDF page rendering + binary scoring |
| multi-paper evidence per topic | 🟡 2/30 | corpus has 2 parsed papers; DAS topics map to neither → no-evidence rows |
| `external/DAS/DAS-Bench` worktree | ✅ | read-only reference harness |

## Full-compliance checklist (to actually *run* DAS-Bench)

1. Fetch DAS-2M metadata + topic pools (Hugging Face) and the gold surveys/PDFs.
2. Build multi-paper evidence per topic (extend S_lit to fetch + parse top-k full texts).
3. Run the released `run_eval_all.sh` evaluators (needs PDF rendering for MAR).
4. Use a ≥300B judge (cloud key or a local OpenAI-compatible endpoint).
5. Report frozen-judge prompt, model id, temperature, aggregation — per protocol.
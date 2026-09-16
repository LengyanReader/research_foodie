# DAS-Bench-style evaluation pilot — research_foodie preview

> Updated: 2026-09-16 · scorer = this repo's LLM judge (default `opencode/big-pickle`), NOT DAS-Bench's frozen ≥300B judge
>
> Status: **preview / directional only**. Full DAS-Bench compliance is out of reach in this env (see feasibility matrix at the end).

## Run summary

| id | kind | paper | candidates | evid. chars | L6 | internal judge | DAS-16 cov. |
|---|---|---|---|---|---|---|---|
| P-A | proxy | 2306.15666 | 2306.15666,2304.02819,1706.03762 | 3570 | 1.00 | pass@4.00 | 16/16 |
| P-B | proxy | 2304.02819 | 2304.02819 | 3039 | 1.00 | pass@5.00 | 16/16 |
| 001 | das | 2306.15666 | 2306.15666,2409.13740,1706.03762 | 3277 | 1.00 | pass@4.00 | 16/16 |
| 019 | das | - | 2409.13740,2510.24701 | 0 | 0.00 | - | - |

## P-A · Proxy · AI-generated text detection (paper-anchored)

- paper_id: 2306.15666 · evidence chars: 3570 · elapsed: 111.5s
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@4.00
- **BSC** — Claim-Level Citation Support: 4 · Reference Faithfulness and Attribution Accuracy: 4 · Multi-Reference Synthesis Coverage and Quality: 1 · Citation Distribution Balance and Non-Redundancy: 2  (avg 2.75)
- **MAR** — Citation and Reference Presentation Integrity: 2 · Figure/Table Quality and Textual Integration: 1 · Layout and Formatting Professionalism: 3 · Manuscript Component Completeness: 2  (avg 2.00)
- **TSQ** — Research-Space Coverage: 2 · Taxonomy Clarity and Boundary Control: 2 · Survey Organization and Functional Coherence: 3 · Synthesis Insight and Gap Analysis: 3  (avg 2.50)
- **HDQ** — Multi-Level Goal Alignment: 4 · Paragraph Argument Progression: 3 · Atomic Claim Specificity and Technical Concreteness: 3 · Local Synthesis and Non-Enumerative Writing: 3  (avg 3.25)
- **Total Avg**: 2.62  (coverage 16/16, judge=opencode/big-pickle)

## P-B · Proxy · Detection-tool bias against non-native writers (paper-anchored)

- paper_id: 2304.02819 · evidence chars: 3039 · elapsed: 80.0s
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@5.00
- **BSC** — Claim-Level Citation Support: 5 · Reference Faithfulness and Attribution Accuracy: 5 · Multi-Reference Synthesis Coverage and Quality: 1 · Citation Distribution Balance and Non-Redundancy: 1  (avg 3.00)
- **MAR** — Citation and Reference Presentation Integrity: 3 · Figure/Table Quality and Textual Integration: 1 · Layout and Formatting Professionalism: 4 · Manuscript Component Completeness: 3  (avg 2.75)
- **TSQ** — Research-Space Coverage: 3 · Taxonomy Clarity and Boundary Control: 2 · Survey Organization and Functional Coherence: 4 · Synthesis Insight and Gap Analysis: 3  (avg 3.00)
- **HDQ** — Multi-Level Goal Alignment: 3 · Paragraph Argument Progression: 4 · Atomic Claim Specificity and Technical Concreteness: 5 · Local Synthesis and Non-Enumerative Writing: 4  (avg 4.00)
- **Total Avg**: 3.19  (coverage 16/16, judge=opencode/big-pickle)

## 001 · Tool Learning and Function Calling for LLM Agents

- paper_id: 2306.15666 · evidence chars: 3277 · elapsed: 117.8s
- L6 gate: score 1.00 passed=True · internal P3 judge: pass@4.00
- **BSC** — Claim-Level Citation Support: 4 · Reference Faithfulness and Attribution Accuracy: 4 · Multi-Reference Synthesis Coverage and Quality: 1 · Citation Distribution Balance and Non-Redundancy: 2  (avg 2.75)
- **MAR** — Citation and Reference Presentation Integrity: 1 · Figure/Table Quality and Textual Integration: 1 · Layout and Formatting Professionalism: 4 · Manuscript Component Completeness: 2  (avg 2.00)
- **TSQ** — Research-Space Coverage: 1 · Taxonomy Clarity and Boundary Control: 1 · Survey Organization and Functional Coherence: 3 · Synthesis Insight and Gap Analysis: 2  (avg 1.75)
- **HDQ** — Multi-Level Goal Alignment: 2 · Paragraph Argument Progression: 4 · Atomic Claim Specificity and Technical Concreteness: 4 · Local Synthesis and Non-Enumerative Writing: 3  (avg 3.25)
- **Total Avg**: 2.44  (coverage 16/16, judge=opencode/big-pickle)

## Family means across scored scenarios (preview)

| method | BSC | MAR | TSQ | HDQ | Total |
|---|---|---|---|---|---|
| research_foodie (preview, n=3) | 2.83 | 2.25 | 2.42 | 3.50 | 2.75 |
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
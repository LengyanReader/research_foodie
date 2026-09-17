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
| QA-3 | qa | 2306.15666 | - | 1 | 1 | 1638 | 1 | 1.00 | QA 3/3 | gold 1/2 |
| QA-4 | qa | 2304.02819 | 2304.02819,1906.04043,2306.15666 | 3 | 3 | 20740 | 7 | 1.00 | QA 5/5 | gold 1/2 |
| QA-5 | qa | 1906.04043 | 1906.04043 | 1 | 1 | 18477 | 7 | 1.00 | QA 4/5 | gold 2/3 |
| QA-6 | qa | 1908.10084 | - | 1 | 1 | 1422 | 1 | 1.00 | QA 5/5 | gold 2/2 |
| QA-7 | qa | 1611.03599 | - | 1 | 1 | 1407 | 1 | 1.00 | QA 5/5 | gold 2/2 |
| QA-8 | qa | 1910.09982 | - | 1 | 1 | 2449 | 1 | 1.00 | QA 5/5 | gold 3/3 |
| QA-9 | qa | 1910.06036 | - | 1 | 1 | 1073 | 1 | 1.00 | QA 5/5 | gold 3/3 |
| QA-10 | qa | 1908.06267 | - | 1 | 1 | 1642 | 1 | 1.00 | QA 5/5 | gold 3/3 |
| SQ-1 | qa | ctx | - | 0 | 1 | 443 | 1 | 1.00 | QA 5/5 | gold 1/1 |
| SQ-2 | qa | ctx | - | 0 | 1 | 428 | 1 | 1.00 | QA 5/3 | gold 1/1 |
| SQ-3 | qa | ctx | - | 0 | 1 | 327 | 1 | 1.00 | QA 5/4 | gold 1/1 |
| SQ-4 | qa | ctx | - | 0 | 1 | 350 | 1 | 1.00 | QA 5/3 | gold 1/1 |
| SQ-5 | qa | ctx | - | 0 | 1 | 215 | 1 | 1.00 | QA 5/4 | gold 1/1 |
| PQ-1 | qa | ctx | - | 0 | 1 | 811 | 1 | 1.00 | QA 2/1 | gold 0/1 |
| PQ-2 | qa | ctx | - | 0 | 1 | 977 | 1 | 1.00 | QA 4/5 | gold 1/1 |
| PQ-3 | qa | ctx | - | 0 | 1 | 1104 | 1 | 1.00 | QA 4/5 | gold 1/1 |
| PQ-4 | qa | ctx | - | 0 | 1 | 1146 | 1 | 1.00 | QA 4/5 | gold 1/2 |
| PQ-5 | qa | ctx | - | 0 | 1 | 1227 | 1 | 1.00 | QA 2/5 | gold 1/2 |
| QA-11 | qa | 1703.10344 | - | 1 | 1 | 502 | 1 | 1.00 | QA 5/5 | gold 1/1 |
| QA-12 | qa | 1703.10344 | - | 1 | 1 | 355 | 1 | 1.00 | QA 5/5 | gold 1/1 |

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
- paper_id: 2306.15666 · evidence chars: 1638 · elapsed: 16.7s · **cached (vintage run)**
- QA judge: correctness **3/5** · groundedness **3/5** · gold-token hit **1/2**
   - judge feedback: The answer is specific and correctly identifies that the survey's core is tool-by-tool testing (14 tools, 6 test-case categories). However, it is only partially correct: the Weber-Wulff survey's background/related-work sections do discuss detection-method approaches (e.g., zero-shot/perplexity-based

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
- paper_id: 1908.10084 · evidence chars: 1422 · elapsed: 15.6s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **2/2**
   - judge feedback: Correctly states Spearman's rank correlation (ρ) between cosine-similarity of sentence embeddings and gold labels as the primary STS metric, noting the ρ×100 convention (Table 1, STS12–16, STSb, SICK-R). Accurately explains Pearson's rejection for standard STS and its limited use for AFS comparabili

## QA-7 · Qasper · UTCNN — Chinese data size

- question: What is the size of the Chinese data?
- paper_id: 1611.03599 · evidence chars: 1407 · elapsed: 15.8s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **2/2**
   - judge feedback: The artifact correctly identifies the Chinese data as the FBFans dataset from arXiv:1611.03599 (Chen & Ku, UTCNN) and gives a complete, precise answer on its size. Verified against the source: 32,595 posts (confirmed directly in the paper text 'from these 32,595 posts'), 505,412 unique users ({2,496

## QA-8 · Qasper · NLP4IF-2019 — propaganda techniques

- question: What are the 18 propaganda techniques?
- paper_id: 1910.09982 · evidence chars: 2449 · elapsed: 21.3s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **3/3**
   - judge feedback: The artifact correctly lists all 18 propaganda techniques from the SemEval-2020 Task 11 paper (arXiv:1910.09982), in the paper's canonical order, with accurate descriptions matching the dataset's official definitions (e.g., loaded language, whataboutism, reductio ad Hitlerum, thought-terminating cli

## QA-9 · Qasper · QG — evaluation metrics

- question: What metrics do they use?
- paper_id: 1910.06036 · evidence chars: 1073 · elapsed: 15.8s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **3/3**
   - judge feedback: The artifact answers precisely and completely: it enumerates all six metrics (BLEU-1/2/3/4, METEOR, ROUGE-L) with their primary citations, names the datasets/splits (SQuAD, Zhou Split, Du Split) and the downstream evaluation script (Chen et al. 2015). Every factual claim is tied to an inline arXiv c

## QA-10 · Qasper · MPAD — datasets

- question: Which datasets are used?
- paper_id: 1908.06267 · evidence chars: 1642 · elapsed: 19.5s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **3/3**
   - judge feedback: The artifact fully and precisely answers 'Which datasets are used?', listing all 11 datasets in the paper's Table 1 (Reuters, Snippets, BBCSport, Polarity, Subjectivity, MPQA, IMDB, TREC, SST-1, SST-2, Yelp2013) with correct per-dataset details (ModApte split/8 classes, BBCSport cross-validation, SS

## SQ-1 · SciQ · frameshift mutation

- question: A frameshift mutation is a deletion or insertion of one or more of what that changes the reading frame of the base sequence?
- paper_id: ctx · evidence chars: 443 · elapsed: 15.4s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **1/1**
   - judge feedback: The artifact gives the correct, precise answer (nucleotides) and supports it with an exact quoted source line that directly matches the claim. Both the English answer and the Chinese 速览 are accurate, and the inline arXiv cite is grounded in the quoted evidence.

## SQ-2 · SciQ · wetland definition

- question: What is an area of land called that is wet for all or part of the year?
- paper_id: ctx · evidence chars: 428 · elapsed: 17.0s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **3/5** · gold-token hit **1/1**
   - judge feedback: The answer 'wetland' is complete and precise, matching the source definition quoted verbatim. However, the artifact cites a source sentence but provides no verifiable arXiv identifier (e.g., arXiv:XXXX.XXXXX), so the claimed quote cannot be independently traced to a paper.

## SQ-3 · SciQ · blood vessels

- question: What are arteries, veins, and capillaries examples of?
- paper_id: ctx · evidence chars: 327 · elapsed: 15.4s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **4/5** · gold-token hit **1/1**
   - judge feedback: Correct, precise answer: blood vessels. Inline cite and source-evidence quote support the claim. Minor deduction: the identifier 'arXiv:SciQ:ctx' is vague and not a verifiable specific arXiv ID or paper, weakening traceability; a precise ID or DOI would make grounding fully checkable.

## SQ-4 · SciQ · volcanic ash clays

- question: Compounds with aluminum and silicon are commonly found in the clay fractions of soils derived from what?
- paper_id: ctx · evidence chars: 350 · elapsed: 14.3s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **3/5** · gold-token hit **1/1**
   - judge feedback: The artifact correctly and precisely answers that the compounds are found in soils derived from volcanic ash, matching the standard SciQ answer. However, the cited source 'arXiv:SciQ:ctx' is the dataset context itself rather than an independent primary-source paper, so the grounding is only partial:

## SQ-5 · SciQ · density definition

- question: What is the ratio of the mass of an object to its volume?
- paper_id: ctx · evidence chars: 215 · elapsed: 11.0s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **4/5** · gold-token hit **1/1**
   - judge feedback: Correctly identifies density as the mass-to-volume ratio. Answer claim is backed by an inline cite and quoted source evidence supports it; cite is a generic context reference (arXiv:SciQ:ctx) rather than a specific paper ID, slightly limiting verifiability.

## PQ-1 · PubMedQA · mitochondria / lace plant PCD (yes)

- question: Do mitochondria play a role in remodelling lace plant leaves during programmed cell death?
- paper_id: ctx · evidence chars: 811 · elapsed: 12.2s · **cached (vintage run)**
- QA judge: correctness **2/5** · groundedness **1/5** · gold-token hit **0/1**
   - judge feedback: The artifact is evasive rather than a definitive answer: it answers 'No' but immediately retreats to 'the paper does not state / makes no claim,' which avoids committing to the actual factual answer. The question asks whether mitochondria play a role in lace plant leaf remodelling during PCD, and a 

## PQ-2 · PubMedQA · Landolt C vs Snellen E acuity (no)

- question: Landolt C and snellen e acuity: differences in strabismus amblyopia?
- paper_id: ctx · evidence chars: 977 · elapsed: 10.8s · **cached (vintage run)**
- QA judge: correctness **4/5** · groundedness **5/5** · gold-token hit **1/1**
   - judge feedback: The artifact correctly identifies that the provided excerpt contains only study-design information (100 patients, median age 60.5, 39 strabismus amblyopia) and explicitly, honestly states that no Landolt C vs. Snellen E result for the strabismus amblyopia subgroup is present, refusing to invent data

## PQ-3 · PubMedQA · transanal vs transabdominal pull-through (no)

- question: Are the long-term results of the transanal pull-through equal to those of the transabdominal pull-through?
- paper_id: ctx · evidence chars: 1104 · elapsed: 15.9s · **cached (vintage run)**
- QA judge: correctness **4/5** · groundedness **5/5** · gold-token hit **1/1**
   - judge feedback: The artifact correctly identifies that the provided excerpt contains only the study design and aim (41 patients, TERPT n=20 vs ABD n=21) and reports no comparative long-term outcomes, so it does not fabricate an equivalence claim. Scoring 4 rather than 5 because the question itself went unanswered (

## PQ-4 · PubMedQA · HER2 immunoreactivity prognosis (maybe)

- question: Does HER2 immunoreactivity provide prognostic information in locally advanced urothelial carcinoma patients receiving adjuvant M-VEC chemotherapy?
- paper_id: ctx · evidence chars: 1146 · elapsed: 12.9s · **cached (vintage run)**
- QA judge: correctness **4/5** · groundedness **5/5** · gold-token hit **1/2**
   - judge feedback: The artifact is fully grounded: every claim (study design, 114 specimens, M-VEC = methotrexate/vinblastine/epirubicin/cisplatin, evaluation of HER2 by IHC and its effect on PFS) is traceable to the quoted excerpt, and it invents no HR, p-value, or conclusion. It honestly and specifically identifies 

## PQ-5 · PubMedQA · emergency laparotomy mortality (maybe)

- question: 30-Day and 1-year mortality in emergency general surgery laparotomies: an area of concern and need for improvement?
- paper_id: ctx · evidence chars: 1227 · elapsed: 18.0s · **cached (vintage run)**
- QA judge: correctness **2/5** · groundedness **5/5** · gold-token hit **1/2**
   - judge feedback: The artifact honestly reports that the paper's own 30-day and 1-year mortality figures are absent from the provided excerpt, so it cannot state the specific numeric answers the question asks for. It provides relevant context (background 30-day mortality 14-15%, study aim, and design), which is parti

## QA-11 · News-suggestion precision (article-entity)

- question: What is the highest precision reported for the article-entity suggestion stage?
- paper_id: 1703.10344 · evidence chars: 502 · elapsed: 15.4s · **cached (vintage run)**
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **1/1**
   - judge feedback: Correct and precise. arXiv:1703.10344 (Fetahu et al., 2017) abstract states: 'We achieve a high precision value of up to 93% in the article-entity suggestion stage and upto 84% for the article-section placement.' The artifact's answer (93%) and its verbatim source quote both match the paper exactly,

## QA-12 · News-suggestion precision (article-section)

- question: What is the precision reported for the article-section placement stage?
- paper_id: 1703.10344 · evidence chars: 355 · elapsed: 15.7s
- QA judge: correctness **5/5** · groundedness **5/5** · gold-token hit **1/1**
   - judge feedback: The artifact correctly and precisely identifies the article-section placement (ASP) stage precision as up to 84%, directly supported by an inline arXiv cite (arXiv:1703.10344) and an exact source quotation confirming the claim.

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
| QA-3 | 3 | 3 | 1/2 | 1 |
| QA-4 | 5 | 5 | 1/2 | 7 |
| QA-5 | 4 | 5 | 2/3 | 7 |
| QA-6 | 5 | 5 | 2/2 | 1 |
| QA-7 | 5 | 5 | 2/2 | 1 |
| QA-8 | 5 | 5 | 3/3 | 1 |
| QA-9 | 5 | 5 | 3/3 | 1 |
| QA-10 | 5 | 5 | 3/3 | 1 |
| SQ-1 | 5 | 5 | 1/1 | 1 |
| SQ-2 | 5 | 3 | 1/1 | 1 |
| SQ-3 | 5 | 4 | 1/1 | 1 |
| SQ-4 | 5 | 3 | 1/1 | 1 |
| SQ-5 | 5 | 4 | 1/1 | 1 |
| PQ-1 | 2 | 1 | 0/1 | 1 |
| PQ-2 | 4 | 5 | 1/1 | 1 |
| PQ-3 | 4 | 5 | 1/1 | 1 |
| PQ-4 | 4 | 5 | 1/2 | 1 |
| PQ-5 | 2 | 5 | 1/2 | 1 |
| QA-11 | 5 | 5 | 1/1 | 1 |
| QA-12 | 5 | 5 | 1/1 | 1 |
| **mean (n=22)** | **4.41** | **4.41** | - | - |

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
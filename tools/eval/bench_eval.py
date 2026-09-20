"""DAS-Bench-style benchmark evaluation for research_foodie.

Uses the *existing* DAS-Bench dataset assets that ship in `external/DAS`
(worktree):
  - `benchmark/topics.json`            — the 30 benchmark topics (ids 001-030)
  - `benchmark/evaluation_protocol.md` — the 16 scoring criteria (4 families:
    BSC, MAR, TSQ, HDQ; each 1-5; family avg = mean of its 4 criteria;
    Total Avg = mean of all 16)
  - `results/main_results_30_topics.csv` — published per-method scores (Human,
    Codex, GPT Deep Research, Gemini Deep Research, Naive RAG) used only as
    *directional context* for our pilot.

NOT full DAS-Bench compliance (see the report's feasibility matrix): the pilot
scorer is our own LLM judge (default `opencode/big-pickle`), not the ≥300B
frozen judge; the DAS-2M candidate-paper metadata pool and gold source PDFs
live on Hugging Face (not fetched here); MAR's rendered-page scoring is
out of reach in this env; proxy topics are paper-anchored, not the vanilla
topic instances. Every number below is therefore labelled a *preview*.

Run (from repo root; mock = deterministic regression via the mock server):
  python -m tools.eval.bench_eval                      # real, opencode default
  python -m tools.eval.bench_eval --backend openai --base-url http://127.0.0.1:8199/v1 --model mock-api   # mock
Reports: `_eval_out/bench_pilot_das.md`, plus a console summary.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.llm.client import LLMClient, Message
from tools.pipeline.graph import Pipeline
from tools.pipeline.validate import parse_json_dict

DAS_BENCH_DIR = Path("external/DAS/DAS-Bench")
TOPICS_JSON = DAS_BENCH_DIR / "benchmark" / "topics.json"
RESULTS_CSV = DAS_BENCH_DIR / "results" / "main_results_30_topics.csv"
DEFAULT_OUT = Path("_eval_out") / "bench_pilot_das.md"

# 16 criteria, verbatim from benchmark/evaluation_protocol.md (as of 2026-09-16).
DAS_16: List[Tuple[str, str]] = [
    ("BSC", "Claim-Level Citation Support"),
    ("BSC", "Reference Faithfulness and Attribution Accuracy"),
    ("BSC", "Multi-Reference Synthesis Coverage and Quality"),
    ("BSC", "Citation Distribution Balance and Non-Redundancy"),
    ("MAR", "Citation and Reference Presentation Integrity"),
    ("MAR", "Figure/Table Quality and Textual Integration"),
    ("MAR", "Layout and Formatting Professionalism"),
    ("MAR", "Manuscript Component Completeness"),
    ("TSQ", "Research-Space Coverage"),
    ("TSQ", "Taxonomy Clarity and Boundary Control"),
    ("TSQ", "Survey Organization and Functional Coherence"),
    ("TSQ", "Synthesis Insight and Gap Analysis"),
    ("HDQ", "Multi-Level Goal Alignment"),
    ("HDQ", "Paragraph Argument Progression"),
    ("HDQ", "Atomic Claim Specificity and Technical Concreteness"),
    ("HDQ", "Local Synthesis and Non-Enumerative Writing"),
]

_RUBRIC_LINES = "\n".join(f"{f}: {c}" for f, c in DAS_16)

_BENCH_RUBRIC_PROMPT = (
    "You are a benchmark scorer for academic-survey generation. Score the "
    "artifact below on the DAS-Bench rubric (16 criteria, 1-5 integer each, "
    "5 = human-survey level). The artifact may be a single-paper grounded "
    "summary rather than a multi-paper survey; score strictly by what the "
    "artifact contains.\n"
    f"The 16 criteria:\n{_RUBRIC_LINES}\n"
    "Respond ONLY as JSON {\"scores\": {\"<criterion>\": int}} — one key per "
    "criterion, using the criterion names above exactly."
)

# Topics we evaluate: two paper-anchored *proxy* topics (evidence available in
# the local corpus) + two verbatim DAS-Bench topics (to probe the evidence gap).
SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "proxy",
        "topic_id": "P-A",
        "topic": "Proxy · AI-generated text detection (paper-anchored)",
        "question": "How reliable are automatic detection tools for AI-generated text?",
    },
    {
        "kind": "proxy",
        "topic_id": "P-B",
        "topic": "Proxy · Detection-tool bias against non-native writers (paper-anchored)",
        "question": "Are GPT detectors biased against non-native English writers?",
    },
    {
        "kind": "proxy",
        "topic_id": "P-C",
        "topic": "Proxy · Methods taxonomy: detect AIGC (statistical, watermark, human)",
        "question": "Which methods for detecting AI-generated text — statistical detection, watermarking, classifiers, human judgment — are documented, and what are their relative limitations?",
    },
    {
        "kind": "das",
        "topic_id": "001",
        "topic": "Tool Learning and Function Calling for LLM Agents",
        "question": "Tool Learning and Function Calling for LLM Agents",
    },
    {
        "kind": "das",
        "topic_id": "019",
        "topic": "Human-AI Collaboration in Scientific Writing and Research Workflows",
        "question": "Human-AI Collaboration in Scientific Writing and Research Workflows",
    },
]

# Track C — evidence-grounded QA pilot. Answerable from the 3-paper local corpus
# (zero downloads); `gold_tokens` drive a deterministic fact hit (soft signal —
# the LLM `correctness`/`groundedness` judge is primary). Directional by design.
QA_SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "qa",
        "topic_id": "QA-1",
        "topic": "QA · GLTR — how the detector visualizes token likelihood",
        "question": "What visualizations and statistics does GLTR use to expose machine-generated text?",
        "gold_tokens": ["histogram", "top-", "rank"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-2",
        "topic": "QA · Liang — detector bias against non-native writers",
        "question": "How does bias against non-native English writers manifest in GPT detectors?",
        "gold_tokens": ["non-native", "TOEFL"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-3",
        "topic": "QA · Weber-Wulff — families of AI-text detection",
        "question": "What families of AI-generated-text detection methods does the Weber-Wulff survey cover?",
        "seed_id": "2306.15666",
        "gold_tokens": ["watermark", "classifier"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-4",
        "topic": "QA · Liang — the human Turing-test protocol",
        "question": "What human experiment protocol did Liang et al. use to test whether GPT detectors misjudge non-native writing?",
        "gold_tokens": ["Turing test", "91"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-5",
        "topic": "QA · GLTR — statistical cues behind detection",
        "question": "Which token statistics make machine text detectable according to GLTR?",
        "gold_tokens": ["probability", "uncertainty", "entropy"],
    },
]

# Qasper (external-author) QA pilot — questions & evidence taken from the Qasper
# dev set (v0.3, allenai/qasper); papers parsed locally from arXiv (Session 18).
QASPER_SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "qa",
        "topic_id": "QA-6",
        "topic": "Qasper · Sentence-BERT — STS evaluation metrics",
        "question": "What metrics are used for the STS tasks?",
        "seed_id": "1908.10084",
        "gold_tokens": ["pearson", "spearman"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-7",
        "topic": "Qasper · UTCNN — Chinese data size",
        "question": "What is the size of the Chinese data?",
        "seed_id": "1611.03599",
        "gold_tokens": ["2,496", "505,137"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-8",
        "topic": "Qasper · NLP4IF-2019 — propaganda techniques",
        "question": "What are the 18 propaganda techniques?",
        "seed_id": "1910.09982",
        "gold_tokens": ["loaded language", "name calling", "repetition"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-9",
        "topic": "Qasper · QG — evaluation metrics",
        "question": "What metrics do they use?",
        "seed_id": "1910.06036",
        "gold_tokens": ["bleu", "meteor", "rouge"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-10",
        "topic": "Qasper · MPAD — datasets",
        "question": "Which datasets are used?",
        "seed_id": "1908.06267",
        "gold_tokens": ["reuters", "imdb", "trec"],
    },
]

# SciQ (AllenAI) — provided-context MCQs: the `support` sentence is the source
# context (no paper download/parse). Zero external resources; tests the answer
# node against short-passage, school-science factoids (Session 19).
SCIQ_SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "qa",
        "topic_id": "SQ-1",
        "topic": "SciQ · frameshift mutation",
        "question": "A frameshift mutation is a deletion or insertion of one or more of what that changes the reading frame of the base sequence?",
        "context": "A frameshift mutation is a deletion or insertion of one or more nucleotides that changes the reading frame of the base sequence. Deletions remove nucleotides, and insertions add nucleotides.",
        "gold_tokens": ["nucleotide"],
    },
    {
        "kind": "qa",
        "topic_id": "SQ-2",
        "topic": "SciQ · wetland definition",
        "question": "What is an area of land called that is wet for all or part of the year?",
        "context": "A wetland is an area that is wet for all or part of the year. Wetlands are home to certain types of plants.",
        "gold_tokens": ["wetland"],
    },
    {
        "kind": "qa",
        "topic_id": "SQ-3",
        "topic": "SciQ · blood vessels",
        "question": "What are arteries, veins, and capillaries examples of?",
        "context": "Blood vessels include arteries, veins, and capillaries.",
        "gold_tokens": ["blood vessels"],
    },
    {
        "kind": "qa",
        "topic_id": "SQ-4",
        "topic": "SciQ · volcanic ash clays",
        "question": "Compounds with aluminum and silicon are commonly found in the clay fractions of soils derived from what?",
        "context": "Compounds with aluminum and silicon are commonly found in the clay fractions of soils derived from volcanic ash. One of these compounds is vermiculite, which is formed in reactions caused by exposure to weather.",
        "gold_tokens": ["volcanic ash"],
    },
    {
        "kind": "qa",
        "topic_id": "SQ-5",
        "topic": "SciQ · density definition",
        "question": "What is the ratio of the mass of an object to its volume?",
        "context": "Density is the ratio of the mass of an object to its volume.",
        "gold_tokens": ["density"],
    },
]

# PubMedQA (qiaojin/PubMedQA, pqa_labeled train) — yes/no/maybe research QAs
# with the abstract supplied as context (same zero-parse `ctx` route). Gold =
# the dataset's final_decision; gold tokens are directional soft signals only
# (the judge's correctness is primary) — Session 19.
PubMedQA_SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "qa",
        "topic_id": "PQ-1",
        "topic": "PubMedQA · mitochondria / lace plant PCD (yes)",
        "question": "Do mitochondria play a role in remodelling lace plant leaves during programmed cell death?",
        "context": "Programmed cell death (PCD) is the regulated death of cells within an organism. The lace plant (Aponogeton madagascariensis) produces perforations in its leaves through PCD. The leaves of the plant consist of a latticework of longitudinal and transverse veins enclosing areoles. PCD occurs in the cells at the center of these areoles and progresses outwards, stopping approximately five cells from the vasculature. The role of mitochondria during PCD has been recognized in animals; however, it has been less studied during PCD in plants.",
        "gold_tokens": ["yes"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-2",
        "topic": "PubMedQA · Landolt C vs Snellen E acuity (no)",
        "question": "Landolt C and snellen e acuity: differences in strabismus amblyopia?",
        "context": "Assessment of visual acuity depends on the optotypes used for measurement. The ability to recognize different optotypes differs even if their critical details appear under the same visual angle. Since optotypes are evaluated on individuals with good visual acuity and without eye disorders, differences in the lower visual acuity range cannot be excluded. In this study, visual acuity measured with the Snellen E was compared to the Landolt C acuity. 100 patients (age 8 - 90 years, median 60.5 years) with various eye disorders, among them 39 with amblyopia due to strabismus.",
        "gold_tokens": ["no"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-3",
        "topic": "PubMedQA · transanal vs transabdominal pull-through (no)",
        "question": "Are the long-term results of the transanal pull-through equal to those of the transabdominal pull-through?",
        "context": "The transanal endorectal pull-through (TERPT) is becoming the most popular procedure in the treatment of Hirschsprung disease (HD), but overstretching of the anal sphincters remains a critical issue that may impact the continence. This study examined the long-term outcome of TERPT versus conventional transabdominal (ABD) pull-through for HD. Records of 41 patients more than 3 years old who underwent a pull-through for HD (TERPT, n = 20; ABD, n = 21) were reviewed.",
        "gold_tokens": ["no"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-4",
        "topic": "PubMedQA · HER2 immunoreactivity prognosis (maybe)",
        "question": "Does HER2 immunoreactivity provide prognostic information in locally advanced urothelial carcinoma patients receiving adjuvant M-VEC chemotherapy?",
        "context": "To evaluate the impact of HER2 immunoreactivity on clinical outcome in locally advanced urothelial carcinoma patients who received surgery alone, or methotrexate, vinblastine, epirubicin, and cisplatin (M-VEC) as adjuvant chemotherapy. We studied 114 formalin-fixed paraffin-embedded specimens obtained from locally advanced urothelial carcinoma patients receiving surgery alone or adjuvant M-VEC. The authors evaluated HER2 immunoreactivity using immunohistochemical staining and explored the influence of pathological parameters and HER2 immunoreactivity on progression-free survival (PFS).",
        "gold_tokens": ["limited", "prognostic value"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-5",
        "topic": "PubMedQA · emergency laparotomy mortality (maybe)",
        "question": "30-Day and 1-year mortality in emergency general surgery laparotomies: an area of concern and need for improvement?",
        "context": "Emergency surgery is associated with poorer outcomes and higher mortality with recent studies suggesting the 30-day mortality to be 14-15%. The aim of this study was to analyse the 30-day mortality, age-related 30-day mortality and 1-year mortality following emergency laparotomy. We hope this will encourage prospective data collection, improvement of care and initiate strategies to establish best practice in this area. This was a retrospective study of patients who underwent emergency laparotomy from June 2010 to May 2012.",
        "gold_tokens": ["mortality", "concern"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-6",
        "topic": "PubMedQA · water-induced urticaria (yes)",
        "question": "Syncope during bathing in infants, a pediatric form of water-induced urticaria?",
        "context": "Apparent life-threatening events in infants are a difficult and frequent problem in pediatric practice. The prognosis is uncertain because of risk of sudden infant death syndrome. Eight infants aged 2 to 15 months were admitted during a period of 6 years; they suffered from similar maladies in the bath: on immersion, they became pale, hypotonic, still and unreactive; recovery took a few seconds after withdrawal from the bath and stimulation. Two diagnoses were initially considered: seizure or gastroesophageal reflux but this was doubtful. The hypothesis of an equivalent of aquagenic urticaria was then considered.",
        "gold_tokens": ["yes"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-7",
        "topic": "PubMedQA · tailored interventions / mammography (yes)",
        "question": "Can tailored interventions increase mammography use among HMO women?",
        "context": "Telephone counseling and tailored print communications have emerged as promising methods for promoting mammography screening. However, there has been little research testing, within the same randomized field trial, of the efficacy of these two methods compared to a high-quality usual care system for enhancing screening. This study addressed the question: Compared to usual care, is tailored telephone counseling more effective than tailored print materials for promoting mammography screening? Three-year randomized field trial. One thousand ninety-nine women aged 50 and older recruited from a health maintenance organization.",
        "gold_tokens": ["yes"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-8",
        "topic": "PubMedQA · double balloon enteroscopy (yes)",
        "question": "Double balloon enteroscopy: is it efficacious and safe in a community setting?",
        "context": "From March 2007 to January 2011, 88 DBE procedures were performed on 66 patients. Indications included evaluation anemia/gastrointestinal bleed, small bowel IBD and dilation of strictures. Video-capsule endoscopy (VCE) was used prior to DBE in 43 of the 66 patients prior to DBE evaluation. The mean age was 62 years. Thirty-two patients were female, 15 were African-American; 44 antegrade and 44 retrograde DBEs were performed. DBE procedures resulted in a definitive diagnosis or therapy in the large majority of cases with no major complications, showing DBE to be efficacious and safe in a community setting.",
        "gold_tokens": ["yes", "safe"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-9",
        "topic": "PubMedQA · reporting heterogeneity / sleep (no)",
        "question": "Is adjustment for reporting heterogeneity necessary in sleep disorders?",
        "context": "Anchoring vignettes are brief texts describing a hypothetical character who illustrates a certain fixed level of a trait under evaluation. This research uses vignettes to elucidate factors associated with sleep disorders in adult Japanese before and after adjustment for reporting heterogeneity in self-reports. This study also evaluates the need for adjusting for reporting heterogeneity in the management of sleep and energy related problems in Japan. We investigated a dataset of 1002 respondents aged 18 years and over from the Japanese World Health Survey.",
        "gold_tokens": ["no"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-10",
        "topic": "PubMedQA · low HDL mutations / cIMT (no)",
        "question": "Do mutations causing low HDL-C promote increased carotid intima-media thickness?",
        "context": "Although observational data support an inverse relationship between high-density lipoprotein (HDL) cholesterol and coronary heart disease (CHD), genetic HDL deficiency states often do not correlate with premature CHD. Carotid intima-media thickness (cIMT) measurements were obtained in cases comprising 10 different mutations in LCAT, ABCA1 and APOA1 to further evaluate the relationship between low HDL resulting from genetic variation and early atherosclerosis. In a 1:2 case-control study of sex and age-related subjects (n=114), cIMT was nearly identical between cases and controls.",
        "gold_tokens": ["no"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-11",
        "topic": "PubMedQA · anticoagulation / trauma (no)",
        "question": "Therapeutic anticoagulation in the trauma patient: is it safe?",
        "context": "Trauma patients who require therapeutic anticoagulation pose a difficult treatment problem. The purpose of this study was to determine: (1) the incidence of complications using therapeutic anticoagulation in trauma patients, and (2) if any patient factors are associated with these complications. An 18-month retrospective review was performed on trauma patients who received therapeutic anticoagulation using unfractionated heparin (UH) and/or fractionated heparin (FH). Forty different pre-treatment and treatment patient characteristics were recorded.",
        "gold_tokens": ["no"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-12",
        "topic": "PubMedQA · Hawkins sign / talar necrosis (maybe)",
        "question": "Is the Hawkins sign able to predict necrosis in fractures of the neck of the astragalus?",
        "context": "To assess if the Hawkins sign can predict whether or not astragalus fractures of the neck will develop avascular necrosis. It is also assessed whether the occurrence of this complication is related to the displacement of the fracture, soft tissue injury, or delay in the reduction or surgery. The results were compared with those found in the literature. A retrospective study was conducted on 23 talar neck fractures recorded over a period of thirteen years.",
        "gold_tokens": ["maybe", "predict"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-13",
        "topic": "PubMedQA · lymphedema detection (maybe)",
        "question": "Can a practicing surgeon detect early lymphedema reliably?",
        "context": "Lymphedema may be identified by simpler circumference changes as compared with changes in limb volume. Ninety breast cancer patients were prospectively enrolled in an academic trial, and seven upper extremity circumferences were measured quarterly for 3 years. A 10% volume increase or greater than 1 cm increase in arm circumference identified lymphedema with verification by a lymphedema specialist. Sensitivity and specificity of several different criteria for detecting lymphedema were compared using the academic trial as the standard.",
        "gold_tokens": ["maybe", "circumference"],
    },
    {
        "kind": "qa",
        "topic_id": "PQ-14",
        "topic": "PubMedQA · mesocolon invasion / T4 staging (maybe)",
        "question": "Should direct mesocolon invasion be included in T4 for the staging of gastric cancer?",
        "context": "One of the sites most frequently invaded by gastric cancer is the mesocolon; however, the UICC does not mention this anatomical site as an adjacent structure involved in gastric cancer. The purpose of this study was to characterize and classify mesocolon invasion from gastric cancer. We examined 806 patients who underwent surgery for advanced gastric carcinoma from 1992 to 2007 at the Department of Surgery, Gangnam Severance Hospital, Korea. Among these, patients who showed macroscopically direct invasion into the mesocolon were compared to other patients with advanced gastric cancer.",
        "gold_tokens": ["maybe", "T4"],
    },
]

# 1703.10344 "Automated News Suggestions for Populating Wikipedia Entity Pages"
# (Besancon et al. 2017). Numbers anchored in the abstract — Session 19.
NEWS_WIKIPEDIA_SCENARIOS: List[Dict[str, Any]] = [
    {
        "kind": "qa",
        "topic_id": "QA-11",
        "topic": "News-suggestion precision (article-entity)",
        "seed_id": "1703.10344",
        "question": "What is the highest precision reported for the article-entity suggestion stage?",
        "gold_tokens": ["93%"],
    },
    {
        "kind": "qa",
        "topic_id": "QA-12",
        "topic": "News-suggestion precision (article-section)",
        "seed_id": "1703.10344",
        "question": "What is the precision reported for the article-section placement stage?",
        "gold_tokens": ["84%"],
    },
]

_QA_RUBRIC_PROMPT = (
    "You grade whether a generated research artifact answers a factual question "
    "correctly and with grounded citations. The artifact was produced from "
    "sourced papers (inline arXiv cites). Score:\n"
    "- correctness (1-5): does the artifact state the correct, specific answer? "
    "5 = complete and precise; 3 = partially correct; 1 = wrong or evasive\n"
    "- groundedness (1-5): is every answer claim backed by an inline arXiv cite "
    "that supports it (no invented numbers/facts)?\n"
    "Respond ONLY as JSON {\"correctness\": int, \"groundedness\": int, "
    "\"feedback\": str}."
)


def score_qa(client: LLMClient, question: str, artifact: str) -> Dict[str, Any]:
    """Judge correctness + groundedness of the artifact as an answer to `question`."""
    r = client.chat(
        [
            Message(role="system", content=_QA_RUBRIC_PROMPT),
            Message(role="user",
                    content=f"Question: {question}\n\nArtifact:\n{artifact[:20000]}"),
        ],
        json_mode=True,
        max_tokens=1000,
    )
    obj = parse_json_dict(r.text)
    if not isinstance(obj, dict):
        # Last-resort recovery for a judge reply truncated by max_tokens /
        # service hiccups: pull the integer fields directly off the raw text.
        corr = re.search(r'"correctness"\s*:\s*(\d+)', r.text)
        grou = re.search(r'"groundedness"\s*:\s*(\d+)', r.text)
        if corr and grou:
            obj = {"correctness": int(corr.group(1)), "groundedness": int(grou.group(1)),
                   "feedback": r.text[:300]}
        else:
            return {"correctness": 0, "groundedness": 0, "coverage": 0,
                    "error": f"unparseable: {r.text[:120]!r}"}
    try:
        correctness = int(obj.get("correctness", 0))
        groundedness = int(obj.get("groundedness", 0))
    except (TypeError, ValueError):
        correctness = groundedness = 0
    return {
        "correctness": max(0, min(5, correctness)),
        "groundedness": max(0, min(5, groundedness)),
        "feedback": str(obj.get("feedback", ""))[:300],
        "coverage": 2,
    }


def load_topics() -> List[Dict[str, str]]:
    """Return the 30 DAS-Bench topics from the local topics.json (for reference)."""
    if not TOPICS_JSON.is_file():
        return []
    with TOPICS_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def reference_means() -> Dict[str, Dict[str, float]]:
    """Published DAS-Bench main results (Total Avg + family avgs), directional."""
    if not RESULTS_CSV.is_file():
        return {}
    out: Dict[str, Dict[str, float]] = {}
    with RESULTS_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        method = " ".join((row.get("Category", "") or "").split()).strip()
        name = " ".join((row.get("Method", "") or "").split()).strip()
        key = name or method
        vals: Dict[str, float] = {}
        for col, short in (("BSC_Avg", "BSC"), ("MAR_Avg", "MAR"),
                           ("TSQ_Avg", "TSQ"), ("HDQ_Avg", "HDQ"),
                           ("Total_Avg", "Total")):
            try:
                vals[short] = float(row.get(col, "") or "nan")
            except ValueError:
                continue
        if vals:
            out[key] = vals
    return out


_MAX_ARTIFACT_CHARS = 40_000  # full manuscript (abstract+sections+table+refs) must be viewable


def score_survey(client: LLMClient, topic: str, artifact: str) -> Dict[str, Any]:
    """Ask an LLM judge to score `artifact` on the 16 DAS-Bench criteria.

    Returns {"scores": {criterion: int}, "coverage": n/16, "error": str?}.
    Never raises: parse/network failures degrade to a low-coverage dict.
    """
    r = client.chat(
        [
            Message(role="system", content=_BENCH_RUBRIC_PROMPT),
            Message(role="user",
                    content=f"Topic: {topic}\n\nArtifact:\n{artifact[:_MAX_ARTIFACT_CHARS]}"),
        ],
        json_mode=True,
        max_tokens=700,
    )
    obj = parse_json_dict(r.text)
    raw = obj.get("scores") if isinstance(obj, dict) else None
    if not isinstance(raw, dict):
        return {"scores": {}, "coverage": 0, "error": f"unparseable: {r.text[:120]!r}"}

    scores: Dict[str, int] = {}
    norm = {str(k).split(": ", 1)[-1].strip(): v for k, v in raw.items()}
    for family, criterion in DAS_16:
        v = norm.get(criterion)
        if v is None:  # tolerate "BSC: <criterion>" / "<criterion>" variants
            v = raw.get(f"{family}: {criterion}")
        try:
            scores[criterion] = int(v)
        except (TypeError, ValueError):
            continue
    return {
        "scores": scores,
        "coverage": len(scores),
        "judge_model": getattr(client, "model", "?"),
    }


def _family_avgs(scores: Dict[str, int]) -> Dict[str, Optional[float]]:
    avgs: Dict[str, Optional[float]] = {}
    for family in ("BSC", "MAR", "TSQ", "HDQ"):
        vals = [scores[c] for f, c in DAS_16 if f == family and c in scores]
        avgs[family] = statistics.mean(vals) if vals else None
    return avgs


def run_scenarios(client: LLMClient, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    import time as _t
    from tools.pipeline.corpus import md_path_for
    from tools.pipeline.answer import answer_question, check_answer

    out: List[Dict[str, Any]] = []
    for s in scenarios:
        row: Dict[str, Any] = {"scenario": s}
        t0 = _t.perf_counter()
        seed = s.get("seed_id")
        if seed:
            # Qasper/BenchQA contract: question + its source paper → grounded
            # extractive answer (not a survey about the paper).
            md_path = md_path_for(seed)
            if not md_path:
                res = {"candidates": [], "papers": [], "paper_id": "",
                       "output": "", "draft": "", "claims": [],
                       "validation": {"passed": False, "score": 0.0,
                                      "error": "no parsed corpus for seed"}}
            else:
                md = md_path.read_text(encoding="utf-8")
                out_txt = answer_question(client, s["question"], seed, md)
                res = {"candidates": [], "papers": [{"arxiv_id": seed, "path": str(md_path)}],
                       "paper_id": seed, "output": out_txt, "draft": out_txt,
                       "claims": [], "validation": check_answer(out_txt, seed)}
        elif s.get("context"):
            # SciQ-style provided-context MCQ: the support sentence is the source.
            mode = "yesno" if (s.get("yesno") or s["topic_id"].startswith("PQ-")) else ""
            out_txt = answer_question(client, s["question"], "SciQ:ctx", s["context"], mode=mode)
            res = {"candidates": [], "papers": [], "paper_id": "ctx",
                   "output": out_txt, "draft": out_txt, "claims": [],
                   "validation": check_answer(out_txt, "SciQ:ctx", require_cite=False)}
        elif s.get("papers"):
            # Prebuilt evidence pool (30-topic battery, tools/eval/pools_30.py):
            # skip live discovery — the pool IS the evidence. Invoke the graph
            # with the same state shape `Pipeline.run` builds internally.
            papers = s["papers"]
            q = s["question"]
            p = Pipeline(client)
            state = {
                "paper_id": papers[0]["arxiv_id"],
                "parsed_md": papers[0]["md"],
                "papers": papers,
                "question": q,
                "iteration": 0,
            }
            res = p.graph.invoke(state)
            res["candidates"] = s.get("candidates", [])
        else:
            p = Pipeline(client)
            question = s["question"]
            res = p.run(question=question)
        row["elapsed"] = res.get("_elapsed", _t.perf_counter() - t0)
        row["paper_id"] = res.get("paper_id", "")
        row["papers"] = res.get("papers", [])
        row["n_cited"] = (res.get("validation") or {}).get("n_papers_cited", 0)
        row["l6"] = dict(res.get("validation") or {})
        artifact = res.get("output", "") or ""
        if artifact and "\n## Sources (" in artifact:
            artifact = artifact.split("\n## Sources (", 1)[0].rstrip()
        row["artifact_chars"] = len(artifact)
        if not artifact:
            row["status"] = "no-evidence"
        elif s["kind"] == "qa":
            row["status"] = "scored"
            low = artifact.lower()
            gold = s.get("gold_tokens", [])
            hits = [t for t in gold if t.lower() in low]
            row["pdf"] = _render_manuscript(s, artifact)
            qa = score_qa(client, s["question"], artifact)
            qa["gold_hits"] = f"{len(hits)}/{len(gold)}"
            row["qa"] = qa
        else:
            row["status"] = "scored"
            row["pdf"] = _render_manuscript(s, artifact)
            row["bench"] = score_survey(client, s["topic"], artifact)
        out.append(row)
    return out


def _render_manuscript(scenario: Dict[str, Any], artifact: str) -> Dict[str, Any]:
    """Best-effort render of the Markdown manuscript to PDF for MAR scoring.

    Returns {"pdf": str, "pages": int} (pages = 0 when rendering unavailable).
    """
    from pathlib import Path
    from tools.eval.render_manuscript import render_to_pdf

    md_dir = Path(DEFAULT_OUT).parent / "manuscripts"
    md_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{scenario.get('topic_id', 'manu')}_manuscript"
    md_path = md_dir / f"{stem}.md"
    pdf_path = md_dir / f"{stem}.pdf"
    try:
        md_path.write_text(artifact, encoding="utf-8")
    except OSError:
        return {"pdf": "", "pages": 0}
    pages = render_to_pdf(md_path, pdf_path, title=str(scenario.get("question", ""))[:80])
    return {"pdf": str(pdf_path), "pages": pages}


def format_report(rows: List[Dict[str, Any]], ref: Dict[str, Dict[str, float]]) -> str:
    L: List[str] = []
    add = L.append
    add("# DAS-Bench-style evaluation pilot — research_foodie preview")
    add("")
    add("> Updated: 2026-09-16 · scorer = this repo's LLM judge (default "
        "`opencode/big-pickle`), NOT DAS-Bench's frozen ≥300B judge")
    add(">")
    add("> Status: **preview / directional only**. Full DAS-Bench compliance is "
        "out of reach in this env (see feasibility matrix at the end).")
    add("")

    scored = [r for r in rows if r["status"] == "scored"]
    das = [r for r in scored if "bench" in r]
    qa = [r for r in scored if "qa" in r]
    add(f"## Run summary")
    add("")
    add("| id | kind | paper | candidates | papers | cited | out chars | pdf pg | L6 | internal judge | DAS-16 cov. |")
    add("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        paper = r.get("paper_id") or "-"
        cands = ",".join(c.get("arxiv_id", "?") for c in r.get("candidates", [])) or "-"
        np = len(r.get("papers") or [])
        nc = r.get("n_cited", 0)
        pages = (r.get("pdf") or {}).get("pages", "-") if r.get("pdf") else "-"
        l6 = (_fmt(r["l6"].get("score")) if r.get("l6") else "-")
        j = (r["l6"].get("judge") or {}) if r.get("l6") else {}
        ji = f"{j.get('label','-')}@{_fmt(j.get('score'))}" if j else "-"
        cov = "-"
        if r.get("bench"):
            cov = f"{r['bench']['coverage']}/16"
        elif r.get("qa"):
            qa_ = r["qa"]
            cov = f"gold {qa_.get('gold_hits','-')}"
            ji = f"QA {qa_.get('correctness','-')}/{qa_.get('groundedness','-')}"
        add(f"| {r['scenario']['topic_id']} | {r['scenario']['kind']} | {paper} | "
            f"{cands} | {np} | {nc} | {r.get('artifact_chars','-')} | {pages} | {l6} | {ji} | {cov} |")
    if not scored:
        add("\nAll scenarios produced **no evidence** (no parsed corpus match).")
    add("")

    for r in qa:
        s = r["scenario"]
        add(f"## {s['topic_id']} · {s['topic']}")
        add("")
        add(f"- question: {s['question']}")
        add(f"- paper_id: {r.get('paper_id')} · evidence chars: {r.get('artifact_chars')} · "
            f"elapsed: {r.get('elapsed', 0):.1f}s" + (" · **cached (vintage run)**" if r.get("cached") else ""))
        qa_ = r["qa"]
        add(f"- QA judge: correctness **{qa_.get('correctness','-')}/5** · "
            f"groundedness **{qa_.get('groundedness','-')}/5** · gold-token hit "
            f"**{qa_.get('gold_hits','-')}**")
        if qa_.get("feedback"):
            add(f"   - judge feedback: {qa_['feedback']}")
        add("")

    for r in das:
        s = r["scenario"]
        add(f"## {s['topic_id']} · {s['topic']}")
        add("")
        add(f"- paper_id: {r.get('paper_id')} · evidence chars: {r.get('artifact_chars')} · "
            f"elapsed: {r.get('elapsed', 0):.1f}s" + (" · **cached (vintage run)**" if r.get("cached") else ""))
        pdfi = r.get("pdf") or {}
        if pdfi.get("pdf"):
            add(f"- rendered manuscript (MAR): `{pdfi['pdf']}` · **{pdfi.get('pages', 0)} pages**")
        add(f"- L6 gate: score {_fmt(r['l6'].get('score'))} passed={r['l6'].get('passed')} · "
            f"internal P3 judge: {r['l6'].get('judge', {}).get('label')}@{_fmt(r['l6'].get('judge', {}).get('score'))}")
        b = r["bench"]
        for family in ("BSC", "MAR", "TSQ", "HDQ"):
            line = " · ".join(
                f"{c}: {b['scores'].get(c, '-')}" for f2, c in DAS_16 if f2 == family
            )
            add(f"- **{family}** — {line}  (avg {_fmt(_family_avgs(b['scores']).get(family))})")
        tot = [v for v in b["scores"].values()]
        total = statistics.mean(tot) if tot else None
        add(f"- **Total Avg**: {_fmt(total)}  (coverage {b['coverage']}/16, "
            f"judge={b.get('judge_model')})")
        if b.get("error"):
            add(f"- ⚠ judge error: {b['error']}")
        add("")

    if qa:
        add("## QA pilot — evidence-grounded answers (preview)")
        add("")
        add("| id | correctness (5) | groundedness (5) | gold-token hit | pdf pg |")
        add("|---|---|---|---|---|")
        for r in qa:
            qa_ = r["qa"]
            pages = (r.get("pdf") or {}).get("pages", "-") if r.get("pdf") else "-"
            add(f"| {r['scenario']['topic_id']} | {qa_.get('correctness','-')} | "
                f"{qa_.get('groundedness','-')} | {qa_.get('gold_hits','-')} | {pages} |")
        if len(qa) >= 3:
            m_c = statistics.mean([r["qa"]["correctness"] for r in qa if r["qa"].get("correctness")])
            m_g = statistics.mean([r["qa"]["groundedness"] for r in qa if r["qa"].get("groundedness")])
            add(f"| **mean (n={len(qa)})** | **{_fmt(m_c)}** | **{_fmt(m_g)}** | - | - |")
        add("")

    if das:
        add("## Family means across scored scenarios (preview)")
        add("")
        add("| method | BSC | MAR | TSQ | HDQ | Total |")
        add("|---|---|---|---|---|---|")
        # our pilot row
        fams: Dict[str, List[float]] = {f: [] for f in ("BSC", "MAR", "TSQ", "HDQ")}
        totals: List[float] = []
        for r in das:
            fa = _family_avgs(r["bench"]["scores"])
            for f in fams:
                if fa.get(f) is not None:
                    fams[f].append(fa[f])
            tot = [v for v in r["bench"]["scores"].values()]
            if tot:
                totals.append(statistics.mean(tot))
        m = lambda xs: statistics.mean(xs) if xs else None  # noqa: E731
        add(f"| research_foodie (preview, n={len(das)}) | {_fmt(m(fams['BSC']))} | "
            f"{_fmt(m(fams['MAR']))} | {_fmt(m(fams['TSQ']))} | {_fmt(m(fams['HDQ']))} | "
            f"{_fmt(m(totals))} |")
        for name, v in ref.items():
            if v.get("Total") is None:
                continue
            add(f"| {name} (published) | {_fmt(v.get('BSC'))} | {_fmt(v.get('MAR'))} | "
                f"{_fmt(v.get('TSQ'))} | {_fmt(v.get('HDQ'))} | {_fmt(v.get('Total'))} |")
        add("")
        add("> ⚠ Directional only: published rows used a multi-paper survey "
            "artifact, a ≥300B frozen judge, rendered pages (MAR) and DAS-2M "
            "pools; our preview artifacts are single-paper grounded summaries "
            "scored by the local judge. Not comparable head-to-head.")
        add("")

    add("## Feasibility matrix — is DAS-Bench usable in this env?")
    add("")
    add("| asset | status | notes |")
    add("|---|---|---|")
    add("| `benchmark/topics.json` (30 topics) | ✅ local | used verbatim (001, 019 probed) |")
    add("| `benchmark/evaluation_protocol.md` (16 criteria) | ✅ local | re-implemented here (frozen judge prompt is not public) |")
    add("| `results/main_results_30_topics.csv` | ✅ local | benchmark published scores (context only) |")
    add("| `evaluation/*.py` + `run_eval_all.sh` | ✅ local | full harness present (BSC/MAR/TSQ/HDQ) |")
    add("| DAS-2M candidate-paper metadata pool | ⛔ Hugging Face | not fetched (network); task pools are the benchmark input |")
    add("| gold source PDFs / reference surveys | ⛔ Hugging Face | not fetched |")
    add("| ≥300B-class frozen judge | ⛔ keys/GPU | config.json also supports a local OpenAI-compatible judge endpoint |")
    add("| MAR rendered-page scoring (dpi/binary) | ⛔ env | needs PDF page rendering + binary scoring |")
    add("| multi-paper evidence per topic | 🟡 2/30 | corpus has 2 parsed papers; DAS topics map to neither → no-evidence rows |")
    add("| `external/DAS/DAS-Bench` worktree | ✅ | read-only reference harness |")
    add("")
    add("## Full-compliance checklist (to actually *run* DAS-Bench)")
    add("")
    add("1. Fetch DAS-2M metadata + topic pools (Hugging Face) and the gold surveys/PDFs.")
    add("2. Build multi-paper evidence per topic (extend S_lit to fetch + parse top-k full texts).")
    add("3. Run the released `run_eval_all.sh` evaluators (needs PDF rendering for MAR).")
    add("4. Use a ≥300B judge (cloud key or a local OpenAI-compatible endpoint).")
    add("5. Report frozen-judge prompt, model id, temperature, aggregation — per protocol.")
    return "\n".join(L)


def _fmt(x: Optional[float], nd: int = 2) -> str:
    return "-" if x is None else f"{x:.{nd}f}"


def _serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-safe copy of a scenario row (for the sidecar cache)."""
    safe = dict(row)
    safe["scenario"] = dict(row["scenario"])
    safe["papers"] = [dict(p) for p in row.get("papers") or []]
    safe["candidates"] = [dict(c) for c in row.get("candidates") or []]
    safe["l6"] = dict(row.get("l6") or {})
    return safe


def _save_cache(rows: List[Dict[str, Any]], cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        (cache_dir / f"{r['scenario']['topic_id']}.json").write_text(
            json.dumps(_serialize_row(r), ensure_ascii=False), encoding="utf-8")


def _load_cache(ids: List[str], cache_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Load cached rows for `ids`; mark them so the report can flag vintage."""
    out: Dict[str, Dict[str, Any]] = {}
    for tid in ids:
        p = cache_dir / f"{tid}.json"
        if not p.is_file():
            continue
        try:
            row = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        row["cached"] = True
        out[tid] = row
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="DAS-Bench-style benchmark pilot")
    ap.add_argument("--backend", default="opencode")
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--scenarios", default=None,
                    help="comma-separated proxy|das topic ids to run (default: all)")
    args = ap.parse_args()

    client = LLMClient(backend=args.backend, base_url=args.base_url, model=args.model)
    all_scenarios = SCENARIOS + QA_SCENARIOS + QASPER_SCENARIOS + SCIQ_SCENARIOS + PubMedQA_SCENARIOS + NEWS_WIKIPEDIA_SCENARIOS
    scenarios = all_scenarios
    run_ids: List[str] = [s["topic_id"] for s in all_scenarios]
    if args.scenarios:
        run_ids = [x.strip() for x in args.scenarios.split(",")]
        scenarios = [s for s in all_scenarios if s["topic_id"] in run_ids]

    print(f"[bench] backend={args.backend} running={run_ids}")

    cache_dir = Path(DEFAULT_OUT).parent / "bench_cache"
    rows = run_scenarios(client, scenarios)
    _save_cache(rows, cache_dir)

    # Merge cached rows for scenarios NOT re-run (keeps the report canonical
    # without re-paying the LLM cost; cached rows are flagged vintage).
    if len(run_ids) < len(all_scenarios):
        cached = _load_cache([s["topic_id"] for s in all_scenarios if s["topic_id"] not in run_ids], cache_dir)
        if cached:
            print(f"[bench] merged cached rows for {sorted(cached)} (vintage, read-only)")
        merged: List[Dict[str, Any]] = []
        by_id = {r["scenario"]["topic_id"]: r for r in rows}
        for s in all_scenarios:
            if s["topic_id"] in by_id:
                merged.append(by_id[s["topic_id"]])
            elif s["topic_id"] in cached:
                merged.append(cached[s["topic_id"]])
        rows = merged

    ref = reference_means()
    report = format_report(rows, ref)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"[bench] wrote {out}")

    # console summary
    for r in rows:
        s = r["scenario"]
        if r["status"] == "no-evidence":
            print(f"  {s['topic_id']:>6} {s['kind']:>5}  NO-EVIDENCE "
                  f"cands={[c.get('arxiv_id') for c in r.get('candidates', [])]}")
        elif r.get("qa"):
            qa_ = r["qa"]
            print(f"  {s['topic_id']:>6} {s['kind']:>5}  paper={r.get('paper_id')} "
                  f"QA c={qa_.get('correctness','-')} g={qa_.get('groundedness','-')} "
                  f"gold={qa_.get('gold_hits','-')} L6={_fmt(r['l6'].get('score'))} "
                  f"L6pass={r['l6'].get('passed')}")
        else:
            b = r["bench"]
            tot = statistics.mean(b["scores"].values()) if b["scores"] else None
            print(f"  {s['topic_id']:>6} {s['kind']:>5}  paper={r.get('paper_id')} "
                  f"total={_fmt(tot)} cov={b['coverage']}/16 "
                  f"judge={b.get('judge_model')} L6={_fmt(r['l6'].get('score'))} "
                  f"L6pass={r['l6'].get('passed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
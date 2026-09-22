"""User-facing survey CLI driver: run the full pipeline on a free-text question.

This is the "run my research question" entry point behind the web form.

    python -m tools.pipeline.run_survey --question "GPT detectors bias against non-native writers"
    python -m tools.pipeline.run_survey "GPT detectors..." --profile free-opencode --backend arxiv
    python -m tools.pipeline.run_survey --question "..." --mock       # deterministic demo (offline)

Pipeline: discovery rails -> resolved evidence pool -> S_lit -> S_org (outline) ->
S_write (grounded claims) -> L6 gate -> P3 judge -> Markdown manuscript (+ best-effort
PDF render). Every stage prints a `[survey]`-prefixed line flushed immediately so the
web dashboard's SSE tail / log shows real progress, not a frozen run. **The mode is
always printed** (`MODE: MOCK` vs `MODE: REAL`) so a demo can never be mistaken for a
fresh live result. A final `[survey-result]` JSON line lets the dashboard render
manuscript/PDF links.

`--mock` spins the deterministic offline OpenAI server (same as `test_pipeline mock`)
and writes to `_eval_out/mock_manuscripts/` so demo artifacts never pollute real ones.
Per-node timings are printed so wall-clock hotspots are visible for optimization.

Exit codes: 0 = manuscript written (gate passed or passed-with-revise), 1 = produced
nothing usable, 2 = usage error.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
from pathlib import Path
from typing import Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from tools.llm.client import LLMClient  # noqa: E402
from tools.llm.profiles import load_profile, clients_for, profile_header  # noqa: E402
from tools.pipeline.graph import Pipeline  # noqa: E402
from tools.pipeline.corpus import discover, resolved_evidence  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_REAL = REPO_ROOT / "_eval_out" / "manuscripts"
OUT_MOCK = REPO_ROOT / "_eval_out" / "mock_manuscripts"


def _slug(question: str, max_len: int = 48) -> str:
    import re
    keep = [c.lower() if c.isalnum() or c in "-_" else " " for c in question]
    slug = re.sub(r"\s+", "-", "".join(keep).strip())
    return (slug[:max_len] or "survey").rstrip("-")


def _render(md_path: Path, question: str) -> dict:
    from tools.eval.render_manuscript import render_to_pdf
    pdf_path = md_path.with_suffix(".pdf")
    try:
        pages = render_to_pdf(md_path, pdf_path, title=question[:80])
        return {"pdf": str(pdf_path), "pages": pages}
    except Exception as e:  # noqa: BLE001
        print(f"[survey] PDF render skipped: {e}", flush=True)
        return {"pdf": "", "pages": 0}


def _stage(stage: str, status: str, tech: Optional[dict] = None, dur_s: float = 0.0):
    """Emit a machine-readable stage event for the dashboard's research-workflow view.

    `status` is 'start' | 'done'. The frontend renders a research-workflow mission
    panel from these events (business framing is added client-side per stage id).
    """
    payload = {"id": stage, "status": status, "dur_s": round(dur_s, 1)}
    if tech:
        payload["tech"] = tech
    print(f"[survey-stage] {json.dumps(payload)}", flush=True)


class _TimedPipeline(Pipeline):
    """Same graph, but wraps every node with a per-node wall-clock timer.

    Node timing is the first step of any performance pass: it shows exactly which
    LLM call dominates (S_org outline vs S_write claims vs revise_para vs L6 gate).
    Each node also emits a [survey-stage] event so the dashboard can narrate the
    research workflow in business terms, not just raw metrics.
    """

    STAGE_OF_NODE = {
        "_lit": "synthesize",        # S_lit — synthesise the evidence base
        "_org": "outline",           # S_org — build the article plan
        "_write": "write",           # S_write — grounded drafting
        "_review": "write",          # revise — the write loop continues
        "_revise_para": "write",
        "_finalize": "finalize",     # assemble abstract/refs/audit annex
        "_gate": "gate",             # L6 deterministic gate
        "_judge": "judge",           # P3 academic-judge gate
    }
    _started: set = set()

    def _build(self):
        def wrap(name: str, fn):
            def timed(state):
                stage = self.STAGE_OF_NODE.get(f"_{name}") or name
                if stage not in self._started:
                    self._started.add(stage)
                    _stage(stage, "start")
                t0 = time.time()
                try:
                    out = fn(state)
                except Exception as e:  # noqa: BLE001
                    print(f"[survey]   node {name:<12} FAILED: {e}", flush=True)
                    raise
                dt = time.time() - t0
                print(f"[survey]   node {name:<12} {dt:6.1f}s", flush=True)
                _stage(stage, "done", tech={"node": name}, dur_s=dt)
                return out
            return timed

        for node in ("_lit", "_org", "_write", "_revise_para",
                     "_finalize", "_gate", "_judge", "_review"):
            if hasattr(self, node):
                setattr(self, node, wrap(node.lstrip("_"), getattr(self, node)))
        return super()._build()


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="run a grounded survey on a research question")
    ap.add_argument("--question", required=True, help="free-text research question")
    ap.add_argument("--profile", default=None, help="model profile (free-opencode|openai-compat|judge-strong)")
    ap.add_argument("--backend", default=None, help="discovery rail override (seed|arxiv|orx)")
    ap.add_argument("--out", default=None, help="output directory (default _eval_out/manuscripts)")
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF render")
    ap.add_argument("--mock", action="store_true",
                    help="deterministic offline demo (labeled MOCK) — repeatable, ~seconds")
    ap.add_argument("--fast", action="store_true",
                    help="performance: cap revisions at 1 (no revise_para loop) — _write runs once")
    args = ap.parse_args(argv)

    question = args.question.strip()
    if not question:
        print("[survey] empty question", file=sys.stderr)
        return 2

    mode = "MOCK" if args.mock else "REAL"
    print(f"[survey] MODE: {mode}", flush=True)
    print(f"[survey] {'deterministic offline demo — repeatable, labeled, NOT a live result' if args.mock else 'live run on the configured free model lane — temperature > 0, directional'}",
          flush=True)

    profile = load_profile(args.profile or "free-opencode")
    print(f"[survey] {profile_header(profile)}", flush=True)
    print(f"[survey] question: {question!r}", flush=True)
    print(f"[survey] discovery backend: {args.backend or 'env default (seed|arxiv|orx)'}", flush=True)
    if args.fast:
        print("[survey] --fast: single-pass write (revisions capped at 1)", flush=True)

    client = judge_client = None
    if not args.mock:
        client, judge_client = clients_for(profile)
        if not client.is_reachable():
            print("[survey] model lane unreachable — nothing will run", file=sys.stderr)
            return 1
    else:
        # deterministic offline server (same one test_pipeline mock uses)
        import socket
        import subprocess
        port = socket.socket(); port.bind(("127.0.0.1", 0))
        free = port.getsockname()[1]; port.close()
        proc = subprocess.Popen(
            [sys.executable, "-m", "tools.llm.mock_openai_server",
             "--host", "127.0.0.1", "--port", str(free)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        base = f"http://127.0.0.1:{free}/v1"
        client = LLMClient(backend="openai", base_url=base, model="mock")
        judge_client = client
        deadline = time.time() + 20
        while time.time() < deadline:
            if client.is_reachable():
                break
            time.sleep(0.3)
        print(f"[survey] mock server up at {base}", flush=True)

    _stage("discover", "start", tech={"backend": args.backend or "env-default"})
    print("[survey] stage 1/5  discovery rails", flush=True)
    t0 = time.time()
    t1 = t0
    try:
        candidates = discover(question, backend=args.backend)
        papers = resolved_evidence(question, limit=3, backend=args.backend)
    except Exception as e:  # noqa: BLE001
        _stage("discover", "done", tech={"error": str(e)})
        print(f"[survey] discovery failed: {e}", flush=True)
        return 1
    t2 = time.time()
    print(f"[survey]   candidates={len(candidates)}  evidence pool={len(papers)} papers  ({t2 - t1:.1f}s)", flush=True)
    _stage("discover", "done", tech={"candidates": len(candidates)}, dur_s=t2 - t1)
    _stage("evidence", "done", tech={"pool_size": len(papers)}, dur_s=0.0)
    if not papers:
        print("[survey] no parsed evidence found — nothing grounded to write. Try a different question.", flush=True)
        return 1

    max_revisions = 1 if args.fast else 2
    pipeline = _TimedPipeline(client, max_revisions=max_revisions, judge_client=judge_client)
    print("[survey] stage 2/5  S_lit→S_org (outline)", flush=True)
    print("[survey] stage 3/5  S_write (grounded claims + BM25 windows)", flush=True)
    print("[survey] stage 4/5  L6 deterministic gate", flush=True)
    result = pipeline.run(question=question, discovery_backend=args.backend)
    elapsed = time.time() - t0
    print(f"[survey] pipeline finished in {elapsed:.1f}s", flush=True)

    validation = result.get("validation") or {}
    passed = bool(validation.get("passed"))
    print(f"[survey] L6 gate passed={passed} score={validation.get('score', 0):.2f}", flush=True)
    print(f"[survey] claims={len(result.get('claims') or [])} papers_cited={validation.get('n_papers_cited', 0)}", flush=True)
    judge = validation.get("judge") or {}
    jc = judge.get("checks") or {}
    print(f"[survey] P3 judge label={judge.get('label')} score={judge.get('score', 0):.1f}", flush=True)
    if isinstance(jc, dict):
        ok = {k: (bool(v) if isinstance(v, bool) else bool(v.get("ok")))
              for k, v in jc.items()}
        print("[survey]   judge checks: " + ", ".join(
            f"{k}={'OK' if ok[k] else '--'}" for k in sorted(ok)), flush=True)

    artifact = result.get("output") or ""
    if not artifact or len(artifact) < 200:
        print("[survey] no usable artifact produced (gate dropped everything?)", flush=True)
        return 1

    out_dir = Path(args.out) if args.out else (OUT_MOCK if args.mock else OUT_REAL)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = _slug(question)
    md_path = (out_dir / slug).with_suffix(".md")
    md_path.write_text(artifact, encoding="utf-8")
    print("[survey] stage 5/5  finalize + manuscript written", flush=True)
    _stage("finalize", "done", tech={"chars": len(artifact)}, dur_s=0.0)

    pdf = {"pdf": "", "pages": 0}
    if not args.no_pdf:
        pdf = _render(md_path, question)
        print(f"[survey] rendered PDF: {pdf['pdf']} ({pdf['pages']} pages)", flush=True)
        _stage("deliver", "done", tech={"pages": pdf.get("pages", 0)}, dur_s=0.0)

    md_rel = str(md_path.relative_to(REPO_ROOT)).replace("\\", "/")
    pdf_rel = str(Path(pdf["pdf"]).relative_to(REPO_ROOT)).replace("\\", "/") if pdf.get("pdf") else ""
    print(f"[survey] DONE ✓  manuscript: {md_path}", flush=True)
    print(f"[survey] open in browser: /manuscripts/{md_path.name}", flush=True)
    if pdf.get("pdf"):
        print(f"[survey] PDF: /manuscripts/{Path(pdf['pdf']).name}", flush=True)
    _summary = {
        "mode": mode.lower(), "question": question, "gate_passed": passed,
        "judge_label": judge.get("label"), "manuscript": md_rel, "pdf": pdf_rel,
        "elapsed_s": round(elapsed, 1),
        "n_papers_cited": validation.get("n_papers_cited", 0),
        "claims": len(result.get("claims") or []),
    }
    print(f"[survey-result] {json.dumps(_summary)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
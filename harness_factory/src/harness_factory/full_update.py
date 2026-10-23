"""One-command full update (P30): the whole observe loop in one instruction.

``harness full-update`` chains every proposal-only half-ring the factory has:
intel (network, skippable) -> probe-domains -> trace-audit -> evolve ->
cycle audit -> scoreboard, then writes one bilingual report
``updates/FULL-UPDATE.md``. Every phase is failure-isolated: a failing phase
reports its error and the rest still run (a phase that fails silently would
fake completeness - M0.3). Nothing here mutates the SSOT; every output is a
proposal for a human (M0.4/M0.8). This is the "say it once" form of the loop:
pull known topics, find unknown clusters, audit traces, audit health, check
the baseline - one instruction, one report, humans decide.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any, Callable

REPORT_REL = "updates/FULL-UPDATE.md"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _phase(report: dict[str, Any], name: str, fn: Callable[[], Any]) -> Any:
    try:
        result = fn()
        report["phases"].append({"name": name, "status": "ok", "result": result})
        return result
    except Exception as exc:  # failure-isolated: never fake a phase (M0.3)
        report["phases"].append(
            {"name": name, "status": "error", "error": f"{type(exc).__name__}: {exc}"}
        )
        return None


def run_full_update(
    root: str | Path, since: str | None = None, offline: bool = False
) -> dict[str, Any]:
    """Run the whole observe loop; returns the phase report and writes the summary."""
    root = Path(root)
    report: dict[str, Any] = {"ts": _now(), "root": str(root), "offline": offline, "phases": []}

    # 1. intel - the only networked phase; skipped offline (the rest need no network)
    if offline:
        report["phases"].append({"name": "intel", "status": "skipped", "why": "offline"})
    else:
        from .collect import feed_provider
        from .refresh import load_sources, run_refresh

        def _intel() -> dict[str, Any]:
            sources = load_sources(None)
            summary = run_refresh(
                root,
                providers=[feed_provider(sources)],
                provider_names=["feed"],
                since=since,
                sources=sources,
                intel=True,
            )
            return {"intel_items": summary["intel_items"], "wrote": "updates/INTEL.md"}

        _phase(report, "intel", _intel)

    # 2. probe-domains - find intel clusters no domain catches
    from . import domain_probe

    def _probe() -> dict[str, Any]:
        proposals = domain_probe.probe(root)
        if proposals:
            domain_probe.emit(root, proposals)
        return {"clusters": len(proposals), "wrote": domain_probe.PROBES_REL}

    _phase(report, "probe-domains", _probe)

    # 3. trace-audit - recorded traces into mutation proposals
    from . import trace_audit

    def _traces() -> dict[str, Any]:
        problems = trace_audit.validate_rules()
        if problems:
            raise ValueError("; ".join(problems))
        proposals = trace_audit.audit(root)
        if proposals:
            trace_audit.emit(root, proposals)
        return {"n_proposals": len(proposals), "wrote": trace_audit.REPORT_REL}

    _phase(report, "trace-audit", _traces)

    # 4. evolve - structural coverage audit into mutation proposals
    from .evolution import run_evolution
    from .refresh import load_sources, load_watchlist

    def _evolve() -> dict[str, Any]:
        summary = run_evolution(root, load_sources(None), load_watchlist())
        return {"n_audits": summary["n_audits"], "n_proposals": summary["n_proposals"]}

    _phase(report, "evolve", _evolve)

    # 5. cycle audit - the round registry's own health
    from . import cycle

    def _cycle() -> dict[str, Any]:
        audit = cycle.audit()
        return {
            "ok": audit["ok"],
            "n_hard": len(audit["problems"]),
            "n_gaps": len(audit["gaps"]),
        }

    _phase(report, "cycle-audit", _cycle)

    # 6. scoreboard - the 1.0 structural baseline check
    from . import scoreboard

    def _sb() -> dict[str, Any]:
        problems = scoreboard.validate_scoreboard()
        if problems:
            raise ValueError("; ".join(problems))
        reports = scoreboard.run_all()
        overall = (sum(r["total"] for r in reports) / len(reports)) if reports else 0.0
        return {"overall": round(overall, 4), "n_tasks": len(reports)}

    _phase(report, "scoreboard", _sb)

    write_report(root, report)
    return report


def render(report: dict[str, Any]) -> str:
    lines = [
        "FULL-UPDATE · 全面更新",
        "",
        f"ts={report['ts']}  root={report['root']}  offline={report['offline']}",
        "",
    ]
    for phase in report["phases"]:
        if phase["status"] == "ok":
            result = json.dumps(phase["result"], ensure_ascii=False)
            lines.append(f"- [{phase['name']:<14}] ok    {result}")
        elif phase["status"] == "skipped":
            lines.append(f"- [{phase['name']:<14}] skip  {phase.get('why', '')}")
        else:
            lines.append(f"- [{phase['name']:<14}] ERROR {phase.get('error', '')}")
    lines.append("")
    lines.append(
        "Human gate · 人工裁决：本报告只含提案与审计结果（M0.4/M0.8）——"
        "接受哪条提案、是否开新域/新能力，由人决定；全部产出在 updates/，删除即撤销。"
    )
    return "\n".join(lines)


def write_report(root: str | Path, report: dict[str, Any]) -> Path:
    path = Path(root) / REPORT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(report), encoding="utf-8")
    return path

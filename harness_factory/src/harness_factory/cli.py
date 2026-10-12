"""Command-line interface: derive / init / explain / check."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from ._version import __version__
from .assemble import write_harness
from .check import check_harness
from .classify import classify
from .derive import derive
from .registry import domain_ids
from .spec import (
    ARTIFACTS,
    COLLABORATION,
    FEATURE_CHOICES,
    FEATURE_FIELDS,
    GROUNDING,
    HORIZONS,
    STAKES,
    TOOL_SURFACES,
    VERIFIABILITY,
    HarnessPlan,
    TaskSpec,
)


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (slug or "harness")[:40]


def _add_task_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task", required=True, help="natural-language task description")
    parser.add_argument("--domain", choices=domain_ids(), help="force a domain")
    parser.add_argument("--goal", default=None, help="explicit goal (optional)")
    parser.add_argument("--horizon", choices=HORIZONS)
    parser.add_argument("--verifiability", choices=VERIFIABILITY)
    parser.add_argument("--stakes", choices=STAKES)
    parser.add_argument("--grounding", choices=GROUNDING)
    parser.add_argument("--artifact", choices=ARTIFACTS)
    parser.add_argument("--tool-surface", dest="tool_surface", choices=TOOL_SURFACES)
    parser.add_argument("--collaboration", choices=COLLABORATION)
    parser.add_argument(
        "--llm",
        action="store_true",
        help="use the LLM classifier if HARNESS_LLM_* is configured",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness",
        description="Derive and scaffold the agent harness any task needs.",
    )
    parser.add_argument("--version", action="version", version=f"harness-factory {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    derive_p = sub.add_parser("derive", help="show the derived harness plan")
    _add_task_args(derive_p)
    derive_p.add_argument("--json", action="store_true", help="emit the plan as JSON")

    init_p = sub.add_parser("init", help="write the harness scaffold to a directory")
    _add_task_args(init_p)
    init_p.add_argument("--out", default=None, help="output directory (default: ./<task-slug>)")
    init_p.add_argument("--force", action="store_true", help="overwrite existing files")

    explain_p = sub.add_parser("explain", help="explain a generated manifest")
    explain_p.add_argument("--dir", default=".", help="directory containing .harness/manifest.json")
    explain_p.add_argument("--manifest", default=None, help="path to a manifest.json")

    check_p = sub.add_parser("check", help="run a generated harness self-check")
    check_p.add_argument("--dir", default=".", help="directory containing .harness/manifest.json")

    refresh_p = sub.add_parser(
        "refresh", help="pull new/leading sources (proposal only; never edits docs)"
    )
    refresh_p.add_argument(
        "--root",
        "--data-dir",
        dest="root",
        default=None,
        help="knowledge-base dir (default: user home; a checkout with review/ also works)",
    )
    refresh_p.add_argument("--inbox", default=None, help="JSONL/JSON of candidates to ingest")
    refresh_p.add_argument("--watchlist", default=None, help="override watchlist.json")
    refresh_p.add_argument("--sources", default=None, help="override sources.json (tracked entities)")
    refresh_p.add_argument(
        "--provider",
        choices=("auto", "file", "llm", "feed", "all"),
        default="auto",
        help="where candidates come from (feed/all use sources.json)",
    )
    refresh_p.add_argument("--intel", action="store_true", help="also extract intel to updates/INTEL.md")
    refresh_p.add_argument("--since", default=None, help="only items published on/after YYYY-MM-DD")
    refresh_p.add_argument("--max-items", dest="max_items", type=int, default=10)
    refresh_p.add_argument("--verify", action="store_true", help="HEAD-check candidate urls")
    refresh_p.add_argument("--dry-run", action="store_true", help="collect+score only; write nothing")
    refresh_p.add_argument("--json", action="store_true")

    apply_p = sub.add_parser(
        "refresh-apply", help="human gate: accept queued candidates into proposal stubs"
    )
    apply_p.add_argument("--root", "--data-dir", dest="root", default=None)
    apply_p.add_argument("--accept", nargs="+", required=True, help="ids/urls/queue-indices")

    sources_p = sub.add_parser(
        "sources", help="list tracked sources (projects/harnesses/venues/people/media)"
    )
    sources_p.add_argument("--sources", default=None, help="override sources.json")
    sources_p.add_argument("--group", default=None, help="restrict to one group")
    sources_p.add_argument("--json", action="store_true")

    intel_p = sub.add_parser(
        "intel", help="pull tracked feeds and extract intel into updates/INTEL.md"
    )
    intel_p.add_argument("--root", "--data-dir", dest="root", default=None)
    intel_p.add_argument("--sources", default=None)
    intel_p.add_argument("--since", default=None, help="only items published on/after YYYY-MM-DD")
    intel_p.add_argument("--json", action="store_true")

    evolve_p = sub.add_parser(
        "evolve", help="self-evolution audit: coverage/gaps -> mutation proposals (no writes to catalogs)"
    )
    evolve_p.add_argument("--root", "--data-dir", dest="root", default=None)
    evolve_p.add_argument("--sources", default=None)
    evolve_p.add_argument("--dry-run", action="store_true")
    evolve_p.add_argument("--json", action="store_true")

    evolve_apply_p = sub.add_parser(
        "evolve-apply", help="human gate: accept evolution proposals into updates/accepted.json"
    )
    evolve_apply_p.add_argument("--root", "--data-dir", dest="root", default=None)
    evolve_apply_p.add_argument("--accept", nargs="+", required=True, help="proposal ids/targets")

    sub.add_parser("doctor", help="show resolved paths, config, and LLM status")

    selfup_p = sub.add_parser(
        "self-update", help="refresh the tool's own catalog from packaged defaults"
    )
    selfup_p.add_argument("--force", action="store_true", help="overwrite existing catalog files")

    return parser


def _overrides(args: argparse.Namespace) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in FEATURE_CHOICES:
        value = getattr(args, key, None)
        if value is not None:
            values[key] = value
    if getattr(args, "domain", None):
        values["domain"] = args.domain
    return values


def _make_plan(args: argparse.Namespace) -> HarnessPlan:
    task = TaskSpec(text=args.task, domain=getattr(args, "domain", None), goal=args.goal)
    features = classify(task, overrides=_overrides(args), use_llm=args.llm)
    return derive(task, features)


def _format_plan(plan: HarnessPlan) -> str:
    f = plan.features
    lines = [
        f"Task   : {plan.task.text}",
        f"Domain : {f.domain}",
        "Features: " + ", ".join(f"{k}={getattr(f, k)}" for k in FEATURE_FIELDS),
        f"Source : {f.source}",
        "Modules:",
    ]
    for m in plan.modules:
        mark = "+" if m.enabled else "-"
        params = f"  {json.dumps(m.params, ensure_ascii=False)}" if m.params else ""
        lines.append(f"  [{mark}] {m.module_id} {m.title_en} / {m.title_zh}{params}")
        for reason in m.reasons:
            lines.append(f"        - {reason}")
    return "\n".join(lines)


def _cmd_derive(args: argparse.Namespace) -> int:
    plan = _make_plan(args)
    if args.json:
        print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_plan(plan))
    return 0


def _cmd_init(args: argparse.Namespace) -> int:
    plan = _make_plan(args)
    out = args.out or str(Path.cwd() / _slug(args.task))
    try:
        written = write_harness(plan, out, force=args.force)
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"harness written to {out} ({len(written)} files)")
    for name in written:
        print(f"  + {name}")

    problems = check_harness(out)
    if problems:
        print("self-check: FAILED", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("self-check: OK")
    return 0


def _cmd_explain(args: argparse.Namespace) -> int:
    manifest = Path(args.manifest) if args.manifest else Path(args.dir) / ".harness/manifest.json"
    if not manifest.exists():
        print(f"error: no manifest at {manifest}", file=sys.stderr)
        return 2
    plan = json.loads(manifest.read_text(encoding="utf-8"))

    features = plan.get("features", {})
    print(f"Task   : {plan.get('task', {}).get('text', '?')}")
    print(f"Version: {plan.get('version', '?')}  Created: {plan.get('created', '?')}")
    print(f"Domain : {features.get('domain')}   Source: {features.get('source')}")
    print("Modules:")
    for module in plan.get("modules", []):
        mark = "+" if module.get("enabled") else "-"
        params = f"  {json.dumps(module.get('params', {}), ensure_ascii=False)}" if module.get(
            "params"
        ) else ""
        print(f"  [{mark}] {module.get('module_id')} {module.get('title_en', '')}{params}")
        for reason in module.get("reasons", []):
            print(f"        - {reason}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    problems = check_harness(args.dir)
    if problems:
        print("self-check: FAILED", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("self-check: OK")
    return 0


def _cmd_refresh(args: argparse.Namespace) -> int:
    from . import config, llm
    from .collect import feed_provider, file_provider, llm_provider
    from .refresh import load_sources, load_watchlist, run_refresh

    root = args.root
    if not root:
        config.ensure_home()
        root = str(config.home())
    inbox = args.inbox or str(Path(root) / "updates" / "inbox.jsonl")
    watchlist = load_watchlist(args.watchlist) if args.watchlist else None
    need_sources = args.provider in ("feed", "all") or args.intel
    sources = load_sources(args.sources) if need_sources else None

    providers = None
    names = None
    if args.provider == "file":
        providers, names = [file_provider(inbox)], ["file"]
    elif args.provider == "llm":
        providers, names = [llm_provider(since=args.since, max_items=args.max_items)], ["llm"]
    elif args.provider == "feed":
        providers, names = [feed_provider(sources)], ["feed"]
    elif args.provider == "all":
        providers, names = [file_provider(inbox), feed_provider(sources)], ["file", "feed"]
        if llm.available():
            providers.append(llm_provider(since=args.since, max_items=args.max_items))
            names.append("llm")

    summary = run_refresh(
        root,
        providers=providers,
        provider_names=names,
        watchlist=watchlist,
        watchlist_path=args.watchlist,
        inbox=inbox,
        since=args.since,
        max_items=args.max_items,
        verify=args.verify,
        dry_run=args.dry_run,
        sources=sources,
        intel=args.intel,
    )

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"refresh @ {summary['root']}  providers={','.join(summary['providers']) or 'none'}")
        print(f"  collected={summary['collected']}  accepted={summary['accepted']}  "
              f"rejected={summary['rejected']}  intel={summary['intel_items']}")
        hot = ", ".join(f"{h['topic']}({h['count']})" for h in summary["hot_topics"]) or "none"
        print(f"  hot topics: {hot}")
        gaps = ", ".join(summary["coverage_gaps"]) or "none"
        print(f"  coverage gaps: {gaps}")
        if not args.dry_run:
            wrote = "updates/REPORT.md, updates/queue.jsonl, updates/JOURNAL.md"
            if args.intel:
                wrote += ", updates/INTEL.md"
            print(f"  wrote {wrote}")
    return 0


def _cmd_sources(args: argparse.Namespace) -> int:
    from .collect import iter_entities
    from .refresh import load_sources

    sources = load_sources(args.sources)
    if args.json:
        print(json.dumps(sources, ensure_ascii=False, indent=2))
        return 0

    for group, entity in iter_entities(sources):
        if args.group and group != args.group:
            continue
        topics = ", ".join(entity.get("topics", []))
        feed = entity.get("feed") or (entity.get("resolve") if entity.get("resolve") else "—")
        print(f"[{group}] {entity.get('id'):<26} {entity.get('name')}")
        print(f"          {entity.get('url')}  feed={feed}")
        if topics:
            print(f"          topics: {topics}")
    return 0


def _cmd_intel(args: argparse.Namespace) -> int:
    from . import config
    from .collect import feed_provider
    from .refresh import load_sources, run_refresh

    root = args.root
    if not root:
        config.ensure_home()
        root = str(config.home())
    sources = load_sources(args.sources)
    summary = run_refresh(
        root,
        providers=[feed_provider(sources)],
        provider_names=["feed"],
        since=args.since,
        sources=sources,
        intel=True,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"intel @ {summary['root']}  items={summary['intel_items']}")
        print(f"  wrote updates/INTEL.md, updates/intel.jsonl, updates/JOURNAL.md")
    return 0


def _cmd_evolve(args: argparse.Namespace) -> int:
    from . import config
    from .evolution import run_evolution
    from .refresh import load_sources, load_watchlist

    root = args.root
    if not root:
        config.ensure_home()
        root = str(config.home())
    sources = load_sources(args.sources)
    watchlist = load_watchlist()
    summary = run_evolution(root, sources, watchlist, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    metrics = summary["metrics"]
    print(f"evolve @ {summary['root'] if 'root' in summary else root}")
    print(f"  entities={metrics['entities']}  coverage={metrics['topic_coverage']:.0%}  "
          f"intel={metrics['intel_items']}")
    print(f"  audits={summary['n_audits']}  proposals={summary['n_proposals']}")
    if args.dry_run:
        print("  dry-run: wrote nothing")
    else:
        print("  wrote updates/EVOLUTION.md, updates/evolution.jsonl, updates/metrics.jsonl")
    return 0


def _cmd_evolve_apply(args: argparse.Namespace) -> int:
    from . import config
    from .evolution import apply_accepted

    root = args.root
    if not root:
        config.ensure_home()
        root = str(config.home())
    applied = apply_accepted(root, args.accept)
    if applied:
        print(f"accepted {len(applied)} proposal(s); ledger at {root}/updates/accepted.json")
        for pid in applied:
            print(f"  + {pid}")
    else:
        print("no matching proposals in updates/evolution.jsonl (nothing accepted)")
    return 0


def _cmd_refresh_apply(args: argparse.Namespace) -> int:
    from . import config
    from .refresh import apply_accepted

    root = args.root
    if not root:
        config.ensure_home()
        root = str(config.home())
    applied = apply_accepted(root, args.accept)
    if applied:
        print(f"accepted {len(applied)} candidate(s); proposals written to {root}/updates/proposals/")
        for title in applied:
            print(f"  + {title}")
    else:
        print("no matching candidates in updates/queue.jsonl (nothing accepted)")
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    from . import config, llm

    existed = config.home().exists()
    home = config.ensure_home()
    seeded = config.seed_catalog()
    catalog_files = sorted(p.name for p in config.catalog_dir().glob("*.json"))

    print(f"harness-factory {__version__}  (python {sys.version.split()[0]})")
    print(f"home        : {home}{'  (created)' if not existed else ''}")
    print(
        f"config      : {config.config_file()}  "
        f"{'[present]' if config.config_file().exists() else '[none]'}"
    )
    print(f"catalog dir : {config.catalog_dir()}  files={catalog_files}")
    print(f"corpus dir  : {config.corpus_dir()}")
    print(f"updates dir : {config.updates_dir()}")
    print(f"llm         : {'configured' if llm.available() else 'not configured (rules only)'}")
    print(f"seed        : added={seeded['added'] or 'none'} kept={seeded['kept'] or 'none'}")
    return 0


def _cmd_self_update(args: argparse.Namespace) -> int:
    from . import config
    from .journal import append_journal

    config.ensure_home()
    result = config.seed_catalog(force=args.force)
    print(f"self-update @ {config.catalog_dir()}")
    print(f"  added: {result['added'] or 'none'}")
    print(f"  kept : {result['kept'] or 'none'} (use --force to overwrite)")
    append_journal(
        config.updates_dir() / "JOURNAL.md",
        [f"self-update added={result['added']} kept={result['kept']} force={args.force}"],
    )
    return 0


def _force_utf8() -> None:
    """Keep bilingual output readable on Windows consoles (cp1252/cp936)."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def main(argv: list[str] | None = None) -> int:
    _force_utf8()
    args = build_parser().parse_args(argv)
    if args.command == "derive":
        return _cmd_derive(args)
    if args.command == "init":
        return _cmd_init(args)
    if args.command == "explain":
        return _cmd_explain(args)
    if args.command == "check":
        return _cmd_check(args)
    if args.command == "refresh":
        return _cmd_refresh(args)
    if args.command == "refresh-apply":
        return _cmd_refresh_apply(args)
    if args.command == "sources":
        return _cmd_sources(args)
    if args.command == "intel":
        return _cmd_intel(args)
    if args.command == "evolve":
        return _cmd_evolve(args)
    if args.command == "evolve-apply":
        return _cmd_evolve_apply(args)
    if args.command == "doctor":
        return _cmd_doctor(args)
    if args.command == "self-update":
        return _cmd_self_update(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

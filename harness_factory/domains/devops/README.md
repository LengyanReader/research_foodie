# Domain · DevOps / platform operations · 运维与平台工程域
> Wiring `core/` modules into a test-gated, observable, reversible delivery path.
> 把 `core/` 模块接线成「测试门禁、可观测、可回退」的交付路径。
**Updated:** 2026-11-07

---

## 中文速览
DevOps 域管的是**把已验产物安全地送达运行环境并保持可观测**，不是 harness 自身的演化（后者见 `harness-evolution/`）。核心风险：**绿流水线≠可用的服务**、**每环境重建=另一产物**、**控制台改基础设施=不可审阅 diff**、**无 SLO/无 runbook/无回滚**。它以 L0–L5 编排 `core/`：L0 定义交付与可靠性目标（M0/M3）、L1 构建一次并记录 digest（M6/M7）、L2 以验收证据过门（M3）、L3 逐环境晋级并 canary（M7）、L4 观测 SLI/SLO 与故障响应（M3/M5）、L5 复盘与回灌（M5/M7）。能力：`delivery-pipeline-discipline` · `service-reliability-discipline` · `infrastructure-as-code-discipline`。

---

## What this domain is for · 用途
Take a verified artifact to a running service — build once, promote the same digest, observe the user-visible signal, and recover safely when it fails. It does **not** govern the harness's own evolution; that is `../harness-evolution/README.md`.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Frame delivery & reliability | M0, M3 | acceptance evidence; SLI/SLO/error budget |
| L1 | Build once | M6, M7 | immutable artifact; record digest |
| L2 | Gate the artifact | M3 | acceptance suite; environment contract |
| L3 | Promote & release | M6, M7 | canary/flag; abort signal; rollback target |
| L4 | Observe & respond | M3, M5 | symptom alerts; runbook; incident roles |
| L5 | Postmortem & improve | M5, M7 | blameless review; owned actions; SLO update |

## Module combination · 模块组合
- **M0** — a green build is not a running service; define done as an observed post-deploy signal.
- **M3** — gate the artifact and observe the service; a missing signal is a failed gate (M3.20).
- **M5** — incidents are mandatory signal; feed postmortem actions into the next gate.
- **M6** — build/promote with a pinned, reproducible toolchain; no console-only state.
- **M7** — releases and infrastructure are reviewable diffs with a named rollback (M7.11).
- **M2** — long-running operations resume from a journal; retries are idempotent.

## Discipline-specific risks · 领域特有风险
- **Green pipeline, unobserved service.**
- **Rebuild per environment** — a different artifact called the same release.
- **Console-only infrastructure** — no review, no drift record, no rollback.
- **No SLO or error budget** — reliability is a feeling, not a measured claim.
- **Incident without a runbook** — mitigation waits on diagnosis.

## Anti-patterns
- Treating CI success as deployment success.
- Promoting a mutable tag (`latest`) instead of a recorded digest.
- Alerting on causes instead of user-visible symptoms.
- Blaming an operator instead of fixing the system.
- Secrets in code or in the plan diff.

## See also
`../core/04-verification-and-gates.md` (M3.20) · `../core/08-change-governance.md` (M7.11) · `../domains/harness-evolution/README.md` (the harness's own evolution) · `../domains/software-engineering/README.md` (change workflow).
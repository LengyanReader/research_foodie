# Security model · 最小权限与安全边界
> Security posture for `harness_factory`: least privilege, read-mostly by default, human-gated writes, reversibility.

**Updated:** 2026-10-14

## 1. 中文速览

`harness_factory` 是**只读优先 + 人工门控写入**的工具：大部分操作不改写注册表（catalog/sources/domains），写入只发生在显式的人机确认路径上，并且全部落在 `updates/`（默认被 git 忽略）。原则是**最小权限（least privilege）**、**可逆（reversible）**、**证据优先（M0.1）**。

## 2. Trust boundary

- **Tracked catalogs (read-only in normal operation):** `src/harness_factory/data/*.json` — SSOT；CLI 的 `derive/catalog/standard list/show/plan` 等大多只读。
- **Mutable outputs (observe-only):** `updates/`（home 或 `--root .`）— `INTEL.md/jsonl`、`EVOLUTION.md`、`metrics.jsonl`、`JOURNAL.md`、`cases.jsonl`、`profile/*`、`proposals/*`、`standard.json`、`accepted.json`。这些是**工件（artifacts）**而非注册表改动。
- **Human gate (M0.8):** `refresh-apply`、`evolve-apply` 只写 `updates/proposals/` 或 `updates/accepted.json`；从不自动合并回 `data/`。采纳是显式动作。
- **Filesystem access:** 工具优先读本仓库内的 JSON；网络抓取限于已跟踪 `sources.json` 中的 `url/feed`（只读拉取），不执行远程代码。
- **Config:** 环境变量 `HARNESS_HOME`、`HARNESS_DATA_DIR`、`HARNESS_USE_HOME_CATALOG` 限定目录边界；默认不跨出工作区。
- **LLM (opt-in):** 仅在配置启用时使用；不传递密钥以外的敏感凭据，默认离线。

## 3. Threat model (minimal)

| surface · 面 | risk · 风险 | mitigation · 缓解 | impact |
|---|---|---|---|
| Network (feeds) | SSRF/malicious feed | 限定 tracked sources（白名单）；只拉取 feed/URL，不跟随任意跳转；读取纯文本/JSON，不执行 JS | low |
| File writes | Path traversal | 使用 `pathlib.Path`、相对根受限于 `--root`/home；`updates/` 隔离 | low |
| Catalog mutation | Unauthorized merge | 没有“auto-apply to data/”路径；`evolve-apply` 只写 `accepted.json`（ledger），采纳需人工编辑 `data/` | low |
| Secrets | Leakage | 禁止日志密钥；不写入 artifacts；`updates/` 可随时删除 | low |
| Long-running agents | State corruption | 状态只写 `updates/`、可从 checkpoint 恢复（`standard.json` append-only 式历史）；可逆删除 | low |

## 4. Principles (enforced by design)

1. **Least privilege** — 只读默认；写入最小必要、范围受限。
2. **Human-in-the-loop (M0.8)** — 所有结构性改动都要显式采纳。
3. **Reversibility (M0.9)** — `updates/` 可整目录删除，不影响 SSOT。
4. **Evidence-first (M0.1)** — bar/claims 要可溯源（http），标杆未核验标为 `unverified`。
5. **No self-declaration (M0.4)** — 工具只测量/记录，不宣称达标。
6. **Observe-only evolution** — `evolve` 只出提案，不改写注册表。

## 5. Operational guidance

- 不要把敏感文件放入 `updates/`（它可能被导出）。
- 生产环境建议将 `HARNESS_HOME` 指向独立目录。
- `harness doctor` 可检查路径解析与配置。

## 6. See also
`../../AGENTS.md`（hard rules）· `../../domains/excellence/README.md`· `../../domains/excellence/self-standard.md`

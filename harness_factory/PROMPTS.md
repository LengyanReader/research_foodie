# Agent prompt templates · 提示词模板

> **Updated:** 2026-10-15 · 从 [`SKILL.md`](SKILL.md) 的「两步：先配置，再提任务」提炼而来，便于直接复制。
> **用法 · How to use：** 把 **① 配置** 贴给任意 vibe-coding 助手**一次**（可存为模板或写进项目规则文件）；
> 之后每次只贴 **② 任务**——同一轮接着写，或**下一轮再发均可**，也可**直接附上文件/目录/链接**。
> 配置固定不变，任务越短越省事。

---

## ① 配置（贴一次，可复用） · Configuration (paste once, reusable)

```text
把本仓库当 skill 使用：读 harness_factory/SKILL.md，按需加载 reference/derivation-rules.md、core/*.md、
data/*.json、domains/<名>/README.md。此后我给你的任务，请据此推导并落盘所需 harness（AGENTS.md +
tasks/* + .harness/*，每条选择写入 .harness/manifest.json），最后跑 check；只提案、不编造任务内容（M0.4）。
若我这条只发了配置、还没给任务，请确认收到并等待，不要提前推导。
```

> 若助手的工作目录不是仓库根，把 `harness_factory/SKILL.md` 换成相对或绝对路径即可（例如从仓库根粘贴就是原样）。
> 只提案、不编造任务实质（M0.4）；破坏性动作（推送 / 发布 / 删除 / 花钱）须人工确认。

---

## ② 任务（同一轮接着写，或下一轮再发） · Task (same turn or next)

直接写目标，或附上文件 / 目录 / 链接。例：

```text
为现有 Python 项目补全类型注解与单元测试，保证可验证闭环。
```

### 变体任务句（按场景替换） · Variant task lines

| 场景 | 任务句（接在 ① 配置之后） |
|---|---|
| 新项目 / 新任务搭 harness | 「为『<目标>』推导并落盘所需 harness。」 |
| 只想先看方案、不落盘 | 「先为『<目标>』推导 harness 方案（逐模块给出规则与理由、能力匹配），**只出方案不写文件**。」 |
| 拆解现有项目、学习其能力 | 「用 `profile` 视角扫描 `<项目路径>`，产出 `PROFILE.md` 并作为一个 case 记录（observe-only）；只观察、不改动该项目。」 |
| 按最高标准定目标 | 「按 `domains/excellence/standard-ladder.md`，为『<目标>』定一个 R4 级 apex bar，列出加权 gap 与补齐配置。」 |

---

## ③ 域任务句（可选，接在 ① 配置之后） · Domain task lines (optional)

**writing 域 · writing domain**

```text
用 writing 域为我建写作 harness：先定 thesis 与 outline，每条 claim 强制配可溯源证据
（semantic-scholar / crossref / openalex），初稿后做 originality check 与校验，再按 writing rubric 自评并棘轮固化（不回退）。
```

**excellence 域 · excellence domain**

```text
用 excellence 域的最高标准棘轮处理 <产出物>：先指名一个可溯源的最高标杆（R4+，给出来源），按本域 rubric
打分 → 审计最大差距 → 逐项提升 → 把达标分固化为新下限（未获人工豁免不得回退），并定期复核标杆是否前移。
```

> 更细的域内指令见各域 README：`domains/<名>/README.md`（如 [`domains/writing/README.md`](domains/writing/README.md)、
> [`domains/excellence/README.md`](domains/excellence/README.md)）。

---

## ④ 存成模板 / 项目规则 · Save as a template / project rule

- **编辑器片段**：把 ① 配置存为 VS Code user snippet（或你惯用的 prompt library），只维护这一处。
- **项目规则文件**：写进目标项目的 `AGENTS.md` / `.cursor/rules` / `CLAUDE.md` 等，使配置对该项目**常驻**，此后每轮只提任务。
- **确定性复现（L1，免安装）**：不想走助手时，直接跑 CLI：

  ```bash
  PYTHONPATH=harness_factory/src python -m harness_factory derive --task "<goal>"
  PYTHONPATH=harness_factory/src python -m harness_factory init   --task "<goal>" --out <project>
  PYTHONPATH=harness_factory/src python -m harness_factory check  --dir <project>
  ```

---

**相关 · Related：** [`SKILL.md`](SKILL.md)（agent 原生入口）· [`introduction.md`](introduction.md)（心智模型 + Quickstart）· [`GUIDE.md`](GUIDE.md)（指南与实例）。

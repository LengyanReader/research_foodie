# Practitioner Playbook · 顶尖实践者技能提炼

> Distilled, project-agnostic skills from Andrej Karpathy and peers of comparable or higher standing, on building reliable agents/harnesses.
> 提炼自 Andrej Karpathy 及同等级/更高等级同行的、与「构建可靠 agent / harness」相关的可迁移技能。
> Sources are listed at the end (IEEE-style). **Updated:** 2026-10-12.

---

## 中文速览

**这份文档做什么。** 把一线最顶级从业者（Karpathy、Sutskever、Sutton、Carmack、Willison、Chollet、Hassabis，以及 Fowler/Böckeler、Hashimoto、Anthropic、OpenAI 的工程团队）关于「如何让 AI agent 可靠工作」的**方法**提炼成**与具体项目无关的操作技能**，并映射到本库的 `core/` 模块。

**一句话结论。** 所有顶尖方法都收敛到同一组不变式：**rigor 不会消失，只会转移**（从写代码转移到写规格、评测与环境）；**「完成」必须是结构性的、有证据的**；**构建者与评判者必须分离**；**给 AI 上缰绳 / 留出人类在关键判断上的控制**；**上下文是稀缺资源**；**能在运行时从经验学习的方法最终胜出**。

**怎么用。** 先看「映射表」找到你要的技能，再读对应小节；每节末尾的 **Apply** 给出可直接落到 harness 的动作。

---

## How to read this · 阅读方式

Each entry gives: **(a)** the practitioner's central idea, **(b)** the *transferable skill* — stated so it applies to any project, **(c)** an **Apply** line and a mapping to `core/` modules. Concrete artifacts from their own projects appear only as **Exemplars**.

---

## Map · 技能 → harness 模块

| Practitioner | Core transferable skill · 核心可迁移技能 | Maps to |
|---|---|---|
| Andrej Karpathy | Keep AI on a leash; autonomy slider; march of nines; context engineering; verifiability spectrum | M0, M1, M4, M8 |
| Ilya Sutskever | Research taste (beauty/simplicity/brain); don't overfit to evals; continual learning | M3, M5, M6 |
| Richard Sutton | Meta-methods over built-in knowledge; runtime learning; agent invents own subproblems | M5, M7 |
| John Carmack | Learn from real experience, not an IID blender; reality is not turn-based | M4, M7 |
| François Chollet | Intelligence = skill-acquisition efficiency; refinement loop; measure efficiency not skill | M3, M5 |
| Simon Willison | Agent = LLM in a loop with tools; lethal trifecta; injection-safe design | M4, M8 |
| Chad Fowler | Relocating rigor: invariants explicit, evaluation rigid, fail loudly | M0, M3, M7 |
| Fowler / Böckeler | Agent = Model + Harness; guides (feedforward) + sensors (feedback) | M1, M3, M7 |
| Mitchell Hashimoto | Harness engineering: every mistake becomes a permanent check | M3, M5, M7 |
| OpenAI Codex team | Agent legibility; AGENTS.md as map; mechanical invariants; garbage collection | M1, M6, M7 |
| Anthropic | Context engineering; generator/evaluator split; default-FAIL contract | M1, M2, M3 |
| Ethan Mollick | Models / apps / harnesses; the harness often matters more than the model | M0, M7 |
| Demis Hassabis | Scientific method as the best tool for AI itself; rigor on claims | M0, M4, M5 |

---

## 1. Andrej Karpathy · 卡帕西

**Central idea.** Software is changing again: 1.0 (hand-written rules) → 2.0 (learned weights) → **3.0 (natural-language programs; the context window is the lever)**. LLMs are fallible "ghosts" — stochastic simulations of people, not reasoning engines — so the engineering problem is *designing systems where their failures land where you can catch them* [1]–[4].

**Transferable skills**

1. **Keep AI on a leash (S1).** Prefer many small, verifiable increments over one giant autonomous blast. A 1,000-line diff you cannot verify is a liability, because *you* remain the bottleneck in the generation–verification loop.
2. **Autonomy slider (S2).** Autonomy is a dial, not a switch. Ship products where you can move from "autocomplete" → "edit one function" → "whole repo" per task risk, and design so the slider can travel rightward over time.
3. **Iron Man suit > Iron Man robot (S3).** Augment a human with fast verify/audit UI (diffs, previews, traces) rather than removing the human. Fast *generation–verification loops* are the real product.
4. **March of nines (S4).** 90% (demo) → 99% → 99.9% → 99.999% each costs roughly as much as all previous effort; end-to-end reliability of an *n*-step workflow ≈ pⁿ, so small per-step error compounds. Match the target nines to the stakes; don't over-engineer the trivial or under-engineer the critical. Beyond the first nines the bottleneck shifts from the *model* to *systems engineering* (schema validation, timeouts, fallbacks, observability).
5. **Context engineering (S5).** "The delicate art and science of filling the context window with just the right information for the next step." It contains prompt engineering as a submodule.
6. **The verifiability spectrum (S6).** Where outputs are cheap to verify (code, math), agents improve fast; where verification is subjective (taste, aesthetics), keep humans in the loop and plan accordingly.
7. **Outsource thinking, not understanding (S7).** You can delegate token production; you cannot delegate *direction* and *judgment*. The scarcest skill is knowing what to build and recognizing when it is right.
8. **Build/verify to understand (S8).** The test of understanding is the ability to rebuild the core from scratch with minimal code; prefer "start from data," "don't be a hero," "resist adding complexity."
9. **Agent-native infrastructure (S9).** Rewrite docs and interfaces to speak the agent's language (machine-readable markdown, `curl`-equivalent actions instead of "click here", protocols like MCP). Meet the agent halfway.
10. **Auto-research / remove yourself as the bottleneck (S10).** Arrange objective, metric, and bounds, then let a loop run without you in the middle; keep a single idea queue with workers pulling items. (His nanochat/GPT-2 harness is the *Exemplar* — a small playground he uses to study recursive self-improvement.)

> **中文**：上缰绳、自主度滑杆、钢铁侠套装、九的进军、上下文工程、可验证性谱系、外包思考不外包理解、构建即理解、agent 原生基建、自动研究。核心：**让失败发生在你能验证的地方**。

**Apply.** For any task, (i) write the per-step success probability and the end-to-end target; (ii) split into verifiable increments; (iii) put a human audit at the irreversible steps; (iv) if a step cannot be verified mechanically, mark it human-gated.

## 2. Ilya Sutskever · 苏茨克沃

**Central idea.** The "age of scaling" (2020–2025) is ending because pre-training data is finite; we return to an **age of research** "just with big computers." The core unsolved problem is **generalization**: models learn dramatically less-sampled and less-robustly than humans, and RL can induce a narrow, eval-overfit tunnel vision [5], [6].

**Transferable skills**

1. **Research taste (S11).** Great ideas feel right from multiple angles at once — "beauty, simplicity, elegance, correct biological inspiration… no room for ugliness." Hold a top-down belief so you don't abandon correct ideas over a bug. Use taste as a *filter*, not a guarantee.
2. **Don't overfit to evals (S12).** Optimizing the measurement (benchmarks, curated demos) produces models that ace tests and fail the world. Guard against "the human researcher as the real reward-hacker."
3. **Value functions as a lever (S13).** A good *value function* (a sense of whether an intermediate step is good) makes search/learning drastically more sample-efficient. In agent terms: good intermediate critique beats brute force.
4. **Continual learning over static knowledge (S14).** The target is not an all-knowing oracle but a "superintelligent 15-year-old" that *learns on the job* and can merge what it learned. Design for deployment-time learning.

> **中文**：研究品味、别对评测过拟合、价值函数提质、持续学习取代静态知识库。

**Apply.** When a task has a measurable proxy, ask "how could this proxy be gamed?"; add an intermediate-scoring signal (a verifier judge) to cut search; keep a place where learnings from real runs flow back into assets (M5).

## 3. Richard Sutton · 萨顿

**Central idea.** *The Bitter Lesson*, in two parts: (1) general methods that leverage computation win; (2) the contents of minds are irredeemably complex, so build in only **meta-methods that discover**, never our discovered knowledge. Today's deep learning does not yet learn well at runtime; the goal is the **Era of Experience** [7]–[9].

**Transferable skills**

1. **Build meta-methods, not knowledge (S15).** Encode *how to find and capture* structure, not the structure itself. Hard-coding our discoveries only hides the discovery process.
2. **Runtime learning beats design-time (S16).** "The world is much bigger than the agent" (big-world perspective): it appears non-stationary, so the agent must customize to the part of the world it actually meets, at runtime.
3. **The agent must invent its own subproblems (S17).** In OaK, options (policy + termination) and subproblems (each with its own value function/policy) are created by the agent, learned from experience — enabling continual, meta-, and hierarchical learning.
4. **Experience over IID data (S18).** Knowledge, planning, and state should be expressed in terms of *experience* (predictions of future experience), enabling autonomous verification and tuning.

> **中文**：只内建「发现的方法」而非「已发现的知识」；运行时学习 > 设计时；agent 自造子问题；一切以经验为锚。

**Apply.** Prefer assets that *generate* structure (a schema-inference step, a signal-harvesting loop) over hand-curated structure; make state and knowledge checkable against observed experience (M4, M5).

## 4. John Carmack · 卡马克

**Central idea.** Aggressive rejection of the LLM-as-oracle path for his own research: "LLMs can know everything without learning anything." He builds a physical robot that plays Atari by actual gameplay — **learning from experience, not an IID blender** [10], [11].

**Transferable skills**

1. **Learn from real interaction, not curated batches (S19).** Prefer environments where the agent confronts latency, noise, and sparse/delayed reward — the messiness is a *feature*, not a bug to remove.
2. **Reality is not turn-based (S20).** Real-time, continuous, non-stationary worlds impose constraints (latency, uncertainty) that must be designed for, not abstracted away.
3. **Respect the difference between knowing and learning (S21).** A system that "contains" knowledge is not the same as one that "discovers" it; do not confuse retrieval with learning.

> **中文**：从真实交互而非 IID 批次学习；现实不是回合制；区分「知道」与「学会」。

**Apply.** For any agent, ask whether it is *containing* the answer or *deriving* it under real conditions; build at least one loop that evaluates against messy, real inputs (M4).

## 5. François Chollet · 肖莱

**Central idea.** Intelligence = **skill-acquisition efficiency** over a scope of tasks, w.r.t. priors, experience, and generalization difficulty — *not* skill itself [12], [13]. The 2025 theme is the **refinement loop**: generate candidates, verify against a feedback signal, iterate — with test-time adaptation/adaptation required to demonstrate genuine fluid intelligence [14].

**Transferable skills**

1. **Measure efficiency, not just success (S22).** For agents: grade not only whether they solve a task, but how *efficiently* they do so on first contact (action efficiency, ARC-AGI-3's metric). Avoid "buying" skill with unlimited data/compute/priors.
2. **Refinement loop as a first-class pattern (S23).** Two phases — (i) exploration generates candidates, (ii) verification produces a feedback signal — repeated per task until it satisfies the checks. Applications-layer refinement improves reliability without retraining.
3. **Control for priors and experience (S24).** If a system has task-specific prior knowledge a human lacks, you are measuring the developer's cleverness, not the system's intelligence. Keep evaluation fair and unsaturatable.
4. **Benchmark the residual gap (S25).** Good tests are "easy for humans, hard for AI" and evolve as capabilities advance.

> **中文**：以「技能获取效率」而非「技能」衡量；把「精炼循环」(探索→验证→迭代) 作为一等模式；控制先验与经验；用不断演进、人类易而 AI 难的基准度量残差。

**Apply.** Attach an efficiency budget (actions/tokens/time) to each acceptance test; implement the refinement loop (generate → verify → refine) as an explicit harness cycle (M3).

## 6. Simon Willison · 威利森

**Central idea.** "An agent is an LLM that runs tools in a loop to achieve a goal." The security core is **prompt injection**, whose root cause is the "original sin of AI engineering": gluing trusted instructions and untrusted input into one string. The **lethal trifecta** — private data + untrusted content + external communication — lets any read content exfiltrate data [15]–[17].

**Transferable skills**

1. **Type the three legs (S26).** Know, per agent, which of {private data, untrusted content, external communication} it holds. A structural design that holds all three at once is a defect; remove a leg or gate it behind approval.
2. **Untrusted input must not trigger consequential actions (S27).** Once an agent has ingested untrusted input, constrain it so that input cannot cause side effects. Candidate patterns: action-selector, plan-then-execute, map-reduce, dual-LLM, code-then-execute, context-minimization.
3. **Filters are defense-in-depth, not boundaries (S28).** Adaptive attacks bypass prompt-level defenses; the boundary must be architectural (authority in the tool, not the prompt).
4. **Observability & human control (S29).** Every agent needs a well-defined human controller; consequential/irreversible actions need explicit confirmation; actions and plans must be auditable with typed read-only vs state-changing semantics.
5. **Meta: name the concept so it spreads (S30).** He deliberately coins sticky names ("lethal trifecta", "prompt injection") so practitioners search and adopt them.

> **中文**：给三条腿分类；不可信输入不得触发实质动作；过滤器只是纵深防御不是边界；可观测与人类控制；命名即传播。

**Apply.** Add a one-line "trifecta audit" per tool/agent; enforce data scope in code (not the prompt); require approval for irreversible/public actions; log tool calls + egress with a session id (M4, M8).

## 7. Chad Fowler & Fowler/Böckeler · 福勒体系

**Central idea (Fowler).** *Relocating Rigor*: shifts that look like removing control actually **move rigor closer to where truth lives** — from design docs to tests, from types to runtime, from hand-written code to **explicit invariants + ruthless evaluation**. "If generation gets easier, judgment must get stricter" [18].
**Central idea (Böckeler/Martin Fowler).** **Agent = Model + Harness** (harness = everything in the agent minus the model). A user harness has two jobs: increase first-try correctness and self-correct before humans look [19], [20].

**Transferable skills**

1. **Make invariants explicit (S31).** Generative systems only work if invariants are explicit rather than implicit; interfaces are real contracts. Missing invariant = lost rigor.
2. **Guides (feedforward) + Sensors (feedback) (S32).** *Guides* steer before the agent acts (types, rules, templates); *sensors* observe after and enable self-correction (tests, linters). A harness is a **cybernetic governor** regulating the repo toward a desired state.
3. **Computational vs inferential controls (S33).** Deterministic/CPU checks (tests, linters, type-checkers) are cheap and run on every change; semantic/GPU checks (AI review, LLM-as-judge) are slower, costlier, non-deterministic — use for richer judgment.
4. **"Positive prompt injection" (S34).** Write custom lint error messages that *inject remediation instructions* for the agent — a violation becomes an actionable fix-it prompt.
5. **Harness = ongoing practice (S35).** Iterate the harness whenever an issue recurs; beware controls that contradict each other; ask whether "sensors never fire" means high quality or weak detection.

> **中文**：rigor 会转移不会消失；把不变式显式化；前馈「导引」+ 反馈「传感器」；确定性检查便宜常跑、语义检查昂贵精用；把修复指令写进 lint 报错；harness 是持续工程而非一次性配置。

**Apply.** For each recurring agent failure, add one *guide* (prevent) and one *sensor* (detect+fix). Keep deterministic checks mandatory; layer inferential ones where judgment helps (M1, M3, M7).

## 8. Mitchell Hashimoto · 桥本

**Central idea — "Harness Engineering" (Feb 2026).** "Anytime you find an agent makes a mistake, take the time to engineer a solution such that the agent never makes that mistake again." Formula: **Agent = Model + Harness** [21], [22].

**Transferable skills**

1. **Every mistake → permanent fix (S36).** Convert each observed bad behavior into a rule or a tool so it becomes structurally hard to repeat. `AGENTS.md` lines should each trace to a real observed failure.
2. **Two forms (S37).** (a) Better implicit prompting in `AGENTS.md` for simple recurring errors; (b) real programmatic tools (screenshot scripts, filtered tests) — and announce the tool in `AGENTS.md` or the agent won't use it.
3. **Clone-your-own-work to learn boundaries (S38).** Have the agent redo a past manual commit *without seeing your solution*; this calibrates delegation.
4. **Off-peak & slam-dunk delegation (S39).** Use otherwise-idle time; delegate tasks you already "know how they'll come out" so you can review quickly.
5. **Six-stage adoption is not linear (S40).** Progress from chatbot → reproduce-your-work → off-peak → slam-dunk → engineer-the-harness → always-have-an-agent, guided by where your failures concentrate.

> **中文**：每个错误都变成永久性防护；`AGENTS.md` 每行对应一次真实失败；配上可编程验证工具并告知 agent；用「重做自己的提交」校准授权；按失败集中处对照六阶段。

**Apply.** Maintain a harness changelog: each entry = observed failure → guide/tool added. Treat `AGENTS.md` as a growing list of anti-patterns derived from incidents (M5, M7).

## 9. OpenAI Codex team · OpenAI 团队

**Central idea.** Shipped a real product with **zero hand-written code** in ~5 months (~1M LOC, ~1,500 PRs), at ~1/10 the time, by making the repo **legible to agents**. The engineer's job becomes *designing environments, specifying intent, and building feedback loops* [23], [24].

**Transferable skills**

1. **Agent legibility is the goal (S41).** Anything the agent cannot access in-context while running effectively does not exist to it. Make app state, logs, metrics, and traces directly inspectable (Exemplar: Chrome DevTools Protocol + ephemeral per-worktree observability with LogQL/PromQL).
2. **`AGENTS.md` is a table of contents, not an encyclopedia (S42).** Keep it ~100 lines as a map pointing into a structured `docs/` **system of record**. A monolithic file is "non-guidance": when everything is important, nothing is. Use **progressive disclosure**.
3. **Enforce architecture & taste mechanically (S43).** Rigid layered domains with validated dependency directions, custom linters, structural tests, and "taste invariants" (structured logging, naming, file-size limits). Lint messages **inject remediation**.
4. **Garbage collection for entropy (S44).** Agents replicate existing (even bad) patterns → drift. Encode "golden principles" and run recurring background cleanup agents that scan for deviations and open small, fast-reviewable PRs. "Technical debt is a high-interest loan: pay it continuously."
5. **When the agent struggles, fix the environment (S45).** The fix is almost never "try harder"; it is identifying the missing tool/guardrail/doc and making it legible and enforceable.
6. **Repo-local artifacts are the source of truth (S46).** Plans are first-class, versioned, co-located; anything not in the repo "doesn't exist" for the agent. Process norms (blocking gates, manual cleanup) relax only when throughput exceeds human attention.

> **中文**：一切以「agent 可读性」为目标；`AGENTS.md` 是目录不是百科（渐进披露）；机制化强制架构与品味；用后台「垃圾回收」对抗熵；agent 卡住时修环境别硬刚；仓库内产物即唯一事实来源。

**Apply.** Shrink your instruction file to a ~100-line map; move depth into an indexed `docs/`; encode each invariant as a mechanical check; schedule a drift-scan (M1, M6, M7).

## 10. Anthropic · 人类学（Claude 团队）

**Central idea.** For long-horizon agents: manage context (compaction, note-taking, subagents) and **separate the builder from the critic**, because "agents cannot accurately evaluate their own work" [25]–[28].

**Transferable skills**

1. **Context engineering toolkit (S47).** Compaction (summarize in place to continue), structured note-taking / agentic memory (a `NOTES.md`/to-do persisted outside the window), and sub-agent architectures (focused sub-contexts returning condensed ~1–2k-token summaries). Find the *smallest set of high-signal tokens*.
2. **Context resets vs compaction (S48).** A reset (fresh window + structured handoff artifact) gives a clean slate and cures "context anxiety"; compaction preserves continuity but not a clean slate. Choose per model/task.
3. **Separate generator from evaluator (S49).** Same model, fresh window, no Write/Edit tools, judges only the *output* (Exemplar: Playwright driving the running app), never the builder's reasoning traces. This is the GAN-style adversarial pattern.
4. **Negotiate "done" before work (S50).** Generator and evaluator agree on a **sprint contract** up front; grade against co-authored, granular criteria (vague criteria → vague critiques).
5. **Default-FAIL + evidence gate (S51).** Every criterion starts `false`; the agent cannot mark it passing without first *observing evidence* (screenshot/log/result file) — a hook denies the write otherwise.
6. **Agent-maintained handoff (S52).** The agent scopes each session, writes structured progress, and commits at checkpoints so the next session resumes cleanly.
7. **Right-size the scaffold (S53).** The evaluator is worth its cost only when the task sits *beyond what the current model does reliably solo*; re-simplify on each model upgrade (they dropped sprints/resets when capability rose).

> **中文**：上下文三件套（压缩/笔记/子 agent）；重置 vs 压缩；生成者与评判者分离（同一模型、全新窗口、只判产出）；开工前协商「完成」定义；默认失败 + 证据门；agent 自维护交接；按模型能力重新简化脚手架。

**Apply.** For anything multi-hour: add a fresh-context evaluator with no write tools, a default-FAIL contract requiring observed evidence, and an agent-maintained progress+commit handoff (M1, M2, M3).

## 11. Ethan Mollick · 莫里克

**Central idea.** Separate **models / apps / harnesses**. A harness "enables AI to do more than produce text… it turns a clever engine into something closer to a digital worker." In practice, the harness often matters more than the model [29], [30].

**Transferable skills**

1. **Think in layers, not brands (S54).** Model = capability; app = interface; harness = tools+workflow that determine what is actually possible. Real productivity lives in the harness.
2. **Delegation & orchestration mindset (S55).** Define task, constraints, source material; treat the AI as a fast, occasionally overconfident junior; verify output.

> **中文**：分模型/应用/harness 三层思考；harness 常比模型更决定产出；以「委派+编排」心态工作。

**Apply.** When something underperforms, check the harness (retrieval, multi-source input, workflow, structured output) before blaming the model (M0, M7).

## 12. Demis Hassabis · 哈萨比斯

**Central idea.** "The scientific method is probably the greatest invention humanity has ever come up with." Apply *it* to AI itself — rigorous tests, cautious claims, thought-through second-order effects — rather than a build-first hacker mentality [31], [32].

**Transferable skills**

1. **Rigor on claims (S56).** Measure what you care about; be careful with the claims made about systems; think through second-order effects before deploying.
2. **Precompute-to-compress (S57).** Much of intelligence is compressing an intractable search space into an efficient artifact usable at test time (AlphaFold/AlphaGo). In harness terms: invest up front to build a retrieval/model artifact that narrows the agent's search.
3. **Humans own conjecture; tools own legwork (S58).** "They can't figure out the right question or hypothesis — that has to come from the human." Best scientists + tools do more, often in smaller teams.

> **中文**：对「主张」保持科学严谨；用大量预计算把搜索空间压缩成测试期可用的人工件；人类负责提出猜想与问题，工具负责跑腿。

**Apply.** Require an explicit, testable claim + measured outcome for each deliverable; prefer pre-built artifacts (indexes, registries, schemas) that shrink the agent's search (M0, M4).

---

## Synthesis · 交汇点（所有顶尖方法的公共内核）

Across every practitioner, the same invariants recur — these are the **skills worth internalizing above any tool**:

1. **Rigor relocates, it never disappears (Fowler).** When generation gets easier, specification + evaluation must get stricter.
2. **Make "done" structural and evidenced (Anthropic, Chollet, Hashimoto).** Acceptance tests before work; default-FAIL + observed evidence; the refinement loop.
3. **Separate builder from critic (Anthropic, Sutskever's value function).** Self-evaluation is biased; an independent, skeptical evaluator is a strong lever.
4. **Keep AI on a leash; slide autonomy by risk (Karpathy, Willison, Böckeler).** Human gates on irreversible acts; autonomy as a dial.
5. **Context is a finite, precious resource (Karpathy, Anthropic, OpenAI).** Smallest high-signal set; maps and progressive disclosure; compaction/resets/notes/subagents.
6. **Provenance & verifiability decide where agents can be trusted (Karpathy, Chollet, Willison, Hassabis).** High-verifiability domains automate; low-verifiability domains stay human.
7. **Build meta-methods; learn at runtime (Sutton, Carmack, Sutskever).** Encode discovery, not discoveries; let agents self-generate subproblems.
8. **Remove the human as a *throughput* bottleneck, never as a *judgment* bottleneck (Karpathy, OpenAI, Hashimoto).** Automate orchestration; keep human taste in the loop.
9. **Engineer the environment, not just the model (Hashimoto, OpenAI, Fowler).** Every recurring failure becomes a permanent guide/sensor; fix legibility, tools, guardrails.
10. **Design so compromise is survivable (Willison, Sutton's big-world).** Assume the model will fail; bound the blast radius; keep an auditable, reversible path.

> **中文·十条公共内核**：rigor 只会转移；「完成」结构化+有证据；构建者≠评判者；上缰绳+自主度滑杆；上下文稀缺；可溯+可验证决定信任边界；内建「发现的方法」并运行时学习；去吞吐瓶颈、留判断瓶颈；改造环境而非只调模型；假设会失败并把爆炸半径做小。

---

## References · 参考文献（IEEE，访问日期 2026-10-12）

[1] A. Karpathy, "Software 2.0," *Medium*, Nov. 11, 2017. [Online]. Available: https://karpathy.medium.com/software-2-0-a64152b37c35
[2] A. Karpathy, "Software Is Changing (Again)," Y Combinator AI Startup School, Jun. 17, 2025. [Online]. Available: https://www.youtube.com/watch?v=LCEmiRjPEtQ
[3] A. Karpathy, "From Vibe Coding to Agentic Engineering," AI Ascent / Sequoia, 2026. Transcript. [Online]. Available: https://singjupost.com/andrej-karpathy-from-vibe-coding-to-agentic-engineering-w-stephanie-zhan-transcript/
[4] A. Karpathy, "Context engineering" (quote), X, Jun. 25, 2025; and D. Patel, "Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI," podcast, Mar. 2026. [Online]. Available: https://exa.ai/library/podcast/f2vwsv8d0s9/episode/zppkvq5d8wy
[5] D. Patel, "Ilya Sutskever — We're moving from the age of scaling to the age of research," *Dwarkesh Podcast*, Nov. 25, 2025. [Online]. Available: https://www.dwarkesh.com/p/ilya-sutskever-2
[6] Calcalist, "Ilya Sutskever: AI's bottleneck is ideas, not compute," Nov. 25, 2025. [Online]. Available: https://www.calcalistech.com/ctechnews/article/h1fudk7z11x
[7] R. Sutton, "The Bitter Lesson," Mar. 13, 2019. [Online]. Available: http://www.incompleteideas.net/IncIdeas/BitterLesson.html
[8] R. Sutton, "The OaK Architecture: A Vision of SuperIntelligence from Experience," RLC 2025. [Online]. Available: https://www.youtube.com/watch?v=dEweRR7tQqg
[9] Inference by Sequoia, "Richard Sutton's Second Bitter Lesson," Sep. 11, 2025. [Online]. Available: https://inferencebysequoia.substack.com/p/richard-suttons-second-bitter-lesson
[10] J. Carmack, Upper Bound talk, 2025 (see [9] for summary). [Online]. Available: https://www.youtube.com/watch?v=HGhFj4v7c7k
[11] R. Sutton, "Rich Sutton's Recent Talks," incompleteideas.net. [Online]. Available: http://incompleteideas.net/Talks/Talks.html
[12] F. Chollet, "On the Measure of Intelligence," arXiv:1911.01547, 2019. [Online]. Available: https://arxiv.org/abs/1911.01547
[13] ARC Prize Foundation, "What is ARC-AGI?" [Online]. Available: https://arcprize.org/arc-agi
[14] ARC Prize Foundation, "ARC Prize 2025: Technical Report," arXiv:2601.10904, Jan. 2026; and "ARC-AGI-3," arXiv:2603.24621, Mar. 2026. [Online]. Available: https://arxiv.org/abs/2601.10904
[15] S. Willison, "The lethal trifecta for AI agents," Jun. 16, 2025. [Online]. Available: https://simonwillison.net/2025/jun/16/the-lethal-trifecta/
[16] S. Willison, "My Lethal Trifecta talk at the Bay Area AI Security Meetup," Aug. 9, 2025. [Online]. Available: https://simonwillison.net/2025/Aug/9/bay-area-ai/
[17] L. Beurer-Kellner *et al.*, "Design Patterns for Securing LLM Agents against Prompt Injections," arXiv:2506.08837, Jun. 2025. [Online]. Available: https://arxiv.org/abs/2506.08837
[18] C. Fowler, "Relocating Rigor," *The Phoenix Architecture*, Jan. 6, 2026. [Online]. Available: https://chadfowler.com/regenerative-software/3mbrvhyye4k2e/
[19] B. Böckeler, "Harness engineering for coding agent users," martinfowler.com, Apr. 2, 2026. [Online]. Available: https://martinfowler.com/articles/harness-engineering.html
[20] B. Böckeler, "Harness Engineering — first thoughts" (memo), martinfowler.com, Feb. 17, 2026. [Online]. Available: https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
[21] M. Hashimoto, "My AI Adoption Journey," Feb. 5, 2026. [Online]. Available: https://mitchellh.com/writing/my-ai-adoption-journey
[22] S. Heijstek, "What is harness engineering?" Software Improvement Group, Apr. 24, 2026. [Online]. Available: https://www.softwareimprovementgroup.com/blog/what-is-harness-engineering/
[23] R. Lopopolo / OpenAI, "Harness engineering: leveraging Codex in an agent-first world," Feb. 11, 2026. [Online]. Available: https://openai.com/index/harness-engineering/
[24] OpenAI Engineering Blog (summary), "Harness engineering…," Engineering.fyi, Feb. 11, 2026. [Online]. Available: https://www.engineering.fyi/article/harness-engineering-leveraging-codex-in-an-agent-first-world
[25] Anthropic, "Effective context engineering for AI agents," Sep. 29, 2025. [Online]. Available: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[26] Anthropic, "Harness design for long-running application development," Mar. 24, 2026. [Online]. Available: https://www.anthropic.com/engineering/harness-design-long-running-apps
[27] Anthropic, "cwc-long-running-agents" (reference repo), GitHub. [Online]. Available: https://github.com/anthropics/cwc-long-running-agents
[28] K. Jayaraman, "The GAN Pattern for Agents: Why Anthropic Stopped Letting Models Grade Their Own Work," Jun. 9, 2026. [Online]. Available: https://kondasamy.com/blog/2026/adversarial-agents-anthropic-generator-evaluator/
[29] E. Mollick, "Models, Apps, and Harnesses," *One Useful Thing*, 2026. [Online]. Available: https://www.oneusefulthing.org/
[30] S. Abel, "Models, Apps, and Harnesses," *The Content Wrangler*, Mar. 16, 2026. [Online]. Available: https://www.thecontentwrangler.com/p/models-apps-and-harnesses-how-tech
[31] D. Hassabis, "AI as the Ultimate Tool for Science," *Dædalus* (American Academy of Arts and Sciences), May 21, 2026. [Online]. Available: https://www.amacad.org/publication/daedalus/ai-ultimate-tool-science-conversation-demis-hassabis
[32] D. Hassabis, "Accelerating scientific discovery with AI" (Nobel Lecture), Dec. 8, 2024. [Online]. Available: https://www.nobelprize.org/uploads/2024/12/hassabis-lecture.pdf

> **Note on the ARC arXiv IDs.** The ARC-AGI-3 (2603.24621) and ARC Prize 2025 (2601.10904) identifiers reflect the search results as of 2026-10-12; verify against arXiv before formal citation. All other URLs were retrieved 2026-10-12.

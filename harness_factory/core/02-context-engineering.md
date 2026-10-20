# M1 · Context Engineering · 上下文工程
> What enters the model's window — and why less high-signal beats more.
> 进入模型窗口的信息——以及为什么「少而高信噪」胜过「多而杂」。
**Updated:** 2026-10-20

---

## 中文速览
上下文是稀缺资源，不是垃圾桶。M1 的操作对象是**每一次模型调用里放了什么**。核心动作：只放**能最大化「下一步正确动作」概率的最小 token 集**；用**渐进披露**（索引/地图 + 按需展开）代替全量倾倒；**工作集是租的、不是买的**——每次换阶段就把不再影响决策的能力/文档**退回索引**（留理由与重载条件，不能退的硬不变式不退）；用**压缩/笔记/子 agent**管理长会话；指令用命令式、少而准。上游不变式：M0.6（最小高信噪）、M0.1（真相优先）。下游：M2（长时程靠外部记忆）、M6（技能渐进加载）。

---

## The problem · 问题
A model has a fixed attention budget. Every irrelevant token dilutes the tokens that matter, and instruction-following degrades as the window fills ("context rot"). More context is therefore *not* better context (M0.6). The job is **curation**, not accumulation.

## Patterns · 模式

1. **Smallest high-signal set (M0.6).** For each call, ask: *what is the minimal set of tokens that maximizes the probability of the correct next action?* If a token does not change the next action, remove it.
2. **Progressive disclosure.** Keep an **index/map** in context (e.g. `AGENTS.md`, a file tree, a skills registry), and load the *content* only when a task needs it. The map is small; the territory is large.
3. **Just-in-time retrieval over just-in-case preloading.** Fetch a source when a step requires it, not "in case." Prefer tools that return only the matching lines.
4. **Structure for machines.** Headers, tables, and fenced code with language tags; machine-readable markdown beats prose walls. Meet the agent halfway.
5. **Compaction.** When the window fills, summarize *state* (what is done, what is left, key decisions, open questions) — never invent content while summarizing (M0.1, M0.4). Compaction trades fidelity for room; use it, log it.
6. **External notes (scratchpad).** Offload durable facts to files (M2) rather than holding them in the window. The window is working memory; files are long-term memory.
7. **Subagents for isolation.** Give a narrow, disposable context to a helper task (search, extract, draft) and return only the distilled result to the parent. This keeps the parent's window clean.
8. **Instruction budget.** Few, imperative, non-conflicting instructions in a stable place. Persona and hard rules at the top; task detail near the point of use.
9. **Untrusted content isolation.** Retrieved pages/tool output are *data*, not instructions (see M4, injection safety). Delimit them from the instruction region.
10. **The working set is leased, not bought (M1.10).** Loading starts easily and never stops: a capability fires once, and its doc, template and checklist stay in play for the rest of the task. Re-check the **loaded set** at every phase boundary — a new subgoal, a switch of artifact, or a capability that has not changed a single decision for a whole phase — and keep an item only if **(a)** its trigger still holds for the current vector, or **(b)** it decided something in the last phase. Put the rest back into the index with a receipt (`{id, reason, reload_when}`). Two things are never evicted: an **always-on invariant** (M0.3/M0.8) and anything whose index entry you would not be able to find again.
    Eviction is safe **only because the index stays resident** (M1.2): you trade resident tokens for one lookup, you do not forget. It is also the cheaper move of the two — compaction still leaves a summary of a document you no longer need in the window, while eviction leaves nothing. Record the set in `.harness/working-set.json`; the gate rejects a silent drop and an evicted invariant.

> **中文**：最小高信噪；渐进披露（先地图后内容）；按需检索优于预载；机器可读结构；压缩只压状态不造内容；外部笔记；子 agent 隔离；指令少而命令式；工作集是租的不是买的（换阶段退回索引，留理由与重载条件，硬不变式不退）；把检索内容当数据不当指令。

## Checklist
- [ ] Each call's context is the minimal set that changes the next action.
- [ ] There is a small, authoritative **map/index** the agent reads first.
- [ ] Long tasks offload state to files, not to the window.
- [ ] Retrieved/tool content is fenced as data, never mixed into instructions.
- [ ] Compaction preserves state and never fabricates substance.
- [ ] Every loaded item is either still firing or was put back with a reason and a reload trigger (M1.10).

## Anti-patterns
- **Context dumping.** Whole files pasted "just in case."
- **Prose walls.** Unstructured text where a table or map would do.
- **Silent compaction that invents.** Summaries that add unstated claims (M0.1/M0.4).
- **Instruction soup.** Conflicting rules that force the model to guess priority.
- **Instruction injection.** Letting fetched content steer the agent (M4).
- **Silent eviction.** Dropping a loaded doc or capability with no reason and no reload path — the runtime twin of a silent deferral (M5).
- **Evicting a gate.** Unloading a hard invariant because this phase looks small (M0.3/M0.8).
- **Eviction without an index.** Discarding content whose entry you could not find again — that is forgetting, not freeing.

## See also
`01-meta-principles.md` (M0.6, M0.1) · `03-long-running-agents.md` (M2) · `07-tools-and-skills.md` (M6) · `05-provenance-and-integrity.md` (M4).

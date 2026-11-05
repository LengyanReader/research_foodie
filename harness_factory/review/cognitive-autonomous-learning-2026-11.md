# Cognitive autonomous learning, System M meta-control, and the Evo-Devo scaffolding thesis — a synthesis for agent harnesses

**Updated:** 2026-11-05 · **Status:** research synthesis — **applied as round P73 on 2026-11-05** (registry: `data/cycles.json` P73; grounding: `core/03` M2.15) · **Scope:** foundational critique and architectural blueprint from cognitive science — Emmanuel Dupoux, Yann LeCun, and Jitendra Malik, *"Why AI systems don't learn and what to do about it: Lessons on autonomous learning from cognitive science"* (arXiv:2603.15381, 2026-03-16) — read against this factory's agent harness architecture (`core/01`–`core/09`, `review/references.md` R293).

> **中文速览**：这是 **P73 认知自主学习轮** 的理论综述与架构映射。本篇深入剖析 Dupoux, LeCun, Malik 三位学者（认知科学 + 深度学习 + 视觉奠基人）在 arXiv:2603.15381 中提出的核心论断：**为什么现有 AI（静态 LLM + 外部脚手架）无法实现真正的自主连续学习**。
>
> **三核心结论**：
> 1. **批判与诊断**：当代大模型依赖外部海量被动数据进行下个 Token 预测，预训练后权重冻结；单纯依赖 Prompt、CoT、RAG 和 Agentic 图结构只是在静态统计流形上采样，造成了“理解与适应的智能假象”，缺乏常识世界模型。
> 2. **A-B-M 三系统解耦**：真正的自主学习需要三系统协作 —— **System A**（被动自监督观察 / JEPA 潜空间世界模型）、**System B**（主动交互与行为试错）、**System M**（基于内在惊奇度、预测误差、不确定性与新颖性的**元控制中枢**，动态仲裁何时观察、何时行动）。
> 3. **Evo-Devo（演化-发育）支架假说**：生物从不从零（tabula rasa）起步；演化硬编码了发育支架（先验约束、反射与安全边界），幼体在支架内通过发育自主学习。
>
> **对外壳（Harness Factory）的深刻映射与落地**：
> - **严守 M0.4 / P15 边界**：本库是 Agent 外壳编译器与模式库，绝不越界去训练底层 JEPA 世界模型或开发仿真器。
> - **System M 在外壳层的投影（M2.15）**：现行 Agent 普遍陷入机械式线性 ReAct 循环；本库引入 **M2.15 认识性元控制**，将智能体动作划分为**认识性动作（降低不确定性）**与**实用性动作（改变状态）**。在遭遇预期差或断言失败时，强制打断盲目重试，切回认识性观察模式。
> - **Evo-Devo 理论为 Harness 提供了认知科学辩护**：Harness（`AGENTS.md` + 门禁规则 + 检查脚本）正是给冻结 LLM 赋予的**演化发育先验支架**，为其自主任务发育划定边界，防止对齐漂移。

---

## 1 · The core critique · 核心批判：当前 AI 为何没有真正“学习”

Dupoux, LeCun, and Malik (2603.15381, `[R293]`) diagnose modern AI's paradox: despite consuming trillions of tokens and passing expert-level exams, state-of-the-art models **fail to learn continuously, autonomously, and efficiently** from ongoing environmental experience.

The authors identify three fatal structural obstacles in contemporary foundation models:
1. **Externalized, frozen training**: Machine learning remains externalized. Humans curate datasets, tune hyperparameters, run offline gradient descent, and then freeze the weights. Once deployed, the model's weights do not change; it is incapable of cumulative lifelong adaptation from its own interactions.
2. **The illusion of reasoning via scaffolding**: Prompting tricks, chains of thought, and multi-agent wrappers create the *appearance* of reasoning and dynamic adaptation. However, these methods merely guide traversal over a pre-computed conditional distribution. They cannot add concepts the model lacks, nor can they repair broken foundational causal models without external human intervention.
3. **Absence of a grounded world model**: Text is a highly compressed, lossy, human-invented symbolic shadow of the physical world. Learning solely by predicting the next symbol leaves models devoid of intuitive physics, object permanence, spatial continuity, and common sense.

---

## 2 · The A-B-M cognitive architecture · A-B-M 三系统认知架构

To overcome these limits, Dupoux, LeCun, and Malik propose an integrated learning architecture structured into three complementary systems:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      System M (Meta-Control Plane)                     │
│  · Driven by internal signals: Prediction Error, Surprise, Uncertainty │
│  · Arbitrates between observation, action, and model updating          │
└───────────────────▲────────────────────────────────┬───────────────────┘
                    │ Monitors divergence            │ Mode dispatch
       ┌────────────┴─────────────┐    ┌─────────────▼────────────┐
       │   System A (Observation) │    │     System B (Action)    │
       │  · Self-supervised world │    │  · Behavioral policies   │
       │    model (JEPA latent)   │    │  · Interactive trials    │
       │  · Passive absorption    │    │  · Grounded feedback     │
       └──────────────────────────┘    └──────────────────────────┘
```

- **System A (Learning from Observation)**: A self-supervised representation engine that passively observes continuous environment streams (multimodal sensory data) without human annotations. It builds a Joint-Embedding Predictive Architecture (JEPA) world model that predicts abstract representations rather than low-level pixel/token noise.
- **System B (Learning from Active Behavior)**: An active behavioral controller that takes physical or digital actions in the environment, observing consequences and optimizing reward signals.
- **System M (The Meta-Controller)**: The crucial orchestrator. Biological organisms do not simply act blindly or watch passively; they are propelled by intrinsic drives (**curiosity, novelty detection, error reduction**). System M monitors prediction errors and internal uncertainty, dynamically switching the agent between observing the world (System A) and acting in it (System B).

---

## 3 · The Evo-Devo scaffolding thesis · 演化-发育支架假说

A pivotal insight from cognitive developmental biology highlighted in `[R293]` is the **Evolutionary-Developmental (Evo-Devo)** framework:

> *"Biological intelligence is never tabula rasa. Evolution spends millions of years pre-wiring inductive biases, survival drives, architectural reflexes, and developmental scaffolds. Development unfolds over hours, weeks, and years within this safe, structured envelope."*

In machine learning, attempting to have an unconstrained model learn everything from raw interaction leads inevitably to **catastrophic forgetting, catastrophic exploration failure, and alignment drift**. The developmental scaffold is what makes open-ended exploration safe.

### Translation to Agent Harness Engineering

This thesis provides an ironclad theoretical justification for the existence of **agent harnesses**:
- The **Harness** (`core/01`–`core/09`, `AGENTS.md`, `check.py`, and domain verification gates) is the **computational analogue of the evolutionary developmental scaffold**.
- A bare LLM placed in a terminal or workspace is an unanchored learner with high variance. The harness provides the hardwired invariants (M0.1 truth over throughput, M0.8 human gates on destructive actions, M0.7 resumability, M3 compile/test verification) that constrain the model's exploratory behavior.
- Under this perspective, **the harness is not an embarrassing temporary workaround for model weaknesses; it is the necessary evolutionary scaffold that enables safe cognitive development.**

---

## 4 · Operationalizing System M: Epistemic meta-control (M2.15) · 认识性元控制

Current agent loop paradigms (such as standard ReAct or naive step iteration) suffer from a glaring cognitive defect: they treat all steps as uniform execution turns. When an error occurs, the agent blindly tries another pragmatic action (e.g. tweaking a command parameter or re-running a broken script) without first reducing its epistemic uncertainty.

In `harness_factory`, this round integrates the System M principle as **M2.15 (Epistemic meta-control)**:

### 1. Functional Action Classification
- **Pragmatic Actions (System B)**: Actions intended to alter the task or environmental state (writing code, executing database migrations, deleting files, running compilation pipelines).
- **Epistemic Actions (System A)**: Actions intended solely to reduce entropy and acquire missing facts (reading source documents, inspecting runtime logs, querying environment status diffs, executing dry-run assertions).

### 2. The System M Meta-Control Rule
When an agent encounters a **high-surprise event** (an unpredicted exception, a failed assertion, a schema contract mismatch, or a sharp drop in judge confidence):
1. **Interrupt pragmatic execution**: The runtime immediately blocks further state mutation.
2. **Force epistemic mode**: The agent is restricted to read-only epistemic actions (inspecting diagnostics, re-verifying source claims, checking schemas).
3. **Resume on verified uncertainty reduction**: Only when the underlying causal mechanism is diagnosed and verified against evidence does the harness permit a resumption of pragmatic actions.

This directly eradicates the anti-pattern **Blind pragmatic looping** (M2.15).

---

## 5 · Comparative spectrum · 横向学术谱系与互补分析

| Paper / Framework | Category | Core Contribution | Relation to `harness_factory` |
|---|---|---|---|
| **Dupoux, LeCun & Malik** `[R293]` (arXiv:2603.15381) | Cognitive Science Foundation | A-B-M tri-system, Evo-Devo scaffolding, critique of static scaffolding | Theoretical grounding for M2.15 epistemic meta-control & harness necessity |
| **ThinkingBox** `[R279]` (Microsoft / HF, 2026) | Environment Verification | Database state grading, 67% failures terminate cleanly, pass@1 vs 20/20 divergence | Environmental truth grounding for System B outcomes (M3.19) |
| **QueenBee** `[R280]` (Tian et al., arXiv:2606.27492) | Harness Self-Evolution | Recursive self-improving communication topology DAGs | External implementation of M5 self-evolution engine |
| **uni-robot-agent** `[R291]` (Yuan et al., arXiv:2611.01560) | Embodied Robot Harness | No-privileged-input state grading, M2.14 pipelined execution | Physical-domain embodiment of System B & fair attribution |
| **Weight-Space Programming** `[R292]` (Takehi et al., 2026) | Direct Weight Adaptation | LLM directly reading/writing weights (0.016% edit fixes MATH-500) | Third self-improvement modality between scaffold and gradient training (M5.13) |

---

## 6 · Invariant boundaries · 边界与不作为声明 (M0.4 & P15)

In strict adherence to **M0.1** (truth before throughput) and **M0.4** (machines observe, humans decide; do not inflate scope):

1. **No model training fabrication**: This factory does *not* implement JEPA pre-training algorithms, latent predictive losses, or raw sensory video pipelines. Such components belong to foundational model laboratories.
2. **No simulated sensorimotor engine**: Emitting a harness compiles orchestration, context, verification, and governance; it does not pretend to supply a physical robotics simulator.
3. **The synthesis is methodological**: The value absorbed from `[R293]` is structural and cognitive — replacing blind reactive retries with formal epistemic meta-control (M2.15) and grounding the library's design in the Evo-Devo scaffolding thesis.

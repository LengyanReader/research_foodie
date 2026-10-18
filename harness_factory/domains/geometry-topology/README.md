# Domain · Geometry & topology · 几何与拓扑域
> Wiring `core/` modules into a certified computation over shape and space: exact predicates, invariants that survive perturbation, and algorithms recorded as part of the evidence.
> 把 `core/` 模块接线成「对形状与空间做可核验计算」：精确谓词、扰动下仍成立的不变量、并把算法本身当作证据的一部分记录下来。
**Updated:** 2026-10-18

---

## 中文速览
几何与拓扑域的目标是**让「算出来的量」成为可核验的命题**：先固定**对象与其表示**（坐标、复形、网格、三角剖分）（M0/M1）；写明**要算的不变量或谓词**（M1/M4）；在**精确算术或带界精度**下计算，并**显式处理退化情形**（M3/M6）；**独立重算**或验证**扰动不变性**（M3）；确认该不变量对这类对象**良定义**（有定理支撑，而非假设）（M4）；最后把算法、界/精度与出处写进结论（M7）。域特有风险：**浮点谓词翻符号**、**退化输入未处理**、**把一次工具输出当证明**、**不变量选错对象**、**精度/边界未声明**。

---

## What this domain is for · 用途
Produce a computed result a skeptical reader can re-derive: the object and its representation fixed, the invariant named, the computation exact or certified, degeneracies handled, and the value reproduced by an independent route. Covers computational and algebraic geometry, polyhedral geometry, low-dimensional topology, persistent homology and topological data analysis, and the geometry/topology that appears inside other sciences.

## Pipeline layers · 分层流水线
| Layer | Step | Core modules | Notes |
|---|---|---|---|
| L0 | Fix the object & representation | M0, M1 | coordinates / complex / mesh / triangulation; the representation is part of the claim |
| L1 | Name the invariant / predicate | M1, M4 | orientation, homology, knot polynomial, intersection sign |
| L2 | Compute so | M3, M6 | exact or certified arithmetic; degeneracies handled explicitly |
| L3 | Independent re-derivation (gate) | M3 | second tool, hand-checkable special case, or perturbation invariance |
| L4 | Well-definedness | M4 | the invariant is theorem-backed for *this* object class |
| L5 | Write up | M7, M4 | algorithm + bound/precision + provenance |

## Module combination · 模块组合
- **M0** — an invariant that changes when you nudge the input was never an invariant.
- **M1** — the representation (mesh, complex, coordinates) is a modelled choice, not neutral scaffolding.
- **M3** — the gate is exactness/certification **plus** an independent re-derivation; a raw tool output is a conjecture.
- **M4** — algorithms, parameters and precision are provenance.
- **M6** — CAS and geometry/topology toolkits are instruments: pin versions, record predicates and tolerances.
- **M7** — "computed" is a governance claim; publish with the algorithm and its bound.

## Instruments · 仪器
Concrete tools for L2–L3 (catalog ids; full map: `../reference/evidence-instruments.md#certified-computation`):
- **Computer algebra** — `sagemath` · `singular` · `macaulay2` (commutative algebra / algebraic geometry) · `gap` (groups) · `pari-gp` (number theory) · `oscar` · `sympy`.
- **Geometry & topology toolkits** — `cgal` (exact predicates, triangulations) · `gudhi` (persistent homology) · `regina` (low-dimensional topology) · `snappy` (3-manifolds, hyperbolic) · `polymake` (polyhedral).
- **Gate evidence** — exact/certified result, degeneracies handled, **and** an independent re-derivation or perturbation-invariance check. Numeric-precision norm: `[R114]` (interval arithmetic).

## Methodology · 方法论
- **Proof methodology (for invariants)** — an invariant claim is a theorem: state the language/definitions and push the derivation through a checker (`formal-verification`); computation *supports* the proof, it does not replace it (M3.12).
- **Reproducible computation** — the algorithm, its version, and its precision travel with the result; a "certified" claim without a recorded method is not certified.
- Full map: `../reference/methodology-map.md` (M3.13).

## Discipline-specific risks · 领域特有风险
- **Floating-point predicates** (an orientation/incidence test that flips under noise invalidates the invariant).
- **Degenerate inputs unhandled** (collinear points, non-manifold meshes, empty complexes).
- **Tool output as proof** ("SageMath said so" without a re-derivation or a proof).
- **Invariant mismatch** (computing a quantity not well-defined for this object class).
- **Undeclared precision/bound** (approximations presented as exact).
- **Representation confusion** (a triangulation's invariant reported as the space's).

**Information outlets · 信息源**：本领域的高质量门户 / 期刊 / 预印本 / 数据库 / 媒体见 `../reference/outlet-map.md`（机器可读：`data/sources.json` 的 `outlets` 组；`harness sources --group outlets` 查看）。

## See also
`../mathematics/README.md` (proof, algebra) · `../logic/README.md` (machine checking) · `../core/04-verification-and-gates.md` (M3.12) · `../reference/evidence-instruments.md` · `../review/integration-map-2026-10.md`.

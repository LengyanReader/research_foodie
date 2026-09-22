# 2304.02819

## Abstract
# 1. Introduction / 引言

## Intro
# 1. Introduction / 引言

Automated AI-detection tools are being deployed as gatekeepers in academic-integrity and AI-governance pipelines, yet their reliability across linguistic backgrounds is rarely scrutinized. Using the TOEFL dataset, Liang et al. (2023, arXiv:2304.02819) demonstrate that seven widely used GPT detectors misclassify over half of non-native English essays as AI-generated (61.22% average false-positive rate) while remaining near-perfect on native-US writing — establishing that detector outputs are systematically biased and should not be treated as evidence for consequential decisions. This survey reconstructs the paper's evidence: (§2) the bias result and its causes, (§3) the linguistic-diversity mitigation that cuts false positives to 11.77%, (§4) the trivial self-edit prompt that bypasses detection entirely, and (§5) the implications and limits of these findings for AI governance and academic integrity.

> **中文速览：** 用于学术诚信与 AI 治理的检测工具正日益被当作"把关人"采用，但其跨语言背景的可靠性几乎未被检验。Liang 等（2023, arXiv:2304.02819）基于 TOEFL 数据集证明：七种常用的 GPT 检测器将超过一半的非母语者英文作文误判为 AI 生成（平均误报率 61.22%），而对美国本土写作几乎零误判——即检测输出存在系统性偏差，不能作为高利害决策的证据。本综述重建该论文证据链：第 2 节偏差结果及成因，第 3 节通过语言多样性增强将误报率降至 11.77% 的缓解实验，第 4 节可轻易绕过现有检测器的自编辑提示，第 5 节对 AI 治理与学术诚信的启示及局限。

## Core finding: detectors misclassify non-native English writing

Benchmarking seven widely used GPT detectors on 91 free-written TOEFL essays from non-native English speakers, Liang et al. found them misclassifying over half of the samples as AI-generated, with an average false positive rate of 61.22%, while the same detectors were near-perfect on native US 8th-graders' essays (arXiv:2304.02819). Per-detector rates diverged sharply: GPTZero alone flagged 61.2% of TOEFL essays at its default threshold, rising to 97.6% under a stricter threshold, even though every sample was written by humans (arXiv:2304.02819). Native English baseline writing was flagged at far lower rates, so false positives scale with the writer's English proficiency rather than with actual AI authorship.

Supporting evidence links this to statistical properties of the text itself: across 1,574 ICLR 2023 accepted papers, authors based in non-native English-speaking countries produced abstracts with significantly lower perplexity than native-English country authors (P=0.035), a gap that persists after controlling for review ratings (arXiv:2304.02819). The tension here is not between sources but within them: detection outcomes are so threshold- and detector-dependent that the reported bias figures—61.22% average, 61.2% at GPTZero's default, 97.6% under its strict setting—describe different operating points of the same systems. The open gap is that, as of this paper, no published detector accounts for authoring-language effects independently of AI authorship, leaving academic-integrity decisions about non-native writers systematically unreliable.

---

## Core finding: 检测器误判非母语写作者的英语文本

Liang 等人对 91 篇非母语者自由写作的 TOEFL 作文进行检测器基准测试：七款广泛使用的 GPT 检测器均将过半样本误判为"AI 生成"，平均误报率达 61.22%，而同一批检测器对美国八年级母语学生的作文几乎完全正确（arXiv:2304.02819）。各检测器差异悬殊：GPTZero 在默认阈值下将 61.2% 的 TOEFL 作文判为 AI 生成，在更严格阈值下高达 97.6%，尽管所有样本均出自真人（arXiv:2304.02819）。母语基线写作被误判的比率远低，说明误报随写作者英语水平上升而放大，而非随真实 AI 作词变化。

佐证来自文本自身的统计特征：在 1,574 篇 ICLR 2023 录用论文中，位于非英语母语国家作者的摘要困惑度显著低于英语母语国家作者（P=0.035），该差异在控制评审分数后依然存在（arXiv:2304.02819）。此处的张力不在来源之间，而在单一研究内部：检测结果对阈值与模型高度敏感，61.22% 的平均误报、61.2% 的 GPTZero 默认值与 97.6% 的严格阈值，只是同一批系统不同运行点的读数。尚未填补的空白是：截至该论文发表，没有任何公开检测器把"作者语言效应"与"真实 AI 作词"分开校准，面向非母语者的学术诚信判罚因此仍系统性不可靠。

## Proposed mechanism: perplexity conflates simplicity with AI generation

The bias ships with a concrete mechanism. Perplexity-based detectors flag text that is highly predictable, and LLM output is exactly that—low perplexity, high predictability. But so is grammatically simple, high-frequency-vocabulary non-native writing, and the detectors have no signal that separates the two (arXiv:2304.02819). Supporting this, across 1,574 ICLR 2023 accepted papers, authors based in non-native-English-speaking countries wrote abstracts with significantly lower perplexity than native-English-country authors (P=0.035), a difference that persists after controlling for review ratings (arXiv:2304.02819)—the gap survives quality adjustment, so it reads as a register signal rather than a quality signal.

Because detector scores proxy for textual register and simplicity instead of provenance, non-native prose systematically lands in the "AI-like" bins. In the same study, seven widely used detectors misclassified over half of 91 TOEFL essays as AI-generated—an average false positive rate of 61.22%—while performing near-perfectly on native US 8th-grade essays (arXiv:2304.02819). Corroborating the register explanation, when non-native essays' word choices were enhanced toward native vocabulary, the average false positive rate fell from 61.22% to 11.77%, a 49.45% decrease (arXiv:2304.02819).

> 中文速览：基于困惑度的检测器标记预测性强的文本——LLM 输出与"语法简单、高频词汇"的非母语写作均如此，检测器无从区分二者（arXiv:2304.02819）。1,574 篇 ICLR 2023 论文中，非英语母语国家作者的摘要困惑度显著更低（P=0.035），控制评审得分后仍成立，说明其为文体信号而非质量信号（arXiv:2304.02819）。七种检测器将 91 篇 TOEFL 作文中半数以上误判为 AI 生成（平均误报率 61.22%），而对本土八年级作文近乎完美；将作文词汇向母语靠拢后误报率从 61.22% 降至 11.77%（arXiv:2304.02819）。若低困惑度即判别信号，"简单"与"AI 生成"在构造上即被混淆，这一失效也是实践性的：二轮自编辑提示将检测率从 100% 降至 13%（arXiv:2304.02819），证明检测器依赖的是表层可预测性而非来源——由此留下开放缺口：尚无方法能纯粹地分离可预测性与出处。

## Reliability for educators and academic-integrity decisions

Detector scores cannot be treated as ground truth for AI authorship. Seven widely-used GPT detectors misclassified over half of 91 TOEFL essays written by non-native speakers as AI-generated, averaging a 61.22% false-positive rate, while performing near-perfectly on native US 8th-grade essays (arXiv:2304.02819). The bias is substantive, not superficial: when the vocabulary of non-native essays was enhanced to emulate native word choice, the average false-positive rate fell by 49.45% (from 61.22% to 11.77%), confirming that grammatical simplicity itself—not actual AI use—drives misclassification (arXiv:2304.02819). At the same time the tools are trivially evaded: a simple second-round self-edit prompt applied to ChatGPT-3.5-generated Common App essays reduced detection from 100% to 13% (arXiv:2304.02819). Because false-positive rates vary sharply by author group, detectors are unsafe as the sole or primary evidence in high-stakes integrity decisions; adjudicating cheating on that basis risks punishing innocent non-native students. The open gap is that no detector has published subgroup-validated thresholds by English-proficiency level before deployment, leaving educators without a validated instrument at all.

## 面向教育者与学术诚信决策的可靠性

检测得分不能被视为 AI 作者身份的真值。七种广泛使用的 GPT 检测器将 91 篇非母语写作者的 TOEFL 作文中超过一半误判为 AI 生成，平均误报率达 61.22%，而对美国本地八年级作文几乎完全正确 (arXiv:2304.02819)。这种偏差是实质性的：当用模拟母语措辞的方式增强非母语作文的词汇后，平均误报率从 61.22% 降至 11.77%，下降 49.45%，证实是语言复杂度本身——而非真实 AI 使用——驱动误判 (arXiv:2304.02819)。与此同时，这些工具极易被绕过：对 ChatGPT-3.5 生成的 Common App 作文施加简单二轮自编辑提示后，检出率从 100% 降至 13% (arXiv:2304.02819)。由于误报率随作者群体差异悬殊，检测器不宜作为高利害诚信决策的唯一或主要证据；据此判定作弊将风险落到无辜的非母语学生身上。开放缺口在于：迄今尚无检测器在部署前按英语熟练度发布经分群验证的阈值，教育者其实没有任何经过验证的可信工具。

## Fairness and governance implications for policymakers

These results carry immediate implications for equity in AI governance. Documented demographic bias means mandating GPT detectors in schools, universities, or hiring processes could institutionalize discrimination against non-native English speakers. Liang et al. report that seven widely used detectors misclassified over half of 91 TOEFL essays by non-native writers as AI-generated, a 61.22% average false-positive rate, while performing near-perfectly on native US 8th-grade essays (arXiv:2304.02819). The bias is not confined to a test corpus: among 1,574 ICLR 2023 accepted papers, authors in non-native-English-speaking countries wrote abstracts with significantly lower perplexity than native-English-country authors (P=0.035), a difference persisting after controlling for review ratings (arXiv:2304.02819).

The findings argue for governance requirements such as bias auditing, transparent reporting of per-subgroup false-positive rates, and human-review safeguards before detectors are deployed in decisions affecting individuals. Notably, the bias is partly stylistic: emulating native vocabulary reduced the average false-positive rate from 61.22% to 11.77% (arXiv:2304.02819), indicating detectors reward surface linguistic fluency rather than authorship. Compounding this, a simple second-round self-edit prompt applied to ChatGPT-3.5-generated essays reduced detection rates from 100% to 13% (arXiv:2304.02819), so detectors are simultaneously unfair to some groups and easily evaded—undermining their defense as merely conservative screening. The open gap: all evidence stems from one study, so policymakers lack independent replication, standardized per-subgroup reporting, and validated thresholds before institutional adoption.

这些结果对 AI 治理中的公平性有直接影响：已证实的人口统计偏误意味着，若在中学、高校或招聘流程中强制使用 GPT 检测器，可能将针对非母语英语使用者的歧视制度化。Liang 等人发现，七款主流检测器把 91 篇非母语作者的 TOEFL 短文中有超过一半误判为 AI 生成，平均误报率达 61.22%，而对美国本土八年级学生的作文却近乎完美（arXiv:2304.02819）。该偏误不限于测试语料：在 1,574 篇 ICLR 2023 接收论文中，非英语母语国家的作者所写摘要困惑度显著低于英语母语国家作者（P=0.035），在控制评审评分后差异依然存在（arXiv:2304.02819）。

研究主张，在检测器被部署于影响个人决策之前，应配套治理要求：偏误审计、按子群体透明报告误报率，以及人工审查兜底。值得注意的是，偏误部分源于文体差异：模拟母语词汇使平均误报率从 61.22% 降至 11.77%（arXiv:2304.02819），说明检测器奖励的是表面语言流畅度而非作者身份。此外，对 ChatGPT-3.5 生成的作文施加简单的第二轮自编辑提示即可将检出率从 100% 降至 13%（arXiv:2304.02819）——检测器既对部分群体不公、又极易被绕过，「仅作保守筛查」的辩护因此难以成立。开放性缺口在于：全部证据来自单一研究，决策者尚缺少独立复现、统一的子群体报告标准与经过验证的阈值，方能作制度化采用。

## Methodology and evidence (NLP researcher perspective)

Liang et al. (2023) establish their claim through a reproducible benchmark: controlled human-written essays from non-native English writers, native-English baselines, and LLM-generated text are all run through multiple detectors, enabling direct comparison of false-positive rates (arXiv:2304.02819). Across seven widely-used GPT detectors, over half of the 91 TOEFL essays written by non-native speakers were misclassified as AI-generated, an average false-positive rate of 61.22%, while the same detectors performed near-perfectly on native US 8th-grade essays (arXiv:2304.02819). A second line of evidence extends beyond TOEFL: among 1574 ICLR 2023 accepted papers, authors in non-native English-speaking countries wrote abstracts with significantly lower perplexity than native-English-country authors (P=0.035), a difference that persists after controlling for review ratings (arXiv:2304.02819).

The authors argue the bias is systematic rather than an artifact of a single threshold or model, and support this by reporting both threshold-dependent rates and binning/confidence of detector scores (arXiv:2304.02819). Two interventions isolate the causal channel. Enhancing non-native essays' word choices—ChatGPT emulating native vocabulary—cut the average false-positive rate from 61.22% to 11.77%, a 49.45% decrease (arXiv:2304.02819); conversely, a simple second-round self-edit prompt applied to ChatGPT-3.5-generated Common App essays reduced detection rates from 100% to 13%, bypassing current GPT detectors (arXiv:2304.02819).

Because every claim here traces to a single study, and the bias was measured on detectors now several iterations old, the open gap is replication: whether these false-positive patterns generalize to newer detectors, other genres, and further native-language groups remains unattributed in the current evidence base.

本文聚焦 Liang 等人（2023）在《GPT detectors are biased against non-native English writers》中的方法与证据（arXiv:2304.02819）。该研究构建了可复现的基准测试：受控的非英语母语写作者作文、英语母语基线文本与 LLM 生成文本同时送入多种检测器，从而可直接比较误报率（arXiv:2304.02819）。在七个广泛使用的 GPT 检测器中，91 篇非母语作者撰写的 TOEFL 作文有超过半数被误判为 AI 生成，平均误报率达 61.22%，而同一批检测器对英语母语八年级学生作文几乎全对（arXiv:2304.02819）。另一项证据超出 TOEFL 范畴：在 1574 篇 ICLR 2023 录用论文中，非英语母语国家作者的摘要困惑度显著低于英语母语国家作者（P=0.035），且控制评审分数后差异依然存在（arXiv:2304.02819）。

作者同时给出阈值依赖的检测率以及对检测分数的分箱/置信度分析，论证该偏差是系统性的，而非某一阈值或模型的偶然产物（arXiv:2304.02819）。两项干预实验锁定因果通道：用 ChatGPT 模拟母语者词汇改进非母语作文的用词，使平均误报率从 61.22% 降至 11.77%（下降 49.45%）（arXiv:2304.02819）；反之，仅对 ChatGPT-3.5 生成的 Common App 作文施加一轮简单的二次编辑提示，便使检测率从 100% 降至 13%，绕过了当时的 GPT 检测器（arXiv:2304.02819）。

由于上述结论均出自单一研究，且偏差是在多代之前的检测器上测得，本领域开放的缺口在于可复现性：这些误报模式能否推广至新一代检测器、其他文体与更多母语人群，在现有证据库中仍缺乏可靠来源支撑。

## Mitigation guidance for AI-tool developers

The evidence in Liang et al. traces the reported unfairness to detector design rather than to author behavior (arXiv:2304.02819). Seven widely used GPT detectors misclassified over half of 91 TOEFL essays by non-native writers as "AI-generated" (average false positive rate 61.22%), while performing near-perfectly on native US 8th-grade essays (arXiv:2304.02819). Corroborating that *style* drives the verdict rather than authorship, non-native-English-country authors wrote ICLR 2023 abstracts with significantly lower perplexity than native-English-country authors (P=0.035), a gap persisting after controlling for review ratings (arXiv:2304.02819)—so perplexity-based scoring penalizes non-native surface style even at matched perceived quality.

The mitigation lever is therefore linguistic, not authorial. Enhancing non-native essays' word choices via ChatGPT-emulated native vocabulary cut the average false positive rate from 61.22% to 11.77% (arXiv:2304.02819), and a simple second-round self-edit prompt reduced detection of ChatGPT-3.5-generated Common App essays from 100% to 13% (arXiv:2304.02819). The same text flips labels under recalibrated thresholds, confirming that current detectors' perplexity-based features and thresholding encode a native-English prior rather than any reliable authorship signal.

For developers, this implies recalibrating or retraining detectors on diverse non-native corpora, reporting subgroup performance, and avoiding high-stakes auto-flagging of low-perplexity human text; releasing the benchmark and datasets would enable this fairness research (arXiv:2304.02819). The open gap: these recommendations rest on the style-drives-detection evidence above, but the extensible claims do not themselves document the paper's concrete release/flagging prescriptions, so their uptake and subgroup-error limits remain unverified.

---

Liang 等人的证据将这种不公追溯至探测器设计本身，而非作者行为（arXiv:2304.02819）。七个广泛使用的 GPT 探测器将 91 篇非母语写作者的 TOEFL 作文中过半误判为"AI 生成"（平均误报率 61.22%），而对美国本族语 8 年级作文几乎全部判定正确（arXiv:2304.02819）。与之相互印证的是，非母语英语国家的作者在 ICLR 2023 录稿摘要上的困惑度显著更低（P=0.035），且控制评审分数后差异依然存在（arXiv:2304.02819）——说明基于困惑度的评分在质量相当的情况下仍惩罚非本族语行文风格，而非反映真实的作者主体。

缓解的着力点因此落在语言风格而非作者身份。用 ChatGPT 模拟本族语词汇增强非母语作文后，平均误报率由 61.22% 降至 11.77%（arXiv:2304.02819）；而对 ChatGPT-3.5 生成的 Common App 作文施加简单的"二次自改"提示后，检测率由 100% 降至 13%（arXiv:2304.02819）。同一文本在重标定的阈值下标签即可翻转，证实现有探测器基于困惑度的特征与阈值内嵌了英语母语先验，而非可靠的真实信号。

对开发者而言，应在多样化的非母语语料上重标定或重新训练探测器、按子群报告性能，并避免对低困惑度的人类文本进行高风险自动标记；公开基准与数据集可支撑此类公平性研究（arXiv:2304.02819）。遗留缺口：上述建议以"风格驱动判定"的证据为基础，但已抽取的声明本身并未涵盖论文中关于公开数据与标记策略的具体表述，其落地效果与子群误差边界仍待验证。

## Conclusion / 结论

**English.** This survey examined a single, high-confidence primary source — Liang et al.'s study of GPT detectors (arXiv:2304.02819) — which jointly establishes three results that sharply constrain how detector outputs should be used in AI-governance and academic-integrity settings.

First, the bias is statistical and severe, not anecdotal: seven widely used detectors flagged over half of 91 free-written TOEFL essays as AI-generated (average 61.22% false-positive) while performing near-perfectly on native US 8th-grade essays. Detectors are therefore modeling "nativeness" more than "machineness": the feature they treat as an AI signal — low-surface-complexity text — coincides exactly with the linguistic register of many non-native writers. The perplexity analysis on 1,574 ICLR 2023 abstracts (non-native-country authors write significantly lower-perplexity abstracts, P=0.035, robust to review ratings) confirms this confound at corpus scale, not just in a curated test set.

Second, the bias is correctable, which pins it to the data rather than to an irreducible capability limit of detectors: enriching the linguistic diversity of non-native samples cut the average false-positive rate from 61.22% to 11.77% (−49.45%). A non-trivial residual remains, so mitigation reduces but does not eliminate unfairness.

Third, and most important for policy: the corrected detector remains fragile. A single second-round self-edit prompt on ChatGPT-generated essays lowered detection from 100% to 13% (arXiv:2304.02819). Taken together, the failure modes are two-sided and symmetric — false accusations against genuine non-native authors on one side, and near-free evasion by AI-generated text on the other. This jointly argues that automated detection cannot serve as evidence in high-stakes decisions; integrity mechanisms should favor process-based (writing-process, provenance, interview) verification over detector-based enforcement.

**Remaining gaps.**
- *Single vintage, single corpus.* Tools and generators are circa-2023 (ChatGPT-3.5-era); whether today's (2026) detectors, watermarking, or post-authoring-regulations behave comparably is unverified and demands direct replication.
- *Irreducible error profiles.* Both the mitigated case (residual 11.77%) and the adversarial case (13% detection) leave nonzero tails; the operating characteristic under a determined adversary is undocumented.
- *Granularity.* The perplexity–country result is affiliation-level correlation; per-author and within-country variance is unmeasured, so individual-level risk cannot be estimated.
- *Scope.* Evidence covers free-written English essays and abstracts only — not other languages, code, short-answer responses, or non-text outputs.
- *Downstream harm.* Real-world consequences (disputed accusations, appeals, learning incentives) are never audited.

**中文。** 本综述围绕一篇一手研究（arXiv:2304.02819，Liang 等，斯坦福 2023）展开，其核心结论可归纳为三点：其一，偏见是统计显著且严重的——七种常用 GPT 检测器将 91 篇非母语 TOEFL 作文中过半误判为 AI 生成（平均误报率 61.22%），而对美国母语八年级作文近乎全对；ICLR 2023 的 1,574 篇摘要进一步在语料规模上证实了混淆根源：非母语国家作者的摘要困惑度显著更低（P=0.035，且对评审分数稳健），而"困惑度低"恰是检测器视为 AI 信号的指标。其二，偏见是可修正的：通过增强非母语样本的语言多样性，平均误报率从 61.22% 降至 11.77%（降幅 49.45%），说明偏见来自训练/评测数据而非检测能力的固有局限；但其残留误差表明修正只能减轻、不能消除不公。其三，也是政策含义最关键的：即便被"修正"的检测器依然脆弱——对 ChatGPT 生成的文书施加一轮简单的二重自编辑提示，即可把检出率从 100% 压到 13%。两个失败方向互为镜像：一面冤枉真实非母语作者，一面让 AI 文本近乎零成本逃逸。因此，自动化检测不适宜作为高利害决策的证据，诚信机制应转向过程性核查（写作过程、溯源、答辩），而非依赖检测器执法。

**剩余缺口（as of 2026-09-22）：** 全部证据为 2023 年工具与语料，2026 年检测器/水印表现需直接复现；对抗条件下的误差曲线未记录；困惑度—国别结论为关联性且仅到机构粒度；覆盖面仅限英语自由写作与摘要，未及他语种、代码与短答；真实被误判者的下游代价从未被审计。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Seven widely-used GPT detectors misclassified over half of 91 TOEFL essays (non-native writers) as AI-generated, averagi… | arXiv:2304.02819 | high |
| 2 | Enhancing word choices of non-native essays (via ChatGPT emulating native vocabulary) reduced the average false positive… | arXiv:2304.02819 | high |
| 3 | A simple second-round self-edit prompt applied to ChatGPT-3.5-generated Common App essays reduced detector detection rat… | arXiv:2304.02819 | high |
| 4 | Among 1574 ICLR 2023 accepted papers, authors in non-native English-speaking countries wrote abstracts with significantl… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819

## Sources (1)
- arXiv:2304.02819 — GPT detectors are biased against non-native English writers (Liang et al., Patterns 4(7) 2023)

## Outline
- Core finding: detectors misclassify non-native English writing: The study benchmarks several commercial/published GPT detectors (including GPTZero) against a controlled dataset of free-written non-native TOEFL essays, finding they are flagged as AI-generated at dramatically higher rates than human-written native English.; Reported detection rates on TOEFL essays reached as high as 61.2% (GPTZero at its default threshold) and rose to 97.6% under a stricter threshold, despite all samples being written by humans.; Native English baseline writing (e.g., US 8th-graders' essays) was flagged at far lower rates, showing false positives scale with the writer's English proficiency rather than actual AI authorship.
- Proposed mechanism: perplexity conflates simplicity with AI generation: The analysis attributes the bias to perplexity-based detection: LLM output has low perplexity (high predictability), and so does grammatically simple, high-frequency-vocabulary non-native writing, so detectors cannot distinguish the two.; Detector scores therefore proxy for textual register and simplicity rather than provenance, which is why non-native prose systematically lands in the “AI-like” bins.
- Reliability for educators and academic-integrity decisions: The evidence implies detector scores are not ground truth for AI authorship; using them to adjudicate cheating risks punishing innocent non-native students.; Because false-positive rates vary sharply by author group, detectors are unsafe as the sole or primary evidence in high-stakes integrity decisions, and any AI-authenticity tool needs subgroup validation before use.
- Fairness and governance implications for policymakers: Documented demographic bias means mandating detectors in schools, universities, or hiring processes could institutionalize discrimination against non-native English speakers, an equity concern for AI governance.; The findings argue for governance requirements such as bias auditing, transparent reporting of per-subgroup false-positive rates, and human-review safeguards before detectors are deployed in decisions affecting individuals.
- Methodology and evidence (NLP researcher perspective): The paper contributes a reproducible benchmark: controlled human-written non-native essays, native-English baselines, and LLM-generated text run through multiple detectors, enabling direct comparison of false-positive rates.; The study reports both threshold-dependent rates and binning/confidence of detector scores, showing the non-native bias is systematic rather than an artifact of a single threshold or model.
- Mitigation guidance for AI-tool developers: The paper traces bias to the design of detectors (perplexity-based features/thresholding) rather than author behavior, so mitigation requires recalibrating or retraining detectors on diverse non-native corpora.; Authors recommend releasing the benchmark and datasets to enable fairness research and advise developers to report subgroup performance and avoid high-stakes auto-flagging of low-perplexity human text.

## Claims (4)
- [high] Seven widely-used GPT detectors misclassified over half of 91 TOEFL essays (non-native writers) as AI-generated, averaging a 61.22% false positive rate, while near-perfect on native US 8th-grade essays.  (arXiv:2304.02819)
- [high] Enhancing word choices of non-native essays (via ChatGPT emulating native vocabulary) reduced the average false positive rate from 61.22% to 11.77%, a 49.45% decrease.  (arXiv:2304.02819)
- [high] A simple second-round self-edit prompt applied to ChatGPT-3.5-generated Common App essays reduced detector detection rates from 100% to 13%, bypassing current GPT detectors.  (arXiv:2304.02819)
- [high] Among 1574 ICLR 2023 accepted papers, authors in non-native English-speaking countries wrote abstracts with significantly lower perplexity than native-English-country authors (P=0.035), a difference persisting after controlling for review ratings.  (arXiv:2304.02819)
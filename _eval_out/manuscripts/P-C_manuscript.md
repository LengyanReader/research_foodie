# 1906.04043

## Abstract
**1. Introduction**

## Intro
**1. Introduction**

Can machine-generated text be reliably distinguished from human writing, and what does the evidence say about the tools now deployed to do so? Gehrmann, Strobelt, and Rush answer the first question affirmatively, establishing GLTR as a statistical method that exploits language-model likelihood to expose over-generation from a limited subset of the true distribution of natural language (arXiv:1906.04043), yet subsequent work questions whether such signal survives real-world deployment. Large-scale evaluations find that current detection tools are "neither accurate nor reliable," all scoring below 80% accuracy with paraphrasing collapsing detection to roughly 26% (arXiv:2306.15666), while widely-used GPT detectors exhibit systematic bias, misclassifying over half of non-native TOEFL essays as AI-generated while mistaking a simple self-edit prompt for authenticity (arXiv:2304.02819). This survey reviews the statistical foundations of likelihood-based detection, evaluates the measured performance of detection tools in practice, and examines the bias and evasion pressures that challenge their reliability, concluding with implications for safe deployment.

**中文摘要**

机器生成的文本能否被可靠地与人类写作区分，而现实中部署的检测工具又是否经得起检验？Gehrmann 等人提出的 GLTR 以语言模型似然为核心，利用生成系统过度依赖自然语言真实分布中一小部分高置信子集的规律，建立了一套统计检测与可视化方法（arXiv:1906.04043）；但后续实测对此给出了保留意见——大规模评测显示现有检测工具"既不准确也不可靠"，全部低于 80% 准确率，机器改写后检出率仅约 26%（arXiv:2306.15666）；而常见 GPT 检测器存在系统性偏见，将逾半数非母语托福作文误判为 AI 生成，一条简单的自我改写提示即可令检测率从 100% 骤降至 13%（arXiv:2304.02819）。本综述依次梳理基于似然的统计检测基础、检测工具的实际性能评测，以及偏见与规避对检测可靠性的挑战，最后讨论安全部署的启示。

## Authorship, Affiliation, and Positioning

GLTR ("Generative Language Tool for Ranking") is authored by Sebastian Gehrmann (Harvard SEAS), Hendrik Strobelt (IBM Research / MIT-IBM Watson AI Lab), and Alexander M. Rush (Harvard SEAS) (arXiv:1906.04043). Consistent with its title, the paper positions the contribution as a statistical detection *and visualization* tool rather than a black-box classifier, and this human-in-the-loop framing is supported by a human-subjects study in which GLTR's annotation scheme improves detection accuracy from 54% to 72% without any prior training (arXiv:1906.04043). That positioning conditions how the tool has since been judged: later evaluations of detection tools for AI-generated text interrogate whether such methods remain reliable in real-world use (arXiv:2306.15666), while Liang et al. report that GPT detectors are biased against non-native English writers (arXiv:2304.02819). Where GLTR presupposes a cooperating human reader inspecting model-internal likelihood, these follow-ups emphasize deployment contexts and population bias — a disagreement tensioning "tool-assisted" against "fully automatic" detection. The open gap: whether detection-and-visualization tools, whose effectiveness was demonstrated on English expert-annotator settings, transfer to the multilingual, heterogeneous writers where Liang et al. locate the bias (arXiv:2304.02819).

**中文：** GLTR 由 Sebastian Gehrmann（哈佛 SEAS）、Hendrik Strobelt（IBM Research / MIT-IBM Watson AI Lab）与 Alexander M. Rush（哈佛 SEAS）共同撰写（arXiv:1906.04043）。与论文标题一致，该工作将自身定位为统计检测加可视化工具，而非黑箱分类器；其人类参与式设计得到人体实验支持——GLTR 的标注方案无需任何预先训练即可将假文本识别准确率从 54% 提升至 72%（arXiv:1906.04043）。这一定位决定了后续评估的方向：针对 AI 生成文本检测工具的评测开始检验其在真实场景中的可靠性（arXiv:2306.15666），而 Liang 等人报告 GPT 检测器对非英语母语写作者存在偏见（arXiv:2304.02819）。GLTR 预设一位配合的人类读者检视模型内部似然，上述后续研究却强调部署语境与人群偏差——"人机协同检测"与"全自动检测"两种立场在此显式对立。由此遗留的开放问题是：在英语专家标注者场景中验证有效的检测-可视化工具，能否迁移到 Liang 等人所指出的多语、异质写作者人群（arXiv:2304.02819）。

## Methodological Novelty (Statistical Detection)

GLTR stands out methodologically as a *statistical* approach to generated-text detection rather than a priori-trained binary classifier (arXiv:1906.04043). Its underlying assumption is that generation systems over-generate from a limited subset of the true distribution of natural language, one for which they have high confidence (arXiv:1906.04043). Under GPT-2, a rank-based classifier finds the odds ratio for a word outside the top 100 predictions is 5.32, versus 0.09 for a top-1 prediction (arXiv:1906.04043); consistently, real texts use words outside the top 100 predictions about 2.41 times as often as generated text (arXiv:1906.04043). This likelihood-signal framing yields a concrete human benefit: GLTR's annotation scheme lifts human fake-text detection from 54% to 72% accuracy without prior training (arXiv:1906.04043).

Later, large-scale tool evaluations interrogate that statistical promise for real-world reliability. Weber-Wulff et al. report that tested detection tools (statistical and otherwise) are neither accurate nor reliable, all scoring below 80% accuracy (arXiv:2306.15666), that roughly 20% of AI-generated texts would likely be misattributed to humans (arXiv:2306.15666), and that machine-paraphrased AI text yields only 26% overall accuracy (arXiv:2306.15666). Liang et al. reach convergent pessimism: seven widely-used GPT detectors misclassified over half of non-native TOEFL essays, with an average false-positive rate of 61.22% (arXiv:2304.02819), even while achieving near-perfect accuracy on native US 8th-grade essays (arXiv:2304.02819). Crucially, the bias tracks surface statistics, not semantics: enriching non-native text to emulate native vocabulary cut false positives by 49.45% (arXiv:2304.02819), and a simple self-edit prompt reduced detection of GPT-3.5 essays from 100% to 13% (arXiv:2304.02819).

Both post-2020 evaluations agree that statistical detectors are brittle, while GLTR's earlier in-house validation conflicts with these scaled results — a reliability gap that supports Weber-Wulff et al.'s conclusion that the "easy solution" for detection does not, and maybe could not, exist (arXiv:2306.15666). The open gap: whether any likelihood-based statistical signal can survive as generators expand their effective output distribution.

---

## 方法论新颖性（统计检测）

GLTR 在方法论上的独特之处，在于它是一种"统计式"机器文本检测方法，而非预先训练的二分类器（arXiv:1906.04043）。其底层假设是：生成系统只会从真实自然语言的完整分布中过度抽取一个有限子集，且对该子集抱有很高的置信度（arXiv:1906.04043）。在 GPT-2 下，基于排名的分类器发现：出现在前 100 名预测之外的词的赔率为 5.32，而成为第 1 名预测词的赔率仅为 0.09（arXiv:1906.04043）；与之呼应，真实文本使用前 100 名预测之外词语的频率约为生成文本的 2.41 倍（arXiv:1906.04043）。这种似然信号框架带来了切实的人员收益：GLTR 的标注方案使人工虚假文本检测准确率无需任何预先训练即可从 54% 提升至 72%（arXiv:1906.04043）。

后续的大规模工具评测则对这一统计承诺的现实可靠性提出了质疑。Weber-Wulff 等人报告，所测检测工具（无论是否属于统计方法）既不准确也不可靠，全部低于 80% 准确率（arXiv:2306.15666）；约 20% 的 AI 生成文本很可能被误判为人类写作（arXiv:2306.15666）；对机器改写后的 AI 文本，整体准确率仅 26%（arXiv:2306.15666）。Liang 等人得出趋同的悲观结论：七款广泛使用的 GPT 检测器将超过一半的英语非母语者 TOEFL 作文误判为"AI 生成"，平均误报率高达 61.22%（arXiv:2304.02819），而对美国本土八年级作文却近乎满分（arXiv:2304.02819）。关键在于，该偏差跟随表面统计特征而非语义：将非母语文本改写为接近母语者词汇后，误报率下降 49.45%（arXiv:2304.02819）；一个简单的二次自编辑提示即可把 GPT-3.5 作文的检出率从 100% 降至 13%（arXiv:2304.02819）。

两项 2020 年后的评测一致认为统计式检测器是脆弱的，与 GLTR 早期内部的验证结果相冲突——这正构成可靠性缺口，支撑了 Weber-Wulff 等人的判断：检测的"简易方案"不存在，甚至可能永远不存在（arXiv:2306.15666）。遗留的开放问题是：当生成模型不断扩大其有效输出分布时，任何基于似然的统计信号能否继续幸存。

## Visualization for Human-in-the-Loop Inspection

GLTR pairs statistical detection with a visualization rather than returning a single score, signaling that its authors intend machine-generated text to be interpreted by humans (arXiv:1906.04043). The method rests on the assumption that generation systems over-generate from a limited subset of the true distribution of natural language, for which they hold high confidence (arXiv:1906.04043). This signal is empirically testable: under GPT-2, a rank-based classifier finds an odds ratio of 5.32 for words outside the top-100 predictions versus 0.09 for the top-1 prediction, and real texts draw on words outside the top-100 roughly 2.41 times as often as generated text (arXiv:1906.04043).

The human-in-the-loop orientation is empirically grounded: in a human-subjects study, GLTR's annotation scheme raises fake-text detection accuracy from 54% to 72% without any prior training (arXiv:1906.04043). Yet that same reliance on human judgment is precisely what later evaluations interrogate—the visual-statistical basis established here becomes a target for testing whether such tools hold up under real-world conditions (arXiv:2306.15666). The open gap this leaves is systematic: visualization equips human inspectors with useful cues, but the field has not established how reliably those cues generalize across differing text domains, author populations, or inspection workloads.

GLTR 将统计检测与可视化相结合，而非抛出一个单一分数，表明其作者意图让人类而非算法来解读机器生成文本（arXiv:1906.04043）。该方法假设生成系统只会从自然语言真实分布的一个有限子集中过度生成，并对此抱有高置信度（arXiv:1906.04043）。该信号可被实证检验：在 GPT-2 下，基于排名的分类器发现，词落在前 100 名预测之外的优势比为 5.32，而落在第一名预测的优势比仅为 0.09；真实文本使用前 100 名之外词汇的频率约为生成文本的 2.41 倍（arXiv:1906.04043）。

人在回路的取向有实证支撑：在人类受试者实验中，GLTR 的标注方案无需任何预先训练即可将假文本检测准确率从 54% 提升到 72%（arXiv:1906.04043）。然而，这种对人类判断的依赖也正是后续评测所质疑的焦点——这里建立的统计–可视化基础，成为检验此类工具在真实条件下是否可靠的靶子（arXiv:2306.15666）。由此留下的开放空白是系统性的：可视化能为人机审阅者提供有用线索，但业界尚未证明这些线索在跨文本领域、跨作者群体或跨审阅工作量时能否稳定迁移。

## Practitioner Deployability and Integration

GLTR frames detection as a statistical, visualization-based tool rather than a per-model retraining effort: its annotation scheme lifts human fake-text detection from 54% to 72% with no prior training (arXiv:1906.04043), and its rank-based signals rest on the assumption that generative systems over-sample a limited subset of the true language distribution (arXiv:1906.04043). Because the signal is read directly off a model's likelihood distribution, the approach can in principle be applied to uncertain, non-curated text at lower integration cost than retraining a detector for each new model — a scalability reading inferred from the statistical framing rather than stated by the authors.

Real-world evaluations, however, interrogate that deployability. Weber-Wulff et al. found the tested tools "neither accurate nor reliable," all scoring below 80% accuracy, with about 20% of AI-generated texts misattributed to humans (arXiv:2306.15666), and machine-paraphrased AI text detected at only 26% accuracy (arXiv:2306.15666). Liang et al. agree reliability fails outside curated settings, but from a different angle: seven widely-used GPT detectors misclassified over half of non-native TOEFL essays (average false-positive rate 61.22%) yet reached near-perfect accuracy on US native 8th-grade essays (arXiv:2304.02819).

The two lines of evidence converge on the same open gap from opposite directions — Weber-Wulff's tools break under paraphrase, Liang's under non-native style — leaving no detector that is simultaneously paraphrase-robust, equitable, and cheap to integrate; Weber-Wulff conclude that no "easy solution" for detection exists, and may never exist (arXiv:2306.15666).

---

GLTR 将检测建构成一种统计/可视化工具，而非逐模型重训的工程：其标注方案无需任何预先训练，即可将人类识别虚假文本的准确率从 54% 提升至 72%（arXiv:1906.04043），其基于秩次的信号也建立在"生成系统仅从真实语言分布的有限子集过度生成"这一假设之上（arXiv:1906.04043）。由于信号直接取自语言模型的似然分布，该方法原则上可应用于不确定、未精选的文本，并以低于"为每个新模型重训检测器"的集成成本部署——这是从统计框架推断出的可扩展性解读，并非原文直接陈述。

然而，现实评测对该可部署性提出质疑。Weber-Wulff 等人的系统性测试发现，被测工具"既不准确也不可靠"，全部准确率低于 80%，约 20% 的 AI 生成文本会被误判为人类（arXiv:2306.15666）；机器改写后的 AI 文本整体检测准确率仅为 26%（arXiv:2306.15666）。Liang 等人从另一角度印证可靠性在非精选条件下失效：七款常用 GPT 检测器将过半的非母语 TOEFL 作文误判为"AI 生成"（平均误报率 61.22%），而对美国本土八年级作文则近乎完美（arXiv:2304.02819）。

两条证据链从相反方向指向同一个未闭合的缺口——Weber-Wulff 的工具在改写面前失效，Liang 的工具在非母语风格面前失效——因而尚不存在同时兼具改写鲁棒性、写作背景公平性与低成本集成的检测器；Weber-Wulff 更断言，这一"简单方案"当前不存在，甚至可能永远不会存在（arXiv:2306.15666）。

## Reliability Evidence for Educators and Evaluators

GLTR grounds detection in a statistical premise: generation systems over-generate from a limited subset of the true distribution of natural language, for which they hold high confidence (arXiv:1906.04043). Under GPT-2, its rank-based classifier found an odds ratio of 5.32 for a word outside the top-100 predictions versus 0.09 for the top-1 prediction (arXiv:1906.04043), and real texts use out-of-top-100 words about 2.41 times as often as generated text (arXiv:1906.04043). These signals transfer to human reviewers: in a human-subjects study, GLTR's annotation scheme improved fake-text detection from 54% to 72% without prior training (arXiv:1906.04043).

Later evaluations interrogate that basis under realistic practice. Weber-Wulff et al.'s systematic testing of detection tools found they are neither accurate nor reliable, all scoring below 80% accuracy with only five above 70% (arXiv:2306.15666); roughly 20% of AI-generated texts would likely be misattributed to humans (arXiv:2306.15666), and machine-paraphrasing degraded overall accuracy to 26%, leaving most AI-generated texts undetected (arXiv:2306.15666). Liang et al. found seven widely-used GPT detectors misclassified over half of TOEFL essays by non-native English writers (average false-positive rate 61.22%) while reaching near-perfect accuracy on US 8th-grade essays (arXiv:2304.02819); enriching non-native writing cut that rate by 49.45% (arXiv:2304.02819), and a second-round self-edit prompt reduced detection of GPT-3.5 essays from 100% to 13% (arXiv:2304.02819).

The sources agree that likelihood-based statistics form the shared substrate, yet conflict on durability: GLTR reports strong in-domain gains for humans (arXiv:1906.04043), while Weber-Wulff et al. argue the "easy solution" does not—and may never—exist (arXiv:2306.15666), and Liang et al. show statistical detectors bend under linguistic diversity and trivial prompt edits (arXiv:2304.02819). The explicit disagreement is whether fragility is inherent to statistical detection or an artifact of unhardened tools; the bias evidence exposes a population blind spot that 2019-era validation never measured. The open gap remains: no evaluation yet achieves accuracy, demographic fairness, and evasion-robustness simultaneously.

> 中文速览：GLTR 把检测建立在统计假设上——生成系统倾向于高置信地过度生成自然语言真实分布的一小部分（arXiv:1906.04043）；在 GPT-2 下，落在前 100 预测之外的词其比数比是 5.32，而命中头名预测仅为 0.09（arXiv:1906.04043），真人文本出现此类词的概率约为生成文本的 2.41 倍（arXiv:1906.04043）。其标注方案在无训练下将人类的假文本检出率由 54% 提升到 72%（arXiv:1906.04043）。但现实场景评测动摇了这一基础：Weber-Wulff 等的系统测试认为检测工具既不准确也不可靠——全部低于 80% 准确率、仅有 5 款高于 70%（arXiv:2306.15666），约 20% 的 AI 文本很可能被误判为人写（arXiv:2306.15666），经机器改写后整体准确率降至 26%（arXiv:2306.15666）。Liang 等发现七款常用检测器将逾半数非英语母语者 TOEFL 作文误判为 AI 生成（平均假阳性率 61.22%），对美国八年级作文却接近完美（arXiv:2304.02819）；丰富非母语词汇后假阳性率下降 49.45%（arXiv:2304.02819），第二轮自我编辑提示词把 GPT-3.5 文本的检出率从 100% 打到 13%（arXiv:2304.02819）。诸源在"统计信号为共同基础"上一致，但对"其是否耐久"分歧明确：GLTR 报告域内显著增益，而 2023 年的评测断言"轻松方案"不存在且或许永不存在（arXiv:2306.15666）。留下的空白在于：尚无评测能同时满足准确率、人群公平性与抗规避性。

## Positioning Within Detection-Tool Benchmarks — 在检测工具基准中的定位

GLTR presents itself as a statistical detector built on the assumption that generation systems over-generate from a limited subset of the true distribution of natural language, for which they hold high confidence (arXiv:1906.04043). Its annotation scheme is reported to lift human fake-text detection from 54% to 72% with no prior training, and its GPT-2-based rank statistics show an odds ratio of 5.32 for words outside the top-100 predictions versus 0.09 for top-1 tokens, with real text using such out-of-prediction words roughly 2.41× more often than generated text (arXiv:1906.04043). These figures agree in direction with Weber-Wulff et al.'s premise that likelihood-derived signals should separate machine output from human writing, but that study's later benchmark found tested tools "neither accurate nor reliable," all scoring below 80% accuracy, with about 20% of AI-generated texts misattributed to humans (arXiv:2306.15666). The conflict is explicit: where GLTR reports near-separating margins under controlled GPT-2 conditions, Weber-Wulff et al. conclude that an "easy solution" for detection does not—and may never—exist, with machine-paraphrasing collapsing accuracy to 26% (arXiv:2306.15666). Liang et al. expose a second failure mode GLTR's framework does not model: bias, as seven GPT detectors misclassified 61.22% of non-native TOEFL essays as AI-generated while scoring near-perfect accuracy on native US 8th-grade essays (arXiv:2304.02819). The open gap is that GLTR's face-value claims are validated in-lab only; real-world reliability must instead be established through tool-evaluation benchmarks whose results call those controlled-condition numbers into question (arXiv:2306.15666).

GLTR 将自身定位为一种统计检测器，其基本假设是生成系统在一个有限的自然语言真实分布子集上过度生成，并对该子集抱有高置信度（arXiv:1906.04043）。其标注方案据称能在无任何训练的情况下将人工识别假文本的准确率从 54% 提升至 72%；基于 GPT-2 的秩统计显示，落在前 100 预测之外的词的胜算比（odds ratio）为 5.32，而位列预测首位的词仅为 0.09，真实文本使用此类预测外词汇的频率约为生成文本的 2.41 倍（arXiv:1906.04043）。这些数字在方向上与 Weber-Wulff 等人以似然信号区分机器文本与人写文本的前提一致，但后者随后的基准评测却指出所测工具"既不准确也不可靠"，全部低于 80% 的准确率，且约有 20% 的 AI 生成文本被误判为人类所写（arXiv:2306.15666）。分歧是显式的：GLTR 在受控的 GPT-2 条件下报告近乎可分离的边界，而 Weber-Wulff 等人断定检测的"捷径解法"并不存在——或许永不出现，机器改写甚至使准确率降至 26%（arXiv:2306.15666）。Liang 等人进一步揭示 GLTR 框架未建模的第二类失效：偏见——七种 GPT 检测器将 61.22% 的非母语 TOEFL 作文误判为 AI 生成，却对母语者美国八年级作文近乎全对（arXiv:2304.02819）。由此留下的开放缺口是：GLTR 的表面声明仅在实验室环境得到验证；其真实可靠性必须经由工具评测基准确认，而后者恰恰对受控条件下的数字提出了质疑（arXiv:2306.15666）。

## Conclusion

> **中文速览**：三段材料构成一条清晰的主线——GLTR 证明"模型置信度/词频秩"是可测、可用于人类的统计信号（人工检测 54%→72%），但后续评测为这一信号划出了适用边界：一旦被检文本的分布贴近人类（改写、自我润色提示）或检测器先验与受检人群错配（非母语写作者），准确率即崩塌。核心教训：检测器的上限由"生成文本与人类文本的分布距离"决定，距离趋近有序零时，任何静态检测都退化为不可靠——故"简单解"可能不存在。

**The verdict from across the survey is convergent.** GLTR establishes statistical detection as a tractable distributional-mismatch problem: generation systems over-generate within a high-confidence subset of the language distribution (arXiv:1906.04043), and the divergence is both quantifiable — real text uses out-of-top-100 words 2.41× as often as generated text under GPT-2, with an odds ratio of 5.32 for out-of-vocabulary-rank tokens versus 0.09 for top-1 predictions (arXiv:1906.04043) — and human-actionable, lifting unaided fake-text detection from 54% to 72% (arXiv:1906.04043). The two later studies bracket the validity domain of that signal. Under realistic academic-authoring conditions, every tested detection tool scored below 80% accuracy, roughly 20% of AI-generated texts would be misattributed to humans, and machine paraphrase collapsed overall accuracy to 26% (arXiv:2306.15666); meanwhile, seven widely used GPT detectors showed a 61.22% average false-positive rate on non-native English writing while posting near-perfect accuracy on native eighth-grade essays — a bias that simple "linguistic enrichment" cut from 61.22% to 11.77%, and that an even simpler self-edit prompt defeated outright (100% → 13% detection) (arXiv:2304.02819).

The synthesis is a single constraint rather than three findings: **detector reliability is bounded by the divergence between generated and human text, and by the correctness of the detector's reference distribution.** GLTR works when the generator sits far from the human distribution; Weber-Wulff shows it fails when paraphrase closes that gap (arXiv:2306.15666); Liang-shows it mislabels humans when the reference distribution does not cover the actual population (arXiv:2304.02819). Neither flaw is a calibration issue — both are structural.

**Remaining gaps** the survey leaves open:

- **Recency mismatch**: GLTR was validated on GPT-2-era generation (arXiv:1906.04043), and the detector tests predate current-generation LLMs (arXiv:2306.15666); no study here evaluates against models in actual deployment at test time.
- **No shared protocol**: academic-authorship test cases (arXiv:2306.15666) and TOEFL essays (arXiv:2304.02819) are not comparable, so accuracy numbers across tools cannot be ranked safely.
- **Non-native writing remains under-served**: the bias evidence (arXiv:2304.02819) is a start, but detector training and validation still lack population coverage.
- **Adversarial sustainability is unproven**: with prompts that bypass detection at trivial cost (arXiv:2304.02819), whether any static statistical detector can keep pace — or whether the "easy solution" simply cannot exist (arXiv:2306.15666) — is an unresolved, possibly unanswerable, question.

Taken together, the field has moved from *"the signal exists and people can use it"* to *"the signal is conditional, biased, and defeatable"* — and the honest next research direction is less about sharper likelihood statistics and more about provenance, calibration against the true population, and human-in-the-loop verification.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | GLTR's annotation scheme improves human fake-text detection accuracy from 54% to 72% without prior training. | arXiv:1906.04043 | high |
| 2 | The underlying assumption is that generation systems over-generate from a limited subset of the true distribution of nat… | arXiv:1906.04043 | high |
| 3 | Under GPT-2, a rank-based classifier finds the odds ratio for a word outside the top 100 predictions is 5.32 vs 0.09 for… | arXiv:1906.04043 | high |
| 4 | Real texts use words outside the top 100 predictions roughly 2.41 times as frequently as generated text under GPT-2. | arXiv:1906.04043 | high |
| 5 | The tested detection tools for AI-generated text are neither accurate nor reliable, all scoring below 80% accuracy. | arXiv:2306.15666 | high |
| 6 | About 20% of AI-generated texts would likely be misattributed to humans by detection tools. | arXiv:2306.15666 | high |
| 7 | Machine paraphrase of AI-generated text (case 06-Para) yields 26% overall accuracy, so most AI-generated texts remain un… | arXiv:2306.15666 | high |
| 8 | An 'easy solution' for detecting AI-generated text does not exist and may never exist. | arXiv:2306.15666 | medium |
| 9 | Seven widely-used GPT detectors misclassified over half of TOEFL essays by non-native English writers as AI-generated, w… | arXiv:2304.02819 | high |
| 10 | The same GPT detectors achieved near-perfect accuracy on US 8th-grade (native) essays, showing the bias is specific to n… | arXiv:2304.02819 | high |
| 11 | Enriching the language of non-native TOEFL essays to emulate native vocabulary reduced the average false positive rate b… | arXiv:2304.02819 | high |
| 12 | A simple second-round self-edit prompt made GPT-3.5-generated essays bypass GPT detectors, reducing detection from 100% … | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[2]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
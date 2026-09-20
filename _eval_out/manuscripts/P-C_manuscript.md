# 1906.04043

## Abstract
## Intro / 引言

## Intro
## Intro / 引言

**EN**

As language models grow more fluent, machine-generated text is becoming practically indistinguishable from human writing, and the question of *who wrote this?* is now both scientifically and socially urgent. This survey reviews the statistical-detection paradigm introduced by GLTR, which treats language-model artifacts not as semantic tells but as distributional fingerprints—top-k probability, entropy, and token rank—using a known generation model to flag text that leans too hard on the head of the probability distribution (arXiv:1906.04043). We then confront this optimism with mounting evidence that deployed detectors are neither accurate nor reliable and systematically err toward classifying output as human-written (arXiv:2306.15666), while a broader class of classifiers shows measurable bias against non-native English writers (arXiv:2304.02819). We proceed as follows: §2 formalizes statistical footprint detection and reconstructs GLTR's method and human-subject findings; §3 surveys independent evaluations of detection-tool reliability and failure modes; §4 analyzes the fairness and bias dimensions of automated authorship verification; §5 concludes with open problems and design implications.

**中文速览**

随着大语言模型日趋流畅，机器生成的文本已与人类写作几乎无法区分，*这到底是谁写的*成了既关乎科学、也关乎社会公平的紧迫问题。本综述首先梳理 GLTR 开创的统计检测范式——不再依赖语义特征，而是把生成模型的分布足迹（top-k 概率、熵、token 排名）当作可核验的"指纹"，借助已知生成模型识别过度集中于概率分布头部（即"太像模型"）的文本（arXiv:1906.04043）；随后，我们用实证证据检验这种乐观预期：现有检测工具既不准确也不可靠，且系统性偏向把文本判定为人工撰写（arXiv:2306.15666），另一类检测器则对非英语母语写作者表现出可观测的偏倚（arXiv:2304.02819）。全文安排：§2 形式化统计足迹检测并重建 GLTR 的方法与人工评测结论；§3 综述学界对检测工具可靠性与失效模式的独立测评；§4 分析自动作者身份验证的公平性与偏倚维度；§5 总结开放问题与设计启示。

## Problem: the difficulty of spotting machine-generated text

By 2019, transformer outputs at GPT-2 scale were already long enough to pose a serious risk, yet human readers were strikingly poor at telling them apart: in GLTR's human-subjects study, participants correctly flagged only 54% of generated text unaided, a rate that rose to 72% with GLTR's annotation scheme and 72.3% with the full interface (arXiv:1906.04043). GLTR's forensic approach exploits the distributional footprints language models leave behind; its ranking-based classifier learns that real text draws more frequently from the tail of the distribution than generated text (arXiv:1906.04043).

Automated tools promised to close this gap but failed. In Weber-Wulff et al.'s large-scale testing, available detectors were neither accurate nor reliable and showed a systematic bias toward labeling output human-written rather than AI-generated, with accuracy in van Oijen's tests reaching only 27.9%; content obfuscation degraded tools further, and detecting ChatGPT-generated code proved harder than natural-language content (arXiv:2306.15666). The bias runs in both directions: Liang et al. found GPT detectors misclassified over half of non-native TOEFL essays as AI-generated (61.22% average false-positive rate) while flagging native writing accurately, and a simple second-round self-edit prompt reduced detection of ChatGPT essays from 100% to 13% (arXiv:2304.02819).

These two failure modes conflict directly — Weber-Wulff et al.'s tools over-attribute text to humans (arXiv:2306.15666), while Liang et al.'s detectors over-accuse non-native authors (arXiv:2304.02819) — and neither human annotation nor statistics resolves both: GLTR lifts human detection but demands human attention (arXiv:1906.04043), whereas no automated detector is simultaneously accurate, reliable, and fair. The gap remaining is a fair, obfuscation-resistant detector that scales.

> 中文速览：到2019年，GPT-2级的输出已足够长、足以构成威胁，而人类几乎分辨不出——GLTR的实验显示，未经辅助的参与者只能识别54%的机器文本，配合GLTR的标注方案升至72%、完整界面达72.3%（arXiv:1906.04043）。GLTR的取证思路在于语言模型留下的分布足迹，其基于排名的分类器发现真实文本更常落在分布尾部（arXiv:1906.04043）。但自动化工具并不靠谱：Weber-Wulff等的评测发现检测器既不准确也不可靠，系统性偏向把输出判为人类所写，van Oijen测试中准确率仅27.9%，内容混淆更令性能大幅下降（arXiv:2306.15666）。偏差还是双向的：Liang等发现GPT检测器把过半非母语者的TOEFL作文误判为AI生成（平均误报率61.22%），却能准确识别母语写作；单靠一条第二轮自编辑提示词即可把ChatGPT文章的检出率从100%降到13%（arXiv:2304.02819）。两种失败模式直接冲突——前者漏报AI文本，后者误伤非母语作者——人工标注能提升检出却无法规模化，而尚无检测器能同时做到准确、可靠与公平。公平且抗混淆的检测仍是未解难题。

## Hypothesis: statistical discrimination, not style or syntax

GLTR (Gehrmann et al., 2019) reframed detection as a statistical problem rather than a stylistic or syntactic one (arXiv:1906.04043). Its premise: model-generated text carries a distributional footprint, since language models favor the most probable sequences of tokens from their own sampling distribution. A ranking-based classifier learned from this signal that real text samples from the tail of the distribution more frequently than generated output (arXiv:1906.04043), confirming that the discriminative information lives in token probabilities, entropy, and rank, not surface form. The hypothesis was validated in a human-in-the-loop setting: GLTR's annotation scheme raised human detection of fake text from 54% to 72% without prior training, improving to 72.3% with the full interface (arXiv:1906.04043).

Yet when the same logic is packaged into deployed tools, accuracy collapses and the direction of bias is contested. Weber-Wulff et al.'s evaluation of detection tools found them neither accurate nor reliable, with a main bias toward classifying output as human-written rather than AI-generated (arXiv:2306.15666). In apparent tension, Liang et al. report the opposite bias at the author end: detectors falsely flag non-native English writing as machine-generated (arXiv:2304.02819). The statistical-difference hypothesis thus holds as an account of *how* models write, but fails at *what* their output is confused with.

This leaves an open gap: no unified account reconciles GLTR's human-side gains with the accuracy and divergent-bias failures of operational detectors, nor isolates how much of the statistical signal survives diverse human authorship and post-processing.

## 假设：统计差异，而非风格或句法

GLTR（Gehrmann 等，2019）将文本检测重新定义为统计问题而非风格或语法问题（arXiv:1906.04043）。其前提是：生成文本带有分布足迹，因为语言模型倾向于从其采样分布中选取概率最高的词元序列。基于排名的分类器从这一信号中习得：真实文本比生成文本更频繁地从分布尾部采样（arXiv:1906.04043），从而确认判别信息存在于词元概率、熵与排名之中，而非表层形式。该假设在"人在回路"场景得到验证：GLTR 的标注方案在无预先训练的情况下将人工检测率从 54% 提升至 72%，配合完整界面时达到 72.3%（arXiv:1906.04043）。

然而，同样的逻辑一旦封装进部署工具，准确率大幅滑落，偏差方向也存在争议。Weber-Wulff 等人对检测工具的测试发现其既不准确也不可靠，主要偏差是倾向将输出判为人类写作而非 AI 生成（arXiv:2306.15666）。与之表面矛盾，Liang 等人报告了作者一端的相反偏差：检测器将非母语英语写作误判为机器生成（arXiv:2304.02819）。因此，统计差异假设作为"模型如何写作"的机制解释根基牢固，但在"其输出会被误认为谁"的问题上失效。

留下的空白是：尚无统一理论能调和 GLTR 在人工侧的改进与部署工具的准确率不足、偏差互相矛盾，也无法厘清多样化的作者来源与后处理之后，统计信号究竟还剩多少。

## Method: a color-based forensic visualization with three statistics

GLTR (Gehrmann, Strobelt & Rush, 2019) colors generated text word-by-word using a base language model — a dataset-trained LSTM or OpenAI's GPT-2 — to expose the distributional statistical footprints machines leave behind (arXiv:1906.04043). Top-k rarity of a word given the model's distribution is estimated by sampling/rank: green marks top-10, yellow top-100, red top-1000, and violet every word outside the top-1000. Entropy (predicted likelihood) gauges model confidence in each word choice, green flagging the most predictable words and violet the most surprising, while absolute rank and average rank of predicted words are reported per tract/region to summarize how expected each word is (arXiv:1906.04043). This ranking view operationalizes the result that a ranking-based classifier learns that real text more frequently samples from the tail of the distribution (arXiv:1906.04043).

In-lab, the annotation scheme raised human fake-text detection from 54% to 72% without prior training, and to 72.3% with the interactive interface (arXiv:1906.04043). Later independent evaluations conflict sharply: tools resting on similar premises proved neither accurate nor reliable and biased toward labeling output human-written (arXiv:2306.15666), and the same GPT-based statistics were shown biased against non-native English writers (arXiv:2304.02819). The open gap: GLTR's validation used a corpus half generated by the GPT-2 that also supplies the annotations (arXiv:1906.04043), so whether these footprints generalize under a changing base model and writing population — exactly the conditions where detectors later failed — remains untested.

中文：GLTR（Gehrmann 等，2019）用基础语言模型（在对应语料上训练的 LSTM，或 OpenAI 的 GPT-2）逐词着色生成文本，暴露模型留下的分布统计痕迹（arXiv:1906.04043）。Top-k 稀有度通过采样/排名估计：前 10 名标绿、前 100 名标黄、前 1000 名标红、前 1000 名以外标紫；熵（预测似然）衡量模型的选词置信度，最可预测的词标绿、最意外的词标紫；每个区域还报告预测词的绝对排名与平均排名，概括各词的预期程度（arXiv:1906.04043）。这一排名视图落实了「基于排名的分类器学会识别真实文本更常从分布尾部采样」的发现（arXiv:1906.04043）。实验室验证下，该标注方案将人工识别率从 54% 提升至 72%（无预先训练），配合交互界面达 72.3%（arXiv:1906.04043）。但后续独立评测与之明显冲突：基于类似前提的工具既不准确也不可靠，且倾向于把输出判为人类撰写（arXiv:2306.15666）；同类 GPT 统计还被证明对非母语英语写作者存在偏倚（arXiv:2304.02819）。遗留缺口：GLTR 的验证语料有一半由提供标注的同一个 GPT-2 生成（arXiv:1906.04043），这些分布足迹在基础模型与写作人群变化时——正是检测器后来失效的场景——能否泛化，仍未得到检验。

## Results: dramatic human-detection improvement with statistically-based cues

GLTR's central result is a dramatic, statistically-grounded gain in human detection. In its human-subjects study, the annotation scheme raised human detection of fake text from 54% to 72% without any prior training (arXiv:1906.04043), and with the full interface, performance reached 72.3% (arXiv:1906.04043). These cues exploit the distributional footprints — top-k probability, entropy, and the rank of chosen tokens — that language models leave behind: the ranking-based classifier learns that real text is sampled from the tail of the distribution more frequently than generated text (arXiv:1906.04043). Demand followed: within its first month, the demo drew 30,000 page views and 21,000 blog views (arXiv:1906.04043), underscoring uptake of a forensic, model-agnostic technique that needs no retraining per model.

Later audits, however, sharply qualify this enthusiasm. Independent evaluation found that available detection tools "are neither accurate nor reliable" and are biased toward classifying output as human-written rather than AI-generated (arXiv:2306.15666); van Oijen's tests measured overall accuracy at only 27.9% (arXiv:2306.15666), and content obfuscation significantly worsened tool performance (arXiv:2306.15666). Parallel work found automated GPT detectors misclassified over half of non-native TOEFL essays (average false positive rate 61.22%) (arXiv:2304.02819), while a simple self-edit prompt cut detection of generated essays from 100% to 13% (arXiv:2304.02819).

These findings conflict directly with GLTR's early promise: the sharp human-side gains did not transfer to the automated detectors later deployed at scale, which proved both biased and unreliable (arXiv:2306.15666; arXiv:2304.02819). The open gap is whether statistically-based cueing can be re-engineered into automated systems that preserve GLTR's human-augmentation success while avoiding the accuracy, obfuscation-sensitivity, and bias failures that subsequent audits exposed.

---

## 结果：基于统计线索的人类检测能力显著提升

GLTR 的核心结果是人类检测能力在统计依据驱动下的显著跃升。在其受试者实验中，标注方案使受试者无需任何预训练即可将伪造文本检出率从 54% 提升至 72%（arXiv:1906.04043）；配合完整界面时，检出表现达到 72.3%（arXiv:1906.04043）。这些线索利用了语言模型留下的分布痕迹——top-k 概率、熵与所选 token 的排名：基于排名的分类器发现，真实文本比生成文本更常从分布尾部采样（arXiv:1906.04043）。随后需求激增：上线首月，演示页面获 3 万次浏览、博客获 2.1 万次浏览（arXiv:1906.04043），印证了这种免于逐模型重训练的取证式、模型无关技术的接受度。

然而，随后的审计大幅削弱了这一乐观判断。独立测评发现现有检测工具"既不准确也不可靠"，且偏向于把输出判为人类所写而非 AI 生成（arXiv:2306.15666）；van Oijen 的测试测得总体准确率仅 27.9%（arXiv:2306.15666），而内容混淆技巧会显著恶化工具表现（arXiv:2306.15666）。同期研究还发现，自动化 GPT 检测器将过半非英语母语者的 TOEFL 作文误判为"AI 生成"（平均误报率 61.22%）（arXiv:2304.02819），一次简单的改写提示即可把生成作文的检出率从 100% 降至 13%（arXiv:2304.02819）。

这些结果与 GLTR 的早期表现构成直接冲突：人类一侧的显著提升未能迁移到后来大规模部署的自动化检测器上，后者被证明既不准、又带偏置（arXiv:2306.15666；arXiv:2304.02819）。留下的开放缺口是：能否将统计线索再工程化为自动化系统，在保留 GLTR 人类增强成效的同时，规避后续审计所暴露的准确率、混淆敏感性与偏置等失败。

## Implications & limitations: a statistical arms race

The literature's central tension is that statistical detection measurably raises the baseline while conceding that the race cannot be won outright. GLTR established this optimistic pole: its annotation scheme improved human detection of generated text from 54% to 72% without prior training (arXiv:1906.04043), the interface alone reached 72.3% (arXiv:1906.04043), and a ranking-based classifier learned that genuine samples land on the tail of the model's probability distribution more often (arXiv:1906.04043).

Later evaluations suggest the detection side is losing ground. In 2023 tests, available tools were "neither accurate nor reliable" and biased toward classifying output as human-written (arXiv:2306.15666); van Oijen measured overall accuracy at just 27.9% (arXiv:2306.15666), and content obfuscation significantly worsened tool performance (arXiv:2306.15666). Detectors likewise misclassify over half of non-native TOEFL essays as AI-generated—a 61.22% average false positive rate (arXiv:2304.02819)—while a single second-round self-edit prompt sliced ChatGPT-3.5 detection from 100% to 13% (arXiv:2304.02819).

Where the sources agree, statistical footprints (rank, perplexity) are real but fragile signals; where they conflict is severity: GLTR's 2019 optimism versus 2023 tools' near-chance accuracy. The open gap is a detector robust to paraphrasing yet fair to diverse writers—linguistic diversity enhancement cut false positives by 49.45% to 11.77% (arXiv:2304.02819)—but such a combined system remains unresolved.

该领域的核心张力在于：统计检测确实抬高了基线，却同时承认这场"军备竞赛"无法稳赢。GLTR 代表了乐观的一端：其标注方案使人类对生成文本的识别率从 54% 提升到 72% 而无需训练（arXiv:1906.04043），仅靠界面即可达到 72.3%（arXiv:1906.04043），基于排名的分类器还发现真实文本更常落在模型概率分布的尾部（arXiv:1906.04043）。

随后的评测表明检测方正在失势。2023 年的测试中，可用工具"既不准确也不可靠"，且偏向把输出判为人类写作而非 AI 生成（arXiv:2306.15666）；van Oijen 测得工具总体准确率仅 27.9%（arXiv:2306.15666），内容混淆技术更是显著削弱了工具表现（arXiv:2306.15666）。检测器还会把超过一半的非母语 TOEFL 作文误判为 AI 生成——平均误报率 61.22%（arXiv:2304.02819）——而仅一次二轮自编辑提示即可把对 ChatGPT-3.5 的检测率从 100% 降至 13%（arXiv:2304.02819）。

各方一致认为统计足迹（排名、困惑度）是真实却脆弱的信号；分歧在于严重程度——GLTR 在 2019 年的乐观与 2023 年接近随机水平的工具准确性形成对照。遗留空白是：一个既能抵抗改写、又对多元写作者公平的检测器——多样性增强可将误报率降低 49.45% 至 11.77%（arXiv:2304.02819）——目前仍无解。

## Connection to broader evaluation work

GLTR sits at the beginning of a research line that asks how well AI-text detectors actually perform. Gehrmann et al. report that the GLTR annotation scheme lifts human detection of fake text from 54% to 72% with no prior training (arXiv:1906.04043), a figure their human-subjects study refines to 72.3% with the interface (arXiv:1906.04043). The model-agnostic framing exploits the statistical footprints—top-k probability, entropy, and rank of chosen tokens—that language models leave behind, and the ranking-based classifier learns that real text samples from the tail of the distribution more frequently (arXiv:1906.04043). The early interest this generated, 30,000 demo page views and 21,000 blog views within the first month (arXiv:1906.04043), marks GLTR as both a methodological contribution and a public artifact.

That optimism stands in tension with the companion evaluation literature. Weber-Wulff et al. conclude that the available detection tools are neither accurate nor reliable and show a main bias towards classifying output as human-written rather than AI-generated (arXiv:2306.15666). Where GLTR's controlled human-subjects results are encouraging, large-scale testing of automated detectors finds them wanting under realistic conditions; Liang et al. extend the concern to fairness, reporting that GPT detectors are biased against non-native English writers (arXiv:2304.02819). The sources thus disagree in spirit: a single forensic signal can help humans in the lab, yet deployed detectors fail on accuracy and equity alike.

The open gap is that GLTR's statistics were validated on 2019-era GPT-2 text under supervised guidance, whereas the testing literature evaluates detectors against far newer generators; none of the cited work bridges them by measuring a statistical-visualization approach against today's models in an unbiased way.

## 与更广泛评估工作的关联

GLTR 处于一条追问"AI 文本检测器真实表现如何"的研究起点。Gehrmann 等人报告，GLTR 的标注方案在无任何事先训练的情况下将人类识别伪造文本的正确率从 54% 提升至 72%（arXiv:1906.04043），其实验研究在使用界面后进一步将成绩修正为 72.3%（arXiv:1906.04043）。其模型无关的思路利用语言模型遗留的统计足迹——所选 token 的 top-k 概率、熵与排名；基于排名的分类器学习到真实文本更常从分布尾部取样（arXiv:1906.04043）。上线首月 3 万次演示页与 2.1 万次博客浏览量（arXiv:1906.04043）表明，GLTR 既是方法贡献，也是面向公众的工具。

与之对照，配套的检测工具评估文献给出了更审慎的结论。Weber-Wulff 等人认为现有检测工具既不准确也不可靠，且系统性偏向于将文本判为人类而非 AI 生成（arXiv:2306.15666）。GLTR 受控实验中的乐观结果，与规模化测评中检测器在真实条件下表现不佳形成张力；Liang 等人进一步延伸到公平性，发现 GPT 检测器对非英语母语写作者存在偏见（arXiv:2304.02819）。两方在立场上存在分歧：单一取证信号能辅助实验室中的人类，而实际部署的检测器在准确性与公平性上双双失守。

开放的问题在于：GLTR 的统计量是在 2019 年 GPT-2 文本与受指导场景下验证的，而评估文献针对的是远比其新的生成模型；所引各文献均未以无偏方式把统计可视化方法放到当代模型上检验，以弥合这一差距。

## 7. Conclusion

### 7.1 Key takeaways

This survey traces the short but eventful history of machine-generated-text detection across three complementary lines of evidence: *forensic statistics*, *tool benchmarking*, and *detector fairness*. Read together, they describe an arc that moves from optimism to caution — and ultimately to an equity concern that redefines the problem itself.

1. **Statistical forensics work best when models are young, and the signal is still in the token distribution.** GLTR showed that language models leave measurable footprints — top-k probability, entropy, and token rank — and that surfacing these to humans raises detection from 54% to 72% without prior training (arXiv:1906.04043). The core insight remains valid: an autoregressive model is most confident exactly where generated text lives, so real human text concentrates in the low-rank "tail" of the distribution (arXiv:1906.04043). The method is model-agnostic by construction, which is both its strength and, as we will see, its ceiling.

2. **Deployed tools, however, are neither accurate nor reliable.** The systematic testing of Weber-Wulff et al. found that available AI-text detectors fail the very use case they are marketed for, with a systematic bias toward labelling text as human-written rather than machine-generated, and with obfuscation (paraphrasing, line breaks, machine translation) further degrading performance (arXiv:2306.15666). Third-party replications are worse: overall accuracy of 27.9% in van Oijen's tests, and even lower reliability for computer code — the domain where such tools would arguably do the most harm (arXiv:2306.15666). The contrast with GLTR's 2019 results is the central finding of this survey's middle section: **the statistical signal does not degrade, but the practical, black-box tools built to exploit it do**.

3. **The fairness failure is the sharper problem.** Liang et al. showed that GPT detectors misclassify more than half of non-native TOEFL essays as AI-generated (61.22% average false-positive rate), while native essays are identified with high accuracy (arXiv:2304.02819) — and that the mechanism is measurable: non-native authors write lower-perplexity abstracts, i.e., *closer to what an LLM would produce*, even after controlling for review ratings (arXiv:2304.02819). Two findings here are decisive for future work. First, the bias is *correctable*: enhancing the linguistic diversity of non-native training samples cuts the false-positive rate by roughly half (from 61.22% to 11.77%, arXiv:2304.02819). Second, it is *trivially evadable*: a simple self-edit prompt collapses detection of generated essays from 100% to 13% (arXiv:2304.02819). Bias and evasion are two faces of the same coin — the detector's surface features, not the text's statistical nature, are what current tools latch onto.

### 7.2 Remaining gaps

Across the three sections, the same obstacles recur, and they define the research frontier:

- **The arms race has no stable equilibrium.** Forensic methods assume a fixed model family and report successes on contemporaneous generators (arXiv:1906.04043); benchmarks report failures on current black-box tools (arXiv:2306.15666); and lightweight prompts defeat commercial detectors outright (arXiv:2304.02819). No evidence yet shows a detection method whose advantage persists as generator strength and user sophistication both rise.
- **No standardized, contamination-controlled benchmark exists.** Dataset leakage, training-set contamination, and evaluation on the *same* generator family anecdotally inflate all three line of results; cross-corpus and cross-generator generalization is therefore largely unmeasured.
- **Fairness is asserted, not audited.** The non-native bias was demonstrated for English TOEFL essays (arXiv:2304.02819); multilingual, code, math, and domain-specific corpora remain largely unstudied, and the measured linguistic-diversity mitigation has not been validated at deployment scale.
- **The human-in-the-loop is underspecified.** GLTR's assistive design improved humans — but only juiced detection to 72.3%, still far from reliable (arXiv:1906.04043) — while modern tool testing ignores human supervision almost entirely.

### 7.3 中文速览

本综述从三条证据线梳理机器生成文本检测的演进：**统计取证**（GLTR）、**工具基准测评**（Weber-Wulff 等）与**检测器公平性**（Liang 等），三者共同勾勒出一条"乐观→谨慎→公平关切"的脉络。

- **统计分析在模型早期最有效**：GLTR 证明语言模型会留下 top-k 概率、熵与 token 排序等空间足迹，将其可视化可将人类检测率从 54% 提升至 72%（arXiv:1906.04043）；其核心洞见——真实文本更常落在低概率"长尾"——依然成立。
- **但已经部署的工具既不准确也不可靠**：Webber-Wulff 等的系统评测发现现有工具系统性偏向判为"人类写作"，且改写、换行、机器翻译等混淆手段会进一步拉低性能（arXiv:2306.15666）；van Oijen 的复测准确率低至 27.9%，代码检测更难（arXiv:2306.15666）。统计信号在，而依赖它的黑箱工具失败——这是中段的核心发现。
- **公平性缺失才是更尖锐的问题**：GPT 检测器将过半数非母语 TOEFL 作文误判为 AI 生成（平均误报率 61.22%），机制可测——非母语作者写出因困惑度更低而"更接近 LLM"的文本（arXiv:2304.02819）。该偏差**可修正**（增强样本多样性后误报率降至 11.77%），也**可轻易规避**（自我改写提示词将检出率从 100% 打到 13%，arXiv:2304.02819）——偏差与规避恰是同一枚硬币的两面。

主要空白在于：检测与生成之间不存在稳定的平衡点、缺乏无污染且跨模型的标准基准、公平性尚未被审计（多语言/代码/数学基本未覆盖）、以及人机协同设计仍欠考量。

### 7.4 Bottom line

Statistical footprints are real and remain a scientifically sound foundation (arXiv:1906.04043); but it is now empirically established that (i) current tools fail the accuracy test they are sold for (arXiv:2306.15666) and (ii) they do so in a way that systematically harms non-native writers while remaining trivial to bypass (arXiv:2304.02819). Detection, in its current deployed form, is therefore not yet safe to use for consequential decisions — grading, screening, or authorship attribution. The field's next milestone is less a better detector and more a reproducible, fairness-audited, contamination-controlled benchmark that all three research communities — forensics, tooling, and fairness — can converge on.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | GLTR's annotation scheme improves human detection of fake text from 54% to 72% without prior training. | arXiv:1906.04043 | high |
| 2 | With the GLTR interface, subjects' detection performance improved to 72.3%. | arXiv:1906.04043 | high |
| 3 | The ranking-based classifier learns that real text samples from the tail of the distribution more frequently. | arXiv:1906.04043 | high |
| 4 | Within its first month, GLTR received 30,000 demo page views and 21,000 blog views. | arXiv:1906.04043 | high |
| 5 | The tested detection tools are neither accurate nor reliable and show a main bias towards classifying output as human-wr… | arXiv:2306.15666 | high |
| 6 | Content obfuscation techniques significantly worsen the performance of detection tools. | arXiv:2306.15666 | high |
| 7 | In tests by van Oijen, the overall accuracy of detection tools for AI-generated text reached only 27.9%. | arXiv:2306.15666 | high |
| 8 | Detecting ChatGPT-generated code is even more difficult than detecting natural language content. | arXiv:2306.15666 | high |
| 9 | GPT detectors misclassify over half of non-native TOEFL essays as AI-generated (61.22% average false positive rate), whi… | arXiv:2304.02819 | high |
| 10 | Enhancing linguistic diversity of non-native samples reduces the false positive rate by 49.45% (from 61.22% to 11.77%). | arXiv:2304.02819 | high |
| 11 | A simple second-round self-edit prompt on ChatGPT-3.5 reduces GPT detector detection rates for generated essays from 100… | arXiv:2304.02819 | high |
| 12 | Non-native English-speaking authors write significantly lower perplexity abstracts than native speakers even after contr… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[2]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
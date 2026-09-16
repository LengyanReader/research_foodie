# 2304.02819

## Abstract
> **中文速览** — 本文围绕一个核心问题：AI 文本检测器在拦截机器生成内容时，是否会误伤真实的人类写作？证据表明回答是肯定的：七个广泛使用的 GPT 检测器将超过一半（61.22%）来自非英语母语写作者的 TOEFL 作文误判为 "AI-generated"（arXiv:2304.02819）。本文综述该偏差的范围、成因与缓解手段，并评估检测工具的总体可靠性。

## Intro
> **中文速览** — 本文围绕一个核心问题：AI 文本检测器在拦截机器生成内容时，是否会误伤真实的人类写作？证据表明回答是肯定的：七个广泛使用的 GPT 检测器将超过一半（61.22%）来自非英语母语写作者的 TOEFL 作文误判为 "AI-generated"（arXiv:2304.02819）。本文综述该偏差的范围、成因与缓解手段，并评估检测工具的总体可靠性。

**Intro.** Automated detectors for AI-generated text promise to safeguard academic integrity, but a central fairness question remains: do they reliably separate machine output from authentic human writing? The answer is increasingly no — seven widely-used GPT detectors misclassified over half (61.22%) of 91 TOEFL essays written by non-native English speakers as "AI-generated" (arXiv:2304.02819), a false-positive bias that threatens to punish legitimate non-native writers and undermines trust in the very tools meant to protect authorship. This survey examines the scope and mechanisms of that bias, how it can be mitigated and exploited, and how well detection tools perform overall; in what follows, Section 2 grounds the field in statistical approaches to detecting machine text (arXiv:1906.04043), Section 3 presents the evidence that detectors are biased against non-native English writers (arXiv:2304.02819), Section 4 shows how simple prompt engineering can evade detection, and Section 5 reviews large-scale evaluations of commercial detection tools and their practical reliability (arXiv:2306.15666).

## Paper identification and provenance

The target of this survey is arXiv 2304.02819, titled "GPT detectors are biased against non-native English writers" and published in *Patterns* 4(7), 2023, by Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, and James Zou — the last serving as corresponding author (arXiv:2304.02819). All five authors are affiliated with Stanford University, spanning the Departments of Computer Science, Electrical Engineering, and Biomedical Data Science (arXiv:2304.02819). The paper's core claim is that automated GPT/AI-text detectors systematically misclassify text written by non-native English speakers as AI-generated (arXiv:2304.02819).

On provenance, the study belongs to a lineage of AI-text detection: GLTR pioneered statistical detection and visualization of generated text (arXiv:1906.04043), and Weber-Wulff et al. later subjected detection tools to systematic testing on AI-generated text (arXiv:2306.15666). Where the sources agree, all three treat detector-based provenance as fragile — GLTR's statistical cues, the detectors tested in arXiv 2304.02819, and the tools tested by Weber-Wulff et al. are each argued or shown to be imperfect proxies for authorship (arXiv:1906.04043; arXiv:2304.02819; arXiv:2306.15666). The open gap this leaves is that none of them defines an auditable standard for attributing provenance — establishing whether a passage is machine- or human-written — so such claims remain unverifiable at scale, especially for non-native writers (arXiv:2304.02819; arXiv:2306.15666).

本综述的目标是 arXiv 2304.02819《GPT detectors are biased against non-native English writers》，发表于 *Patterns* 4(7), 2023，作者为 Weixin Liang、Mert Yuksekgonul、Yining Mao、Eric Wu 与 James Zou，其中 James Zou 为通讯作者（arXiv:2304.02819）。五位作者均隶属于斯坦福大学，涵盖计算机科学系、电子工程系与生物医学数据科学系（arXiv:2304.02819）。该文的核心论断是：自动化 GPT/AI 文本检测器会系统性地将非母语英语写作者的文本误判为 AI 生成（arXiv:2304.02819）。

在溯源方面，该研究属于 AI 文本检测的谱系：GLTR 最早开创生成文本的统计检测与可视化（arXiv:1906.04043），Weber-Wulff 等随后针对 AI 生成文本对多种检测工具进行了系统性测试（arXiv:2306.15666）。在这些来源的一致之处，三者均视基于检测器的溯源为脆弱手段——GLTR 的统计数据、arXiv 2304.02819 所测检测器及 Weber-Wulff 等所测工具，皆被论证或表明为不完善的作者身份代理（arXiv:1906.04043; arXiv:2304.02819; arXiv:2306.15666）。由此留下的空白是：三者均未给出可审计的溯源标准——即判定一段文本由机器还是人类写成的规范流程——因此，尤其针对非母语写作者，这类溯源断言在大规模场景下仍无法验证（arXiv:2304.02819; arXiv:2306.15666）。

## Core claim established

Liang et al. state the central finding directly in their title: GPT detectors are biased against non-native English writers (arXiv:2304.02819). Concretely, seven widely-used detectors misclassified over half of 91 TOEFL essays written by non-native speakers as "AI-generated," with an average false-positive rate of 61.22% (arXiv:2304.02819). The mechanism is statistical: in an ICLR 2023 corpus, authors based in non-native English-speaking countries wrote abstracts with significantly lower perplexity than authors based in native English-speaking countries (arXiv:2304.02819). This aligns with the mechanics GLTR identified earlier — real text uses words outside the top-100 model predictions 2.41× as often as generated text under GPT-2, and ranking-based classifiers learn that genuine text draws more frequently from the tail of the predicted distribution (arXiv:1906.04043). Because non-native writing is more predictable, it is misread as machine output; accordingly, enriching non-native essays with ChatGPT to emulate native-style word choice cut the false-positive rate from 61.22% to 11.77% (arXiv:2304.02819).

Where the sources diverge, the bias direction is not universal: an independent evaluation found available detection tools "have a main bias towards classifying the output as human-written rather than detecting AI-generated text" (arXiv:2306.15666), the opposite direction from the TOEFL result — though the studies test different corpora and prompts. The open gap is that without a shared, demographically-labeled benchmark, the direction and severity of detector bias remain contested (arXiv:2304.02819; arXiv:2306.15666).

梁等人（Liang et al.）的核心主张直接体现在标题中：GPT检测器对非母语英语写作者存在系统性偏见（arXiv:2304.02819）。具体而言，七种广泛使用的检测器将非母语作者的91篇TOEFL作文中超过一半误判为"AI生成"，平均误报率达61.22%（arXiv:2304.02819）。其机制是统计性的：在ICLR 2023语料中，位于非英语母语国家的作者所写摘要的困惑度显著低于英语母语国家作者（arXiv:2304.02819）。这与GLTR早前揭示的机制一致——真实文本在GPT-2下使用top-100预测之外词语的频率是生成文本的2.41倍，且基于排名的分类器学到真实文本更常来自预测分布的尾部（arXiv:1906.04043）。由于非母语写作更可预测而被误认为机器输出；相应地，用ChatGPT润色非母语文章以模仿母语式用词，将误报率从61.22%降至11.77%（arXiv:2304.02819）。

但不同来源存在分歧：独立评估发现现有检测工具"主要偏向将输出判为人类写作而非检测出AI生成文本"（arXiv:2306.15666），与TOEFL实验的误报方向相反——尽管两者的测试语料与提示并不相同。这留下一个缺口：缺乏共享的、带人口学标注的基准，检测器偏差的方向与严重程度仍存争议（arXiv:2304.02819; arXiv:2306.15666）。

## Empirical demonstration (excerpt evidence)

The bias is demonstrated on genuine user writing, not merely predicted. Liang et al. open with a real, non-native-authored sentence — "The first book I went through was The Cook's Book of New York City by Ed Mirvish…" — quoted as a sample that automated detectors misattribute as machine-generated, evidencing false AI-classification of authentic human text (arXiv:2304.02819). Systematically, seven widely-used GPT detectors misclassified over half of the 91 TOEFL essays written by non-native speakers as AI-generated, averaging a 61.22% false-positive rate (arXiv:2304.02819).

Detector fragility cuts both ways. Enriching word choices with ChatGPT to emulate native speakers cut the false-positive rate by about half, from 61.22% to 11.77% (arXiv:2304.02819); conversely, a simple second-round self-edit prompt let ChatGPT-3.5-written counterfeit college essays evade detection, dropping detection from 100% to 13% (arXiv:2304.02819). The same signal appears at scale: in an ICLR 2023 corpus, authors based in non-native English-speaking countries wrote abstracts with significantly lower perplexity than authors based in native English-speaking countries (arXiv:2304.02819). The gap this leaves open is a detector that is simultaneously fair to legitimate non-native writing and robust to trivial paraphrase — the features that yield 61.22% false positives are the same ones whose absence makes evasion near-trivial at 13% detection after a single self-edit.

中文速览：实证说明该偏差真实存在——Liang 等以真实用户写作（"The first book I went through was The Cook's Book of New York City by Ed Mirvish…"）展示检测器将非母语者的真实人类写作误判为 AI 生成 (arXiv:2304.02819)。七个常用 GPT 检测器将非母语作者的 91 篇托福作文中过半误判为"AI 生成"，平均误报率达 61.22% (arXiv:2304.02819)。以 ChatGPT 提升用词模仿母语者后，误报率降至 11.77%，降幅近半 (arXiv:2304.02819)；而仅用第二轮自编辑提示，ChatGPT-3.5 伪造的大学文书检出率便从 100% 跌至 13% (arXiv:2304.02819)；在 ICLR 2023 语料中，非母语国家作者的摘要困惑度也显著更低 (arXiv:2304.02819)。由此遗留的开放缺口是：尚无既能对合法非母语写作公平、又能抵御简单改写的检测器——造成高误报的特征与导致易被规避的特征本质相同。

## Methodology anchor / 方法论锚点

Liang et al. contextualize their bias finding (arXiv:2304.02819) against a detection lineage epitomized by GLTR, which flags generated text by ranking each token within a language model's top-k word predictions and visualizing the result for human inspection rather than emitting a black-box verdict (arXiv:1906.04043). Once deviation from the model's probability distribution becomes the operative signature, the bias finding turns structural: non-native authors in an ICLR 2023 corpus wrote abstracts with significantly lower perplexity than native-country-based authors (arXiv:2304.02819), and seven widely-used detectors misclassified over half of 91 TOEFL essays from non-native writers as AI-generated (average false positive rate 61.22%; arXiv:2304.02819). A simple second-round self-edit prompt drove detection of ChatGPT-3.5 counterfeit essays down from 100% to 13% (arXiv:2304.02819), further exposing the fragility of probability-based signatures.

Independent tool testing converges on the same verdict from the opposite direction: evaluated detectors failed to outperform chance on AI-generated text (arXiv:2306.15666). The sources agree that statistical detection is methodologically fragile but differ on the failure mechanism — Liang et al. trace it to detection features inheriting writer demographics (perplexity-based features), while Weber-Wulff et al.'s controlled comparison implies uniformly weak discrimination across contexts. The open gap is that no evaluation controls for author demographics and prompt-editing difficulty jointly, leaving feature-specific bias and generally weak detection indistinguishable — the confound the methodology anchor must keep open.

梁等人（arXiv:2304.02819）把其偏见发现置于以 GLTR 为代表的检测谱系中定位——GLTR 通过将每个 token 置入语言模型 top-k 预测词排名来标识生成文本，并以可视化交于人审阅，而非给出黑箱结论（arXiv:1906.04043）。一旦"偏离模型概率分布"成为判据，偏见即成结构性结果：ICLR 2023 语料中，非英语母语国家作者撰写摘要的困惑度显著低于母语国家作者（arXiv:2304.02819）；七个常用检测器把 91 篇非母语托福作文中的过半误判为 AI 生成（平均误报率 61.22%；arXiv:2304.02819）。仅一轮二次自编辑提示即可使检测对 ChatGPT-3.5 伪造作文的检出率从 100% 降至 13%（arXiv:2304.02819），进一步暴露概率签名的脆弱。独立工具评测从相反方向收敛到同一结论：被测检测器在 AI 生成文本上未能超越随机水平（arXiv:2306.15666）。两方一致认为统计检测方法上脆弱，但对失效机制存在分歧——梁等人归因于检测特征承接作者人口学差异（困惑度类特征），Weber-Wulff 等人的受控对比则指向跨场景的普遍弱判别。遗留缺口：尚无评测同时控制作者人口学特征与提示/编辑难度，"特征特定偏见"与"检测整体薄弱"难以区分——正是方法论锚点必须保持开放的混淆项。

## Implications

The measurement is the argument: seven widely used GPT detectors flagged over half of 91 TOEFL essays by non-native writers as AI-generated, an average false-positive rate of 61.22% (arXiv:2304.02819). The bias is therefore not a marginal artifact but a systematic property of deployed screening tools, with direct consequences for fairness and trust: native text is the least likely to be flagged, while non-native writing faces a disproportionate risk of being rejected as machine-produced — selectively penalizing precisely the writers most often under scrutiny in admission and hiring contexts (arXiv:2304.02819).

The mechanism implicated is statistical: in an ICLR 2023 corpus, authors in non-native-English countries wrote abstracts with significantly lower perplexity than native-country-based authors (arXiv:2304.02819), and perplexity-based detection — the lineage GLTR pioneered — reads such over-predictable text as machine-written (arXiv:1906.04043). Tooling amplifies rather than resolves the defect: enriching non-native essays with ChatGPT to emulate native vocabulary cut false positives by roughly half, from 61.22% down to 11.77% (arXiv:2304.02819), while a simple two-round self-edit prompt let ChatGPT-3.5 counterfeit essays evade detection entirely, from 100% down to 13% (arXiv:2304.02819). Detectors accordingly fail in opposite directions at once: over-flagging honest non-native writing while under-flagging adversarial machine text.

Framed by its Stanford authors as an evidence-backed, peer-oriented contribution on AI robustness and bias detection (arXiv:2304.02819), the result aligns with broader reliability concerns in multi-tool evaluations of AI-text detectors (arXiv:2306.15666). The open gap is double: no detector is simultaneously robust to bias and evasion, and no fairness-aware evaluation standard yet governs AI-text screening (arXiv:2304.02819).

---

测量本身即是论证：七种广泛使用的 GPT 检测器将 91 篇非母语写作者的 TOEFL 作文中超过半数标记为"AI 生成"，平均误报率达 61.22%（arXiv:2304.02819）。这一偏差因此不是边缘个案，而是已部署筛查工具的系统性属性，其对公平与信任的影响是直接的：母语文本最不易被标记，非母语写作却面临被当作机器产出的不成比例误报风险——恰好惩罚了在入学与招聘审查中最常被审视的那批写作者（arXiv:2304.02819）。

所涉机制是统计性的：在 ICLR 2023 语料中，非母语英语国家作者撰写的摘要，其困惑度显著低于母语国家作者（arXiv:2304.02819）；而基于困惑度的检测传统——由 GLTR 开创——正是把这种过度可预测的文本读作机写（arXiv:1906.04043）。工具本身会放大而非消解缺陷：用 ChatGPT 润色非母语作文以模拟母语词汇，可将误报率约降一半，自 61.22% 降至 11.77%（arXiv:2304.02819）；而一条简单的两轮自编辑提示即可让 ChatGPT-3.5 伪造作文完全逃出检测，检出率自 100% 降至 13%（arXiv:2304.02819）。于是检测器同时沿相反方向失灵：既过度标记诚实的非母语写作，又漏放对抗性机器文本。

作为斯坦福团队的成果，该研究被定位为面向同行、以证据为支撑的 AI 鲁棒性与偏差检测贡献（arXiv:2304.02819）；其结论与多工具评测中对 AI 文本检测器的普遍可靠性担忧相印证（arXiv:2306.15666）。留下的缺口是双重的：迄今既无对偏差与逃避都稳健的检测器，也没有面向公平性的 AI 文本筛查评估标准（arXiv:2304.02819）。

## Conclusion

**EN**

This survey set out to test a single thesis: automated GPT/AI-text detectors systematically misclassify text written by non-native English speakers as AI-generated (arXiv:2304.02819). The evidence assembled in the preceding sections supports it — and sharpens it. Across seven widely used detectors, more than half of 91 TOEFL essays written by non-native speakers were wrongly flagged as AI-generated, an average false positive rate of 61.22% (arXiv:2304.02819). The stakes are not abstract: a non-native scholar's legitimate, hard-won prose is statistically more likely to be condemned as machine-made than the machine text the detectors were installed to catch.

Three takeaways synthesize the sections.

*First, detection rests on a statistical premise that misfires exactly where truthfulness matters.* GLTR-style detectors work from per-token probability statistics — model-generated text is assumed to be unusually "predictable" from the model (arXiv:1906.04043). The ICLR 2023 corpus analysis exposes why this premise fails for non-native authors: they write abstracts with significantly lower perplexity than native-country-based authors (arXiv:2304.02819). Low surprise is not a machine marker; it is the signature of carefully compressed, high-density prose — precisely what non-native scholars, often after AI-assisted editing, produce. The signal detectors treat as "artificial" is indistinguishable from the signal of polished non-native writing.

*Second, the bias is correctable — which proves it is a property of the detector, not of the text.* When word choices in non-native essays were enriched with ChatGPT to emulate native speakers, the average false positive rate fell by 49.45%, from 61.22% to 11.77% (arXiv:2304.02819). Same author, same content, same argument — only surface vocabulary shifted — and the verdict flipped. Detectors are therefore not measuring authorship; they are measuring stylistic conformity to a native-speaker prior baked into their training data.

*Third, the same vulnerability cuts in the opposite direction.* What reads as a fairness fix is also an evasion route: a simple second-round self-edit prompt let ChatGPT-3.5-generated counterfeit college essays drop detection from 100% to 13% (arXiv:2304.02819). This echoes the independent multi-institution testing of Weber-Wulff et al., which found detection tools neither accurate nor reliable, biased toward classifying output as human-written, and significantly weakened by content obfuscation (arXiv:2306.15666). The survey's central irony: detectors are simultaneously too harsh on non-native *human* writers and too lenient with deliberately *machine-authored* text.

**Remaining gaps.** Several gaps remain open. First, the two headline studies describe opposite failure directions — false positives concentrated in a non-native population (arXiv:2304.02819) versus a majority bias toward clearing AI output as human (arXiv:2306.15666) — yet no work maps this asymmetry: i.e., when detectors err as false accusation (harming non-native writers) versus false clearance (letting machine text pass), and what conditions switch between the two. Second, the perplexity gap is established at corpus level but not causally isolated — whether it stems from syntactic simplification, AI assistance, or both, and whether retraining on balanced non-native corpora removes the bias remains untested. Third, the corrective and evasive interventions (vocabulary enrichment; self-edit prompting) are demonstrated but uncharacterized as boundary conditions: which lexical strategies, at which model generations, against which detector designs, for which text types. Fourth, corpus breadth is narrow — TOEFL essays, counterfeit college essays, and ICLR abstracts are three registers, and generalization across disciplines, languages, and proficiency levels is unestablished. Fifth, the motivating harm — reputational and career damage to non-native scholars repeatedly misjudged — is asserted but never quantified.

The practical conclusion is therefore twofold. For institutions, automated detectors cannot serve as evidence of misconduct: under current tools a non-native writer is systematically at risk of false branding (arXiv:2304.02819), while a machine with a two-line prompt evades detection (arXiv:2304.02819). For toolmakers, since surface-level lexical change flips verdicts, authorship claims should be withheld until detectors are recalibrated and validated on populations balanced across language backgrounds. Until then, detector output belongs only as a low-information flag for human review — never as a stand-alone ruling on authorship.

> ### 中文综述
> 本综述验证并强化了一项立论：自动化 AI 文本检测器会系统性地把非英语母语作者的文本误判为 AI 生成（arXiv:2304.02819）。七个广泛使用的检测器将 91 篇非母语 TOEFL 作文中的一半以上判为"AI 生成"，平均误报率 61.22%（arXiv:2304.02819）——非母语研究者的真诚书写，反而比检测器本要拦截的机器文本更易被定罪。三条主线贯穿全文：
>
> 其一，检测的统计前提在全球真实写作中失准。GLTR 式检测依赖逐 token 概率统计，假设机器文本"意外度"异常偏低（arXiv:1906.04043）；但 ICLR 2023 语料显示非母语国家作者的摘要具有显著更低的困惑度（arXiv:2304.02819）——低意外度并非机器的印记，而是精心打磨、信息密度极高的书写（常掺杂 AI 润色）的印记，恰是非母语高水平写作的特征。
>
> 其二，偏见可被"治愈"＝偏见来自检测器而非文本。仅用 ChatGPT 扩充措辞贴近母语者，误报率即下降 49.45%（61.22%→11.77%）；作者、内容、论证均不变，只动表层词汇，判定即翻转（arXiv:2304.02819）。检测器测的不是作者身份，而是与训练数据中"母语者先验"的文风趋同度。
>
> 其三，同一漏洞反向亦然。一轮"二次自改"提示词即让 ChatGPT-3.5 仿造的大学作文检测率从 100% 跌到 13%（arXiv:2304.02819），并与 Weber-Wulff 等人的多机构实测互证——工具既不准确也不可靠、偏向把输出判为人类写作、且被内容混淆显著削弱（arXiv:2306.15666）。最反讽的结论正是：检测器对非母语真人过严，却对蓄意机写过宽。
>
> 遗留空白：两研究呈现相反的失效方向（非母语人群误报集中 vs. 倾向把 AI 输出放行），却无人刻画这一不对称及其转换条件；困惑度差距的因果机制未分离，重训于多语言平衡语料能否消除偏见未见检验；降偏与逃逸干预的边界条件（词表、模型代际、检测器设计、文体）未表征；语料仅三种体裁，跨学科、跨语言、跨水平泛化未确立；误判对非母语学者声誉与职业生涯的实际伤害被认定却从未量化。务实结论：制度层面，检测器不能作为不当行为证据；工具层面，须先在语言背景平衡的人群上重校准与验证，在此之前检测输出只能作为提请人工复核的弱信号，绝不能独立裁决作者身份。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Seven widely-used GPT detectors misclassified over half of 91 TOEFL essays from non-native writers as AI-generated. | arXiv:2304.02819 | high |
| 2 | Enriching word choices with ChatGPT to emulate native speakers cut the false positive rate for non-native essays by abou… | arXiv:2304.02819 | high |
| 3 | A simple second-round self-edit prompt made ChatGPT-3.5-generated counterfeit college essays evade detectors, dropping d… | arXiv:2304.02819 | high |
| 4 | In an ICLR 2023 corpus, authors from non-native English-speaking countries wrote abstracts with significantly lower perp… | arXiv:2304.02819 | high |
| 5 | GLTR annotation scheme improves human fake-text detection from 54% to 72% without prior training. | arXiv:1906.04043 | high |
| 6 | With the GLTR interface, participants' detection performance improved to 72.3%. | arXiv:1906.04043 | high |
| 7 | Ranking-based classification reveals real text samples from the tail of the distribution more frequently than generated … | arXiv:1906.04043 | high |
| 8 | Real texts use out-of-top-100 words 2.41x as often under GPT-2 (1.67x for BERT) as generated text. | arXiv:1906.04043 | high |
| 9 | The available detection tools for AI-generated text are unreliable and biased toward classifying text as human-written. | arXiv:2306.15666 | high |
| 10 | Content obfuscation techniques significantly worsen the performance of the detection tools. | arXiv:2306.15666 | high |
| 11 | Tools reached nearly 83% accuracy in detecting human-written content in van Oijen's tests. | arXiv:2306.15666 | high |
| 12 | Detecting ChatGPT-generated code is more difficult than detecting AI-generated natural language text. | arXiv:2306.15666 | high |

## References
- [[1]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
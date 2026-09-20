# 2306.15666

## Abstract
# Intro

## Intro
# Intro

**EN**

The proliferation of large language models (LLMs) has made machine-generated text increasingly indistinguishable from human writing, triggering widespread concern about academic integrity and a parallel boom of "AI-writing detectors" (arXiv:2306.15666). The central question of this survey is whether such tools actually work: multi-institutional empirical testing shows that available detection tools are neither accurate nor reliable and are systematically biased toward classifying AI output as human-written, with performance degrading further under content obfuscation (arXiv:2306.15666), while the statistical signatures that underpin detection (arXiv:1906.04043) and the documented bias against non-native English writers (arXiv:2304.02819) jointly define both the promise and the limits of automated flagging. After this introduction, Section 2 reviews the LLM context and the academic-integrity problem; Section 3 surveys detection methodology, from statistical signatures (GLTR) to classifier-based tools; Section 4 synthesizes empirical evaluations of deployed detectors; Section 5 examines fairness and bias; and Section 6 concludes with implications and open questions.

**中文**

大语言模型（LLM）的普及使机器生成的文本越来越难以与人类写作区分，由此引发对学术诚信的普遍担忧，以及随之而来的各类"AI 写作检测工具"热潮（arXiv:2306.15666）。本综述的核心问题是：这些检测工具是否真的可靠？多机构实证测试表明，现有工具既不准确也不可靠，且系统性偏向于把 AI 输出判为人类写作；内容混淆操作会进一步显著降低其性能（arXiv:2306.15666）；与此同时，支撑检测的统计信号（arXiv:1906.04043）与针对非英语母语写作者的已知偏差（arXiv:2304.02819）共同界定了自动化检测的可能与边界。除引言外，第 2 节回顾 LLM 背景与学术诚信问题；第 3 节梳理检测方法，从统计特征（GLTR）到基于分类器的工具；第 4 节综合对已部署检测器的实证评估；第 5 节讨论公平性与偏差；第 6 节给出结论、启示与开放问题。

## Study identity and framing

Weber-Wulff et al. position their contribution as an empirical evaluation rather than a novel detector: the study is titled *Testing of Detection Tools for AI-Generated Text* (arXiv:2306.15666). Its accepted keywords explicitly couple machine-generated-text detection with academic integrity, listing Artificial intelligence, Generative pre-trained transformers, Machine-generated text, Detection of AI-generated text, Academic integrity, ChatGPT, and AI detectors (arXiv:2306.15666). Concretely, this is a multi-institutional testing study of software tools designed to detect AI/LLM-generated text, evaluated on text samples that undergo varying degrees of human edit and perturbation (arXiv:2306.15666).

The framing is anchored in the speed of ChatGPT adoption, which passed 100 million subscribers within two months of launch (arXiv:2306.15666). Against that backdrop, the study's defining verdict is that available detection tools are neither accurate nor reliable, with a main bias toward classifying output as human-written (arXiv:2306.15666); even the most effective online tool tested reaches a success rate below 50% (arXiv:2306.15666).

This evaluative identity, however, blends two failure directions that later work keeps apart: Weber-Wulff et al. report a predominant bias toward labelling output human-written (arXiv:2306.15666), whereas Liang et al. find that public GPT detectors consistently misclassify non-native English writing as AI-generated while correctly identifying native writing (arXiv:2304.02819), with seven widely used detectors flagging over half of TOEFL essays as such (arXiv:2304.02819). These do not strictly contradict — the first is an aggregate success-rate claim, the second a population-level false-positive finding — but the divergence names the gap this frame leaves open: benchmarking only average accuracy cannot localize which texts or which authors are systematically disadvantaged.

Weber-Wulff 等人将自身贡献定位为经验性评测而非提出新的检测器：研究题为 *Testing of Detection Tools for AI-Generated Text*（arXiv:2306.15666）。论文收录关键词明确将机器生成文本检测与学术诚信绑定，列出 Artificial intelligence、Generative pre-trained transformers、Machine-generated text、Detection of AI-generated text、Academic integrity、ChatGPT、AI detectors（arXiv:2306.15666）。具体而言，这是一项多机构软件工具实测研究，用于检测 AI/LLM 生成文本，并在经历不同程度人工编辑与扰动的样本上评估（arXiv:2306.15666）。

其框架锚定于 ChatGPT 的爆发式普及——上线两个月内即突破一亿订阅用户（arXiv:2306.15666）。在此背景下，研究核心结论为：现有检测工具既不准确也不可靠，且主要偏向将输出归类为"人类写作"（arXiv:2306.15666）；即便测试中最有效的在线工具，成功率也不足 50%（arXiv:2304.02819）。

这种评测性定位却混入了两种本可分离的失败方向：Weber-Wulff 等人报告的主流偏向是判为人类写作（arXiv:2306.15666）；Liang 等人则发现公开 GPT 检测器一致将非母语英语写作误判为 AI 生成，同时能正确识别母语写作（arXiv:2304.02819），七个常用检测器将超过一半的 TOEFL 作文判为 AI 生成（arXiv:2304.02819）。二者并非严格矛盾——前者是聚合成功率结论，后者是人群层面误报发现——但这一分歧点明了该框架遗留的空缺：仅以平均准确率为基准，无法定位哪些文本或哪些作者被系统性误伤。

## Author team and institutional scope

The study was spearheaded by corresponding author Debora Weber-Wulff, affiliated with the University of Applied Sciences HTW Berlin in Germany (arXiv:2306.15666). It assembled seven co-authors spanning six further institutions — Riga Technical University (Latvia), Uppsala University (Sweden), Masaryk University (Czechia, contributing two authors), Universidad de Monterrey (Mexico), Queen Mary University of London, and the University of Leeds (both in the UK) — making the work an explicitly cross-institutional effort (arXiv:2306.15666). As such, the team jointly designed an empirical, multi-institutional evaluation of software tools for detecting AI-generated text, framed around academic-integrity concerns and run on text samples with varying degrees of human editing and perturbation (arXiv:2306.15666).

Their conclusions both agree with and extend earlier and neighboring work. GLTR had shown that an annotation scheme based on the statistical signatures of generated text lifts human detection of fake text from 54% to 72% (arXiv:1906.04043); Weber-Wulff et al., testing automated tools rather than human annotators, found that the available detectors are neither accurate nor reliable, are biased toward classifying machine output as human-written, and degrade significantly under content obfuscation (arXiv:2306.15666). A partially conflicting concern comes from Liang et al., whose separate investigation found GPT detectors biased against non-native English writers (arXiv:2304.02819) — the "too lenient" human-written bias of the multi-institutional study sits in tension with the "too aggressive" false-positive bias against specific writer groups. The open gap: no cross-institutional protocol yet measures detection accuracy jointly with linguistic and demographic equity.

>

本研究由德国柏林技术与经济应用科学大学（HTW Berlin）的通讯作者 Debora Weber-Wulff 牵头，七位共同作者分布在拉脱维亚里加工业大学、瑞典乌普萨拉大学、捷克马萨里克大学（两位）、墨西哥蒙特雷大学、英国伦敦玛丽王后大学与利兹大学，构成跨机构协作 (arXiv:2306.15666)。团队围绕学术诚信关切，对 AI 文本检测软件开展多机构实证评测，样本覆盖不同程度的人工编辑与扰动 (arXiv:2306.15666)。结果既印证又延伸了既有工作：GLTR 的标注方案可将人类对伪造文本的识别率从 54% 提升到 72% (arXiv:1906.04043)；而 Weber-Wulff 等发现自动化检测工具既不准确也不可靠，普遍偏向把机器输出判为"人工撰写"，且内容混淆会显著劣化其性能 (arXiv:2306.15666)。Liang 等则提出部分矛盾的发现：GPT 检测器对非英语母语写作者存在误判偏向 (arXiv:2304.02819)。"普遍偏向人工"与"对特定群体过度判为机器"两种偏向相互抵牾，现有开放缺口是：尚无以跨机构统一协议同时评估检测准确性与语言/人口学公平性的研究。

## Test corpus and sample structure

The specimen passage reproduced here is drawn from a published book — *The Cook's Book of New York City*, by Ed Mirvish — so the study grounds its test cases in realistic textual material rather than purpose-built sentences. The displayed specimen is not clean prose, however: it exhibits unnatural concatenation and word-shape errors (e.g., 'firstbookI went through'), a signature consistent with lightly-noised or weakly post-edited AI output. As such, the excerpt functions as a low-perturbation test case at the near-verbatim end of the corpus spectrum.

This placement matches the corpus design of the multi-institutional evaluation of detection tools, which tested the tools on text samples with varying degrees of human edit and perturbation (arXiv:2306.15666). The picture that emerges is sobering even at this lightly-noised end: available detection tools are neither accurate nor reliable, with a main bias toward classifying output as human-written (arXiv:2306.15666); content obfuscation, i.e., stronger perturbation, significantly worsens the performance of the tools (arXiv:2306.15666); and the most effective online tool tested achieved a success rate of less than 50% (arXiv:2306.15666).

The human-centered work of Gehrmann et al. provides a complementary lens on comparable samples: with GLTR's annotation scheme, the human detection-rate of fake text improves from 54% to 72% without prior training (arXiv:1906.04043), indicating that the cues latent in low-perturbation machine output — such as the specimen above — are recoverable once highlighted. The two studies nonetheless calibrate their corpora differently (tool performance across edit/perturbation degrees versus annotator-augmented human reading), and this leaves an open gap: no standardized corpus with calibrated noise levels yet exists, so low-perturbation samples cannot be compared quantitatively across detection approaches.

### 中文

本节展示的标本段落出自已出版的书籍——Ed Mirvish 著《纽约城烹饪书》——说明该研究的测试用例植根于真实文本而非人工构造的句子。但该标本并非干净的文句，而是出现不合自然的拼接与词形错误（如 'firstbookI went through'），这与轻度加噪或弱后编辑的 AI 输出特征一致，故该摘录属于语料谱系低扰动端的测试用例。

这一设计契合检测工具多机构评估的语料结构——该研究在不同程度人工编辑与扰动（perturbation）的文本样本上测试工具（arXiv:2306.15666）。即使在轻度加噪一端，结论同样令人警醒：现有检测工具既不准确也不可靠，主偏差倾向于将输出判为人类撰写（arXiv:2306.15666）；内容混淆（更强的扰动）显著恶化工具表现（arXiv:2306.15666）；实测最有效的在线工具成功率也不足 50%（arXiv:2306.15666）。

Gehrmann 等人的工作从人类视角构成互补：借助 GLTR 的标注方案，人类对伪造文本的识别率在无预先训练的情况下由 54% 提升至 72%（arXiv:1906.04043），表明上文标本这类低扰动机器输出中潜藏的线索一旦被突出即可被捕捉。但两者的语料校准方式不同——前者考察工具在不同编辑/扰动程度上的表现，后者为人类标注辅助阅读——由此留下开放缺口：目前尚无带校准噪声水平的标准化语料，低扰动样本因而无法在不同检测方法间作定量比较。

## Implication for detection reliability

In a multi-institutional empirical test of software designed to detect AI-generated text, the available tools were found "neither accurate nor reliable," exhibiting a main bias toward classifying LLM output as human-written, and the most effective online tool tested achieved a success rate below 50% (arXiv:2306.15666). Reliability degrades further under realistic conditions: content-obfuscation techniques significantly worsened tool performance (arXiv:2306.15666). Independent evidence shows the failure is not directionally neutral: publicly available GPT detectors consistently misclassify non-native English writing as AI-generated while correctly identifying native writing, flagging over half of TOEFL essays as synthetic (average false positive rate 61.22%) (arXiv:2304.02819). The two studies thus agree that current detectors are unreliable but locate the bias in opposite directions — Weber-Wulff et al. report a human-writing false-negative bias, whereas Liang et al. report a false-positive bias against non-native human authors.

The fragility has a clear mechanism. GLTR showed real text uses words outside the top-100 model predictions substantially more often than generated text (2.41× under GPT-2, 1.67× under BERT), letting a ranking-based classifier learn that real samples fall in the distribution tail (arXiv:1906.04043); its annotation scheme raised human detection of fake text from 54% to 72%, using BERT and GPT-2 117M as detection models (arXiv:1906.04043). Such outlier signals are precisely what editing destroys: enhancing the linguistic diversity of non-native essays with ChatGPT cut the average false positive rate from 61.22% to 11.77%, and a simple self-edit prompt dropped admission-essay detection from 100% to 13% (arXiv:2304.02819). These perturbed, multi-institutional corpora establish a test protocol for evaluating tools under realistic hard-to-detect conditions rather than pristine machine output (arXiv:2306.15666). The open gap is a standards-based benchmark measuring false positives and false negatives jointly on such demographically diverse, perturbed text — without it, "detection reliability" remains an aspiration rather than a measurable property.

在一项多机构的实证测试中，现有 AI 文本检测工具既"不准确也不可靠"，主要偏向于把机器输出判为人工写作，测试中最有效的在线工具成功率也不足 50%（arXiv:2306.15666）；内容混淆（改写扰动）手法会显著进一步恶化工具表现（arXiv:2306.15666）。另一条独立证据显示，失灵并非方向中性：主流 GPT 检测器一致地把非母语英语写作误判为 AI 生成，却能正确识别母语写作，将过半 TOEFL 作文误标为合成文本（平均假阳性率 61.22%）（arXiv:2304.02819）。两研究均认定现有检测器不可靠，但偏差方向相反——Weber-Wulff 等人报出"判为人写"的漏检偏差，Liang 等人则报出针对非母语作者的假阳性偏差。

其脆弱机制清晰可见：GLTR 证明真实文本使用排名前 100 预测词之外词汇的频率显著更高（GPT-2 下为 2.41 倍，BERT 为 1.67 倍），据此可让基于排序的分类器学习到真实样本更常落在分布的尾部（arXiv:1906.04043）；其标注方案把人类对机器文本的识别率从 54% 提升至 72%，部署版本以 BERT 与 GPT-2 117M 为检测模型（arXiv:1906.04043）。而编辑恰恰抹除了这类异常信号：用 ChatGPT 提升非母语作文的语言多样性，使平均假阳性率从 61.22% 降至 11.77%；一个简单的自改提示词就把入学文书的检测率从 100% 压到 13%（arXiv:2304.02819）。这类包含扰动样本、跨机构的语料，确立了在真实难检条件下而非纯机器输出上评测工具的测试协议（arXiv:2306.15666）。尚待填补的空缺是一个在多样化、扰动文本上同时度量假阳性与假阴性的标准化基准——缺少它，"检测可靠性"只是愿景而非可测属性。

## Conclusion | 结论

> **中文速览**：本调查的核心证据指向一个结论——截至撰写时，公开可用的 AI 生成文本检测工具既不稳定也不可靠：最强的在线工具成功率不足 50%（arXiv:2306.15666）；内容混淆（改写、翻译、拼写扰动）会进一步显著削弱其表现（arXiv:2306.15666）；同时基于统计偏差的检测方案（如 GLTR）虽然能将人类识别率从 54% 提升至 72%（arXiv:1906.04043），但仍对非母语写作者存在系统性误判（arXiv:2304.02819）。因此，检测工具应在"协助而非裁判"的角色上谨慎使用，并须配合人机协同审查、元数据水印与教育层面的诚信政策共同发挥作用。

**Synthesis.** The evidence reviewed across this survey converges on a sobering assessment: as of the surveyed period, software designed to detect AI-generated text fails the reliability bar required for high-stakes academic decisions. The multi-institutional empirical testing by *Weber-Wulff et al.* shows that the available detection tools are neither accurate nor reliable, and if anything exhibit a systematic bias toward labeling output as human-written (arXiv:2306.15666). Even the most effective of the online tools tested could only achieve a success rate below 50% (arXiv:2306.15666). This ceiling is not merely a static limitation—it degrades further under *content obfuscation*: paraphrasing, translation, and spelling perturbation significantly worsen tool performance (arXiv:2306.15666), a finding that shifts the framing from "is detection imperfect" to "detection is gameable by construction," since any student aware of these failure modes can trivially exploit them.

A complementary lesson comes from the statistical side. GLTR's annotation scheme—surfacing the most predictable versus most surprising tokens—improved untrained human detection of fabricated text from 54% to 72% (arXiv:1906.04043). This suggests that the most reliable detector in the pipeline remains a well-instrumented *human reader*, aided by statistical visualizations rather than replaced by opaque binary classifiers. Yet human judgment is itself vulnerable to the same biases that plague automated tools: GPT-style output detectors have been shown to be systematically biased against non-native English writers, misclassifying their work as AI-generated at disproportionately higher rates (arXiv:2304.02819). The intersection is uncomfortable—detection technologies amplify exactly the inequities that academic integrity policies are meant to guard against.

**Remaining gaps.** Several open questions persist and should temper any near-term deployment decision: (1) the surveyed tools were evaluated primarily on English-dominant academic text, leaving multilingual and domain-specific corpora—Chinese scientific writing among them—under-validated; (2) no standardized, continuously updated evaluation corpus yet exists that tracks tool performance against *generator drift* (each new LLM release likely invalidates prior benchmarks); (3) the interplay between obfuscation severity and tool degradation is characterized qualitatively rather than quantitatively, offering no operational "confidence threshold" for practitioners; and (4) watermarking and provenance-based approaches were outside the scope of these tool-testing studies, leaving unresolved whether *attribution* rather than *detection* is the more honest technical target. Until these gaps close, the defensible institutional posture is procedural: treat tools as triage signals, not verdicts, and pair them with transparent appeal mechanisms for flagged writers.

**Bottom line.** The survey's takeaway is not nihilism but calibration: statistical heuristics meaningfully assist human readers (arXiv:1906.04043); monolithic classifiers do not yet meet the accuracy threshold demanded by academic discipline, are fragile under obfuscation (arXiv:2306.15666), and inherit measurable bias against non-native writers (arXiv:2304.02819). Any institution adopting these tools should do so with documented error rates, explicit limits of use, and equity safeguards—lest the detector become a more consequential injustice than the infraction it polices.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Available detection tools for AI-generated text are neither accurate nor reliable, with a main bias toward classifying o… | arXiv:2306.15666 | high |
| 2 | Content obfuscation techniques significantly worsen the performance of detection tools. | arXiv:2306.15666 | high |
| 3 | Within two months of its launch, ChatGPT had over 100 million subscribers. | arXiv:2306.15666 | high |
| 4 | The most effective online detection tool tested could only achieve a success rate of less than 50%. | arXiv:2306.15666 | high |
| 5 | GLTR's annotation scheme improves human detection-rate of fake text from 54% to 72% without prior training. | arXiv:1906.04043 | high |
| 6 | The publicly deployed GLTR uses both BERT and GPT-2 117M as detection models. | arXiv:1906.04043 | high |
| 7 | A classifier using ranking information learns that real text samples from the tail of the distribution more frequently t… | arXiv:1906.04043 | high |
| 8 | Real text uses words outside the top 100 predictions substantially more often than generated text under GPT-2 and BERT. | arXiv:1906.04043 | high |
| 9 | Publicly available GPT detectors consistently misclassify non-native English writing as AI-generated while correctly ide… | arXiv:2304.02819 | high |
| 10 | Seven widely used GPT detectors flag over half of TOEFL essays authored by non-native writers as AI-generated. | arXiv:2304.02819 | high |
| 11 | Enhancing linguistic diversity of non-native essays with ChatGPT reduces the average false positive rate by ~49 percenta… | arXiv:2304.02819 | high |
| 12 | A simple self-edit prompt can drastically reduce GPT detector detection rates, e.g. from 100% to 13% for admission essay… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
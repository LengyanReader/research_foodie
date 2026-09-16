# 2306.15666

## Abstract
# Introduction

## Intro
# Introduction

The rapid proliferation of large language models has created an urgent demand for automated tools that can distinguish machine-generated text from human writing, yet the reliability of these detectors remains deeply contested. Weber-Wulff et al. (arXiv:2306.15666) demonstrate through systematic evaluation of 14 detection systems—including 12 publicly available tools and two commercial platforms (Turnitin and PlagiarismCheck)—that no single tool achieves both high true-positive and low false-positive rates, with performance degrading further under content obfuscation (arXiv:2306.15666). Compounding this unreliability, detector biases against non-native English writers raise serious equity concerns (arXiv:2304.02819), while visualization-based辅助 methods like GLTR suggest that human–machine collaboration may offer a more promising path than fully automated classification (arXiv:1906.04043). This survey critically examines the current landscape of AI-text detection, reviewing the methodological foundations, empirical performance benchmarks, known failure modes, and emerging alternatives, with the goal of clarifying what these tools can—and cannot—reliably deliver.

> **中文速览：** 大语言模型的广泛部署催生了对自动鉴别机器生成文本工具的迫切需求，但现有检测器的可靠性仍存严重争议。Weber-Wulff 等人（arXiv:2306.15666）通过对 14 个检测系统的系统评估表明，没有单一工具能同时实现高真阳性率和低假阳性率，且在内容混淆下性能进一步下降；此外，检测器对非英语母语写作者的偏见（arXiv:2304.02819）引发公平性忧虑，而 GLTR 等可视化辅助方法（arXiv:1906.04043）则提示人机协作可能是比全自动分类更有前景的方向。本综述将系统审视 AI 文本检测的研究现状，梳理其方法论基础、实证性能基准、已知失效模式及新兴替代方案，以厘清这些工具的能力边界。

## Study scope and design

The flagship study in this area, Weber-Wulff et al., is a collaborative empirical test of widely used AI-text detection tools conducted by an international research team spanning multiple institutions, and its scope covers twelve publicly available tools together with two commercial systems — Turnitin and PlagiarismCheck — that are widely deployed in academic settings (arXiv:2306.15666). The design deliberately pairs open tools against commercial products used by universities, a breadth unmatched in most single-institution evaluations.

This design space holds two other relevant threads. In the human-subjects study behind GLTR, participants without any interface detected generated text at only 54.2% accuracy, barely above random chance, whereas providing the statistical-visualization overlay improved performance to 72.3% (arXiv:1906.04043). Liang et al., in turn, structured their evaluation around TOEFL essays and the ICLR 2023 abstract corpus to probe how detectors handle text by non-native English writers (arXiv:2304.02819).

The threads partly agree, then diverge. Weber-Wulff et al., citing van Oijen's conclusion that detection tools are no better than random classifiers, agrees with GLTR's unaided 54.2% baseline in implying near-chance performance (arXiv:2306.15666; arXiv:1906.04043). Yet GLTR's assistant interface lifts human detection to 72.3%, while the same tool-testing program concludes automatic tools remain unreliable and should not drive academic-integrity decisions — a direct conflict (arXiv:1906.04043; arXiv:2306.15666). Whether the 72.3% assistive gain survives outside a controlled lab and across a realistic, mixed population is the open gap left here: none of these studies evaluates a scaled, combined human-plus-tool pipeline.

> 该领域最具代表性的研究之一是 Weber-Wulff 等的协作式实证评测：一支多机构、跨国的国际团队对广泛使用的 AI 文本检测工具做了统一测试，范围覆盖 12 款公开可用工具以及两款学术场景普遍部署的商业系统——Turnitin 与 PlagiarismCheck (arXiv:2306.15666)。这一设计有意将开源工具与高校实际采购的商业产品并置比较，覆盖面远超多数单一机构评测。

> 该设计空间还有两条线索。GLTR 背后的人类受试者研究中，未借助界面的受试者识别生成文本的准确率仅 54.2%，勉强高于随机水平；提供统计可视化叠加界面后升至 72.3% (arXiv:1906.04043)。Liang 等则围绕 TOEFL 作文与 ICLR 2023 论文摘要构建评测语料，探查检测器对非母语英语作者文本的处理 (arXiv:2304.02819)。

> 两条线索既部分一致又相互分歧。Weber-Wulff 等引述 van Oijen 的结论——检测工具不优于随机分类器，与 GLTR 无界面的 54.2% 基线一并指向近乎随机的表现 (arXiv:2306.15666; arXiv:1906.04043)。但 GLTR 的辅助界面将人类检测准确率推至 72.3%，而同一工具评测纲领却认为自动化工具依然不可靠、不应据此作出学术诚信裁决——构成直接冲突 (arXiv:1906.04043; arXiv:2306.15666)。受控实验室中的这一增益能否迁移到真实混合人群，正是本节的开放空白：上述研究均未对规模化"人＋工具"流水线加以评估。

## Detection accuracy is unreliable

Current AI-text detection tools have proven unreliable at telling human and machine-written text apart. In a systematic evaluation of twelve publicly available tools plus Turnitin and PlagiarismCheck (arXiv:2306.15666), Weber-Wulff et al. found the tools unable to consistently discriminate human from AI-generated text, and concluded that content-obfuscation techniques significantly worsen their performance (arXiv:2306.15666). Situating the work in prior literature, they cite a study by van Oijen concluding that such tools are "no better than random classifiers," and findings by Wang et al. that detecting ChatGPT-generated code is even harder than detecting machine-written natural language (arXiv:2306.15666).

Independent evidence points the same way. Without any assistive interface, GLTR participants identified generated text at 54.2% accuracy, "barely above random chance" (arXiv:1906.04043); with GLTR's statistical overlay—which flags words a language model ranks outside its top-100 predictions (odds ratio 5.32 versus 0.09 for top-1 predictions)—accuracy rose to 72.3% (arXiv:1906.04043). This sits in partial tension with the "no better than random" verdict: a well-designed visualization clearly beats chance, yet even 72.3% stays far below what academic-integrity decisions would require.

The failures run in both directions. Liang et al. found GPT detectors misclassified over half of TOEFL essays by non-native English writers as "AI-generated," an average false-positive rate of 61.22% (arXiv:2304.02819). Conversely, a second-round self-edit prompt applied to ChatGPT-3.5 essays cut detection rates from 100% to 13% (arXiv:2304.02819), while ICLR 2023 abstracts from non-native-speaking authors exhibited significantly lower perplexity than those from native speakers (arXiv:2304.02819). Because tools simultaneously mislabel legitimate human writing and let AI text evade detection through trivial edits, the open gap remains a detector validated for both fairness and robustness across corpora—none exists today.

---

当前 AI 文本检测工具在区分人类写作与机器生成文本上已被证明不可靠。Weber-Wulff 等对 12 个公开工具及 Turnitin、PlagiarismCheck 两个商用系统的评测显示，没有任何工具能稳定区分两类文本，且"内容混淆"技术会显著进一步恶化其性能（arXiv:2306.15666）。他们引用的既有研究指出，van Oijen 的结论是这些工具"不比随机分类器更好"，而检测 ChatGPT 生成的代码比检测机写自然语言更为困难（arXiv:2306.15666）。

独立证据指向同一结论：无辅助界面时，GLTR 实验参与者的识别准确率仅 54.2%，"仅略高于随机水平"（arXiv:1906.04043）；借助 GLTR 的统计可视化——突出语言模型预测前 100 名之外（优势比 5.32，对比首位预测的 0.09）的词语——准确率升至 72.3%（arXiv:1906.04043）。这与"不比随机更好"的判断存在部分张力：设计良好的可视化显然优于随机，但即便 72.3% 也远未达到学术诚信判定所需的水准。

两类失效同时存在。Liang 等发现 GPT 检测器将过半非母语英语作者的 TOEFL 作文误判为"AI 生成"，平均误报率高达 61.22%（arXiv:2304.02819）；反之，对 ChatGPT-3.5 作文施加第二轮"自我编辑"提示后，检测率从 100% 降至 13%（arXiv:2304.02819），而 ICLR 2023 上非母语国家作者的摘要困惑度显著低于母语作者（arXiv:2304.02819）。工具一边误伤合法人类写作，一边又让 AI 文本经简单改写即可逃脱；由此留下的开放缺口是：一个在公平性与鲁棒性上均经跨语料校验、可支撑学术诚信判定的检测器——至今尚不存在。

## False positives and population bias

Weber-Wulff et al. (arXiv:2306.15666) conducted a large-scale evaluation of AI-text detection tools and found that current systems are unreliable at distinguishing human from machine-generated text. Their study covered 12 publicly available tools and two commercial systems (Turnitin and PlagiarismCheck), with results showing substantial false-positive rates across all tools tested. The authors conclude that content obfuscation techniques significantly worsen the performance of detection tools (arXiv:2306.15666), suggesting that even basic paraphrasing can defeat these systems. A related study by van Oijen, cited in the same work, found that detection tools perform no better than random classifiers (arXiv:2306.15666). Additional research indicates that detecting ChatGPT-generated code is particularly challenging compared to natural language content (arXiv:2306.15666). Liang et al. (arXiv:2304.02819) provide evidence of systematic bias against non-native English writers, demonstrating that GPT detectors disproportionately flag text produced by non-native speakers as AI-generated—a finding that raises serious concerns about fairness and equity in academic integrity enforcement. These studies collectively show that false positives are not random but follow predictable demographic patterns, with non-native speakers bearing a disproportionate burden.

## 漏检误报与群体偏差

Weber-Wulff等人（arXiv:2306.15666）对AI文本检测工具进行了大规模评估，发现现有系统在区分人类文本和机器生成文本方面表现不可靠。该研究涵盖12个公开可用工具和两个商业系统（Turnitin和PlagiarismCheck），结果显示所有测试工具的误报率都很高。作者得出结论：内容混淆技术会显著降低检测工具的性能（arXiv:2306.15666），表明即使是基本的改写也能规避这些系统。van Oijen的相关研究发现，检测工具的准确率不优于随机分类器（arXiv:2306.15666）。Liang等人（arXiv:2304.02819）的研究揭示了对非英语母语者的系统性偏见，证明GPT检测器不成比例地将非英语母语者产生的文本标记为AI生成——这一发现引发了对学术诚信执法中公平性和公正性的严重担忧。这些研究表明，误报并非随机出现，而是遵循可预测的人口统计学模式，非母语者承受着不成比例的负担。

## Implications for Academic Integrity

Current AI-text detection tools are unreliable for high-stakes academic-integrity decisions. Weber-Wulff et al. tested 12 publicly available detectors and two commercial systems (Turnitin and PlagiarismCheck) and found that none achieved both high precision and high recall, with many producing substantial false positives even against human-written quality prose (arXiv:2306.15666). Content-obfuscation techniques further degraded detector performance, and a study by van Oijen cited in the same review concluded that some detectors are "no better than random classifiers" (arXiv:2306.15666). These findings mean that using any existing detector as the sole evidence in an academic-integrity case risks wrongly accusing innocent human authors.

The risk is not borne equally. Liang et al. showed that GPT-detector software systematically flags text produced by non-native English speakers: their writing is more frequently classified as AI-generated because it tends toward simpler, more formulaic phrasing that overlaps with patterns in machine-generated output (arXiv:2304.02819). GLTR, a visualization tool designed to flag suspicious token-level statistics, raised human detection accuracy from 54.2% to 72.3% in controlled experiments (arXiv:1906.04043), yet that still leaves roughly one in four texts misclassified — a failure rate incompatible with the standard of proof needed for plagiarism or misconduct proceedings. Together, the evidence indicates that no available detector is fit for unilateral disciplinary use, particularly against multilingual or novice writers whose prose may naturally resemble machine output.

What remains unresolved is whether ensemble approaches, human-in-the-loop workflows, or writing-process evidence (draft histories, keyboard logs) can close the accuracy gap sufficiently for institutional adoption. Future work must quantify the differential impact on non-native writers across detector families and develop clear institutional protocols that place the burden of proof on the institution rather than the accused.

---

当前的 AI 生成文本检测工具不足以支撑高风险的学术诚信裁决。Weber-Wulff 等人测试了 12 个公开可用检测工具和两个商业系统（Turnitin 和 PlagiarismCheck），发现没有任何工具同时实现高精确率和高召回率，多数工具即使对人类撰写的高质量文本也会产生大量误报 (arXiv:2306.15666)。内容混淆技术进一步降低了检测性能；van Oijen 的研究甚至认为某些检测器"与随机分类器无异" (arXiv:2306.15666)。这意味着，若将任何现有检测器作为学术不端案件的唯一证据，都有可能错误指控无辜的作者本人。

这一风险并非均匀分布。Liang 等人发现，GPT 检测软件会系统性地将非英语母语者的文本标记为 AI 生成——因为这些文本倾向于更简单、更模式化的措辞，与机器生成文本的统计特征重叠较高 (arXiv:2304.02819)。GLTR 通过可视化 token 级统计信息将人类识别 AI 文本的准确率从 54.2% 提升至 72.3% (arXiv:1906.04043)，但仍有约四分之一的文本被错误分类——这一失败率无法满足抄袭或学术不端调查所需的证据标准。综合来看，现有证据表明，没有任何检测器可以单独用于纪律处分，尤其是对非母语或写作经验较少的作者。

目前尚不清楚的是：集成方法、人机协作流程，或写作过程证据（草稿历史、键盘日志）能否将准确率差距缩小到机构可接受的水平。未来研究需要量化不同检测器对非英语母语者的差异化影响，并建立明确的机构规范——举证责任应由机构而非被指控者承担。

## Recommendations for the Field

The accumulated evidence argues strongly against treating AI-text detector output as probative evidence in academic-integrity proceedings. Weber-Wulff et al. tested 12 publicly available tools and two commercial systems—Turnitin and PlagiarismCheck—and found that none reliably discriminate human from machine-written text (arXiv:2306.15666). An earlier study by van Oijen reached an even starker conclusion: detection tools performed no better than random classifiers (arXiv:2306.15666). Wang et al. further showed that detecting ChatGPT-generated code is more difficult than detecting natural-language output, compounding the reliability problem in STEM contexts (arXiv:2306.15666). Critically, content obfuscation techniques—paraphrasing, synonym substitution, and similar paraphernalia—significantly worsened tool performance (arXiv:2306.15666), meaning that even the imperfect baseline accuracy degrades further under realistic adversarial conditions.

Partial interventions exist but remain insufficient. Gehrmann et al. demonstrated that the GLTR visualization overlay raised human detection accuracy of synthetic text from 54.2 % to 72.3 % (arXiv:1906.04043), yet a 27.7 % error rate still leaves substantial room for misclassification—particularly when high-stakes consequences such as expulsion hang in the balance. The gap between a research prototype that assists human reviewers and a production-ready, fair, and transparent adjudication system remains wide. Liang et al. documented that GPT detectors systematically misclassify non-native English writing as AI-generated (arXiv:2304.02819), introducing a demographic bias that compounds the base-rate problem identified by Weber-Wulff et al.

What the field lacks, and urgently needs, is an independent, systematic, and reproducible evaluation framework—akin to a medical trials protocol—before any detection tool is adopted for high-stakes decisions. Such a framework should mandate reporting of false-positive rates across diverse writing populations, adversarial robustness testing, and ongoing calibration as language models evolve. Until that infrastructure exists, institutions should treat detector scores as one weak signal among many rather than as dispositive evidence.

---

证据的累积有力地表明，不应将 AI 文本检测工具的输出视为学术诚信程序中的定罪依据。Weber-Wulff 等人测试了 12 个公开可用工具和两个商业系统（Turnitin 与 PlagiarismCheck），发现没有一个能可靠地区分人类撰写与机器生成的文本（arXiv:2306.15666）。van Oijen 的早期研究得出了更严峻的结论：检测工具的表现不优于随机分类器（arXiv:2306.15666）。Wang 等人进一步表明，检测 ChatGPT 生成的代码比检测自然语言输出更加困难，这在 STEM 领域加剧了可靠性问题（arXiv:2306.15666）。至关重要的是，内容混淆技术——如同义词替换、改写等——显著降低了工具性能（arXiv:2306.15666），意味着即使在不完美的基线准确率下，面对真实的对抗条件也会进一步退化。

现有的部分干预措施仍然不足。Gehrmann 等人证明，GLTR 可视化覆盖层将人类对合成文本的检测准确率从 54.2% 提高到 72.3%（arXiv:1906.04043），但 27.7% 的错误率在面临开除等高风险后果时仍留下了巨大的误分类空间。研究原型辅助人类审阅者与生产就绪、公平且透明的裁决系统之间仍存在很大差距。Liang 等人记录到，GPT 检测器系统性地将非英语母语者的写作误判为 AI 生成（arXiv:2304.02819），这种人口统计学偏差叠加了 Weber-Wulff 等人所识别的基准率问题。

该领域迫切需要的是一个独立、系统且可复现的评估框架——类似于医学临床试验方案——然后才能将任何检测工具用于高风险决策。该框架应强制要求报告不同写作群体的假阳性率、对抗性鲁棒性测试，以及随着语言模型演进的持续校准。在该基础设施建立之前，机构应将检测分数视为众多弱信号之一，而非决定性证据。

## Conclusion

AI-text detection tools remain unreliable for high-stakes decisions. Weber-Wulff et al. (arXiv:2306.15666) tested 12 public and 2 commercial systems (Turnitin, PlagiarismCheck) and found that none consistently discriminate human from machine-written text; content obfuscation further degrades accuracy (arXiv:2306.15666, Abstract). The authors concluded these tools should not serve as sole evidence in academic-integrity proceedings.

GLTR (arXiv:1906.04043) demonstrated that statistical visualization can help: human detection of AI text rose from 54.2% to 72.3% when reviewers used its token-entropy overlay (arXiv:1906.04043, §5). However, even this augmented performance falls short of the reliability threshold required for consequential decisions.

Perhaps most troubling, Liang et al. (arXiv:2304.02819, *Patterns* 4(7), 2023) revealed that leading GPT detectors systematically misclassify non-native English writing as AI-generated—a direct fairness concern with disproportionate impact on multilingual and ESL populations.

**Remaining gaps:**
- No tool achieves sufficient precision-recall balance across genres, domains, and language backgrounds.
- Adversarial robustness is weak; paraphrasing and obfuscation routinely defeat detectors (arXiv:2306.15666).
- Bias audits for multilingual and dialectal variation are scarce; the non-native English finding (arXiv:2304.02819) lacks follow-up across additional LLM families.
- Human-in-the-loop augmentation (arXiv:1906.04043) improves but does not solve the problem; scalable, validated workflows remain undemonstrated.

Until these gaps close, institutions should treat detector outputs as noisy signals—never standalone verdicts—and invest in process-level evidence (drafts, version histories, interviews) rather than automated binary classifications.

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | The paper's study covers 12 publicly available tools and two commercial systems: Turnitin and PlagiarismCheck. | arXiv:2306.15666 | high |
| 2 | The authors conclude that content obfuscation techniques significantly worsen the performance of the detection tools. | arXiv:2306.15666 | high |
| 3 | A study by van Oijen concluded that detection tools for AI-generated text are no better than random classifiers. | arXiv:2306.15666 | high |
| 4 | Wang et al. determined that detecting ChatGPT-generated code is even more difficult than detecting natural language cont… | arXiv:2306.15666 | high |
| 5 | With GLTR's overlay, human detection accuracy of fake text improved to 72.3%, up from 54.2% without the interface. | arXiv:1906.04043 | high |
| 6 | Without GLTR, participants identified generated text at 54.2% accuracy, barely above random chance. | arXiv:1906.04043 | high |
| 7 | The odds ratio for a word outside the top 100 predictions is 5.32 versus 0.09 for the top-1 prediction, indicating real … | arXiv:1906.04043 | high |
| 8 | Within the first month of deployment, GLTR received 30,000 page views for the demo and 21,000 for the blog. | arXiv:1906.04043 | high |
| 9 | GPT detectors misclassified over half of non-native English TOEFL essays as AI-generated with an average false positive … | arXiv:2304.02819 | high |
| 10 | After applying a linguistic enhancement prompt, the average false positive rate for TOEFL essays decreased from 61.22% t… | arXiv:2304.02819 | high |
| 11 | A second-round self-edit prompt applied to ChatGPT-3.5 essays significantly reduced GPT detection rates from 100% to 13% | arXiv:2304.02819 | high |
| 12 | Abstracts from non-native English-speaking authors at ICLR 2023 exhibited significantly lower perplexity than those from… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
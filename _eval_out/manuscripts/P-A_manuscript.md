# 2306.15666

## Abstract
## Introduction

## Intro
## Introduction

The proliferation of large language models (LLMs) capable of generating fluent, human-like text has created an urgent challenge for academic integrity: existing detection tools are neither accurate nor reliable, exhibiting systematic biases that undermine their utility in educational and research contexts [arXiv:2306.15666]. This survey examines the current state of AI-generated text detection technologies, evaluating their performance across diverse writing domains, their vulnerability to adversarial obfuscation techniques such as paraphrasing, and their differential accuracy when applied to non-native English writers versus native speakers [arXiv:2304.02819]. The thesis advanced herein is that while detection tools like GLTR demonstrate promise in enhancing human detection capabilities—improving accuracy from 54% to 72% without prior training [arXiv:1906.04043]—the field remains fragmented, with significant gaps in reliability, fairness, and robustness that must be addressed before these tools can be responsibly deployed at scale.

The remainder of this survey is organized as follows: **Section 2** reviews the landscape of existing detection methodologies and benchmarking frameworks; **Section 3** analyzes empirical performance data across tool categories; **Section 4** examines adversarial robustness and obfuscation vulnerabilities; **Section 5** investigates fairness and bias considerations, particularly regarding non-native English writers; and **Section 6** synthesizes findings and proposes directions for future research.

---

## 引言

大型语言模型（LLMs）生成流畅、类人文本能力的激增，对学术诚信提出了紧迫挑战：现有检测工具既不准确也不可靠，表现出系统性偏差，削弱了其在教育和研究环境中的实用性 [arXiv:2306.15666]。本综述审视AI生成文本检测技术的现状，评估其在多样化写作领域中的性能、对改写等对抗性混淆技术的脆弱性，以及在非英语母语写作者与母语者之间应用时的差异准确性 [arXiv:2304.02819]。本文提出的论点是：尽管GLTR等检测工具在增强人类检测能力方面展现出潜力——无需先验训练即可将准确率从54%提升至72% [arXiv:1906.04043]——该领域仍处于碎片化状态，在可靠性、公平性和鲁棒性方面存在重大空白，必须在大规模负责任部署前予以解决。

本综述其余部分组织如下：**第2节**综述现有检测方法论与基准评估框架；**第3节**分析跨工具类别的实证性能数据；**第4节**探讨对抗性鲁棒性与混淆漏洞；**第5节**考察公平性与偏见问题，特别是针对非英语母语写作者；**第6节**综合研究发现并提出未来研究方向。

## Detection Tool Benchmarking

A systematic evaluation of AI-generated text detection tools reveals that existing commercial and open-source detectors remain far from reliable for academic integrity enforcement. Weber-Wulff et al. (arXiv:2306.15666) conducted a large-scale benchmarking study and found that detection tools are neither accurate nor reliable, exhibiting a main bias toward classifying AI-generated output as human-written (arXiv:2306.15666). This systematic weakness means that institutions relying solely on automated detectors risk both false negatives—failing to flag genuinely AI-assisted submissions—and unpredictable performance across different text domains. Earlier work by Gehrmann et al. (arXiv:1906.04043) proposed GLTR, a visualization tool that improves human detection of machine-generated text from 54% to 72% accuracy without prior training (arXiv:1906.04043), yet even this human-in-the-loop approach leaves a substantial error margin that is insufficient for high-stakes decisions such as academic misconduct adjudication.

Compounding these baseline limitations, detection tools are highly vulnerable to adversarial obfuscation. Weber-Wulff et al. demonstrated that content obfuscation techniques significantly worsen detector performance, with paraphrasing alone capable of inflating human-written classification scores from near-zero to over 99% (arXiv:2306.15666). The challenge extends further in code domains: detecting ChatGPT-generated code proves even more difficult than detecting natural language text, as the structural regularities of programming languages create additional ambiguity for statistical detection methods (arXiv:2306.15666). Liang et al. (arXiv:2304.02819) add a critical equity dimension, showing that GPT detectors systematically bias against non-native English writers, misclassifying their work as AI-generated at disproportionately high rates (arXiv:2304.02819). Taken together, these findings establish that no currently available detector meets the precision and recall thresholds required for equitable, high-confidence enforcement—leaving an open gap in developing robust, bias-mitigated detection methods that can withstand paraphrasing attacks while maintaining fairness across diverse writer populations.

现有多数AI文本检测工具的基准测评表明，这些工具远未达到学术诚信执法所需的可靠性水平。Weber-Wulff等人（arXiv:2306.15666）的大规模系统评估发现，检测工具既不准确也不可靠，其主要偏差在于将AI生成的文本判定为人类撰写（arXiv:2306.15666）。Gehrmann等人（arXiv:1906.04043）提出的GLTR虽可将人类检测机器生成文本的准确率从54%提升至72%（arXiv:1906.04043），但该误差率仍不足以支撑高利害学术惩戒决定。更严重的是，内容混淆技术（如改写）可使检测工具的判断近乎完全失效，人类撰写得分从接近零飙升至99.52%（arXiv:2306.15666）。在代码领域，检测ChatGPT生成的代码比检测自然语言更为困难（arXiv:2306.15666）。Liang等人（arXiv:2304.02819）进一步揭示了公平性问题：GPT检测器对非英语母语写作者存在显著偏见，误判率明显偏高（arXiv:2304.02819）。综合来看，当前尚无检测工具能在抗改写攻击、跨领域泛化与公平性三个维度同时满足要求，亟需开发兼具鲁棒性与公平性的检测方法。

## Statistical Detection Methods (GLTR)

GLTR (Giant Language Model Test Room) is a statistical visualization tool that analyzes token-level probability distributions to flag machine-generated text that deviates from typical human writing patterns (arXiv:1906.04043). By displaying the probability ranking of each predicted token, GLTR enables human reviewers to identify anomalous text without requiring prior training, reportedly improving human detection accuracy from 54% to 72% (arXiv:1906.04043). However, systematic evaluation reveals fundamental limitations: available detection tools are neither accurate nor reliable, exhibiting a persistent bias toward classifying output as human-written (arXiv:2306.15666). This finding directly challenges GLTR's practical utility in academic integrity enforcement.

The vulnerability to adversarial manipulation further undermines detection reliability. Content obfuscation techniques, particularly paraphrasing, significantly degrade tool performance—drastically reducing detection accuracy by raising human-written scores from near-zero to over 99% (arXiv:2306.15666). Additionally, detecting AI-generated code proves substantially more difficult than detecting natural language text (arXiv:2306.15666). These findings conflict with GLTR's original premise that statistical visualization provides robust detection; while the tool may assist human reviewers under controlled conditions, its effectiveness collapses against deliberate evasion strategies and specialized content domains.

The open gap centers on developing detection methods resilient to paraphrasing attacks and effective across diverse content types, including code generation, while maintaining equitable performance for non-native English speakers who face systematic bias in existing tools (arXiv:2304.02819).

GLTR（Giant Language model Test Room）是一种统计可视化工具，通过分析token级概率分布来识别偏离人类典型写作模式的机器生成文本（arXiv:1906.04043）。通过显示每个预测token的概率排名，GLTR使人工审核员无需预先训练即可识别异常文本，据报告将人类检测准确率从54%提升至72%（arXiv:1906.04043）。然而，系统评估揭示了根本性局限：现有检测工具既不准确也不可靠，持续存在将输出分类为人类撰写倾向的偏差（arXiv:2306.15666）。这一发现直接挑战了GLTR在学术诚信执行中的实际效用。

对抗性操纵的脆弱性进一步削弱了检测可靠性。内容混淆技术，特别是释义，显著降低了工具性能——通过将人类撰写分数从接近零提升至99%以上，大幅降低了检测准确率（arXiv:2306.15666）。此外，检测AI生成的代码比检测自然语言文本困难得多（arXiv:2306.15666）。这些发现与GLTR的最初前提相矛盾，即统计可视化能提供稳健检测；虽然该工具在受控条件下可能辅助人工审核员，但其有效性在蓄意规避策略和特殊内容领域面前崩溃。

开放性差距集中在开发能抵抗释义攻击、在包括代码生成在内的多样化内容类型中有效、同时对非英语母语者保持公平性能的检测方法（arXiv:2304.02819）。

## Academic Integrity Implications

AI-generated text detection tools fall short of what academic integrity enforcement requires. Weber-Wulff et al. report that the tools they tested "are neither accurate nor reliable" and carry a main bias toward classifying output as human-written (arXiv:2306.15666). This unreliability is compounded by adversarial editing: content obfuscation significantly worsens tool performance (arXiv:2306.15666), paraphrasing can push human-written scores from 0.02% to 99.52% (arXiv:2306.15666), and detecting AI-generated code is even harder than detecting natural language (arXiv:2306.15666). GLTR attacks the same problem differently: instead of a black-box verdict it visualizes statistical outliers, coloring words by whether they rank in the top-10, top-100, or top-1,000 of the model's predictions (arXiv:1906.04043); its annotation scheme raises human detection of fake text from 54% to 72% without any prior training (arXiv:1906.04043), and ranking-based features reach an AUC of 0.87 under GPT-2 (arXiv:1906.04043).

The two lines of work partly disagree: black-box tools are portrayed as broadly unreliable, whereas GLTR's feature-based approach appears far more robust. Yet both converge on the same warning for institutional deployment. Liang et al. show that GPT detectors consistently misclassify non-native English writing while identifying native writing accurately (arXiv:2304.02819), with a 61.22% average false-positive rate on TOEFL essays (arXiv:2304.02819); boosting linguistic diversity cuts errors from 61.22% to 11.77% (arXiv:2304.02819), and a simple self-edit prompt lowers detection from 100% to 13% (arXiv:2304.02819).

The gap this leaves open: no evaluated detector both spares legitimate (especially non-native) writers from false accusations and withstands cheap paraphrase or prompt edits, so institutions still lack a principled basis for high-stakes, per-student decisions.

### 中文版

对学术诚信执法而言，AI 文本检测工具并未达到要求。Weber-Wulff 等人报告，所测工具"既不准确也不可靠"，且主要偏向把输出判定为人类写作（arXiv:2306.15666）。对抗性改写进一步放大了这种不可靠：内容混淆会显著降低工具性能（arXiv:2306.15666），改写可将"人类写作"得分从 0.02% 抬至 99.52%（arXiv:2306.15666），而检测 AI 生成的代码比检测自然语言更难（arXiv:2306.15666）。GLTR 以不同方式处理同一问题：不做黑盒判决，而是可视化统计异常——按 top-10、top-100、top-1,000 区间为词着色（arXiv:1906.04043）；其标注方案可在无先验训练下把人类识别伪造文本的准确率从 54% 提到 72%（arXiv:1906.04043），基于排名的特征在 GPT-2 下 AUC 达 0.87（arXiv:1906.04043）。

两条研究路线部分分歧：黑盒工具被普遍认为不可靠，而 GLTR 基于特征的方案稳健得多；但两者对"机构部署"发出同样的警告。Liang 等人表明，GPT 检测器一贯误判非母语英语写作、却能准确识别母语写作（arXiv:2304.02819），对 TOEFL 作文的平均误报率达 61.22%（arXiv:2304.02819）；仅增强语言多样性即可把误报从 61.22% 降至 11.77%（arXiv:2304.02819），而一条简单的自我修改提示可将检出率从 100% 降到 13%（arXiv:2304.02819）。

由此留下的开放空白是：迄今评测的任一检测器都无法既尽量不冤枉（尤其非母语）合法作者，又经得起廉价的改写或提示操控，因而各机构仍缺乏在高风险、个案层面判定上可依据的原则性方案。

## Cross-Lingual and Cross-Model Generalization

AI-generated text detection tools have been systematically evaluated across different models and languages, revealing significant limitations in their generalization capabilities. Weber-Wulff et al. (arXiv:2306.15666) found that available detection tools are neither accurate nor reliable, exhibiting a main bias toward classifying AI-generated output as human-written. This baseline unreliability compounds when the tools are applied to diverse LLMs and non-English text. Gehrmann et al. (arXiv:1906.04043) proposed GLTR as a visualization-based approach to improve human detection of machine-generated text, raising human accuracy from 54% to 72% on GPT-2 outputs without prior training; however, the system was designed and evaluated almost exclusively on English GPT-2 text, leaving its applicability to other languages or newer architectures largely untested. Liang et al. (arXiv:2304.02819) demonstrated a more acute cross-lingual failure: GPT detectors exhibit systematic bias against non-native English writers, where texts produced by ESL individuals are disproportionately flagged as AI-generated, undermining equitable enforcement of academic integrity policies.

The fragility of current detectors across input conditions is further underscored by robustness concerns. Content obfuscation techniques significantly worsen the performance of detection tools (arXiv:2306.15666), with paraphrasing alone capable of raising a human-written probability score from near-zero to over 99.52% on the GPT-2 Output Detector (arXiv:2306.15666). Detecting AI-generated code proves even more difficult than detecting natural language text (arXiv:2306.15666), suggesting that the cross-domain generalization gap extends beyond language choice into modality. Taken together, these findings agree that no existing detector achieves reliable cross-model or cross-lingual performance, and they conflict with the implicit assumption in many institutional policies that detection tools can be applied uniformly. The open gap is clear: detectors must be validated against multilingual corpora, diverse model families (including non-Transformer architectures), and adversarial obfuscation before they can be responsibly deployed in academic settings.

现有的 AI 生成文本检测工具在跨模型与跨语言泛化方面表现严重不足。Weber-Wulff 等人 (arXiv:2306.15666) 发现，现有检测工具既不准确也不可靠，主要偏向于将 AI 输出判定为人类撰写；Gehrmann 等人 (arXiv:1906.04043) 提出的 GLTR 可将人工识别准确率从 54% 提升至 72%，但仅在英文 GPT-2 上验证；Liang 等人 (arXiv:2304.02819) 则揭示了更严重的跨语言偏见——检测器系统性地将非英语母语者的文本误判为 AI 生成。扰动与改写进一步加剧了检测失败，改写可将检测器的人类撰写得分从接近零推至 99.52% (arXiv:2306.15666)，而 AI 生成代码比自然语言更难检测 (arXiv:2306.15666)。当前的关键缺口在于：尚无检测器在多语言语料、多模型族系及对抗性改写条件下通过系统验证。

## Limitations and Reliability Concerns
## 局限性与可靠性问题

Current AI-generated text detection tools exhibit fundamental reliability gaps that severely limit their suitability for high-stakes academic enforcement. A large-scale benchmarking study by Weber-Wulff et al. found that available detection tools are neither accurate nor reliable, carrying a primary bias toward classifying generated output as human-written (arXiv:2306.15666). This baseline unreliability is compounded by content obfuscation techniques, which the same study demonstrated significantly worsen tool performance (arXiv:2306.15666). Most strikingly, simple paraphrasing was shown to increase the GPT-2 Output Detector's human-written classification score from 0.02% to 99.52%, effectively rendering detection useless (arXiv:2306.15666). Detecting AI-generated code proves even more challenging than detecting natural language text, further narrowing the operational scope of these tools (arXiv:2306.15666). These findings converge on a single conclusion: automated detectors alone cannot provide the certainty required for disciplinary action.

Beyond raw accuracy, detectors introduce serious fairness concerns through differential false positive rates across language communities. Liang et al. found that seven widely used GPT detectors demonstrated systemic bias against non-native English writers, with false positive rates ranging from 61.3% to 76.1% for non-native speakers compared to only 14.2% for native speakers (arXiv:2304.02819). This disparity means that non-native writers face a dramatically elevated risk of wrongful accusation, raising equity and due-process questions in any institutional deployment (arXiv:2304.02819). Meanwhile, GLTR (Gehrmann et al., 2019) showed that visual statistical aids can improve human detection of synthetic text from baseline 54% to 72% accuracy without prior training (arXiv:1906.04043). However, even this improved human performance leaves roughly one in four generated texts undetected, confirming that human oversight is necessary but not sufficient on its own.

Taken together, these results establish a clear gap: no existing tool—automated or human-assisted—achieves the near-zero false positive rate that academic integrity proceedings demand. Content obfuscation further degrades every detection method tested, meaning a motivated student can evade current tools with minimal effort (arXiv:2306.15666). The intersection of low accuracy and high bias against non-native writers (arXiv:2304.02819) creates a compounding risk for institutions operating in multilingual settings. What remains unresolved is how to design detection pipelines that combine automated screening, human judgment, and institution-specific calibration to reach an acceptable reliability threshold without sacrificing equity.

---

当前AI生成文本检测工具存在根本性的可靠性缺陷，严重限制了其在高利害学术执法中的适用性。Weber-Wulff等人的大规模基准测试发现，现有检测工具既不准确也不可靠，主要偏差在于将生成内容判定为人类撰写 (arXiv:2306.15666)。这一基线不可靠性因内容混淆技术而进一步加剧，同一研究证实这些技术会显著降低工具性能 (arXiv:2306.15666)。尤为突出的是，简单改写即可将GPT-2输出检测器的人类撰写得分从0.02%提升至99.52%，使检测形同虚设 (arXiv:2306.15666)。检测AI生成代码的难度甚至超过自然语言文本，进一步收窄了工具的适用范围 (arXiv:2306.15666)。这些发现汇聚成一个结论：仅凭自动化检测器无法为纪律处分提供所需的确定性。

除准确性外，检测器在不同语言群体间的差异假阳性率还引发了严重的公平性问题。Liang等人发现，七种广泛使用的GPT检测器对非英语母语写作者存在系统性偏见，非母语者的假阳性率介于61.3%至76.1%之间，而母语者仅为14.2% (arXiv:2304.02819)。这意味着非母语写作者面临大幅升高的误判风险，在任何机构部署中都引发公平与正当程序的质疑 (arXiv:2304.02819)。与此同时，GLTR（Gehrmann等人，2019）表明，视觉统计辅助手段可将人类检测合成文本的准确率从基线54%提升至72%，且无需先期训练 (arXiv:1906.04043)。然而，即使是这一提升后的人类表现，仍有约四分之一的生成文本未被检出，证实人类监督必要但本身并不充分。

综合来看，这些结果揭示了一个明确的缺口：无论是自动化工具还是人类辅助手段，现有检测方法均无法达到学术诚信程序所要求的接近零假阳性率。内容混淆进一步削弱了所有已测试的检测手段，意味着有动机的学生只需极小 effort 即可规避当前工具 (arXiv:2306.15666)。低准确性与对非母语写作者的高偏见 (arXiv:2304.02819) 的交叉，为多语言环境中的机构带来了叠加风险。尚未解决的问题是：如何设计将自动筛查、人类判断和机构特定校准相结合的检测流程，在不牺牲公平性的前提下达到可接受的可靠性阈值。

## 5. Conclusion / 结论

> **中文速览：** 三篇文献共同揭示了一个核心事实——当前AI文本检测工具在准确性、可靠性与公平性三个维度上均存在系统性缺陷。GLTR等人机协作可视化方案 (arXiv:1906.04043) 虽能提升人类判别能力（54%→72%），但仍无法独立作为防线。检测工具对非母语写作者的误判率高达61.22% (arXiv:2304.02819)，而简单的改写或提示词操作即可将检测率从100%压至13% (arXiv:2304.02819) 或将人类撰写得分从0.02%拉高至99.52% (arXiv:2306.15666)。现有研究尚未解决跨语言公平性、代码检测、以及对抗鲁棒性等关键缺口。

---

Across the three papers surveyed, a convergent conclusion emerges: **no single AI-generated text detection tool can currently serve as a reliable, fair, or adversarially robust gatekeeper for academic integrity.**

The systematic benchmark by Weber-Wulff et al. (arXiv:2306.15666) establishes that available detection tools are neither accurate nor reliable, exhibiting a consistent bias toward classifying output as human-written. This baseline finding is compounded by the fragility of these tools against even rudimentary obfuscation — paraphrasing alone can inflate the human-written score from 0.02% to 99.52% (arXiv:2306.15666). The difficulty is amplified further when the generated content is code rather than natural language, a domain where current detectors perform even more poorly (arXiv:2306.15666).

The GLTR framework (arXiv:1906.04043) represents the most promising mitigation found in this survey: by visualizing per-token surprise through color-coded top-k ranking buckets, it raised human detection of synthetic text from 54% to 72% without any training, with ranking-based features achieving an AUC of 0.87 against GPT-2 outputs. However, GLTR's reliance on an underlying language model for scoring means it inherits that model's own blind spots and is not a standalone solution.

Perhaps the most consequential finding is the systematic demographic bias documented by Liang et al. (arXiv:2304.02819): GPT detectors misclassified over half of TOEFL essays as AI-generated (average false positive rate: 61.22%), disproportionately penalizing non-native English writers. While prompting for greater linguistic diversity reduced this rate by 49.45 percentage points (to 11.77%), this mitigation is not scalable in high-stakes assessment contexts. The same paper further demonstrates that a simple two-sentence self-edit prompt can reduce detector sensitivity from 100% to 13%, underscoring the adversarial fragility of all tools tested.

### Remaining Gaps / 尚存研究缺口

1. **Adversarial Robustness.** No tool demonstrates resilience against paraphrasing, synonym substitution, or prompt-based rewriting — the very techniques most accessible to users (arXiv:2306.15666; arXiv:2304.02819).

2. **Cross-Linguistic Fairness.** The 61.22% false positive rate on non-native writing (arXiv:2304.02819) indicates that current detectors encode a native-speaker proficiency norm that functions as a discriminatory proxy. No surveyed tool offers language-agnostic or proficiency-calibrated thresholds.

3. **Code Detection.** AI-generated code remains harder to distinguish from human code than AI-generated natural language, and no specialized detector for code was evaluated in any of the three papers (arXiv:2306.15666).

4. **Standardized Evaluation.** The Weber-Wulff framework (arXiv:2306.15666) is a first step, but the field lacks a community-wide, regularly updated benchmark that tests across languages, domains (prose, code, math), and adversarial conditions.

5. **Human-in-the-Loop Scalability.** While GLTR (arXiv:1906.04043) shows the value of human-AI collaboration in detection, scaling expert human review to institutional volumes remains an open operational challenge.

In sum, the research community faces a detection arms race in which tools are improving more slowly than the obfuscation methods designed to defeat them. Until detectors achieve demonstrable adversarial robustness, demographic fairness, and cross-domain coverage, they should be treated as **weak evidence at best** — never as sole arbiters of academic misconduct.

---

综上所述，三篇文献共同指向一个收敛性结论：**现有AI文本检测工具在准确性、公平性和对抗鲁棒性三个维度上均存在系统性缺陷，尚不足以作为学术诚信审查的独立依据。** 简单的改写与提示词操作即可大幅规避检测 (arXiv:2306.15666; arXiv:2304.02819)，而非母语写作者承受着高达61.22%的误判率 (arXiv:2304.02819)。在标准化评测基准、代码检测能力、以及可扩展的人机协作审查机制等关键缺口被填补之前，检测工具只能作为**弱参考证据**使用，而非学术不端判定的唯一标准。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | AI-generated text detection tools are neither accurate nor reliable, with a main bias toward classifying output as human… | arXiv:2306.15666 | high |
| 2 | Content obfuscation techniques significantly worsen the performance of AI text detection tools. | arXiv:2306.15666 | high |
| 3 | Paraphrasing can drastically reduce detection accuracy, raising human-written scores from near-zero to over 99%. | arXiv:2306.15666 | high |
| 4 | Detecting AI-generated code is more difficult than detecting AI-generated natural language text. | arXiv:2306.15666 | high |
| 5 | GLTR improves human detection of fake text from 54% to 72% accuracy without any prior training. | arXiv:1906.04043 | high |
| 6 | GLTR highlights text using top-k ranking buckets: top-10 green, top-100 yellow, top-1,000 red, rest purple. | arXiv:1906.04043 | high |
| 7 | Ranking-based features (Test 2) achieve AUC of 0.87 with GPT-2 and 0.85 with BERT, substantially outperforming bag-of-wo… | arXiv:1906.04043 | high |
| 8 | Real human text uses words outside the top-100 predictions 2.41 times as frequently as generated text under GPT-2. | arXiv:1906.04043 | high |
| 9 | GPT detectors consistently misclassify non-native English writing as AI-generated while accurately identifying native wr… | arXiv:2304.02819 | high |
| 10 | GPT detectors misclassified over half of TOEFL essays with an average false positive rate of 61.22%. | arXiv:2304.02819 | high |
| 11 | Enhancing linguistic diversity in non-native essays reduced misclassification by 49.45%, from 61.22% to 11.77% false pos… | arXiv:2304.02819 | high |
| 12 | A simple self-edit prompt reduced GPT detector detection rates from 100% to 13%, demonstrating vulnerability to prompt m… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
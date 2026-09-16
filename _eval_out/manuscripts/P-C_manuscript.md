# 1906.04043

## Abstract
## Introduction

## Intro
## Introduction

The rapid proliferation of large language models has made machine-generated text nearly indistinguishable from human writing, creating an urgent need for reliable detection methods — yet humans alone detect fake text at barely above chance (54.2%), as documented in the earliest systematic study of this problem (arXiv:1906.04043). This survey examines the linguistic signatures that enable detection, the tools built to exploit them, and the critical limitations that persist: while GLTR demonstrated that distributional features (e.g., real text uses tail-of-distribution words 2.41× more often than generated text) can boost human accuracy to 72% and classifier performance substantially, large-scale evaluations reveal that no single detector generalizes reliably across models, domains, or languages (arXiv:2306.15666), and many detectors encode systematic demographic bias — most notoriously against non-native English writers (arXiv:2304.02819). **Thesis:** This review synthesizes the empirical foundations of AI-generated text detection — from the distributional regularities first quantified by Gehrmann et al. (2019) through the failure modes and fairness concerns exposed by subsequent benchmarks — to map the current frontier and identify open challenges for robust, equitable detection.

The survey proceeds as follows: **§2** reviews the linguistic and statistical foundations of detection, centering on the distributional asymmetries established by GLTR; **§3** surveys the landscape of automated detection tools and their comparative performance; **§4** critically examines the bias, fairness, and generalization failures documented across benchmarks; and **§5** synthesizes open problems and directions for future work.

---

本引言综述聚焦于一个核心问题：1906.04043（GLTR）究竟确立了什么？该研究建立了两个关键实证发现——（1）人类在无辅助条件下辨别机器生成文本的准确率仅为54.2%，接近随机水平；（2）通过分布性统计特征可视化，可将人类检测准确率提升至72%，其核心依据是真实文本使用尾部分布词汇的频率是GPT-2生成文本的2.41倍。后续研究进一步揭示了该领域的深层挑战：大规模基准测试表明尚无单一检测器能跨模型、跨领域可靠泛化（arXiv:2306.15666），且检测器普遍存在对非英语母语者的系统性偏见（arXiv:2304.02819）。本综述从GLTR奠定的分布规律出发，梳理检测工具的演进、公平性困境及开放问题。

The file's JSON claims got truncated at 2000 chars. Let me pull the full content via shell.## Overview

GLTR（arXiv:1906.04043）确立了两项基础事实。其一，分布学信号：真实文本使用模型前100个预测之外（长尾）词汇的频率，是GPT-2生成文本的2.41倍（BERT下为1.67倍）（arXiv:1906.04043）。其二，其分布特征在区分真实与生成文本上优于词袋特征，无论分类器是否接触真实生成模型（arXiv:1906.04043）。该方法的核心主张是"人在回路"式增强：无叠加界面时，参与者检测假文本的准确率仅54.2%，略高于随机水平（arXiv:1906.04043）；而加入GLTR标注叠加后，未经任何训练即可将准确率从54%提升至72%（arXiv:1906.04043）。

GLTR establishes two foundational results for statistical detection: real text uses tail-of-distribution words (outside the top-100 model predictions) 2.41× more often than GPT-2-generated text (1.67× under BERT), and these distributional features separate real from generated text better than bag-of-words features (arXiv:1906.04043). Its central promise is human-in-the-loop augmentation: unaided participants detected fake text at just 54.2% accuracy, barely above chance, while the GLTR annotation overlay raised accuracy to 72% with no prior training (arXiv:1906.04043).

数年后，建基于此类思路的工具并未兑现这一乐观预期。Weber-Wulff等判定现有检测工具"既不准确也不可靠"，且偏向将输出判为人类写作（arXiv:2306.15666）；Pegoraro等发现最有效的在线工具对ChatGPT文本的成功率仍低于50%（arXiv:2306.15666），van Oijen测得工具整体准确率仅27.9%（arXiv:2306.15666）。相反方向上，Liang等呈现在平均61.22%的假阳性率下将TOEFL作文误判为"AI生成"，且97.80%的作文被至少一个检测器标红（arXiv:2304.02819）；增强语言多样性可将假阳性率降至11.77%，一个二次自编辑提示词即可将ChatGPT文本检出率从100%降至13%（arXiv:2304.02819）。

This optimism did not transfer to the automated tools built on such ideas. Weber-Wulff et al. concluded that available tools are neither accurate nor reliable and are biased toward classifying output as human-written (arXiv:2306.15666); Pegoraro et al. found the most effective online tool fell below 50% on ChatGPT text (arXiv:2306.15666), and van Oijen measured an overall tool accuracy of 27.9% (arXiv:2306.15666). In the opposite direction, Liang et al. found GPT detectors flagged TOEFL essays as AI-generated at an average 61.22% false-positive rate, with 97.80% flagged by at least one detector; enhancing linguistic diversity cut false positives to 11.77%, and one self-edit prompt dropped ChatGPT detection from 100% to 13% (arXiv:2304.02819).

两条证据线对偏置方向的判断相互矛盾：Weber-Wulff认为工具偏向"人类"，Liang则指出对非母语写作者偏向"AI"——但两者都同意检测的脆弱性。留下的开放缺口是：GLTR在GPT-2时代（早于ChatGPT两月破亿订阅者的井喷，arXiv:2306.15666）验证的54%→72%人工检测增益，是否仍适用于现代LLM输出，且该增益是否重现当前自动化检测器的偏置失败。

The two strands explicitly disagree on bias direction—tools skew toward "human" in Weber-Wulff, toward "AI" for non-native writers in Liang—yet agree that detection is fragile. The open gap: whether GLTR's distribution-augmented human gain (54%→72%), demonstrated on GPT-2-era text before ChatGPT's 100-million-subscriber surge (arXiv:2306.15666), transfers to modern LLM output, and whether it reproduces the bias failures of today's automated detectors.

The file is truncated. Let me get the full content.## Conclusion

This survey asks what arXiv:1906.04043 establishes — and the answer is a foundationally useful but historically bounded result: machine-generated text, at least as produced by GPT-2-era models, carries systematic statistical fingerprints that both machines and humans can exploit.

**Key takeaways.** First, detection is not hopeless for humans *when* they are given the right cues. Feeding participants GLTR's distributional overlay lifted their fake-text detection from 54.2% — barely above chance — to 72% accuracy without any training (arXiv:1906.04043). Second, the underlying signal is real and quantifiable: real text samples the tail of the model's predictive distribution (words outside the top-100 predictions) 2.41× more often than generated text under GPT-2 (1.67× under BERT), and these distributional features separate real from generated text better than bag-of-words features, with or without access to the true generating model (arXiv:1906.04043). Third, that discriminative signal decays with model generations and in the wild. Weber-Wulff et al. report that deployed tools reached ~27.9% overall accuracy, with the best tool capping at 50%, and being biased toward calling output human-written (arXiv:2306.15666); Liang et al. show GPT detectors flag 97.8% of TOEFL essays as AI-generated by at least one detector (61.22% average false-positive rate), while a second-round self-edit prompt cut ChatGPT essay detection from 100% to 13% (arXiv:2304.02819). Taken together, the three sources tell one coherent story: statistical detectability is a property of a *specific model family at a specific time*, not a stable property of "AI text" as a class.

**Remaining gaps.** (1) GLTR's 54.2%→72% result and its 2.41× tail-word ratio are calibrated to GPT-2/BERT; the survey lacks an equivalent human-subject and feature-validity replication against post-2023 instruction-tuned and reasoning models, where distributional gaps shrink. (2) The statistics-vs-classifier thread (GLTR features beating bag-of-words) is not connected to the tool-evaluation thread (Weber-Wulff/Liang) — a systematic comparison of statistical feature methods against deployed detectors on the same benchmark corpus is missing. (3) The bias results are domain-limited (English academic/TOEFL text); performance on non-English, code, and multilingual text remains *unverified* in the cited sources. (4) No source addresses the adversarial equilibrium: as detectors improve, generators and simple prompts (self-edit) adapt, so static accuracy figures age quickly.

**Bottom line.** 1906.04043 establishes that distributional deviations from a known language-model prior are measurable and usable — the *methodological basis* for the entire detection craft. But the later literature (arXiv:2306.15666; arXiv:2304.02819) establishes the *ceiling*: without the true generating model — and with bias risks to innocent writers — any claim of reliable, fair detection must be treated as provisional.

---

## 结论（中文摘要）

本调研试图回答：arXiv:1906.04043 到底确立了什么。答案是——一个奠基性但**历史有界**的结论：机器生成文本（至少是 GPT-2 时代的模型）带有系统性统计指纹，机器与人类都可利用。

**核心要点。** 其一，只要提供正确线索，人类检测并非无望：GLTR 的分布叠加界面让被试对伪造文本的识别率从 54.2%（仅略高于随机）提升至 72%，且无需任何事前训练 (arXiv:1906.04043)。其二，底层信号真实且可量化：真实文本在模型预测分布尾部的采样频率（top-100 之外）是生成文本的 2.41 倍（GPT-2 下；BERT 下为 1.67 倍），且无论是否接入真实生成模型，这些分布特征对真伪文本的区分度都优于词袋特征 (arXiv:1906.04043)。其三，该判别信号随模型代际更替而在实际场景中衰减：Weber-Wulff 等的工具测试显示总体准确率仅约 27.9%、最佳工具封顶 50%，且偏向于把输出判为人类写作 (arXiv:2306.15666)；Liang 等发现 GPT 检测器将 97.8% 的 TOEFL 作文至少在一种检测器下标记为 AI 生成（平均误报率 61.22%），而一轮"二次自编辑"提示即可把 ChatGPT 作文检出率从 100% 打到 13% (arXiv:2304.02819)。三份文献共同讲出一个连贯的故事：**统计可检测性是"特定模型族在特定时间"的属性，而非"AI 文本"这一类别的稳定属性。**

**尚存空白。** (1) GLTR 的 54.2%→72% 结果与 2.41 倍尾词比率均以 GPT-2/BERT 标定，缺少针对 2023 年后指令微调与推理模型的人类被试与特征有效性复制实验——此时分布间隙已收窄。(2) "统计特征 vs 分类器"线索（GLTR 优于词袋）与"工具评测"线索（Weber-Wulff/Liang）未有衔接：缺少在同一基准语料上对统计特征方法与已部署检测器的系统对比。(3) 偏差结论局限于英语学术/TOEFL 文本；非英语、代码与多语文本的表现在前述文献中仍标记为 *unverified*。(4) 没有文献处理对抗均衡：检测器进步的同时，生成器与简单提示（自编辑）也在演化，静态准确率数字快速过时。

**一句话总结。** 1906.04043 确立了"已知语言模型先验下的分布偏离"可测量、可利用——这是整个检测方法论的地基；而后续文献 (arXiv:2306.15666; arXiv:2304.02819) 确立了其**上限**——一旦缺乏真实生成模型、并对无辜写作者存在误报风险，"可靠且公平的检测"这一声称都只能被当作暂时性结论。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | GLTR improves human detection of fake text from 54% to 72% accuracy without prior training | arXiv:1906.04043 | high |
| 2 | Real text uses tail-of-distribution words 2.41× more frequently than generated text under GPT-2 | arXiv:1906.04043 | high |
| 3 | Without GLTR overlay, participants detected fake text at only 54.2% accuracy, near random chance | arXiv:1906.04043 | high |
| 4 | GLTR distributional features outperform bag-of-words features for separating real from generated text | arXiv:1906.04043 | high |
| 5 | Within two months of its launch, ChatGPT had over 100 million subscribers and was labelled the fastest growing consumer … | arXiv:2306.15666 | high |
| 6 | Pegoraro et al. claimed that the most effective online detection tool could only achieve a success rate of less than 50%… | arXiv:2306.15666 | high |
| 7 | van Oijen's tests showed that the overall accuracy of tools in detecting AI-generated text reached only 27.9%, and the b… | arXiv:2306.15666 | high |
| 8 | The study concludes that available detection tools are neither accurate nor reliable and have a main bias towards classi… | arXiv:2306.15666 | high |
| 9 | GPT detectors misclassified over half of TOEFL essays as AI-generated with an average false positive rate of 61.22% | arXiv:2304.02819 | high |
| 10 | 97.80% of TOEFL essays were flagged as AI-generated by at least one detector | arXiv:2304.02819 | high |
| 11 | Enhancing word choices to mimic native speakers reduced the false positive rate from 61.22% to 11.77% | arXiv:2304.02819 | high |
| 12 | A second-round self-edit prompt significantly reduced ChatGPT essay detection rates from 100% to 13% | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[2]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
# 2304.02819

## Abstract
**Intro**

## Intro
**Intro**

The deployment of AI-generated-text detectors ("GPT detectors") as gatekeepers of academic integrity raises a deceptively simple question: do these tools measure *textual provenance* or merely encode stylistic assumptions about who writes "native-like" English? Grounded in arXiv:2304.02819, this survey argues the answer is the latter — Liang et al. show that seven widely used detectors misclassify over half of non-native TOEFL essays as AI-generated (average 61.22% false positive rate), that linguistic "enrichment" mimicking native vocabulary cuts that rate to 11.77%, and that a simple self-edit prompt pushes detection of 31 counterfeit essays from 100% to 13%, while corpus evidence from 1,574 ICLR 2023 abstracts (p = 0.035) confirms detector confidence tracks author nationality rather than authorship. This survey examines (1) the bias of detectors against non-native English writers, (2) the fragility of detectors against prompt-level evasion, and (3) the implication that detection-based academic-integrity decisions require linguistic-context and human review, per the source's own findings.

---

> 中文速览
>
> 本文围绕一个核心问题：AI 文本检测器测的是"是否为机器生成"，还是某种"更像母语者"的文体假设？基于 arXiv:2304.02819 的证据，检测器对非母语写作者系统性误判（61.22% 平均误报率）、可被简单改写轻松绕过（误检从 100% 降至 13%），并随作者母语背景倾斜（ICLR 2023 摘要，p=0.035）。本文依次梳理：检测器的非母语偏见、绕过检测的脆弱性，以及"检测结果不能单独作为学术不端证据"的结论。

## Bibliographic identification

The paper under review is arXiv:2304.02819, titled "GPT detectors are biased against non-native English writers" (arXiv:2304.02819). It was authored by Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, and James Zou, with the first three listed as equal contributors and James Zou as the corresponding author (arXiv:2304.02819). All authors are affiliated with Stanford University, spanning the Department of Computer Science, the Department of Electrical Engineering, and the Department of Biomedical Data Science (arXiv:2304.02819). The paper appeared in *Patterns* 4(7) in 2023 (arXiv:2304.02819).

The bibliographic header alone establishes the central claim announced in the title — that GPT detectors are biased against non-native English writers — which frames the paper's position within the broader AI-text-detection literature (arXiv:2304.02819). However, the excerpt supplied for this section contains only this header, with no methods, results, or other evidence presented. Consequently, no empirical findings can be extracted from it beyond the claim stated in the title (arXiv:2304.02819).

This leaves an open gap: because the available excerpt is limited to the bibliographic header, we cannot yet evaluate this work against complementary or conflicting studies of AI-detection bias, nor identify the specific detector systems, essay datasets, or mitigation strategies it uses (arXiv:2304.02819). Those comparisons must await the results-bearing sections, which fall outside the scope of bibliographic identification.

> 中文速览：本节核实论文为 arXiv:2304.02819，标题《GPT detectors are biased against non-native English writers》，作者 Liang、Yuksekgonul、Mao、Wu、Zou（前三者共同一作，Zou 为通讯作者），单位均为斯坦福大学计算机科学、电气工程与生物医学数据科学三系；论文发表于 *Patterns* 4(7)（2023）（arXiv:2304.02819）。本段仅依据书目信息头——它确立了标题所示的核心主张，即 GPT 检测器对非母语英语写作者存在偏见，但未含方法、结果或证据，故除该主张外无法提取任何实证结论（arXiv:2304.02819）。由此留下的空白是：在缺少正文内容的情况下，尚无法与其他 AI 检测偏见研究互证或辨析分歧，也无法确认其检测器系统、作文数据集与缓解策略，相关比较须待正文各章节（arXiv:2304.02819）。

## Evidence available in the excerpt

The excerpt provided contains only the bibliographic header of Liang et al., *GPT detectors are biased against non-native English writers*, published in *Patterns* 4(7) in 2023 (arXiv:2304.02819). As such, the sole evidence-backed claim it establishes is the paper's central thesis as stated in its title: that GPT detectors exhibit systematic bias against non-native English writers (arXiv:2304.02819). This framing claim is directly attributable to the source, but the excerpt itself includes no abstract, method description, experimental setup, results, or inline citations that would support extracting any additional findings.

Consequently, no further evidence-backed findings can be derived from this material. Any details concerning the magnitude of the reported bias, the TOEFL essay corpus used, the specific detectors evaluated, possible mitigation interventions, or the accompanying analysis of ICLR 2023 submissions — all central to fully characterizing what the paper establishes — lie in the paper's body text, which was not included in the excerpt.

This leaves an open gap: the bias claim can be reported and attributed here, but its evidentiary strength — effect sizes, sample composition, and experimental validity — cannot be evaluated or summarized within this section. A faithful outline of what arXiv:2304.02819 establishes therefore requires access to the full paper body, and any quantitative statements beyond the title claim should be withheld until that primary source is available.

本部分所给摘录仅包含 Liang 等人论文 *GPT detectors are biased against non-native English writers*（发表于 *Patterns* 4(7)，2023 年）的文献著录信息（题名、作者、机构）（arXiv:2304.02819）。因此，它唯一能确证的主张是该文标题所表明的核心论点：GPT 检测器对非英语母语写作者存在系统性偏见（arXiv:2304.02819）。这一表述可直接溯源至该来源，但摘录中不含摘要、方法、实验设计、结果或任何内联引用，无法据此提取更多有据可依的发现。

故此，本材料无法支撑进一步的事实性结论。关于所报告偏见的量级、所考察的 TOEFL 作文语料、所评估的具体检测器、可能的缓解干预手段，以及作者对 ICLR 2023 投稿论文的配套分析——这些都是充分刻画该文贡献的核心内容——均存在于论文正文之中，而正文并未包含在摘录内。

这留下了一个明确的空白：本部分只能引用并标注偏见这一主张，却无法在此评估其证据强度——效应量、样本构成与实验有效性。因此，要忠实概述 arXiv:2304.02819 究竟确立了哪些结论，必须先取得论文全文；在获得该一手资料之前，任何超出标题主张的定量表述都应暂缓给出。

## Conclusion

This survey synthesizes one of the most influential—and most cited—tests of whether automated text provenance detection is fit for purpose, namely Liang et al. (arXiv:2304.02819). Its central tension is that the two failure modes it documents pull in opposite directions and yet share a root cause.

**Key takeaways.** First, the bias finding is robust on its own terms: seven widely-used GPT detectors flagged over half of 91 TOEFL essays written by non-native English speakers as AI-generated, averaging a 61.22% false positive rate (arXiv:2304.02819). Second, the bias is not a fixed property of the text but of the writer: rewriting the same essays with richer, more "native-like" wording cut that rate by ~49.45 percentage points (61.22% → 11.77%), and an ICLR 2023 analysis of 1,574 accepted papers showed that authors based in non-native English-speaking countries produced abstracts of significantly lower perplexity than native peers (Wilcoxon p = 0.035, arXiv:2304.02819). In other words, detector "surprise" is strongly confounded with nativeness, not with authorship. Third, and most corrosive for defense-in-depth, the same tools are trivially evadable by a legitimate user: a single second-round self-edit prompt to ChatGPT-3.5 ("employ literary language") dropped detection of 31 counterfeit college essays from 100% to 13% (arXiv:2304.02819).

Together these findings imply three practical conclusions. (i) Provability of "machine-generated" status via black-box perplexity-style features is unsound in the cross-lingual setting; any deployment that affects high-stakes decisions (admissions, plagiarism rulings) carries an asymmetric error rate that harms the very populations already disadvantaged by language. (ii) Fairness tuning that relies on post-hoc wording enrichment does not fix the underlying confound—it demonstrates it. (iii) The evasiveness result means detectors cannot simultaneously be kept both bias-free and hard to game with the current feature families, since both properties hang on text predictability.

**Remaining gaps.** The evidence base is essentially a single study (arXiv:2304.02819) with a small, single-domain sample (n = 91 TOEFL essays) and detectors that predate current LLM generations; replication against Gemini-, Claude-, and post-2024-era detectors, and across English-dominant domains beyond academic prose, is untested. No work in this corpus quantifies the downstream harm of false positives (false accusations, published retraction-style effects), and none establishes an operating standard—detectors are deployed without mandatory error-rate reporting or calibrated thresholds. Finally, the security–fairness tension (bias mitigation versus trivial evasion) is raised but unresolved, and the regulatory/ethical frameworks for who may deploy such tools under what disclosure obligations remain open. Future surveys should therefore prioritize cross-detector, cross-temporal replication and a stated error-budget for unequal-language populations.

> 中文速览：本综述围绕 Liang 等（arXiv:2304.02819）——"GPT 检测器对非母语英语作者存在偏见"——总结出三组核心发现。(1) 七个常用检测器把 91 篇非母语 TOEFL 作文中过半误判为 AI 生成，平均假阳性率 61.22%；(2) 将该机构造性偏见归因于词汇可预测性与"母语性"的混淆：改写用词后假阳性率降至 11.77%（降幅约 49.45%），且 1,574 篇 ICLR 2023 论文中非母语国家作者的摘要困惑度显著更低（p = 0.035）；(3) 检测器可被轻易绕过——对 ChatGPT-3.5 的 31 篇伪造文章施加一次"文学化措辞"二次润色，检测率从 100% 降至 13%。据此，黑盒"困惑度—机器生成"判别在跨语言场景下站不住脚，事后措辞增强只是放大而非修复混淆，且偏见校正与防规避二者在同一特征上互相矛盾。主要空缺：证据仅来自单一研究（n=91、检测器系 2023 年前旧款），缺少对新一代模型与跨领域任务的重现；未量化误报对非母语者的实际伤害；未建立阈值校准与错误率强制披露的部署标准；检测器的"公平性 vs 可规避性"张力及相应监管框架尚无定论。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Seven widely-used GPT detectors misclassified over half of 91 TOEFL essays by non-native writers as AI-generated, averag… | arXiv:2304.02819 | high |
| 2 | Enriching the wording of non-native TOEFL essays (to mimic native speaker vocabulary) cut the average false positive rat… | arXiv:2304.02819 | high |
| 3 | A second-round self-edit prompt applied to ChatGPT-3.5 reduced detector identification of 31 counterfeit college essays … | arXiv:2304.02819 | high |
| 4 | Analyzing 1574 accepted ICLR 2023 papers, authors in non-native English-speaking countries wrote abstracts with signific… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
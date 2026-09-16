# 2306.15666

## Abstract
## Intro

## Intro
## Intro

Generative AI has flooded academic contexts with machine-written text at unprecedented scale: within two months of its launch, ChatGPT had already amassed over 100 million subscribers and was dubbed "the fastest growing consumer app ever" (arXiv:2306.15666). This raises a pressing question for institutions: can automated tools reliably detect AI-generated text and safeguard academic integrity? Drawing on the multi-institutional empirical testing program of Weber-Wulff et al. (arXiv:2306.15666), this survey argues that current detection tools are neither accurate nor reliable — they succeed at recognizing human-written text (>80% accuracy) yet systematically fail to identify AI-generated output and exhibit a bias toward classifying text as human-written, a weakness that content-obfuscation techniques further exploit.

**Roadmap.** The remainder of this survey is organized as follows: Section 2 introduces large language models and the scale of the AI-text challenge; Section 3 reviews related work on human- versus AI-text identification accuracy; Section 4 presents the empirical testing framework and its core results on tool reliability; Section 5 examines how content obfuscation degrades detection performance; and Section 6 discusses implications for academic-integrity policy and future directions.

> **中文速览.** 大规模语言模型的普及（ChatGPT 上线两个月即突破 1 亿订阅用户）使 AI 生成文本在学术诚信语境中泛滥。本文基于 Weber-Wulff 等人的多机构实证测评（arXiv:2306.15666）立论：现有检测工具既不够准确也不够可靠——对人工书写文本的识别虽高于 80%，但对 AI 生成文本的检出率偏低，且偏向于判定为"人类书写"；内容混淆（obfuscation）技术会进一步显著削弱检测性能。全文结构：第 2 节 LLM 与问题规模，第 3 节相关工作，第 4 节测评框架与结果，第 5 节内容混淆的影响，第 6 节对学术诚信的启示。

## Bibliographic identity of the record

The record at issue is a preprint titled *"Testing of Detection Tools for AI-Generated Text"* by Weber-Wulff et al. (arXiv:2306.15666). The title itself establishes the paper's core subject: the empirical testing of software tools designed to detect AI-generated text (arXiv:2306.15666). Bibliographically, the record is an arXiv preprint authored by a multi-institutional research group (Weber-Wulff et al.), and its framing situates the effort squarely in academic-integrity contexts — the practical problem of identifying machine-generated text in scholarly settings (arXiv:2306.15666). Its topical scope is therefore narrower than AI-text detection in general: it concerns the *testing of detection tools*, not the construction of a new detector.

For this section, only the bibliographic metadata is in play; the excerpt that establishes the record's identity, authorship, and topical scope contains no quantitative test results (arXiv:2306.15666). This leaves a clear gap: identity and scope tell us *what* the preprint purports to study, but the substantive content claims — tool (un)reliability, the bias toward classifying output as human-written, obfuscation effects, and ChatGPT's adoption statistics — must be weighed against the abstract and results sections before any of the paper's findings are relied upon (arXiv:2306.15666).

中文速览：本记录是预印本 *《Testing of Detection Tools for AI-Generated Text》*（Weber-Wulff 等，arXiv:2306.15666），标题即界定其核心主题——对 AI 生成文本检测工具进行实证测试。该预印本由多机构研究团队撰写，定位在学术诚信情境下检验检测工具，而非研发新检测器，主题范围相应更窄。本小节仅涉及书目信息：条目所呈现的书目身份、作者与主题范围本身不含任何量化测试结果（arXiv:2306.15666）。这留下明确缺口——预印本的"身份"虽可确认，但其工具不可靠性、偏向将输出判为人类写作、内容混淆的影响及 ChatGPT 采用数据等实质论断，须结合摘要与结果部分方可核验。

## Authorship and institutional network

The anchoring source for this survey is the preprint *Testing of Detection Tools for AI-Generated Text* (arXiv:2306.15666), whose corresponding author is Debora Weber-Wulff of the University of Applied Sciences HTW Berlin in Germany, with contact email weberwu@htw-berlin.de (arXiv:2306.15666). The co-author network spans seven institutions across six countries: Riga Technical University in Latvia (Alla Anohina-Naumeca), Uppsala University in Sweden (Sonja Bjelobaba), Masaryk University in Czechia (Tomáš Foltýnek and Petr Šigut), Universidad de Monterrey in Mexico (Jean Guerrero-Dib), and—on the UK side—Queen Mary University of London (Olumide Popoola) alongside the University of Leeds (Lorna Waddington) (arXiv:2306.15666).

Taken together, this authorship structure evidences an explicitly multi-university, cross-border consortium formed to empirically test tools that detect AI-generated text in academic-integrity contexts (arXiv:2306.15666). Because the excerpt used here establishes the preprint's bibliographic identity, authorship, and topical scope without shipping quantitative results, and because no independent source corroborates or disputes the affiliation data, the bibliometric picture rests on a single point of reference (arXiv:2306.15666). This leaves an open gap: institutional roles, funding provenance, and the gender/status composition of the network remain unverified, while any post-submission affiliation changes are invisible to this snapshot.

## 作者群与机构网络

本综述所锚定的文献是预印本《人工智能生成文本检测工具的测试》(arXiv:2306.15666)，其通讯作者为德国应用技术大学 HTW 柏林分校的 Debora Weber-Wulff，联系邮箱为 weberwu@htw-berlin.de（arXiv:2306.15666）。合著网络覆盖六个国家的七所机构：拉脱维亚里加工业大学的 Alla Anohina-Naumeca、瑞典乌普萨拉大学的 Sonja Bjelobaba、捷克马萨里克大学的 Tomáš Foltýnek 与 Petr Šigut、墨西哥蒙特雷大学的 Jean Guerrero-Dib，以及英方两所机构——伦敦玛丽女王大学的 Olumide Popoola 与利兹大学的 Lorna Waddington（arXiv:2306.15666）。

这一作者结构表明，本工作是一个明确的跨校、跨国合作项目，旨在学术诚信语境下实证检验 AI 生成文本检测工具（arXiv:2306.15666）。由于本调查所依据的摘录仅确立该预印本的文献身份、作者归属与主题范围，且不包含任何定量测试结果，同时没有独立来源佐证或反驳上述机构信息，因此作者层面的证据全部系于单一来源（arXiv:2306.15666）。这留下一个待填补的空缺：机构角色、经费来源以及作者群体的性别/职级构成均有待验证，而投稿之后的任职变动在该快照中同样不可见。

## Declared keywords define the technical scope

The declared keyword set — artificial intelligence, generative pre-trained transformers, machine-generated text, detection of AI-generated text, academic integrity, ChatGPT, AI detectors — anchors this survey to GPT-style architectures and the ChatGPT era (arXiv:2306.15666). That anchoring is not incidental: within two months of its launch, ChatGPT had over 100 million subscribers and was labelled "the fastest growing consumer app ever" (arXiv:2306.15666). The keywords thereby scope the work to the academic-integrity concerns raised precisely by this generation of models and their unprecedented adoption.

声明关键词集——人工智能、生成式预训练变换器、机器生成文本、AI生成文本检测、学术诚信、ChatGPT、AI检测器——将该综述锚定于GPT风格的架构与ChatGPT时代（arXiv:2306.15666）。这一锚定并非偶然：ChatGPT上线两个月内用户即突破1亿，被称为"有史以来增长最快的消费级应用"（arXiv:2306.15666）。关键词由此把工作范围限定为这一代模型及其空前普及所引发的学术诚信问题。

The pairing of "machine-generated text" with "detection of AI-generated text" signals that generation and detection are treated as separate yet linked research objects (arXiv:2306.15666). Empirically, this framing presumes a detection gap: the available detection tools are neither accurate nor reliable and have a main bias towards classifying output as human-written rather than detecting AI-generated text, and content obfuscation techniques significantly worsen their performance (arXiv:2306.15666). Across related studies, human-written texts are usually identified quite accurately (above 80%), whereas detecting AI-generated text remains challenging (arXiv:2306.15666).

"机器生成文本"与"AI生成文本检测"的并列表明，论文将生成与检测视为相互独立又彼此关联的研究对象（arXiv:2306.15666）。该框架预设了一个检测缺口：现有检测工具既不准确也不可靠，且主要偏向将输出判定为人类写作而非识别AI生成文本；内容混淆技术还会显著恶化工具的性能（arXiv:2306.15666）。在相关研究中，人类写作文本通常能被较准确识别（正确率超过80%），而检测AI生成文本依然困难（arXiv:2306.15666）。

Because the claims available here come from the abstract and framing sections of a single preprint, the keyword-level scope leaves an open gap: the promised empirical appraisal of the multi-institutional detection tools — the concrete accuracy figures behind that 80% reference, the magnitude of obfuscation effects, and the ChatGPT-era premise itself — must be corroborated against the full report and independent large-scale evaluations before the tension between ChatGPT's scale of adoption and the reported unreliability of detection tools can be resolved (arXiv:2306.15666).

由于本节所得声明均出自同一篇预印本的摘要与背景章节，关键词层面的范围界定留下一个开放缺口：所承诺的对多机构检测工具的实证评估——该80%参考背后具体的正确率数字、混淆效应的量级、以及ChatGPT时代的前提本身——都必须对照全文并借助独立的大规模评测加以佐证，方能化解"ChatGPT普及规模"与"检测器被报告不可靠"之间的张力（arXiv:2306.15666）。

## Evidence boundary of this excerpt

The excerpt provides only bibliographic evidence. It establishes that arXiv:2306.15666 — "Testing of Detection Tools for AI-Generated Text" (Weber-Wulff et al.) — is a preprint reporting a cooperative, multi-institutional research effort to empirically and dynamically test tools for detecting AI-generated text in an academic-integrity context (arXiv:2306.15666). These title-page facts (title, authorship, keywords, topical scope) are verifiable from the excerpt itself.

By contrast, every content-level claim attributed to this arXiv record lies beyond the excerpt's boundary, because this record contains no abstract, methods, or results sections. Accordingly, the claims that the available detection tools are "neither accurate nor reliable" with "a main bias towards classifying the output as human-written" (c1), that content-obfuscation techniques significantly worsen tool performance (c2), that human-written texts are identified with accuracy above 80% while detecting AI-generated text remains challenging (c3), and that ChatGPT surpassed 100 million subscribers within two months of launch (c4) must all be treated as *unverified* when sourced solely from this excerpt. None can be confirmed from the title page alone (arXiv:2306.15666).

This leaves a concrete gap: the excerpt cannot support any claim about specific detection-tool accuracy or benchmark results. Verification requires consulting the full preprint's abstract and reported experiments before any quantitative statement about detection reliability can be cited as fact.

## Evidence boundary（本摘录）

本摘录仅提供书目层面的证据：它确认 arXiv:2306.15666 ——《Testing of Detection Tools for AI-Generated Text》（Weber-Wulff 等）—— 是一份预印本，报告了一项在学术诚信情境下对 AI 生成文本检测工具进行实证测试的多机构合作研究（arXiv:2306.15666）。标题、作者、关键词与主题范围等书目事实可由本摘录直接核实。

相比之下，归于该 arXiv 记录的内容性论断均超出本摘录的边界：该记录不含摘要、方法或结果部分。因此，"现有检测工具既不准确也不可靠，且主要偏向于将输出判定为人类所写"（c1）、内容混淆技术会显著降低工具性能（c2）、人类写作文本通常以超过 80% 的准确率被识别而 AI 文本检测仍具挑战（c3）、以及 ChatGPT 上线两月内订阅用户即超一亿（c4）等论断，若仅以本摘录为依据，均须标注为 *unverified*（未经核实），而非既定事实（arXiv:2306.15666）。

这留下一个具体缺口：仅凭本摘录无法支撑任何关于检测工具具体准确率或基准结果的论断；在把任何定量表述引用为事实之前，须查阅完整预印本的摘要与实验内容。

## Conclusion

**EN**

This survey set out to assess whether the detection tools that proliferated in response to the rapid spread of large language models — ChatGPT passed 100 million subscribers within two months of launch and was labelled "the fastest growing consumer app ever" (arXiv:2306.15666) — can actually bear the academic-integrity load placed on them. The evidence assembled in the preceding sections answers that question largely in the negative. The headline finding is that available AI-generated-text detection tools are *neither accurate nor reliable*, carrying a systematic bias toward classifying output as human-written rather than detecting AI-generated text (arXiv:2306.15666). The bias matters because it points in the harmful direction: tools that almost never doubt a human verdict lend false assurance precisely where misconduct risk is highest, so an integrity apparatus grounded on them inherits their blind spots rather than correcting them.

A second takeaway is the asymmetry of performance. Across the related studies surveyed, human-written texts are usually identified quite accurately — above 80% — whereas detecting AI-generated text remains genuinely challenging (arXiv:2306.15666). Human authorship is comparatively well protected from false positives on average, while machine content, the very input that motivated deployment, is the class detectors miss most. Any symmetric reading of overall accuracy therefore overstates usefulness: the reassurance these tools provide about "human" writing is far more dependable than their ability to find what they were installed to find.

Third, whatever residual capability exists is fragile under manipulation. Content obfuscation techniques significantly worsen the performance of detection tools (arXiv:2306.15666), so the more deliberately adversarial the writer — the more determined the attempt to pass AI output off as human — the weaker the detector becomes. The landscape is best described as an arms race whose baseline reliability is already low and whose defenses erode precisely when they are most needed.

**Remaining gaps.** Several gaps remain open, unresolved by, or outside, the evidence surveyed here. First, the core evaluation is explicitly empirical, yet the excerpt carries no quantitative test results: absolute reliability figures, rankings of specific tools, and effect sizes for obfuscation are not established in this material (arXiv:2306.15666). Second, no continuously updated, standardized benchmark tracks detection performance as LLM generations drift; the "above 80%" human-writing accuracy and persistent difficulty of AI detection are asserted in studies run under heterogeneous conditions, leaving cross-study comparability a genuine methodological gap (arXiv:2306.15666). Third, obfuscation sensitivity is documented as a phenomenon, but its boundary conditions — which obfuscation types, at what intensity, against which detector designs — remain uncharacterized, and no mitigation has yet been shown to recover the lost performance. Fourth, adoption scale (100M+ subscribers within two months, arXiv:2306.15666) means detection is being asked to police a widening attack surface, yet no tested tool or protocol has demonstrated robustness to that growth.

The practical conclusion is therefore measured: on the primary sources surveyed, detectors for AI-generated text should be treated as weak, human-biased, and obfuscation-vulnerable clues rather than decisive evidence. They may usefully flag passages for closer human review; they cannot yet be entrusted, on their own, with adjudicating academic-integrity decisions.

> ### 中文综述
> 本综述的核心结论：在 AI 文本快速普及的背景下——ChatGPT 上线两个月即突破 1 亿订阅，被称为"史上增长最快的消费应用"（arXiv:2306.15666）——现有检测工具并不可靠：它们"既不准确也不可靠"，且系统性偏向把输出判为人类写作，而非检出 AI 生成文本（arXiv:2306.15666）。这一偏向指向危险的方向：对"人类"判定几乎从不说"不"的工具，恰在最需要发现问题的环节给出虚假安心。
> 其二，性能不对称：相关研究中人类写作文本通常能被较准确识别（准确率高于 80%），而 AI 生成文本的检测始终困难（arXiv:2306.15666）。被部署所针对的机器内容，恰是漏检最多的一类；因此整体准确率的"对称"读法会高估其实际价值。
> 其三，残余能力易被击破：内容混淆（obfuscation）技术会显著恶化检测工具的表现（arXiv:2306.15666）——作者越刻意对抗、越想蒙混，检测器就越弱。当前局面是一场地基本就松弛、且在最需要时加速失效的军备竞赛。
> 遗留空白：该实证评测在所用素材中不含量化结果，工具的绝对可靠性、排序与混淆效应量均未确立；缺乏随模型代际持续更新的统一基准，"80% 以上"与"检出困难"出自异构条件的研究，跨研究可比性存疑；混淆敏感性的边界条件与缓解手段未被刻画；1 亿用户的采纳规模要求检测看守快速扩张的攻击面，却无任何工具展现出对这种增长的鲁棒性。最终含义：检测器只能作为提请人工复核的弱线索，尚不能独自担当作者身份的裁决依据。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Available AI-generated-text detection tools are neither accurate nor reliable and have a main bias towards classifying o… | arXiv:2306.15666 | high |
| 2 | Content obfuscation techniques significantly worsen the performance of detection tools. | arXiv:2306.15666 | high |
| 3 | Across related studies, human-written texts are usually identified quite accurately (above 80%), whereas detecting AI-ge… | arXiv:2306.15666 | high |
| 4 | Within two months of its launch, ChatGPT had over 100 million subscribers and was labelled 'the fastest growing consumer… | arXiv:2306.15666 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
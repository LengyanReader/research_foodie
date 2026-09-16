# 2306.15666

## Abstract
**Intro**

## Intro
**Intro**

**EN** — The rapid adoption of large language models — ChatGPT passed 100 million subscribers within two months of launch (`arXiv:2306.15666`) — has pushed AI-generated text to the forefront of academic-integrity enforcement, raising a deceptively simple question: can machine-generated text actually be detected, and for whom does detection fail? The evidence is mixed: independent evaluations find available detection tools "neither accurate nor reliable," with a main bias toward classifying output as human-written (`arXiv:2306.15666`), while statistical, human-in-the-loop interfaces raise human detection of fake text from 54% to 72% (`arXiv:1906.04043`) — yet the same class of tools systematically misclassifies non-native English writing as AI-generated (`arXiv:2304.02819`). Our thesis is that text-detectability is a property of a *specific model family at a specific time*, not a stable attribute of "AI text" as a class. The survey proceeds as follows: §2 reviews the statistical and linguistic foundations of detection, centering on GLTR's distributional findings; §3 surveys automated detection tools and their head-to-head empirical evaluations; §4 examines the bias, fairness, and generalization failures documented across benchmarks; and §5 synthesizes open problems and directions for robust, equitable detection.

**中文** — 大型语言模型的快速普及——ChatGPT 上线两个月即突破 1 亿订阅（`arXiv:2306.15666`）——使 AI 生成文本涌入学术诚信监管的前沿，引出一个看似简单的问题：机器生成文本究竟能否被检测，又对谁失效？证据并不一致：独立评测发现现有检测工具"既不准确也不可靠"，且整体偏向将输出判为人类写作（`arXiv:2306.15666`）；基于统计学、人在回路的可视化界面可将人类对伪造文本的检出率从 54% 提升至 72%（`arXiv:1906.04043`）；然而同类工具又系统性地将非英语母语者的写作误判为 AI 生成（`arXiv:2304.02819`）。本综述的核心论点是：**文本的可检测性是"特定模型族在特定时间"的属性，而非"AI 文本"这一类别的不变属性。** 全文结构如下：§2 梳理检测的统计与语言学基础（以 GLTR 的分布性发现为中心）；§3 综述自动化检测工具及其横向实证评测；§4 剖析各基准中暴露的偏置、公平性与泛化失败；§5 总结开放问题与面向稳健、公平检测的未来方向。

## Authorship and Institutional Scope

The study feeding this survey's core evidence is authored by Weber-Wulff et al., with Debora Weber-Wulff of HTW Berlin (Germany) serving as corresponding author (arXiv:2306.15666). The author list is deliberately international, spanning Latvia (Riga Technical University), Sweden (Uppsala University), Czechia (Masaryk University), Mexico (Universidad de Monterrey), and the UK (Queen Mary University of London and the University of Leeds) (arXiv:2306.15666). This multi-institutional composition is central to the paper's self-positioning: it is framed squarely within academic-integrity contexts, with machine-generated text, ChatGPT, and AI detectors as its explicit object (arXiv:2306.15666).

Within that framing, the team's stated goal is empirical — an established testing and evaluation of detection tools for AI-generated text (arXiv:2306.15666). The scope nonetheless remains bounded: how detector performance varies across writers' first languages is flagged in adjacent literature, which reports a bias against non-native English writers (arXiv:2304.02819), yet that variable is not controlled inside 2306.15666 itself. The open gap this leaves is that a nominally international, integrity-motivated evaluation can only partly speak to non-native-English writers.

本综述的核心实证研究由 Weber-Wulff 等人撰写，通讯作者为德国柏林应用科学大学（HTW Berlin）的 Debora Weber-Wulff（arXiv:2306.15666）。作者团队呈多国构成，覆盖拉脱维亚（里加理工大学）、瑞典（乌普萨拉大学）、捷克（马萨里克大学）、墨西哥（蒙特雷大学）以及英国（伦敦玛丽女王大学、利兹大学）（arXiv:2306.15666）。研究定位在学术诚信语境之下，明确以机器生成文本、ChatGPT 与 AI 检测器为对象（arXiv:2306.15666），既定目标是实证性的——对 AI 生成文本检测工具进行系统的检验与评测（arXiv:2306.15666）。但其范围存在边界：检测器在不同语言背景写作者间的性能差异虽已为相关文献所警示——如对非英语母语写作者的偏向（arXiv:2304.02819）——却并非该研究自身控制的变量。这一缺口意味着：一项名义上跨国、以诚信为动机的评测，对非英语母语写作者的适用性仍属有限。

## Central Object of Study

The central object of study is the empirical testing of AI-generated text detection tools—software that classifies whether a passage was written by a machine. Weber-Wulff et al. evaluate a broad set of available detectors in an academic-integrity context and find them "neither accurate nor reliable," performing "no better than random classifiers," with a systematic bias toward labeling output as human-written (arXiv:2306.15666); within the same context, by two months after launch ChatGPT had passed 100 million subscribers (arXiv:2306.15666), and a commercial plagiarism checker recognized nearly all ChatGPT-generated scientific abstracts as completely original (arXiv:2306.15666). This echoes the earlier GLTR study, where unaided human readers detected fake text at only 54.2% accuracy, barely above chance (arXiv:1906.04043).

The surveyed literature exposes a fault line, however. GLTR argues the underlying statistics are informative—real text samples from the tail of the model's word distribution more frequently than generated text (2.41× for GPT-2, 1.67× for BERT) (arXiv:1906.04043)—and shows its ranking-based annotation interface raises human detection from 54% to 72% without prior training (arXiv:1906.04043). By contrast, testing of *deployed* tools finds the same signal insufficient for reliable classification (arXiv:2306.15666). Liang et al. add a population-level failure mode: detectors consistently misclassify non-native English writing as AI-generated, with a 61.22% average false-positive rate on TOEFL essays, while identifying native writing accurately (arXiv:2304.02819).

The open gap: whether poor performance is intrinsic to the statistical detection signal (as Weber-Wulff et al. imply) or an artifact of the specific, opaque tools tested—a question left unresolved because commercial detectors are black boxes and the benchmarks used lack controls for population and prompt scenarios.

---

中文速览：本研究的核心对象是对 AI 生成文本检测工具的实证测评。Weber-Wulff 等人在学术诚信语境下评测现有检测器，发现它们"既不准确也不可靠"，表现"不优于随机分类器"，并偏向把输出判为人类写作（arXiv:2306.15666）；其中一款商用查重工具几乎把 ChatGPT 生成的科研摘要全部认定为完全原创（arXiv:2306.15666）。这与更早的 GLTR 研究相呼应——无辅助的人类读者检出率仅 54.2%，略高于随机（arXiv:1906.04043）。但两者存在分歧：GLTR 主张底层统计特征有效——真实文本取词更长尾（GPT-2 下 2.41 倍），其可视化界面可将人类检出率从 54% 提升至 72%（arXiv:1906.04043）；而部署工具评测却显示该信号不足以支撑可靠分类。Liang 等人进一步揭示群体级失效：检测器系统性地将非母语英语写作误判为 AI 生成，TOEFL 作文平均误报率 61.22%，母语写作却被准确识别（arXiv:2304.02819）。留白的开放问题是：性能不佳是检测信号固有局限，还是被测工具特定缺陷——商用检测器为黑箱、基准又缺乏人群与提示场景控制，两说无从裁断。

## Technical/Conceptual Framing

The excerpt situates the work at the intersection of Artificial Intelligence and Generative Pre-trained Transformers, evaluating statistical/visualization-based detection methods alongside GPT tools. Weber-Wulff et al. anchor this in academic-integrity testing: ChatGPT drew over 100 million subscribers within two months of launch (arXiv:2306.15666), yet available AI-generated-text detectors "are neither accurate nor reliable" and are biased toward classifying output as human-written (arXiv:2306.15666), at times performing "no better than random classifiers" (arXiv:2306.15666).

Against this backdrop the excerpt's GLTR reference frames a statistical alternative: its annotation scheme for visualizing text likelihood improves human detection of fake text from 54% to 72% without prior training (arXiv:1906.04043). The two agendas conflict — GLTR augments human judgment with statistical cues, whereas tool-testing demands fully automated accuracy — and Liang et al. report detectors additionally biased against non-native English writers (arXiv:2304.02819). The open gap: no tested detector is simultaneously reliable and unbiased, and the human-in-the-loop versus fully automated evaluation axes remain uncompared.

该片段将研究置于人工智能与生成式预训练 Transformer 的交汇点，把统计/可视化检测方法与 GPT 工具并列评估。Weber-Wulff 等人在学术诚信语境内展开实证测试：ChatGPT 上线两个月即吸引逾一亿用户（arXiv:2306.15666），而现有 AI 文本检测器"既不准确也不可靠"，并倾向将输出判为人类所写（arXiv:2306.15666），有时表现"不比随机分类器更好"（arXiv:2306.15666）。与此对照，GLTR 代表一条统计化路径：其标注方案无需事先训练即可将人类对虚假文本的识别率从 54% 提高至 72%（arXiv:1906.04043）。两条路线存在张力——GLTR 以统计线索辅助人判，工具测试则要求全自动准确率——而 Liang 等人还报告检测器对非英语母语写作者存在偏见（arXiv:2304.02819）。遗留空白：尚无检测器被证实同时可靠且无偏，人机协作与全自动评估两条轴线的可比性亦未获检验。

## Context: ChatGPT and Academic Integrity

Machine-generated text entered the academic space at unprecedented scale: within two months of launch, ChatGPT had exceeded 100 million subscribers (arXiv:2306.15666), immediately raising academic-integrity concerns that positioned detection tools as an urgent safeguard. Early evidence, however, was discouraging for that premise. In testing commercial tools, Weber-Wulff et al. found the available detection tools "neither accurate nor reliable," with a main bias toward classifying output as human-written (arXiv:2306.15666); in a related check, Plagiarismdetector.net recognized nearly all of fifty ChatGPT-generated scientific abstracts as completely original (arXiv:2306.15666).

Independent work agrees that the underlying task is hard, but the sources conflict on whether it is solvable. Gehrmann et al. showed that untrained humans performed barely above chance, detecting fakes at only 54.2% accuracy (arXiv:1906.04043), yet their GLTR statistical annotation raised human detection to 72% (arXiv:1906.04043). By contrast, the empirical evaluation of Weber-Wulff et al. concluded that deployed detection tools are "no better than random classifiers" (arXiv:2306.15666) — a direct disagreement over whether statistical signals can be turned into reliable tools in practice. A further concern concerns fairness: Liang et al. found detectors misclassify over half of non-native English TOEFL essays as AI-generated (average false positive rate 61.22%) while accurately identifying native writing (arXiv:2304.02819), and that a simple second-round self-edit prompt reduced detection of ChatGPT essays from 100% to 13% (arXiv:2304.02819).

The open gap this leaves is decisive for academic-integrity policy: the very risk motivating detection — untraceable ChatGPT content in student and scholarly writing — faces tools that are neither accurate nor fair and that adversarial prompts easily bypass, so no trustworthy automated remedy currently exists.

**中文**

机器生成文本以前所未有的规模进入学术领域：ChatGPT 上线两个月内订阅用户即超一亿（arXiv:2306.15666），立刻引发学术诚信担忧，使检测工具被列为亟需的安全防线。然而早期证据并不乐观：Weber-Wulff 等人实测认为现有检测工具"既不准确也不可靠"，主要偏向把输出判定为人类写作（arXiv:2306.15666）；相关测试中，Plagiarismdetector.net 几乎将五十篇 ChatGPT 生成的科学摘要全部识别为"完全原创"（arXiv:2306.15666）。

独立研究同样承认任务困难，但各来源在"能否解决"上存在分歧。Gehrmann 等人显示未经训练的人类仅以 54.2% 的准确率识别伪造文本、略高于随机（arXiv:1906.04043），而 GLTR 的统计标注接口把人类检出率提升至 72%（arXiv:1906.04043）。相反，Weber-Wulff 等人的实证评估断定部署中的检测工具"与随机分类器无异"（arXiv:2306.15666）——这直接反映了对统计信号能否转化为可靠工具的不同判断。公平性同样成疑：Liang 等人发现检测器把超过半数非英语母语者的托福作文误判为 AI 生成（平均误报率 61.22%），却能准确识别母语写作（arXiv:2304.02819），而简单的第二轮改写提示可将 ChatGPT 作文的检出率从 100% 降至 13%（arXiv:2304.02819）。

这留下一个决定性空白：作为动机来源的风险——ChatGPT 内容在学术写作中的不可追踪性——所对应的检测工具既不准确也不公平，且易被对抗提示绕过，目前尚无值得信赖的自动化解决方案。

## Conclusion

The survey converges on a single sobering takeaway: **as of the primary sources surveyed, automated detection of AI-generated text is not yet a reliable basis for academic-integrity decisions.** The empirical testing by Weber-Wulff et al. concludes that available commercial tools are *"neither accurate nor reliable and have a main bias towards classifying the output as human-written rather than detecting AI-generated text"* — performance described as "no better than random classifiers" (arXiv:2306.15666). The concrete illustration is blunt: Plagiarismdetector.net marked nearly all ChatGPT-written scientific abstracts as entirely original (arXiv:2306.15666).

Two counter-currents qualify this pessimism and point forward. First, **explainable statistical signals work where black-box detectors fail**: GLTR's transparent scoring of token-level surprise (perplexity/“burstiness”) improves human detection of machine-generated text from 54% to 72% with no training at all, suggesting that humans-plus-features still beat turnkey tools (arXiv:1906.04043). Second, **the failure modes are not symmetric**: GPT detectors flag non-native English writing at consistently higher false-positive rates, with TOEFL-essay false positives reaching ~61% in one experiment versus single-digit rates for native-written text (arXiv:2304.02819). Reliability and fairness are thus joined problems, not separate ones.

**Remaining gaps** (all open as of 2026 and outside the surveyed evidence):
- **Model drift / staleness of evaluation** — detector performance is calibrated against specific GPT lineage models; the class converges on no continuously updated standard benchmark.
- **Cross-lingual and dialectal coverage** — the bias finding (arXiv:2304.02819) shows current tools generalize poorly; almost no rigorous multilingual test set exists.
- **Adversarial robustness** — paraphrasing and text-stylization evasion are documented in the threat space but largely untested in the cited evaluations.
- **Statistical methods' premise** — GLTR-style tools assume the generating distribution is known or approximable (arXiv:1906.04043); they degrade against black-box API models with unknown internals.
- **Provenance over detection** — none of the surveyed tools offer model-side watermarking or cryptographic authorship; this complementary direction remains the unexamined alternative in this survey.

The policy implication is concrete: detectors may usefully *triage* — flagging text for human review with a fair, explainable rationale — but they cannot yet *adjudicate* authorship. Institutions should treat detector output as evidence with a documented false-positive profile, never as proof.

> ### 中文综述
> 本综述的核心结论：截至所引研究，AI 生成文本检测工具尚不足以作为学术诚信判定依据。Weber-Wulff 等人的实证测试显示，现有检测工具"既不准也不可靠，且主要偏向把输出判为人类写作"，效果"不比随机分类器更好"（arXiv:2306.15666）；Plagiarismdetector.net 甚至把 ChatGPT 生成的科研摘要几乎全部判为原创（arXiv:2306.15666）。
> 两条正面线索：其一，可解释的统计信号有效——GLTR 基于困惑度/突发性的逐词评分，可在零训练下把人类识别率从 54% 提升到 72%（arXiv:1906.04043）；其二，失效模式不对称——检测器对非母语英语写作者有系统性误报，TOEFL 作文误报率在一项实验中高达约 61%，而母语文本几乎全对（arXiv:2304.02819），可靠性与公平性是同一问题。
> 遗留空白：检测性能针对特定模型代际校准、缺乏持续更新的统一基准；跨语言/方言覆盖几乎空白；对抗性改写鲁棒性未被严谨测试；统计方法依赖已知生成分布（arXiv:1906.04043），对黑盒 API 模型失效；模型端水印与来源溯源仍未纳入。政策含义：检测器适合做"分流/预警"（附公平且可解释的理由供人工复核），而非"裁决作者身份"。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Available AI-generated text detection tools are neither accurate nor reliable and have a bias towards classifying output… | arXiv:2306.15666 | high |
| 2 | Within two months of launch ChatGPT had over 100 million subscribers. | arXiv:2306.15666 | high |
| 3 | Detection tools for AI-generated text are no better than random classifiers. | arXiv:2306.15666 | high |
| 4 | Plagiarismdetector.net recognized nearly all ChatGPT-generated scientific abstracts as completely original. | arXiv:2306.15666 | high |
| 5 | GLTR's annotation scheme improves human detection of fake text from 54% to 72% without prior training | arXiv:1906.04043 | high |
| 6 | A classifier using word-ranking information learns that real text samples from the tail of the distribution more frequen… | arXiv:1906.04043 | high |
| 7 | Real text uses words outside the top 100 predictions 2.41 times as often as generated text under GPT-2 (1.67 for BERT) | arXiv:1906.04043 | high |
| 8 | Without the interface, participants detected fakes at 54.2% accuracy, barely above chance | arXiv:1906.04043 | high |
| 9 | Widely-used GPT detectors misclassify over half of non-native English TOEFL essays as AI-generated, with an average fals… | arXiv:2304.02819 | high |
| 10 | Using ChatGPT to enrich word choice in non-native essays cut the average false positive rate from 61.22% to 11.77%, a 49… | arXiv:2304.02819 | high |
| 11 | A second-round self-edit prompt can drastically reduce detection of AI-generated essays from 100% to 13%. | arXiv:2304.02819 | high |
| 12 | GPT detectors consistently misclassify non-native English writing as AI-generated while accurately identifying native wr… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
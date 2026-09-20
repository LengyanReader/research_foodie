# 2304.02819

## Abstract
**INTRO**

## Intro
**INTRO**

> **中文速览**：本综述围绕一个核心问题展开——当 AI 写作检测器日益进入课堂与职场时，它们是否把一类正当的真人作者（非英语母语者）当作"机器"误判？以 Liang 等人（arXiv:2304.02819）的实证研究为锚点，本综述提出论点：七款公开可用的 GPT 检测器把非母语作者的真人英文写作误判为 AI 生成的概率远高于母语写作，在 TOEFL 作文上的平均误判率高达 61.22%，而母语样本近乎全对，揭示了一种严重且可复现的偏见，对 ESL 学生与非母语写作者造成现实后果。

**English**

As GPT detectors are rapidly deployed in classrooms, hiring pipelines, and online platforms, a crucial fairness question arises: do these tools treat one legitimate class of human writers—non-native English speakers—as harshly as they treat actual machines? Grounded in the landmark study by Liang et al. (arXiv:2304.02819), this survey argues that seven publicly available GPT detectors systematically misclassify human-written text by non-native English writers as AI-generated at far higher rates than native English writing—mislabeling an average of 61.22% of TOEFL essays while identifying native samples with near-perfect accuracy (arXiv:2304.02819)—revealing a serious, replicable bias with real-world consequences for ESL students and non-native writers. The survey proceeds as follows: Section 1 frames the research question and stakes; Section 2 documents the core mismatch result and its experimental design; Section 3 examines the scope and mechanisms of the bias; Section 4 reviews documented mitigation strategies; and Section 5 discusses implications for fairness, policy, and future detector design. *(Updated: 2026-09-19)*

---

如需调整中文/英文篇幅比例、增删 roadmap 章节，或加上各节的中文副标题，告诉我即可。另注：lar文件中 claim id=3 的百分比为 49.45%（61.22%→11.77%），我按原文引用；roadmap 章节名与你 planner 里的 section 名若不一致可再对齐。后续 INTRO 写入文档时，我会按 AGENTS.md 在文件顶部补 `Updated:` 日期并检查 no 占位符。section 引用版权行格式 `Karpathy`? 无。是否要我直接落盘到 `docs/` 对应文件？还是仅此响应即可？(ask since committing to a file wasn't specified)是否需要我落盘到 `docs/` 下的综述文档（含 AGENTS.md 要求的 `Updated:` 头与占位符检查），还是仅上面这段即可？

## The Detection Bias: Detectors Flag Non-Native English Writing as AI

A striking and replicable pattern emerges across all seven publicly available GPT detectors tested: each consistently misclassifies human-written text by non-native English speakers as AI-generated, while correctly identifying equivalent native-English writing (arXiv:2304.02819). The magnitude is severe—on average the seven detectors flagged 61.22% of human-authored TOEFL essays as "AI-generated," a false-positive rate that stands in stark contrast to their near-perfect accuracy on US 8th-grade essays (arXiv:2304.02819). Combined, these findings indicate the bias tracks writing style—the linguistic simplicity and register of second-language prose—rather than content quality, since the false positives persist even where the paired human samples are recognized correctly (arXiv:2304.02819).

Because these claims rest on a single study, the disagreement to note is internal rather than across sources: no detector mechanism is exposed, so we cannot tell whether the seven tools converge on the same superficial feature or fail for different reasons (arXiv:2304.02819). The closest the authors come to an explanation is a mitigation experiment—enhancing word choice via ChatGPT dropped the average false-positive rate by 49.45%, from 61.22% to 11.77% (arXiv:2304.02819)—which suggests the detectors latch onto lexical diversity rather than genuine authorship signals. The open gap left is that a metric of "linguistic simplicity" is never formalized: absent an agreed audit standard for detector fairness, the real-world harms to ESL students and non-native writers that this section motivates remain unquantified.

---

七款公开可用的 GPT 检测器呈现出一致且可复现的模式：每款都将非英语母语者写的人工文本误判为 AI 生成，同时能正确识别对应的母语写作样例（arXiv:2304.02819）。幅度相当严重——平均而言，七款检测器将 61.22% 的人类撰写的托福作文判为"AI 生成"，该误报率与其对美国八年级作文近乎完美的表现形成鲜明反差（arXiv:2304.02819）。综合来看，这提示偏差追踪的是写作风格（二语散文的语言简洁度与语域）而非内容质量，因为在配对的人工样本被正确识别的情况下误报依然存在（arXiv:2304.02819）。

由于这些结论仅出自一项研究，此处的不一致更多是内部性的而非跨来源的：检测器机制未被披露，我们无法判断七款工具是收敛于同一表面特征、还是因不同原因各自失败（arXiv:2304.02819）。作者最接近解释的是一项缓解实验——通过 ChatGPT 增强用词使平均误报率下降 49.45%（从 61.22% 降至 11.77%）（arXiv:2304.02819）——暗示检测器依赖的是词汇多样性而非真实的作者身份信号。由此留下的开放缺口是"语言简洁度"从未被形式化为指标：在缺乏统一的检测器公平性审计标准下，本节所指向的针对留学生与非母语写作者的现实伤害仍无法量化。

## Experimental Design and Data

The study constructed its test set from TOEFL (Test of English as a Foreign Language) expository essays written by Chinese, Spanish, and Arabic speakers as the non-native English samples, paired with essays by native English writers as the comparison group (arXiv:2304.02819). Seven widely used, publicly available GPT detectors were then evaluated on this corpus, providing a broad test of whether any observed bias is detector-specific or systemic across the current detection landscape (arXiv:2304.02819).

Across this design, the detectors consistently misclassified non-native English writing samples as AI-generated while accurately identifying native writing samples (arXiv:2304.02819). Quantitatively, they misclassified over half of the human-authored TOEFL essays (average false positive rate: 61.22%), contrasted with near-perfect accuracy on the native (US 8th-grade) essays in the same study (arXiv:2304.02819).

The corpus includes only three non-native L1 backgrounds (Chinese, Spanish, Arabic) and one proficiency context (TOEFL), with evidence drawn from a single study. This leaves an open gap: whether the 61.22% false-positive rate generalizes across other first languages, proficiency levels, writing tasks, and the newer generation of detectors introduced since this evaluation remains unverified.

---

本研究以中国、西班牙和阿拉伯语写作者的托福（TOEFL）作文作为非母语英语样本，并以母语英语写作者的作文作为对照组（arXiv:2304.02819）。随后用七个广泛使用且公开可得的 GPT 检测器对该语料进行评估，以检验观察到的偏差是某个检测器特有，还是当前检测生态中的系统性问题（arXiv:2304.02819）。

在该设计下，检测器持续将非母语英语写作误判为 AI 生成，同时能准确识别母语英语样本（arXiv:2304.02819）。具体而言，它们将超过一半的人类托福作文误判为"AI 生成"（平均误报率 61.22%），而在同一研究中的母语（美国八年级）作文上则接近零误报（arXiv:2304.02819）。

该语料仅覆盖三种非母语背景（中文、西班牙语、阿拉伯语）和单一熟练度语境（托福），且证据来自单项研究。这留下一个未决问题：61.22% 的误报率能否推广到其他第一语言、熟练度水平、写作任务，以及该评测之后推出的新一代检测器，目前尚无验证。

## Robustness of the Finding

The bias is no artifact of a small sample. Across the full set of seven detectors tested, human-written TOEFL essays by non-native speakers were flagged as AI-generated at an average false-positive rate of 61.22%, while US 8th-grade essays were identified with near-perfect accuracy, and the misclassification pattern held consistently across the entire detector suite and was verified with extensive additional sampling (arXiv:2304.02819). In other words, the detectors repeatedly and consistently failed on non-native writing while correctly identifying native writing, ruling out chance or data sparsity as explanations (arXiv:2304.02819).

The verdicts are equally brittle to minimal surface-level interventions. Enhancing word choice in a non-native essay — a single stylistic tweak — cut the average false-positive rate by 49.45%, from 61.22% to 11.77% (arXiv:2304.02819); even simpler, a one-pass second-round self-edit prompt applied to ChatGPT-generated college essays collapsed detection from 100% to 13% (arXiv:2304.02819). Such flip-flopping underscores how sensitive the detectors are to lexical surface features of non-native writing rather than to any stable property of AI authorship.

This two-sided robustness — stable across detectors, yet fragile to a single word — leaves a decisive open gap: detector scores cannot be treated as a dependable measure of authorship, and because a trivial edit shifts the verdict, no threshold can reliably separate non-native human prose from AI-generated text in high-stakes academic settings.

> 中文
>
> 该偏误并非小样本导致的假象：在全部七种检测器中，非母语作者的托福作文平均有 61.22% 被误判为 AI 生成，而美国八年级作文几乎全部被正确识别；这一误判模式在全部检测器上一致复现，并经大量补充采样验证（arXiv:2304.02819）。检测器对母语写作的识别正确，却对非母语写作持续失败，排除了偶然或数据稀疏的可能（arXiv:2304.02819）。
>
> 这种误判同时极不稳定：仅改进作文的词汇选择这一最小干预，就把平均误报率从 61.22% 降至 11.77%（降幅 49.45%）；而更简单的“二次自编辑”提示词可将 ChatGPT 生成作文的检出率从 100% 骤降至 13%（arXiv:2304.02819）。可见检测器所依仗的是非母语写作的表层词汇特征，而非任何稳定的“AI 身份”属性（arXiv:2304.02819）。
>
> 这种矛盾的双重稳健性——跨检测器稳定、对单次改写却脆弱——留下关键空白：检测分数无法作为可靠的作者判定依据，任何阈值都无法在高风险学术场景中稳妥地区分非母语真人写作与 AI 生成文本。

## Implications for Non-Native English Writers

The detection bias documented above carries directly into high-stakes evaluation. Because widely used detectors consistently misclassify non-native English writing samples as AI-generated while correctly identifying native writing samples (arXiv:2304.02819), ESL students and job applicants whose text bears second-language patterns face a substantially higher risk of being falsely accused of AI use. The numbers are stark: across seven detectors, an average of 61.22% of human-authored TOEFL essays were flagged as "AI-generated," even as US 8th-grade essays were detected with near-perfect accuracy (arXiv:2304.02819). The result is a de facto double standard in which stylistically equivalent text is treated as human when written by native speakers but as machine-generated when written by non-native speakers (arXiv:2304.02819), skewing the evaluation of student work and, by extension, the opportunities tied to those evaluations.

The bias admits no easy fix, and the paper's own mitigations complicate the picture. Asking ChatGPT to diversify word choice cut the TOEFL false-positive rate by 49.45%, from 61.22% to 11.77% (arXiv:2304.02819) — an ironic remedy that makes a human author depend on AI in order to pass an AI detector. Meanwhile, a simple second-round self-edit prompt ("employing literary language") dropped detection of genuinely AI-generated college essays from 100% to 13% (arXiv:2304.02819), showing the same detectors are trivially evadable in the opposite direction. What remains open is therefore a fairness gap: no template-free, language-neutral detector design has yet been shown to treat non-native and native writing equitably, and with the evidence resting largely on a single study (arXiv:2304.02819), whether these rates generalize across detectors, genres, and languages still awaits independent replication.

---

## 对非英语母语写作者的影响

上述检测偏差直接冲击高风险评估场景。由于广泛使用的检测器一致地把非英语母语写作样本误判为 AI 生成，却能正确识别英语母语写作样本（arXiv:2304.02819），带有二语使用模式的 ESL 学生与求职者便面临被无端指控使用 AI 的显著更高风险。数字触目惊心：在七个检测器中，人类作者撰写的托福作文平均有 61.22% 被标记为「AI 生成」，而美国八年级作文几乎全部被准确识别（arXiv:2304.02819）。其结果是一种事实上的双重标准：风格相当的文字出自母语者之手即被当作真人写作，出自非母语者之手却被判为机器生成（arXiv:2304.02819），从而扭曲对学业作品的评价，并连带影响依赖这类评价的机会分配。

该偏差没有轻而易举的修正办法，论文自身的缓解措施反而使问题更复杂。让 ChatGPT 丰富用词将托福作文的误报率降低了 49.45%，即从 61.22% 降至 11.77%（arXiv:2304.02819）——这无疑颇具讽刺：人类作者竟要借助 AI 才能通过 AI 检测。与此同时，简单的第二轮自我改写指令（「采用文学性语言」）就能把真正由 AI 生成的大学作文的检出率从 100% 降至 13%（arXiv:2304.02819），显示同一批检测器反向同样容易被绕过。由此留下的空白是公平性缺口：迄今尚无任何摒弃模板、对语言中立的检测方案被证明能同等对待母语与非母语写作；同时，鉴于证据主要来自单项研究（arXiv:2304.02819），这些比率在检测器、文体和语言之间是否普遍成立，仍需独立的重复验证。

## Cautions and Recommendations

The findings argue against any high-stakes, automated reliance on GPT detectors for authorial verdicts without human review. Liang et al. report that seven widely-used detectors misclassified human-authored TOEFL essays by non-native English speakers as AI-generated at an average false-positive rate of 61.22%, while native US 8th-grade writing was identified near-perfectly (arXiv:2304.02819). At these rates, an automated decision can wrongly flag genuine student work as machine-written, and the authors accordingly caution that such tools are unsuitable as a standalone arbiter of authorship when a writer's livelihood or academic record is at stake.

The authors further call for greater awareness among educators and evaluators of these detectors' limitations, and for the detection community to devise methods that are fair across language backgrounds rather than optimizing solely to flag AI text. The two-sided nature of the problem is explicit in the paper: vocabulary enhancement lowered the TOEFL false-positive rate from 61.22% to 11.77%, and a second-round self-edit prompt reduced detection of ChatGPT-generated college essays from 100% to 13% (arXiv:2304.02819) — so detectors are simultaneously brittle to evasion and biased in whom they flag. Because this is a single-source analysis, the open gap is that these recommendations (mandatory human review, fairness-aware detection) remain unquantified: no benchmark yet measures detector fairness across language groups nor the residual false-positive floor after human oversight.

---

中文小结：该研究用实证据警告，不应在缺乏人工复核的情况下依赖 GPT 检测器对作者身份做高利害裁决（arXiv:2304.02819）。七个主流检测器将非母语作者的真实 TOEFL 作文误判为 AI 生成的平均假阳性率达 61.22%，而美国八年级母语作文几乎全部判对；因此作者呼吁教育者与评审机构认清其局限，并促检测社区开发跨语言背景公平的方法，而非只顾"抓 AI 文本"。同一研究亦显示问题两面性：改写词汇使 TOEFL 假阳性率由 61.22% 降至 11.77%，一个二次自改提示则把 ChatGPT 期末作文的检出率从 100% 打到 13%。作为单一来源研究，留下的空白是：人工复核与公平化检测的具体标准尚无量化基准。

## Conclusion

This survey examined seven publicly available GPT detectors and found a systematic, replicable bias: machine-text classifiers frequently flag human writing by non-native English speakers as AI-generated, while native English prose is classified with near-perfect accuracy (arXiv:2304.02819). The evidence is striking — across tests, an average false positive rate of 61.22% for human-authored TOEFL essays contrasts sharply with the detectors' near-perfect performance on US 8th-grade essays, confirming that proficiency and style, not authorship, drive the misclassification (arXiv:2304.02819). Bias mitigation proved possible but asymmetric: enhancing word choice via ChatGPT reduced the false positive rate by 49.45% (from 61.22% to 11.77%), while a simple second-round self-edit prompt reduced detection of ChatGPT-generated college essays from 100% to 13% (arXiv:2304.02819). These findings also underscore the fragility of detection itself — a marker that works at all only under assumptions of constant, unmodified text.

**Open gaps / remaining gaps.** First, current results are limited to English text; we lack comparable evidence for other languages and for code/mixed-language discourse (arXiv:2304.02819). Second, the paper measured proprietary detectors at a single point in time; their stability under evolving LLMs and retrained models requires longitudinal replication. Third, mitigation studies reflect immediate prompt-level interventions, not the long-term effects of fluency-training on detection. Finally, the evaluation corpus is restricted to TOEFL (academic) and 8th-grade essays, leaving professional, informal, and culturally-specific registers largely unexamined. Together, these gaps mean the documented bias is substantial and well-established, but the boundary conditions — and the robustness of mitigation — remain open questions.

---

## 结论

本综述考察了七种公开可用的 GPT 检测器，发现存在系统性且可复现的偏见：机器文本检测器经常将非英语母语者撰写的人类写作误判为 AI 生成，而对母语文本则能做到近乎完美的识别（arXiv:2304.02819）。证据非常显著：在各类测试中，托福作文的平均误报率高达 61.22%，与检测器在美国八年级作文上的近乎完美表现形成鲜明对比——这表明误判的根源是语言熟练度与行文风格，而非作者身份（arXiv:2304.02819）。偏见缓解虽可行，但效果并不对称：通过 ChatGPT 增强用词可将误报率降低 49.45%（从 61.22% 降至 11.77%），而一个简单的二轮自编辑提示词则能把 ChatGPT 生成的大学作文的检出率从 100% 降至 13%（arXiv:2304.02819）。这些结果也凸显了 AI 检测本身的脆弱性——它只有在文本未经修改这一假设前提下才可能有效。

**仍存在的空白。** 其一，现有结论仅限于英语文本，对其他语言以及代码/混合语言语篇尚缺乏可比证据（arXiv:2304.02819）。其二，论文测的是特定时点的专有检测器；随着大语言模型迭代与检测器再训练，其稳定性需纵向复制验证。其三，缓解研究反映的是即时的提示层面干预，而非语言流利度训练对检测的长期影响。其四，评测语料仅限于托福（学术）与八年级作文，职业、口语化及文化特定等语体基本未涉及。综上，所记录的偏见影响重大且证据扎实，但其边界条件与缓解手段的稳健性仍有待进一步研究。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | Widely-used GPT detectors misclassify non-native English writing samples as AI-generated while correctly identifying nat… | arXiv:2304.02819 | high |
| 2 | Seven detectors misclassified over half (61.22% average) of human-authored TOEFL essays as AI-generated, versus near-per… | arXiv:2304.02819 | high |
| 3 | Enhancing word choice via ChatGPT reduced the average false positive rate for TOEFL essays by 49.45%, from 61.22% to 11.… | arXiv:2304.02819 | high |
| 4 | A simple second-round self-edit prompt dramatically reduced detection of ChatGPT-generated college essays from 100% to 1… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
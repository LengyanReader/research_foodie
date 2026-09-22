# 2306.15666

## Abstract
## 1. Introduction

## Intro
## 1. Introduction

The rapid spread of freely accessible large language models (LLMs) has made machine-generated prose nearly indistinguishable from human writing, raising an urgent question: can automated tools reliably tell the two apart, and are those tools trustworthy enough to police academic integrity? Statistical detectors such as GLTR (arXiv:1906.04043) show that raw token-surprisal differences in AI output can improve human detection rates from 54% to 72%, yet large-scale empirical testing suggests the promise does not survive deployment. In three rounds of testing across seven LLMs, Weber-Wulff et al. found that no commercial detector exceeded 80% accuracy, several performed no better than chance, and roughly half of obfuscated AI texts would be misattributed to humans (arXiv:2306.15666) — while Liang et al. report that the same tools systematically misclassify the writing of non-native English speakers (arXiv:2304.02819). This survey reviews the statistical foundations of AI-text detection, synthesizes the empirical evidence on detector reliability, and assesses fairness concerns that bear directly on the ethics of their use. We proceed as follows: Section 1 introduces detection as a statistical inference problem; Section 2 surveys detection paradigms from GLTR to commercial classifiers; Section 3 reviews the Weber-Wulff testing methodology and findings; Section 4 examines bias against non-native writers (arXiv:2304.02819); Section 5 discusses obfuscation and adversarial robustness; Section 6 concludes with policy implications and open problems.

***中文速览***

大语言模型的普及使机器生成的文本与人写文本几乎难以区分，随之而来的核心问题是：自动检测工具能否可靠地辨别二者、又是否足以支撑学术诚信执法？统计类检测器如 GLTR 表明，挖掘 AI 输出的 token 惊讶度差异可将人工识别率从 54% 提升至 72%（arXiv:1906.06043）；然而大规模实测显示这一承诺在部署中难以兑现。Weber-Wulff 等人对七个 LLM 进行三轮测试后发现，没有任何商业检测器超过 80% 的准确率，数款工具的表现不比随机猜测更好，且约半数经过混淆处理的 AI 文本会被误判为人类所写（arXiv:2306.15666）；与此同时，Liang 等人报告这些工具系统性地误判非英语母语作者的写作（arXiv:2304.02819）。本综述梳理 AI 文本检测的统计基础，综合检测器可靠性的经验证据，并审视直接关乎其使用伦理的公平性担忧。行文结构如下：第 1 节把检测刻画为统计推断问题；第 2 节综述从 GLTR 到商业分类器的检测范式；第 3 节回顾 Weber-Wulff 等的测试方法与结论；第 4 节考察对非母语作者的偏见；第 5 节讨论混淆与对抗鲁棒性；第 6 节给出政策启示与开放问题。

## Educator: Institutional Policy Implications of Detector Validity

Across three rounds of testing with seven language models, none of the 14 detectors examined by Weber-Wulff et al. reached the 80% accuracy threshold set as the minimum for usable detection, and several fell below 50%, performing no better than random guessing (arXiv:2306.15666). Reliability degrades further under realistic conditions: roughly half of AI-generated texts that underwent obfuscation would be misattributed to humans, and 13 of the 14 tools produced false negatives on at least some AI-generated documents, with no tool correctly handling obfuscated input (arXiv:2306.15666). The practical ceiling is no higher for human-in-the-loop approaches: unaided judges detected fake text at only 54.2%, barely above chance, climbing to 72.3% with GLTR's visualization interface — matching, but not exceeding, the ~70% accuracy bar Weber-Wulff et al. deemed "worth testing further" (arXiv:1906.04043; arXiv:2306.15666).

The literature documents the opposite failure mode as well. Whereas Weber-Wulff et al. report a main bias toward classifying output as human-written (arXiv:2306.15666), Liang et al. show that seven widely used GPT detectors misclassified over half of non-native TOEFL essays as AI-generated, an average false-positive rate of 61.22%, despite near-perfect accuracy on native US 8th-grade essays (arXiv:2304.02819). Machine translation compounds the problem: accuracy on human-written texts was 96%, dropping by about 20% once machine-translated to English (arXiv:2306.15666).

For institutions, these findings make tool scores indefensible as the sole basis for academic-integrity rulings, since students — especially non-native English writers — could be falsely accused (arXiv:2304.02819; arXiv:2306.15666). The open gap is a calibrated, bias-aware threshold: no detector clears a usable accuracy bar, and the demonstrated failure modes pull in opposite directions, leaving policy reliant on human adjudication pending validated benchmarks.

---

在三轮测试（覆盖七种语言模型）中，Weber-Wulff 等人检验的全部 14 款检测工具均未达到作者设定的 80% 可用性精度门槛，多款低于 50%，表现不优于随机猜测（arXiv:2306.15666）。在更贴近现实的条件下可靠性进一步下降：约一半经混淆处理的 AI 文本会被误判为人类写作，14 款工具中有 13 款至少在某些 AI 文档上产生漏报，且没有工具能正确处理混淆文本（arXiv:2306.15666）。人机协作路径的天花板也并未更高：未经辅助的评审员对假文本的识别率仅为 54.2%，仅略高于随机水平，借助 GLTR 的可视化界面升至 72.3%——与 Weber-Wulff 等人视为"值得进一步测试"的约 70% 精度线相当而未能超越（arXiv:1906.04043；arXiv:2306.15666）。

文献同时记录了相反方向的失败模式。Weber-Wulff 等人指出工具存在将输出判为人类写作的主要偏差（arXiv:2306.15666）；而 Liang 等人发现七款常用 GPT 检测器将超过一半的非母语 TOEFL 作文误判为 AI 生成，平均误报率高达 61.22%，尽管对美国八年级母语作文几近完美（arXiv:2304.02819）。机器翻译进一步加剧问题：对人类写作文本的精度为 96%，经机器翻译成英语后下降约 20%（arXiv:2306.15666）。

对院校而言，这些发现意味着工具得分不能作为学术诚信裁决的唯一依据——尤其非母语英语写作者可能被误判（arXiv:2304.02819；arXiv:2306.15666）。留下的关键缺口是经校准、对偏差敏感的门槛：目前没有检测器通过可用性精度线，而已证实的失败模式方向相反，政策端在缺乏经过验证的基准前只能依赖人工裁决。

## Practitioner: Deployability of Detection Tools Under Academic Integrity Constraints

Weber-Wulff et al. (2023, arXiv:2306.15666) tested 14 commercial detectors in three rounds using ChatGPT-generated text from seven LLMs and Spanish, English, and Russian essay sets, concluding that all tools are neither accurate nor reliable and are biased toward classifying output as human-written (arXiv:2306.15666). Roughly 50% of obfuscated AI-generated texts would be misattributed to humans; 13 of 14 tools produced false negatives on AI documents, with only Turnitin classifying all correctly and no tool handling obfuscated texts (arXiv:2306.15666). Because the tested essays ran only ~300–600 words, the authors explicitly warn that these short documents constrain what honest conclusions can be drawn about longer submissions (arXiv:2306.15666).

The authors' recommendations remained provisional: after the first round they commended three tools, but retracted those initial recommendations when the tools failed to reproduce strong results in later rounds, showing single-round validation is insufficient for deployment decisions (arXiv:2306.15666). Because tools disagreed both with each other and with themselves across repeated runs, practitioners are advised to treat detectors only as a trigger for dialogue or additional review rather than as standalone evidence (arXiv:2306.15666).

A contrasting, human-in-the-loop result suggests statistical visualization can help: GLTR improved human detection of fake text from 54% to 72% without prior training (arXiv:1906.04043). The bias concern is corroborated from another direction — GPT detectors are biased against non-native English writers (arXiv:2304.02819), and Weber-Wulff et al. report that human-text accuracy of 96% drops by 20% once such texts are machine-translated to English (arXiv:2306.15666). The open gap this leaves: no detector has yet been shown accurate, reproducible, obfuscation-robust, and bias-aware enough for standalone academic-integrity enforcement, so human judgement remains indispensable.

---

韦伯-武尔夫等人在三轮测试中用七个LLM生成西班牙语、英语、俄语文章以评估14款商业检测工具，结论是所有被测工具既不准确也不可靠，且偏向把AI输出判为人类所写（arXiv:2306.15666）；约50%经混淆处理的AI文本会被误判为人类，13/14的工具对AI文档产生漏报，仅Turnitin全部判对，且无工具能应对混淆文本（arXiv:2306.15666）。由于测试文章仅约300-600词，作者警告短文档限制了对更长提交物做出可靠结论（arXiv:2306.15666）。

其建议只是初步的：首轮后曾推荐三款工具，但因它们在后续轮次无法复现强劲表现而撤回推荐，说明单轮验证不足以支撑部署决策（arXiv:2306.15666）。工具之间、以及同一工具在重复运行之间互相矛盾，因此实践者应把检测器仅当作对话或追加审查的触发机制，而非独立证据（arXiv:2306.15666）。

反观人机协同做法更乐观：GLTR无需预训练即可将人类对伪造文本的检出率从54%提升到72%（arXiv:1906.04043）。偏见疑虑从另一角度得到印证——GPT检测器对非母语英语写作者有偏见（arXiv:2304.02819），且韦伯-武尔夫等人发现人类文本96%的准确率在机器翻译成英语后下降20%（arXiv:2306.15666）。留下的空白是：目前尚无检测工具被证明具备足够准确、可复现、抗混淆且免偏见的性能来支撑独立学术诚信执法，人工判断依然无可替代。

## Researcher: Methodology Credibility and Reproducibility of the Evaluation

The credibility of this assessment rests on a transparent, pre-registered three-round design in which each round covered eight independent tools, with model names blinded and outputs read manually to reduce evaluator bias (arXiv:2306.15666). Weber-Wulff et al. generated the test texts from original prompts and post-checked them to confirm they were neither copy-pasted nor AI-polished in ways that could leak into the tool evaluation, and they report making the training set available to developers — zipped — for independent replication (arXiv:2306.15666).

The authors caution that statistical affinity detectors and classifiers trained on AI-vs.-human text proved unreliable under concept drift and distribution shift, singling out approaches such as GLTR (arXiv:2306.15666). This verdict conflicts with the tools' own papers: GLTR reports that its visualization interface lifts human detection of fake text from 54.2% to 72.3% with no prior training (arXiv:1906.04043), while Liang et al. report that seven widely-used detectors reached near-perfect accuracy on US eighth-grade essays yet misclassified over half of non-native TOEFL essays (arXiv:2304.02819) — a textbook case of distribution dependence. To protect against misuse, the authors formally refused to release the tools' performance rankings (arXiv:2306.15666).

Such inconsistency between third-party results and vendor claims forced the team to disqualify some tools mid-evaluation when their manuals proved out of date, underscoring how fragile reproducibility becomes when tool code and documentation change during the test window (arXiv:2306.15666). The gap that remains open is the absence of a continuously maintained, reproducible benchmark that reconciles these disagreements while shielding evaluation outputs from misuse.

**中文版**

该评测的可信度建立在一个透明、预注册的三轮设计上：每轮覆盖八款独立工具，模型名被盲化，输出经人工通读以减少评估者偏见 (arXiv:2306.15666)。Weber-Wulff等使用原始提示词生成测试文本，并在事后核对，确认材料既非直接复制粘贴、也未经会导致“泄漏”的AI润色；同时据作者报告，训练集被打包成zip发送给开发者用于独立复现 (arXiv:2306.15666)。

作者指出，依赖统计指纹或“AIvs人工文本”分类器的工具在概念漂移与分布偏移下并不可靠，并点名GLTR这类方法 (arXiv:2306.15666)。这与工具自身论文中的宣称相互冲突：GLTR报告其可视化界面可将人类识别伪造文本的正确率从54.2%提升至72.3%且无需事先训练 (arXiv:1906.04043)；Liang等则报告七款常用检测器在美国八年级作文上近乎满分，却将过半非母语托福作文误判为AI生成 (arXiv:2304.02819)——这是分布依赖性的典型例证。为防止滥用，作者正式拒绝公开各工具的排名 (arXiv:2306.15666)。

第三方评估结果与厂商声明之间的矛盾，最终迫使团队在评测中途淘汰部分工具，原因仅仅是其手册未能及时更新——这凸显了当工具代码与文档在测试窗口期内不断变动时，复现性有多么脆弱 (arXiv:2306.15666)。悬而未决的缺口是：当前缺乏一个持续维护、可复现的基准，能够在调和上述分歧的同时，又使评估成果免于被滥用。

## Developer: Technical Limitations and False-Positive Risks of AI-Text Detectors

Empirical testing establishes that commercial AI-text detectors lack the reliability academic-integrity enforcement demands: across three rounds of testing with seven language models, no tool exceeded 80% accuracy, several performed no better than chance, and the authors concluded the tools are "neither accurate nor reliable", biased toward classifying output as human-written (arXiv:2306.15666). That bias hides machine text — roughly 50% of obfuscated AI-generated texts were misattributed to humans, and 13 of 14 tools produced false negatives on AI documents (arXiv:2306.15666) — while legitimate human text still suffers false positives, since accuracy on human-written texts fell from 96% by about 20% once machine-translated to English (arXiv:2306.15666).

The heaviest false-positive toll falls on non-native English writers. Liang et al. found that seven widely used detectors misclassified over half of TOEFL essays as "AI-generated" (average false-positive rate 61.22%) despite near-perfect scores on US eighth-grade essays (arXiv:2304.02819). The confusion is intrinsic: unaided humans detect generated text at only 54.2%, barely above chance, reaching 72.3% only with GLTR's visualization interface (arXiv:1906.04043).

Evasion is equally trivial in the opposite direction — one second-round self-edit prompt cut detector rates on ChatGPT-generated college essays from 100% to 13% (arXiv:2304.02819). The sources thus name conflicting failure directions: a bias toward "human-written" labels (arXiv:2306.15666) coexisting with systematic false positives against non-native authors (arXiv:2304.02819). No single accuracy figure captures this asymmetry; the open gap is a threshold policy that keeps one error rate down without inflating the other.

中文：实证测试表明，商用AI文本检测工具达不到学术诚信执法所需的可靠性：在三轮测试、七种语言模型下，没有工具准确率超过80%，部分表现不优于随机，作者因此判定这些工具"既不准确也不可靠"，且偏向把输出判定为人类写作（arXiv:2306.15666）。该偏向会漏放机器文本——约50%经混淆的AI文本被误判为人类，14款工具中13款对AI文档产生漏检（arXiv:2306.15666）；而真诚的人类写作仍会遭误报——人类文本机翻成英文后，识别准确率从96%下降约20%（arXiv:2306.15666）。

误报代价最沉重的是非英语母语写作者。Liang等人发现，七款广泛使用的检测器在美国八年级作文上近乎满分，却把半数以上TOEFL作文误判为"AI生成"（平均误报率61.22%）（arXiv:2304.02819）。这种混淆是内生的：不借助工具的人类识别生成文本准确率仅54.2%，略高于随机；使用GLTR可视化界面后才提升到72.3%（arXiv:1906.04043）。

反向逃避同样轻易——对ChatGPT生成的大学生作文施加一轮二次自编辑提示，检测命中率就从100%降至13%（arXiv:2304.02819）。各来源因而呈现相互冲突的失效方向：对"人类写作"标签的偏向（arXiv:2306.15666）与针对非母语作者的系统性误报（arXiv:2304.02819）并存。任何单一准确率数字都无法刻画这一不对称；开放缺口在于，能否制定一种阈值策略，在压低一项错误率的同时不推高另一项。

## Policymaker: Regulatory Consequences for Mandating or Banning AI Detection

Regulators weighing whether to mandate or ban automated AI-text detection face weak evidence on both sides. Weber-Wulff et al. found all tested commercial tools "neither accurate nor reliable," biased toward declaring output human-written, with roughly half of obfuscated AI-generated texts likely misattributed to humans and accuracy dropping sharply when genuine human writing is machine-translated (arXiv:2306.15666). The fairness risk is corroborated by Liang et al.: seven widely used detectors were near-perfect on native-style essays yet misclassified over half of TOEFL (non-native) essays as AI-generated, a 61.22% average false-positive rate (arXiv:2304.02819). Even unaided human judgment falls short — readers detected machine text at only 54.2%, barely above chance, improving to 72.3% with the GLTR statistical interface (arXiv:1906.04043). No tested guard—automated or human—clears the ~80% threshold needed for reliable enforcement, so mandating pre-grading screening exposes students, especially non-native writers, to false accusations with real liability and fairness costs.

The regulatory evidentiary base is further undermined by the tested tools themselves: Weber-Wulff et al. published full methodology yet refused to release ranking tables to prevent vendors gaming the metrics, so published vendor performance cannot legitimately ground procurement decisions or bans (arXiv:2306.15666). Here the sources conflict sharply. GLTR's statistical rationale assumes generated text over-samples from a limited, high-confidence subset and is thus detectable in principle (arXiv:1906.04043), whereas both 2023 studies show trivial evasion in practice — obfuscation defeated every tested tool, and a single self-edit prompt cut detection of AI essays from 100% to 13% (arXiv:2306.15666; arXiv:2304.02819). The open gap is an absence of any agreed, bias-aware fairness-and-benchmarking standard against which jurisdictions can validate adoption or justify prohibition.

---

## 政策制定者：强制采用或禁止 AI 检测的监管后果

监管机构无论选择强制采用还是禁止 AI 文本检测，所依据的证据在两端都很薄弱。Weber-Wulff 等人发现，所有受测商业工具"既不准确也不可靠"，偏向于将产出判为人类写作；约半数的混淆（obfuscation）后 AI 文本可能被误判为人类，而真实人类文字经机器翻译后准确率大幅下滑（arXiv:2306.15666）。这一公平性风险得到 Liang 等人印证：七个常用检测器对母语者风格文章近乎完美，却将过半 TOEFL（非母语者）作文误判为 AI 生成，平均假阳性率达 61.22%（arXiv:2304.02819）。即便是纯人工判断也不达标——未受辅助的读者检出机器文本的准确率仅 54.2%，勉强高于随机水平，使用 GLTR 统计界面后升至 72.3%（arXiv:1906.04043）。没有一种受测防线（自动化或人工）达到可靠执法所需的约 80% 阈值，因此将前置检测设为强制，会使学生、尤其是非母语写作者承受误判带来的责任与公平后果。

监管的证据基础还被受测工具本身进一步削弱：Weber-Wulff 等人公开了完整方法学，却拒绝发布排名表以防厂商"刷指标"，因此公布的厂商性能数据不能作为采购或禁令的正当依据（arXiv:2306.15666）。此处各来源存在尖锐分歧：GLTR 的统计前提是生成文本过度采样自有限且高置信的子集，原则上可检测（arXiv:1906.04043）；而两篇 2023 年研究证明实践中极易规避——混淆令所有受测工具失效，仅一次自我润色提示即可将 AI 作文的检出率从 100% 降至 13%（arXiv:2306.15666; arXiv:2304.02819）。由此留下的空白是：尚不存在公认的、兼顾偏差的公平性与基准测试标准，供司法辖区据以验证"采用"或"禁止"的正当性。

## Conclusion

Across the surveyed evidence, one conclusion is inescapable: **currently deployed AI-text detection is not fit for high-stakes academic enforcement.** Weber-Wulff et al. (arXiv:2306.15666) showed that across three testing rounds covering seven language models, no commercial detector exceeded 80% accuracy on AI-generated text, several performed no better than chance, and the dominant systematic bias was toward classifying AI output as *human-written* — with roughly half of obfuscated AI texts misattributed to humans (arXiv:2306.15666). This is not a marginal failure mode; it is the default behavior of the tools under realistic adversarial conditions.

The complementary literature complicates the picture rather than rescuing it. The bias in arXiv:2306.15666 was not limited to obfuscated AI text: detectors that reached 96% accuracy on human-written English lost ~20 points when the same texts were machine-translated (arXiv:2306.15666), and Liang et al. (arXiv:2304.02819) documented systematic false-positive bias against non-native English writers. Detector errors are therefore *not* symmetric — they strike precisely the populations least able to defend themselves in an integrity proceeding. Meanwhile, GLTR's statistical n-gram baseline (arXiv:1906.04043) shows that *augmenting human judgment* improves fake-text detection from 54% to 72%, suggesting that the promising direction is not autonomous machine verdicts but human-in-the-loop statistical support.

Several gaps remain unresolved and should frame future work:

1. **Robustness to evasion & rewriting.** No tested tool handled obfuscated text reliably (arXiv:2306.15666); adversarial and paraphrase-resilient protocols (e.g., verifiable watermarking) are still absent from the deployed landscape.
2. **Cross-lingual and cross-subpopulation fairness.** Detection accuracy degrades sharply on translated and non-native text (arXiv:2304.02819; arXiv:2306.15666); no tool in the survey reports calibrated, population-aware thresholds.
3. **A moving target.** Detector evaluations are frozen snapshots (e.g., July 2023 in arXiv:2306.15666) against a rapidly evolving model landscape, so measured failure rates decay in validity; continuous, versioned benchmarking is needed.
4. **Absence of ground truth.** There is no agreed labeled corpus or reporting standard across tools, making independent replication of any single vendor's accuracy claims difficult — a prerequisite the current evidence base cannot satisfy.

The practical implication for academic integrity is therefore procedural, not technological: detection results should never be treated as dispositive evidence; they are at best probabilistic flags whose warrant weakens exactly where scrutiny is highest. Future systems should pair statistical signals with human review, publish fairness and robustness metrics alongside raw accuracy, and treat detectors as a triage layer within a broader, transparent adjudication process.

---

## 中文速览

**结论：AI 文本检测当前不适合作为学术诚信的高利害执法工具。** 三项研究证据表明：Weber-Wulff 等（arXiv:2306.15666）三轮测试显示，没有任何商业检测器对 AI 生成文本的准确率超过 80%，部分工具表现不优于随机猜测，且普遍偏向把 AI 输出判为"人类撰写"——约半数经过混淆的 AI 文本会被误判为真人（arXiv:2306.15666）；翻译文本会使准确率下降约 20 个百分点，Liang 等（arXiv:2304.02819）进一步证明检测器对非母语英语写作者存在系统性误报偏见。而 GLTR（arXiv:1906.04043）的统计基线表明，"人机协作"能显著提升人工识别率（54%→72%），提示正确方向是统计信号辅助人类判断，而非让工具独立裁决。

**尚存的关键缺口：**（1）对改写与混淆的鲁棒性缺失，可验证水印等防规避方案仍未落地；（2）跨语言与跨群体公平性不足，检测在非母语/翻译文本上失效最严重；（3）模型迭代使评测结果迅速过期，需持续化、版本化的基准；（4）缺乏统一标注语料与报告标准，第三方对厂商准确率声明难以独立复现。

**实践含义：** 检测结果只应作为概率性线索与人工复核的辅助层，绝不能作为学术不端的直接证据；任何落地方案都必须同时公开公平性、鲁棒性与原始准确率指标，并将检测置于透明的审裁流程之内。

## Evidence Table
| # | Claim (abridged) | Source | Confidence |
|---|--------------------|--------|------------|
| 1 | All tested detection tools for AI-generated text are neither accurate nor reliable and are biased towards classifying ou… | arXiv:2306.15666 | high |
| 2 | About half of AI-generated texts that undergo obfuscation would be misattributed to humans. | arXiv:2306.15666 | high |
| 3 | Tools achieve 96% accuracy on human-written texts, but accuracy drops by 20% when those texts are machine-translated to … | arXiv:2306.15666 | medium |
| 4 | 13 of the 14 tested tools produced false negatives on AI-generated documents; only Turnitin classified all correctly, an… | arXiv:2306.15666 | medium |
| 5 | GLTR improves human detection of fake text from 54% to 72% without prior training | arXiv:1906.04043 | high |
| 6 | Without the GLTR interface, participants detected fake text at 54.2% accuracy, barely above chance | arXiv:1906.04043 | high |
| 7 | With the GLTR interface, detection performance improved to 72.3% | arXiv:1906.04043 | high |
| 8 | Generated text over-samples from a limited subset of the distribution where the model has high confidence | arXiv:1906.04043 | high |
| 9 | Seven widely-used GPT detectors achieved near-perfect accuracy on US 8th grade essays but misclassified over half of the… | arXiv:2304.02819 | high |
| 10 | Enhancing the linguistic diversity of non-native essays via ChatGPT substantially reduced their misclassification as AI-… | arXiv:2304.02819 | high |
| 11 | A simple second-round self-edit prompt applied to ChatGPT-3.5 reduced detector rates on AI-written college essays from 1… | arXiv:2304.02819 | high |
| 12 | In ICLR 2023 papers, authors from non-native English-speaking countries wrote abstracts with significantly lower perplex… | arXiv:2304.02819 | high |

## References
- [[1]](https://arxiv.org/abs/2306.15666) arXiv:2306.15666
- [[2]](https://arxiv.org/abs/1906.04043) arXiv:1906.04043
- [[3]](https://arxiv.org/abs/2304.02819) arXiv:2304.02819
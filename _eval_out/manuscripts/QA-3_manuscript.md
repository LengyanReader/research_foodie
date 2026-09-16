## Answer (EN)

The (arXiv:2306.15666) paper does **not** organize AI-generated-text detection into methodological "families." It evaluates detection by **tool**, not by method class. In §4.1–4.2 it constructs six test-case categories (01-Hum human-written, 02-MT human-written + machine translation to English, 03-AI/04-AI ChatGPT-generated, 05-ManEd ChatGPT + human manual edits, 06-Para ChatGPT + machine paraphrase) and tests 14 tools: Check For AI, Compilatio, Content at Scale, Crossplag, DetectGPT, Go Winston, GPT Zero, GPT-2 Output Detector Demo, OpenAI Text Classifier, PlagiarismCheck, Turnitin, Writeful GPT Detector, Writer, and ZeroGPT. The only functional distinction the paper makes is that "PlagiarismCheck and Turnitin are combined text similarity detectors and offer an additional functionality of determining the probability the text was written by an AI." The survey's aim is accuracy and error-type analysis of present-day commercial/free tools, not a taxonomy of detection approaches (arXiv:2306.15666).

## 中文速览

该调研（arXiv:2306.15666）并未按"检测方法家族/技术流派"进行分类，而是按**检测工具**逐一评测。它构建6类测试文档（人类手写、手写+机器翻译、ChatGPT生成、ChatGPT+人工修改、ChatGPT+机器改写等），测试14个工具（Check For AI、Compilatio、GPTZero、DetectGPT、Turnitin、PlagiarismCheck等）。文中唯一的功能性区分是：Turnitin 与 PlagiarismCheck 是"结合文本相似度检测，并额外提供AI文本概率判定"的工具。研究聚焦工具的准确性与错误类型，而非检测方法的分类体系。

## Source evidence

"The following 14 detection tools were tested: ● Check For AI ... ● ZeroGPT" (§4.2)

"PlagiarismCheck and Turnitin are combined text similarity detectors and offer an additional functionality of determining the probability the text was written by an AI" (§4.2)

(Cite: arXiv:2306.15666)
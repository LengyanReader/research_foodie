# Harness Index · Harness 索引

> Generated from `src/harness_factory/data/harnesses.json` — **do not edit by hand**; run `harness catalog --write` to regenerate.
> 由 `data/harnesses.json` 生成，**请勿手改**；用 `harness catalog --write` 重新生成。

**Updated:** 2026-10-19 · 201 entries · 12 classes · companion to `harness-catalog.md` (the prose taxonomy).

---

## How to use · 用法

```bash
harness catalog                       # list everything
harness catalog --class self-evolution
harness catalog --kind memory-system
harness catalog --module M5           # harnesses that exercise a core module
harness catalog --search voyager
harness catalog --tracked             # only entities also tracked in sources.json
harness catalog claude-code           # detail one entry
```

---

## Coding / software harnesses · 编码 harness  (12)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `opencode` | opencode · opencode | 终端编码 agent | M1, M6, M7 | https://github.com/sst/opencode |
| `claude-code` | Claude Code · Claude Code | 终端编码 agent | M1, M6, M7 | https://docs.anthropic.com/en/docs/claude-code · tracked:anthropic-claude-code |
| `codex-cli` | Codex CLI · Codex CLI | 终端编码 agent | M1, M6, M7 | https://github.com/openai/codex · tracked:openai-codex-cli |
| `gemini-cli` | Gemini CLI · Gemini CLI | 终端编码 agent | M1, M6, M7 | https://github.com/google-gemini/gemini-cli · tracked:google-gemini-cli |
| `openhands` | OpenHands · OpenHands | 终端编码 agent | M1, M6, M7, M8 | https://github.com/All-Hands-AI/OpenHands · tracked:openhands |
| `swe-agent` | SWE-agent · SWE-agent | 终端编码 agent | M1, M6, M7 | https://github.com/SWE-agent/SWE-agent · tracked:swe-agent |
| `aider` | Aider · Aider | 终端编码 agent | M1, M6, M7 | https://github.com/Aider-AI/aider |
| `cline` | Cline · Cline | IDE 侧 agent | M1, M6, M7, M8 | https://github.com/cline/cline |
| `roo-code` | Roo Code · Roo Code | IDE 侧 agent | M1, M6, M7 | https://github.com/RooCodeInc/Roo-Code |
| `goose` | goose · goose | 终端编码 agent | M1, M6, M7 | https://github.com/block/goose · tracked:goose |
| `crush` | crush · crush | 终端编码 agent | M1, M6, M7 | https://github.com/charmbracelet/crush |
| `pi-mono` | pi (pi-mono) · pi (pi-mono) | 终端编码 agent | M1, M6 | https://github.com/badlogic/pi-mono · tracked:pi-mono |

## Orchestration frameworks / agent SDKs · 编排框架与 SDK  (11)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `claude-agent-sdk` | Claude Agent SDK · Claude Agent SDK | agent SDK / 框架 | M6, M7, M8 | https://docs.anthropic.com/en/api/agent-sdk/overview · tracked:anthropic-agent-sdk |
| `openai-agents-sdk` | OpenAI Agents SDK · OpenAI Agents SDK | agent SDK / 框架 | M6, M7, M8 | https://github.com/openai/openai-agents-python · tracked:openai-agents-sdk |
| `openai-swarm` | Swarm · Swarm | agent SDK / 框架 | M6, M8 | https://github.com/openai/swarm · tracked:openai-swarm |
| `google-adk` | Agent Development Kit (ADK) · Agent Development Kit (ADK) | agent SDK / 框架 | M6, M7, M8 | https://github.com/google/adk-python · tracked:google-adk |
| `smolagents` | smolagents · smolagents | agent SDK / 框架 | M6 | https://github.com/huggingface/smolagents |
| `langgraph` | LangGraph · LangGraph | agent SDK / 框架 | M2, M6, M7, M8 | https://github.com/langchain-ai/langgraph · tracked:langchain |
| `autogen` | AutoGen · AutoGen | agent SDK / 框架 | M6, M8 | https://github.com/microsoft/autogen · tracked:autogen |
| `crewai` | CrewAI · CrewAI | agent SDK / 框架 | M6, M8 | https://github.com/crewAIInc/crewAI · tracked:crewai |
| `llama-stack` | Llama Stack · Llama Stack | agent SDK / 框架 | M6, M7 | https://github.com/meta-llama/llama-stack · tracked:meta-llama-stack |
| `a2a` | Agent2Agent (A2A) · Agent2Agent (A2A) | 协议 | M7, M8 | https://github.com/a2aproject/A2A · tracked:google-a2a |
| `dspy` | DSPy · DSPy | agent SDK / 框架 | M6 | https://github.com/stanfordnlp/dspy · tracked:dspy |

## Self-evolution methods · 自我演化方法  (15)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `adas` | ADAS / Meta Agent Search · ADAS / Meta Agent Search | 改自身脚手架 | M5, M7 | arXiv:2408.08435 (ICLR 2025) |
| `godel-agent` | Gödel Agent · Gödel Agent | 改自身脚手架 | M5, M7 | arXiv:2410.04444 / ACL 2025 |
| `sica` | Self-Improving Coding Agent (SICA) · 自改进编码 agent (SICA) | 改自身脚手架 | M5, M7 | arXiv:2504.15228 |
| `dgm` | Darwin Gödel Machine (DGM) · 达尔文哥德尔机 (DGM) | 改自身脚手架 | M5, M7 | arXiv:2505.22954 |
| `funsearch` | FunSearch · FunSearch | 进化式代码搜索 | M5 | Nature 624:545-552 (2023) |
| `alphaevolve` | AlphaEvolve · AlphaEvolve | 进化式代码搜索 | M5 | arXiv:2506.13131 |
| `openevolve` | OpenEvolve · OpenEvolve | 进化式代码搜索 | M5 | https://github.com/algorithmicsuperintelligence/openevolve |
| `codeevolve` | CodeEvolve · CodeEvolve | 进化式代码搜索 | M5 | arXiv:2510.14150 |
| `seal` | SEAL (Self-Adapting Language Models) · SEAL（自适配语言模型） | 改自身权重 | M5 | arXiv:2506.10943 (NeurIPS 2025) |
| `self-rewarding-lm` | Self-Rewarding Language Models · 自奖励语言模型 | 改自身权重 | M5 | arXiv:2401.10020 |
| `reflexion` | Reflexion · Reflexion | 推理期自我修正 | M3, M5 | arXiv:2303.11366 (NeurIPS 2023) |
| `self-refine` | Self-Refine · Self-Refine | 推理期自我修正 | M3 | arXiv:2303.17651 (NeurIPS 2023) |
| `voyager` | Voyager · Voyager | 技能沉淀 | M5, M6 | arXiv:2305.16291 |
| `hermes-agent` | Hermes Agent · Hermes Agent | 技能沉淀 | M2, M5, M6, M8 | https://github.com/NousResearch/hermes-agent · tracked:hermes-agent |
| `hermit-file-first` | hermit (file-first) · hermit（文件优先） | 改自身脚手架 | M2, M5, M7 | https://github.com/benschrauwen/hermit · tracked:hermit-file-first |

## Memory & persistence · 记忆与持久化  (5)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `memgpt-letta` | MemGPT / Letta · MemGPT / Letta | 记忆系统 | M2 | arXiv:2310.08560 |
| `mem0` | Mem0 · Mem0 | 记忆系统 | M2, M4 | arXiv:2504.19413 |
| `zep-graphiti` | Zep / Graphiti · Zep / Graphiti | 记忆系统 | M2, M4 | arXiv:2501.13956 |
| `a-mem` | A-MEM · A-MEM | 记忆系统 | M2 | Xu et al. 2025 |
| `letta-code` | Letta Code · Letta Code | 记忆系统 | M2, M5 | https://github.com/letta-ai/letta · tracked:letta |

## Skills ecosystems & protocols · 技能生态与协议  (4)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `anthropic-agent-skills` | Anthropic Agent Skills · Anthropic Agent Skills | 技能生态 | M1, M6 | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview |
| `mcp` | Model Context Protocol (MCP) · 模型上下文协议 (MCP) | 协议 | M1, M6 | https://modelcontextprotocol.io · tracked:anthropic-mcp |
| `agentskills-standard` | Agent Skills standard · Agent Skills 标准 | 技能生态 | M1, M6 | https://agentskills.io/specification · tracked:agentskills |
| `openclaw` | OpenClaw · OpenClaw | 技能生态 | M2, M6, M8 | https://github.com/openclaw/openclaw · tracked:openclaw |

## Evaluation harnesses · 评测 harness  (11)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `swe-bench` | SWE-bench · SWE-bench | 基准/评测器 | M3 | arXiv:2310.06770 |
| `terminal-bench` | Terminal-Bench · Terminal-Bench | 基准/评测器 | M3 | https://github.com/laude-institute/terminal-bench |
| `arc-agi` | ARC-AGI · ARC-AGI | 基准/评测器 | M3 | https://arcprize.org |
| `livecodebench` | LiveCodeBench · LiveCodeBench | 基准/评测器 | M3 | https://github.com/LiveCodeBench/LiveCodeBench |
| `polyglot` | SWE-bench Polyglot · SWE-bench Polyglot | 基准/评测器 | M3 | https://github.com/swe-bench/swe-bench.github.io |
| `locomo` | LoCoMo · LoCoMo | 基准/评测器 | M2, M3 | https://github.com/snap-research/locomo |
| `longmemeval` | LongMemEval · LongMemEval | 基准/评测器 | M2, M3 | https://github.com/xiaowu0162/LongMemEval |
| `lm-eval-harness` | LM Evaluation Harness · LM Evaluation Harness | eval-framework | M3 | https://github.com/EleutherAI/lm-evaluation-harness |
| `helm` | HELM · HELM | eval-framework | M3, M4 | https://github.com/stanford-crfm/helm |
| `simple-evals` | simple-evals · simple-evals | eval-framework | M3 | https://github.com/openai/simple-evals |
| `lighteval` | LightEval · LightEval | eval-framework | M3 | https://github.com/huggingface/lighteval |

## Surveys (orientation) · 综述导航  (5)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `survey-self-evolving-agents` | Self-Evolving Agents: What/When/How/Where · 自演化 agent 综述（What/When/How/Where） | 综述 | M0, M5 | arXiv:2507.21046 (TMLR 2026) |
| `survey-co-evolution` | Co-Evolution in Agentic Systems · agent 系统中的共同演化 | 综述 | M5, M8 | arXiv:2608.10299 |
| `survey-self-improvements` | Self-Improvements in Modern Agentic Systems · 现代 agent 系统的自我改进综述 | 综述 | M5 | arXiv:2607.13104 |
| `survey-agentic-rl` | Agentic RL for LLMs · LLM 的 agentic 强化学习综述 | 综述 | M5 | arXiv:2509.02547 |
| `survey-memory` | Memory in the Age of AI Agents · AI agent 时代的记忆综述 | 综述 | M2 | arXiv:2512.13564 |

## Safety of self-evolution · 自我演化安全  (2)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `saver` | SAVER (Safety in Self-Evolving Agents) · SAVER（自演化 agent 的安全） | 安全框架 | M0, M5, M8 | arXiv:2610.00093 |
| `misevolution` | Misevolution (Emergent Risks in Self-evolving LLM Agents) · Misevolution（自演化 agent 的涌现风险） | 安全框架 | M0, M5, M8 | arXiv:2509.26354 |

## Discovery / evidence & model search · 发现·证据与模型搜索  (5)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `elicit` | Elicit · Elicit | evidence-extractor | M1, M4 | https://elicit.com/ |
| `consensus` | Consensus · Consensus | evidence-synthesizer | M1, M4 | https://consensus.app/ |
| `connected-papers` | Connected Papers · Connected Papers | graph-explorer | M1, M4 | https://www.connectedpapers.com/ |
| `researchrabbit` | ResearchRabbit · ResearchRabbit | graph-explorer | M1, M4 | https://www.researchrabbit.ai/ |
| `paperswithcode` | PapersWithCode · PapersWithCode | index | M1, M4 | https://paperswithcode.com/ |

## Reading, acquisition & distillation · 读物阅读·获取与提炼  (20)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `project-gutenberg` | Project Gutenberg · Project Gutenberg | 原文获取 | M4, M6 | https://www.gutenberg.org/ · tracked:gutenberg |
| `standard-ebooks` | Standard Ebooks · Standard Ebooks | 原文获取 | M4, M6 | https://standardebooks.org/ · tracked:standard-ebooks |
| `internet-archive` | Internet Archive · Internet Archive | 原文获取 | M4, M6 | https://archive.org/ · tracked:internet-archive |
| `open-library` | Open Library · Open Library | 原文获取 | M4, M6 | https://openlibrary.org/ · tracked:open-library |
| `hathitrust` | HathiTrust · HathiTrust | 原文获取 | M4, M6 | https://www.hathitrust.org/ · tracked:hathitrust |
| `doab` | DOAB · DOAB | 原文获取 | M4, M6 | https://www.doabooks.org/ · tracked:doab |
| `unpaywall` | Unpaywall · Unpaywall | 原文获取 | M4, M6 | https://unpaywall.org/ |
| `arxiv` | arXiv · arXiv | 原文获取 | M4, M6 | https://arxiv.org/ |
| `google-books` | Google Books · Google Books | 原文获取 | M4 | https://books.google.com/ |
| `pandoc` | Pandoc · Pandoc | 文档解析 / OCR | M6 | https://pandoc.org/ |
| `calibre` | Calibre · Calibre | 文档解析 / OCR | M6 | https://calibre-ebook.com/ |
| `mineru` | MinerU · MinerU | 文档解析 / OCR | M6 | https://github.com/opendatalab/MinerU |
| `grobid` | GROBID · GROBID | 文档解析 / OCR | M6 | https://github.com/kermitt2/grobid |
| `docling` | Docling · Docling | 文档解析 / OCR | M6 | https://github.com/DS4SD/docling |
| `marker` | Marker · Marker | 文档解析 / OCR | M6 | https://github.com/VikParuchuri/marker |
| `tesseract` | Tesseract OCR · Tesseract | 文档解析 / OCR | M6 | https://github.com/tesseract-ocr/tesseract |
| `hypothesis` | Hypothesis · Hypothesis | 标注与批注 | M4, M6 | https://web.hypothes.is/ |
| `zotero` | Zotero · Zotero | 标注与批注 | M4, M6 | https://www.zotero.org/ |
| `readwise` | Readwise · Readwise | 标注与批注 | M4, M6 | https://readwise.io/ |
| `notebooklm` | NotebookLM · NotebookLM | 提炼与综述 | M1, M4 | https://notebooklm.google/ |

## Deep research — search, retrieval & synthesis · 深度调研·检索与综合  (43)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `openai-deep-research` | OpenAI Deep Research · OpenAI Deep Research | 深研代理 / 产品 | M1, M4 | https://openai.com/index/introducing-deep-research/ · tracked:openai-deep-research |
| `gemini-deep-research` | Gemini Deep Research · Gemini Deep Research | 深研代理 / 产品 | M1, M4 | https://gemini.google/overview/deep-research/ · tracked:gemini-deep-research |
| `claude-research` | Claude Research · Claude Research | 深研代理 / 产品 | M1, M3, M4 | https://www.anthropic.com/news/research · tracked:claude-research |
| `perplexity` | Perplexity · Perplexity | 深研代理 / 产品 | M1, M4 | https://www.perplexity.ai/ · tracked:perplexity |
| `you-com` | You.com · You.com | 深研代理 / 产品 | M1, M4 | https://you.com/ · tracked:you-com |
| `grok-deepsearch` | Grok DeepSearch · Grok DeepSearch | 深研代理 / 产品 | M1, M4 | https://x.ai/ · tracked:grok-deepsearch |
| `gpt-researcher` | GPT Researcher · GPT Researcher | 深研代理 / 产品 | M1, M4 | https://github.com/assafelovic/gpt-researcher · tracked:gpt-researcher |
| `open-deep-research` | open-deep-research · open-deep-research | 深研代理 / 产品 | M1, M4 | https://github.com/dzhng/deep-research · tracked:open-deep-research |
| `storm` | STORM · STORM | 深研代理 / 产品 | M1, M4 | https://github.com/stanford-oval/storm · tracked:storm |
| `jina-deepsearch` | Jina DeepSearch · Jina DeepSearch | 深研代理 / 产品 | M1, M4 | https://github.com/jina-ai/node-DeepResearch · tracked:jina |
| `exa` | Exa · Exa | 网页检索 API / 引擎 | M6 | https://exa.ai/ · tracked:exa |
| `tavily` | Tavily · Tavily | 网页检索 API / 引擎 | M6 | https://tavily.com/ · tracked:tavily |
| `brave-search` | Brave Search API · Brave Search API | 网页检索 API / 引擎 | M6 | https://brave.com/search/api/ · tracked:brave-search |
| `searxng` | SearXNG · SearXNG | 网页检索 API / 引擎 | M6 | https://github.com/searxng/searxng · tracked:searxng |
| `serpapi` | SerpApi · SerpApi | 网页检索 API / 引擎 | M6 | https://serpapi.com/ · tracked:serpapi |
| `semantic-scholar` | Semantic Scholar · Semantic Scholar | 学术检索 API | M1, M4 | https://www.semanticscholar.org/product/api · tracked:semantic-scholar |
| `crossref` | Crossref · Crossref | 学术检索 API | M1, M4 | https://www.crossref.org/ · tracked:crossref |
| `openalex` | OpenAlex · OpenAlex | 学术检索 API | M1, M4 | https://openalex.org/ · tracked:openalex |
| `europepmc` | Europe PMC · Europe PMC | 学术检索 API | M1, M4 | https://europepmc.org/ · tracked:europepmc |
| `core` | CORE · CORE | 学术检索 API | M1, M4 | https://core.ac.uk/ · tracked:core |
| `scite` | Scite · Scite | 学术检索 API | M1, M4 | https://scite.ai/ · tracked:scite |
| `litmaps` | Litmaps · Litmaps | graph-explorer | M1, M4 | https://www.litmaps.com/ · tracked:litmaps |
| `inciteful` | Inciteful · Inciteful | graph-explorer | M1, M4 | https://inciteful.xyz/ · tracked:inciteful |
| `llamaindex` | LlamaIndex · LlamaIndex | 检索增强 / 向量 | M1, M2, M6 | https://github.com/run-llama/llama_index · tracked:llamaindex |
| `langchain` | LangChain · LangChain | 检索增强 / 向量 | M1, M6 | https://github.com/langchain-ai/langchain · tracked:langchain |
| `faiss` | FAISS · FAISS | 检索增强 / 向量 | M1, M2 | https://github.com/facebookresearch/faiss · tracked:faiss |
| `qdrant` | Qdrant · Qdrant | 检索增强 / 向量 | M1, M2 | https://github.com/qdrant/qdrant · tracked:qdrant |
| `chroma` | Chroma · Chroma | 检索增强 / 向量 | M1, M2 | https://github.com/chroma-core/chroma · tracked:chroma |
| `sentence-transformers` | sentence-transformers · sentence-transformers | 检索增强 / 向量 | M1, M6 | https://github.com/UKPLab/sentence-transformers · tracked:sentence-transformers |
| `bm25s` | bm25s · bm25s | 检索增强 / 向量 | M1, M6 | https://github.com/xhluca/bm25s · tracked:bm25s |
| `trafilatura` | Trafilatura · Trafilatura | 抓取 / 正文提取 | M6 | https://github.com/adbar/trafilatura · tracked:trafilatura |
| `readability` | Readability · Readability | 抓取 / 正文提取 | M6 | https://github.com/mozilla/readability · tracked:readability |
| `jina-reader` | Jina Reader · Jina Reader | 抓取 / 正文提取 | M6 | https://github.com/jina-ai/reader · tracked:jina-reader |
| `firecrawl` | Firecrawl · Firecrawl | 抓取 / 正文提取 | M6 | https://github.com/mendableai/firecrawl · tracked:firecrawl |
| `crawl4ai` | Crawl4AI · Crawl4AI | 抓取 / 正文提取 | M6 | https://github.com/unclecode/crawl4ai · tracked:crawl4ai |
| `rayyan` | Rayyan · Rayyan | 筛选 / 系统综述 | M3, M4 | https://www.rayyan.ai/ · tracked:rayyan |
| `covidence` | Covidence · Covidence | 筛选 / 系统综述 | M3, M4 | https://www.covidence.org/ · tracked:covidence |
| `asreview` | ASReview · ASReview | 筛选 / 系统综述 | M3, M4 | https://github.com/asreview/asreview · tracked:asreview |
| `gaia` | GAIA · GAIA | 调研质量评测 | M3 | https://huggingface.co/datasets/gaia-benchmark/GAIA · tracked:gaia |
| `browsecomp` | BrowseComp · BrowseComp | 调研质量评测 | M3 | https://openai.com/index/browsecomp/ · tracked:browsecomp |
| `hle` | Humanity’s Last Exam · Humanity’s Last Exam | 调研质量评测 | M3 | https://lastexam.ai/ · tracked:hle |
| `frames` | FRAMES · FRAMES | 调研质量评测 | M3 | https://huggingface.co/datasets/google/frames-benchmark · tracked:frames |
| `deepresearch-bench` | DeepResearch Bench · DeepResearch Bench | 调研质量评测 | M3 | https://github.com/Ayanami0730/deep_research_bench · tracked:deepresearch-bench |

## Scientific & formal instruments (evidence tools) · 科学仪器与形式工具（证据工具）  (68)

| id | name | kind | core modules | source |
|---|---|---|---|---|
| `lean4` | Lean 4 · Lean 4 | 证明助手（交互式定理证明器） | M3, M4, M6 | https://lean-lang.org/ |
| `mathlib` | mathlib4 · mathlib4 | 形式化数学库 | M3, M4 | https://github.com/leanprover-community/mathlib4 |
| `rocq` | The Rocq Prover · Rocq 证明器（原 Coq） | 证明助手（交互式定理证明器） | M3, M4, M6 | https://rocq-prover.org/ |
| `isabelle` | Isabelle · Isabelle | 证明助手（交互式定理证明器） | M3, M4, M6 | https://isabelle.in.tum.de/ |
| `agda` | Agda · Agda | 证明助手（交互式定理证明器） | M3, M4, M6 | https://agda.readthedocs.io/ |
| `dafny` | Dafny · Dafny | 证明助手（交互式定理证明器） | M3, M4, M6 | https://dafny.org/ |
| `z3` | Z3 · Z3 | SMT 求解器 | M3, M6 | https://github.com/Z3Prover/z3 |
| `cvc5` | cvc5 · cvc5 | SMT 求解器 | M3, M6 | https://cvc5.github.io/ |
| `tla-plus` | TLA+ · TLA+ | 模型检验与规约分析器 | M2, M3, M6 | https://lamport.azurewebsites.net/tla/tla.html |
| `alloy` | Alloy · Alloy | 模型检验与规约分析器 | M2, M3, M6 | https://alloytools.org/ |
| `pint` | Pint · Pint | 量纲与不确定度库 | M3, M6 | https://pint.readthedocs.io/ |
| `uncertainties` | uncertainties · uncertainties | 量纲与不确定度库 | M3, M6 | https://pypi.org/project/uncertainties/ |
| `rdkit` | RDKit · RDKit | 化学与生物信息工具包 | M3, M4, M6 | https://www.rdkit.org/ |
| `biopython` | Biopython · Biopython | 化学与生物信息工具包 | M3, M4, M6 | https://biopython.org/ |
| `rcsb-pdb` | RCSB PDB · RCSB PDB | 生物大分子参考数据库 | M3, M4 | https://www.rcsb.org/ |
| `uniprot` | UniProt · UniProt | 生物大分子参考数据库 | M3, M4 | https://www.uniprot.org/ |
| `universal-dependencies` | Universal Dependencies · Universal Dependencies | 语料库与树库资源 | M1, M4, M6 | https://universaldependencies.org/ |
| `inception` | INCEpTION · INCEpTION | 标注平台 | M3, M4, M8 | https://inception-project.github.io/ |
| `elan` | ELAN · ELAN | 标注平台 | M3, M4, M8 | https://archive.mpi.nl/tla/elan |
| `psychopy` | PsychoPy · PsychoPy | 实验运行时与范式构建器 | M3, M6 | https://psychopy.org/ |
| `jspsych` | jsPsych · jsPsych | 实验运行时与范式构建器 | M3, M6 | https://www.jspsych.org/ |
| `osf` | OSF (Open Science Framework) · OSF 开放科学框架 | 预注册归档与服务 | M3, M7 | https://osf.io/ |
| `statsmodels` | statsmodels · statsmodels | 统计建模工具 | M3 | https://www.statsmodels.org/ |
| `lme4` | lme4 · lme4 | 统计建模工具 | M3 | https://cran.r-project.org/package=lme4 |
| `stan` | Stan · Stan | 统计建模工具 | M3 | https://mc-stan.org/ |
| `snakemake` | Snakemake · Snakemake | 可复现流水线引擎 | M2, M4, M6 | https://snakemake.readthedocs.io/ |
| `nextflow` | Nextflow · Nextflow | 可复现流水线引擎 | M2, M4, M6 | https://www.nextflow.io/ |
| `sagemath` | SageMath · SageMath | 计算机代数系统 | M3, M6 | https://www.sagemath.org/ |
| `singular` | Singular · Singular | 计算机代数系统 | M3, M6 | https://www.singular.uni-kl.de/ |
| `macaulay2` | Macaulay2 · Macaulay2 | 计算机代数系统 | M3, M6 | https://macaulay2.com/ |
| `gap` | GAP · GAP | 计算机代数系统 | M3, M6 | https://www.gap-system.org/ |
| `pari-gp` | PARI/GP · PARI/GP | 计算机代数系统 | M3, M6 | https://pari.math.u-bordeaux.fr/ |
| `oscar` | OSCAR · OSCAR | 计算机代数系统 | M3, M6 | https://www.oscar-system.org/ |
| `sympy` | SymPy · SymPy | 计算机代数系统 | M3, M6 | https://www.sympy.org/ |
| `cadical` | CaDiCaL · CaDiCaL | SAT 求解器 | M3, M6 | https://github.com/arminbiere/cadical |
| `mathcomp` | Mathematical Components · Mathematical Components | 形式化数学库 | M3, M4, M6 | https://math-comp.github.io/ |
| `metamath` | Metamath · Metamath | 证明助手（交互式定理证明器） | M3, M4 | https://us.metamath.org/ |
| `cgal` | CGAL · CGAL | 计算几何/拓扑工具 | M3, M6 | https://www.cgal.org/ |
| `gudhi` | GUDHI · GUDHI | 计算几何/拓扑工具 | M3, M6 | https://gudhi.inria.fr/ |
| `regina` | Regina · Regina | 计算几何/拓扑工具 | M3, M6 | https://regina-normal.github.io/ |
| `snappy` | SnapPy · SnapPy | 计算几何/拓扑工具 | M3, M6 | https://snappy.computop.org/ |
| `polymake` | polymake · polymake | 计算几何/拓扑工具 | M3, M6 | https://polymake.org/ |
| `r-project` | R · R | 统计建模工具 | M3, M4 | https://www.r-project.org/ |
| `pymc` | PyMC · PyMC | 统计建模工具 | M3, M4 | https://www.pymc.io/ |
| `numpyro` | NumPyro · NumPyro | 统计建模工具 | M3, M4 | https://num.pyro.ai/ |
| `arviz` | ArviZ · ArviZ | 统计建模工具 | M3, M4 | https://python.arviz.org/ |
| `brms` | brms · brms | 统计建模工具 | M3, M4 | https://paulbuerkner.com/software/ |
| `r-inla` | R-INLA · R-INLA | 统计建模工具 | M3, M4 | https://www.r-inla.org/ |
| `emcee` | emcee · emcee | 统计建模工具 | M3, M4 | https://emcee.readthedocs.io/ |
| `dowhy` | DoWhy · DoWhy | 因果推断工具 | M3, M4 | https://www.pywhy.org/dowhy/ |
| `protege` | Protege · Protégé | 本体编辑器 / RDF 工具 | M4, M6 | https://protegeproject.github.io/protege/ |
| `rdflib` | RDFLib · RDFLib | 本体编辑器 / RDF 工具 | M4, M6 | https://rdflib.readthedocs.io/en/stable/ |
| `apache-jena` | Apache Jena · Apache Jena | 本体编辑器 / RDF 工具 | M4, M6 | https://jena.apache.org/documentation/shacl/ |
| `neo4j` | Neo4j · Neo4j | 图数据库 / 三元组库 | M4, M6 | https://neo4j.com/docs/cypher-manual/current/ |
| `microsoft-graphrag` | Microsoft GraphRAG · Microsoft GraphRAG | 知识图谱构建 | M3, M4, M6 | https://github.com/microsoft/graphrag |
| `openrefine` | OpenRefine · OpenRefine | 实体归一 / 记录链接 | M4, M6 | https://openrefine.org/docs/technical-reference/reconciliation-api |
| `splink` | Splink · Splink | 实体归一 / 记录链接 | M4, M6 | https://moj-analytical-services.github.io/splink/ |
| `dedupe` | Dedupe · Dedupe | 实体归一 / 记录链接 | M4, M6 | https://docs.dedupe.io/en/latest/ |
| `pleiades` | Pleiades · Pleiades | 地名权威表 | M4 | https://pleiades.stoa.org/ |
| `geonames` | GeoNames · GeoNames | 地名权威表 | M4 | https://www.geonames.org/export/web-services.html |
| `getty-tgn` | Getty TGN · 盖蒂地名表 TGN | 地名权威表 | M4 | https://www.getty.edu/research/tools/vocabularies/tgn/ |
| `transkribus` | Transkribus · Transkribus | 手写文本识别 | M3, M4 | https://www.transkribus.org/ |
| `escriptorium` | eScriptorium · eScriptorium | 手写文本识别 | M3, M4 | https://escriptorium.readthedocs.io/en/latest/ |
| `vale` | Vale · Vale | prose-linter | M3, M4 | https://vale.sh/ |
| `languagetool` | LanguageTool · LanguageTool | prose-linter | M3, M4 | https://languagetool.org/ |
| `textstat` | textstat · textstat | readability-metric | M4 | https://github.com/textstat/textstat |
| `hermit` | HermiT · HermiT | 本体编辑器 / RDF 工具 | M3, M4 | http://www.hermit-reasoner.com/ |
| `elk` | ELK · ELK | 本体编辑器 / RDF 工具 | M3, M4 | https://github.com/liveontologies/elk-reasoner |

---

## Cross-links · 交叉链接

- Prose taxonomy & design lessons: [`harness-catalog.md`](harness-catalog.md).
- Tracked feeds for these entities: `data/sources.json` (`harness sources`).
- Core modules M0–M8: [`../core/00-index.md`](../core/00-index.md).

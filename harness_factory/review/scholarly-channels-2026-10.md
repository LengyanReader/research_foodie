# Scholarly discovery & citation channels · 学术检索与引用渠道

> Where to look, what is first-party vs aggregator, and what actually answers from a CLI.
> 去哪查、谁是一手、命令行实测哪些可达。
**Updated:** 2026-10-19

## 0. Method, legend, and what "first-party" means

- **How tested.** Every row was fetched on **2026-10-19** with `python` + `urllib`, a Firefox 131 User-Agent, TLS verification disabled, 20–30 s timeout, from this Windows host. Statuses are **as observed**, not from documentation. `L` = landing page; `A` = API endpoint.
- **Legend.** `200` usable · `200*` HTTP 200 but the body is a bot/consent gate, not content · `403/405/429/404` HTTP error · `Err` transport/SSL/timeout · `—` no public API found (none invented).
- **First-party (1P)** = the party that produces or is the authoritative registry of the artifact (publisher, preprint server, DOI agency, identifier registry, the journal itself). **Aggregator/index (agg)** = a discovery layer over other parties' artifacts. Most of the list is an aggregator; a hit there is a *lead*, never the source.
- **"High quality" claims** below come only from what the service's own landing/API page states or from structural facts visible on it — no third-party rankings, no invented endpoints.
- Cross-reference: repo `data/sources.json` (`outlets`, `tools`) already carries arXiv, Google Scholar, OpenAlex, Semantic Scholar, Crossref, Europe PMC, CORE, scite, Litmaps, Inciteful, DOAJ, ORCID, Retraction Watch, dblp, ACM DL, IEEE Xplore, JMLR, RePEc, SSRN, ERIC, PhilPapers, JSTOR, Project MUSE, PubMed, PMC.

---

## 1. Cross-domain discovery & indexes

| Channel | One line | URL | API | Kind | Fetched 2026-10-19 |
|---|---|---|---|---|---|
| Google Scholar | Broadest scholarly web index, incl. grey literature | https://scholar.google.com/ | — | agg | L 200, search 200 (brief listed it blocked; this host answered) |
| Semantic Scholar | Paper graph + TLDRs, citation contexts, embeddings | https://www.semanticscholar.org/ | https://api.semanticscholar.org/graph/v1/ | agg | L 200 · A 429 (key/rate-limit) |
| OpenAlex | Open catalog of works · authors · venues · institutions | https://openalex.org/ | https://api.openalex.org/works | agg (open) | L 200 · A 200 |
| CORE | Open-access full-text aggregator across repositories | https://core.ac.uk/ | https://api.core.ac.uk/v3/search/works | agg | L 200 · A Err (timeout; key) |
| BASE | Huge OA meta-index harvested from repositories | https://www.base-search.net/ | https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi | agg | L 200 · A 200 (body: "Access denied for IP") |
| OpenAIRE | EC-driven OA research graph + CRIS metadata | https://www.openaire.eu/ | https://api.openaire.eu/search/publications | agg | L 200 · A 200 (XML) |
| Lens.org | Scholarly works **and** patents in one graph | https://www.lens.org/ | https://api.lens.org/scholarly/search | agg | L 200 · A 401 (token) |
| Dimensions | Works, grants, patents, clinical trials | https://www.dimensions.ai/ | (api.dimensions.ai gated) | agg | L 200 · A not verified |
| Scilit | MDPI-run cross-domain literature index | https://www.scilit.com/ | — | agg | L 200 |
| Scinapse | Cross-domain paper search (Pluto) | https://www.scinapse.io/ | — | agg | L 200 |
| Connected Papers | Citation-graph explorer from a seed paper | https://www.connectedpapers.com/ | (graph route serves SPA HTML) | agg | L 200 |
| ResearchRabbit | Citation-network discovery + alerts | https://www.researchrabbit.ai/ | — | agg | L 200 |
| Litmaps | Citation maps over time | https://www.litmaps.com/ | — | agg | L 200 |
| Inciteful | Free citation-graph tool | https://inciteful.xyz/ | — | agg | L 200 → incitefulmed.com/academic/ |
| Elicit | LLM-assisted literature review & screening | https://elicit.com/ | — | agg | L 200 |
| Consensus | LLM "what does the research say" search | https://consensus.app/ | — | agg | L 200 |
| scite | Citation statements (supporting/contrasting) | https://scite.ai/ | https://api.scite.ai/ (token) | agg | L 200 · A 200 root |
| SciSpace | LLM literature assistant | https://scispace.com/ | — | agg | L 202 |

*(Google Scholar, Semantic Scholar, OpenAlex, CORE, scite, Litmaps, Inciteful are already catalogued in `sources.json`.)*

## 2. Metadata, registry & DOI infrastructure

| Channel | One line | URL | API | Kind | Fetched 2026-10-19 |
|---|---|---|---|---|---|
| Crossref | DOI registration agency for scholarly content; metadata REST API | https://www.crossref.org/ | https://api.crossref.org/works | **1P registry** | L 200 · A 200 |
| Crossref retraction data | Retraction/update notices queryable by filter | — | https://api.crossref.org/works?filter=update-type:retraction | **1P** | A 200 |
| DataCite | DOI agency for data, software, preprints | https://datacite.org/ | https://api.datacite.org/dois | **1P registry** | L Err (SSL) · A 200 |
| ORCID | Researcher identifier registry | https://orcid.org/ | https://pub.orcid.org/v3.0/expanded-search/ | **1P registry** | L 200 · A 200 |
| ROR | Research-organization registry with stable ids | https://ror.org/ | https://api.ror.org/organizations | **1P registry** | L 429 (Vercel gate) · A 200 |
| ISSN portal | Serial (journal) identity registry | https://portal.issn.org/ | https://portal.issn.org/resource/ISSN/2049-3630?format=json | **1P registry** | L 200 · A 200* (Anubis bot gate) |
| Retraction Watch | Retraction & integrity tracking; DB now mirrored via Crossref | https://retractionwatch.com/ | (data: Crossref filter above) | media | L 200 · guide 200 |
| PubPeer | Post-publication peer-comment threads | https://pubpeer.com/ | /api/v2, /v3 | qa (1P for its comments) | L 200 · A 404/405 (no public GET) |

## 3. Discipline-specific

| Channel | One line | URL | API | Kind | Fetched 2026-10-19 |
|---|---|---|---|---|---|
| PubMed | NLM MEDLINE biomedical index | https://pubmed.ncbi.nlm.nih.gov/ | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi | index (1P NLM) | L 403 · A 200 |
| PubMed Central | NIH free full-text biomedical archive | https://pmc.ncbi.nlm.nih.gov/ | eutils `db=pmc` | repository | L 200 |
| Europe PMC | Life-science literature + full text + citations | https://europepmc.org/ | https://www.ebi.ac.uk/europepmc/webservices/rest/search | index | L 403 · A 200 |
| DOAJ | Vetted open-access journals index | https://doaj.org/ | https://doaj.org/api/search/articles/{query} | index | L 403 · A 200 |
| dblp | Curated CS bibliography (author/venue metadata) | https://dblp.org/ | https://dblp.org/search/publ/api | index | L 202 · A 202 |
| ACL Anthology | ACL/EMNLP/NAACL proceedings, fully open | https://aclanthology.org/ | (bulk BibTeX/RDF) | **1P** for ACL venues | L 200 |
| PMLR | Proceedings of Machine Learning Research | https://proceedings.mlr.press/ | — | publisher | L 200 |
| JMLR | Journal of Machine Learning Research | https://jmlr.org/ | — | journal | L 200 |
| OpenReview | Host for ICLR/NeurIPS, public reviews | https://openreview.net/ | https://api2.openreview.net/ | portal | L 200 · A groups 200, notes 403 (challenge) |
| arXiv | Canonical multi-field preprint server | https://arxiv.org/ | https://export.arxiv.org/api/query | **1P preprint** | L 200 · A 200 |
| bioRxiv | Life-science preprints (CSHL) | https://www.biorxiv.org/ | https://api.biorxiv.org/details/biorxiv/{from}/{to} | preprint | L 200 · A 200 |
| medRxiv | Health-science preprints | https://www.medrxiv.org/ | https://api.biorxiv.org/details/medrxiv/{from}/{to} | preprint | L 200 · A 200 |
| SSRN | Preprints/postprints, econ·law·social science | https://www.ssrn.com/ | — | repository | L 403 |
| RePEc / IDEAS | Volunteer economics-paper network | https://repec.org/ · https://ideas.repec.org/ | — | index | http 200 · https Err (SSL) · IDEAS 200 |
| ERIC | US education-research index (IES) | https://eric.ed.gov/ | https://api.ies.ed.gov/eric/ | index | L 200 · A 200 |
| PhilPapers | Philosophy bibliography & repository | https://philpapers.org/ | — | index | L 403 |
| JSTOR | Digitised journals & books (humanities/SS) | https://www.jstor.org/ | — | repository | L 200 (gated) |
| Project MUSE | University-press journals & books | https://muse.jhu.edu/ | — | publisher | L 200 |
| SciELO | Latin-American/Iberian/African OA platform | https://www.scielo.org/ | — | repository | L 200 |
| Redalyc | Ibero-American OA journals | https://www.redalyc.org/ | — | repository | L 200 |
| HAL | French multidisciplinary OA repository | https://hal.science/ | https://api.archives-ouvertes.fr/search/ | repository | L 200 · A 200 |
| CNKI | China academic journals (licensed) | https://www.cnki.net/ | — | portal | L 200 |
| Wanfang | China journals & dissertations | https://www.wanfangdata.com.cn/ | — | portal | L 200 |
| Airiti | Taiwan academic library | https://www.airitilibrary.com/ | — | portal | Err (SSL) |
| CiNii Research | Japan scholarly index (NII) | https://cir.nii.ac.jp/ | https://cir.nii.ac.jp/opensearch/all | index | L 200 · A 200 |
| J-STAGE | Japan platform of sci/tech journals | https://www.jstage.jst.go.jp/ | — | publisher | L 200 |
| KISS | Korean studies information system | https://kiss.kstudy.com/ | — | index | L 200 (gated) |
| Shodhganga | Indian PhD theses repository | https://shodhganga.inflibnet.ac.in/ | — | repository | L 200* (Anubis gate) |
| EThOS | UK doctoral theses (British Library; now Hyku) | https://ethos.bl.uk/ | — | repository | L 200 |
| ProQuest | Dissertations & licensed databases | https://www.proquest.com/ | — | portal | L 302 |

## 4. Publishers & platforms — the version of record

| Channel | One line | URL | API | Kind | Fetched 2026-10-19 |
|---|---|---|---|---|---|
| ACM Digital Library | ACM journals & proceedings | https://dl.acm.org/ | — | publisher | L 403 |
| IEEE Xplore | IEEE journals, conferences, standards | https://ieeexplore.ieee.org/ | — | publisher | L 200 |
| SpringerLink | Springer/Nature journals & books | https://link.springer.com/ | — | publisher | L 200 |
| ScienceDirect | Elsevier journals | https://www.sciencedirect.com/ | — | publisher | L 403 |
| Wiley Online Library | Wiley journals | https://onlinelibrary.wiley.com/ | — | publisher | L 403 |
| Taylor & Francis | T&F journals | https://www.tandfonline.com/ | — | publisher | L 403 |
| SAGE Journals | SAGE journals | https://journals.sagepub.com/ | — | publisher | Err (SSL) |
| Oxford Academic | Oxford University Press | https://academic.oup.com/ | — | publisher | L 403 |
| Cambridge Core | Cambridge University Press | https://www.cambridge.org/core | — | publisher | L 200 |
| PLOS | Open-access journals + full search API | https://plos.org/ | https://api.plos.org/search | publisher | L 200 · A 200 |
| Frontiers | Open-access journals | https://www.frontiersin.org/ | — | publisher | L 200 |
| MDPI | Open-access journals/publisher | https://www.mdpi.com/ | — | publisher | L 200 |
| De Gruyter Brill | Humanities & social-science books/journals | https://www.degruyter.com/ | — | publisher | L 200 (→ degruyterbrill.com) |
| Brill | Humanities & social-science publisher | https://brill.com/ | — | publisher | L 405 (WAF "Human Verification") |

## 5. AI/ML venue indices

| Channel | One line | URL | API | Kind | Fetched 2026-10-19 |
|---|---|---|---|---|---|
| NeurIPS proceedings | Open archive of NeurIPS papers | https://proceedings.neurips.cc/ | — | publisher | L 200 |
| ICML | Conference site (papers via PMLR) | https://icml.cc/ | — | index | L 200 |
| ICLR | Conference site (papers via OpenReview) | https://iclr.cc/ | — | index | L 200 |
| AAAI | AAAI proceedings (OJS) | https://ojs.aaai.org/index.php/AAAI | — | publisher | L 200 |
| IJCAI | IJCAI proceedings | https://www.ijcai.org/proceedings/ | — | publisher | L 200 |
| ACL / EMNLP / NAACL | All papers, free, at the ACL Anthology | https://aclanthology.org/ | (bulk BibTeX/RDF) | publisher | L 200 |
| TMLR | Transactions on ML Research (open review) | https://jmlr.org/tmlr/ | — | journal | L 200 |

## 6. How to use without laundering · 不洗稿地使用

1. **Aggregator = discovery, never the source.** Scholar/Semantic Scholar/OpenAlex/CORE/BASE/Dimensions/Lens are indexes. Take the *identifier* (`10.…` DOI, arXiv id, ISBN, `OpenAlex ID`), then fetch the artifact at the producing party (publisher page or preprint server). 聚合器只做发现；引用必须落到**产出方**。
2. **Follow to the version of record.** Prefer the published article; if you must cite a preprint, cite its **stable id** (arXiv `arXiv:XXXX.XXXXX`, bioRxiv/medRxiv DOI) and say it is a preprint. Never cite two conflated versions.
3. **Check retraction/update status** before relying on any claim — Crossref `filter=update-type:retraction` or the Retraction Watch database; note the notice date. 先查撤稿/更正状态。
4. **Comment/QA layers (PubPeer, Retraction Watch news, blogs) are leads**, not evidence: cite the notice or the article, not the thread.
5. **A search result count is never evidence.** "N results on Google Scholar" measures the index, not the literature. Same for citation counts from any aggregator — they are index artifacts and differ by source; if you use one, name the source and date.
6. **Registries don't vouch for quality.** ORCID/ROR/ISSN/DataCite assert identity, not merit; DOI resolution asserts persistence, not peer review.
7. **Record what you actually opened:** first-party URL + identifier + access date (this repo's rule); an abstract or an LLM-summary is not the study.

## 7. Observed blocked / gated on 2026-10-19 (not evidence of unusability)

`403` gateways: pubmed.ncbi.nlm.nih.gov, europepmc.org, doaj.org, philpapers.org, dl.acm.org, sciencedirect.com, onlinelibrary.wiley.com, tandfonline.com, academic.oup.com, ssrn.com. `429`: ror.org (Vercel), api.semanticscholar.org without a key. `SSL Err`: datacite.org, journals.sagepub.com, airitilibrary.com, https repec.org. Bot-gated `200*`: portal.issn.org API, shodhganga.inflibnet.ac.in, base-search.net/about, brill.com (WAF). Timeout: api.core.ac.uk. Network-gated API: api.base-search.net (IP registration required). These are **environment-specific**; the underlying services are live and their APIs (where listed as `A 200`) did answer.

---

## 中文

**这是什么。** 一份「去哪查、谁是一手、命令行实测哪些可达」的学术检索与引用渠道清单。全部条目于 **2026-10-19** 用 `python`+`urllib`、Firefox UA 实测（关闭 TLS 校验，20–30 秒超时），状态为**实测值**而非文档值；`L`=落地页，`A`=API。`200` 可用 · `200*` 返回 200 但页面是机器人/同意门（非内容）· `403/405/429/404` 出错 · `Err` 传输/SSL/超时 · `—` 未找到公开 API（**未编造**任何端点）。

**一手 vs 聚合。** **一手（1P）**＝产出或权威登记该成果的主体（出版商、预印本服务器、DOI 机构、标识登记库、期刊本体）；**聚合/索引（agg）**＝在他人成果之上的发现层。本清单绝大多数是聚合器——**聚合器命中只是线索，绝不是引用源**。

**五组渠道（见上表）。**
1. **跨域发现/索引**（23 条）：Semantic Scholar、OpenAlex、CORE、BASE、OpenAIRE、Lens、Dimensions、Scilit、Scinapse、Connected Papers、ResearchRabbit、Litmaps、Inciteful、Elicit、Consensus、scite、SciSpace、Google Scholar。实测 **OpenAlex（L/A 均 200）、scite API 根 200、OpenAIRE API 200** 最稳；CORE API 超时、BASE API 返回「IP 拒绝」（需登记）、Lens API 401（需 token）。
2. **元数据/登记/DOI 基础设施**：**Crossref**（学术 DOI 登记机构，L 200 / A 200；撤稿过滤 `update-type:retraction` 实测 200）、**DataCite**（数据/软件 DOI，API 200）、**ORCID**（L/A 200）、**ROR**（API 200，落地 429）、**ISSN 门户**（落地 200，JSON 被 Anubis 门挡）、**Retraction Watch**（落地/指南 200）、**PubPeer**（落地 200，无公开 GET API）。
3. **学科专属**：PubMed/PMC（E-utilities 实测 200，PubMed 落地 403）、Europe PMC（REST 200，落地 403）、DOAJ（API 200，落地 403）、dblp（202）、ACL Anthology / PMLR / JMLR（200）、OpenReview（落地 200，`/groups` 200，`/notes` 被挑战门 403）、arXiv（导出 API 200）、bioRxiv+medRxiv（api.biorxiv.org 200）、HAL（API 200）、CiNii（OpenSearch 200）、J-STAGE / SciELO / Redalyc（200）、CNKI / Wanfang / KISS（200，正文有登录墙）、EThOS（ethos.bl.uk 200，已迁 Hyku）、ERIC（API 200）；受阻：SSRN 403、PhilPapers 403、Shodhganga 机器人门、Airiti SSL 失败、ProQuest 302。
4. **出版商/平台（版本记录）**：Cambridge Core、PLOS（搜索 API 实测 200）、Frontiers、MDPI、De Gruyter Brill、SpringerLink、IEEE Xplore 可达；ACM DL / ScienceDirect / Wiley / T&F / Oxford Academic 返回 403，SAGE SSL 失败。
5. **AI/ML 会议索引**：NeurIPS proceedings、ICML、ICLR、AAAI（OJS）、IJCAI proceedings、ACL Anthology、TMLR 落地页均 200。

**如何不洗稿（关键）。** ① 聚合器只做发现，命中后取标识符（DOI / arXiv id）到**产出方**取原文；② 优先**版本记录**，只能引预印本时给**稳定标识**并注明是预印本；③ 使用前**查撤稿/更正状态**（Crossref 撤稿过滤或 Retraction Watch 数据库）；④ 评论/QA 层（PubPeer、新闻）是线索不是证据；⑤ **检索结果条数永远不是证据**，「Google Scholar 有 N 条」度量的是索引，不是文献，引用次数同理（须注明来源与日期）；⑥ ORCID/ROR/ISSN/DataCite 只证身份，不证质量；DOI 可解析只证持久性，不证同行评审；⑦ 记录你**真正打开过**的一手 URL + 标识 + 访问日期。

**受阻清单（§7）。** 403：PubMed/Europe PMC/DOAJ/PhilPapers/ACM DL/ScienceDirect/Wiley/T&F/Oxford/SSRN；429：ror.org、无 key 的 Semantic Scholar API；SSL 失败：datacite.org、SAGE、Airiti、https repec.org；机器人门：ISSN API、Shodhganga、BASE about、Brill（WAF）；超时：CORE API。均为**本环境特有**，服务本身健在——凡标注 `A 200` 的 API 实测确有响应。

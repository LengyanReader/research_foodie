# Information outlets · 各领域信息源地图

> **What this is.** A curated map of the **high-quality information outlets, portals and media** per
> field — where to *look* and *draw first-party evidence* when a task lands in a discipline. It is the
> companion to `data/sources.json` (the machine-readable `outlets` group) and to `reference/evidence-instruments.md`
> (which *instrument* observes a claim). It is **not** a ranking and **not** exhaustive: each entry says *why*
> it is high-quality **and what it is NOT for**, so a reader can appraise a source rather than trust a list.
> · 本文是**按领域组织的高质量信息源地图**（门户 · 期刊 · 预印本 · 数据库/登记库 · 数据仓储 · 媒体）：
> 任务落到某学科时「去哪查、从哪取一手证据」。它是 `data/sources.json` 的 `outlets` 组与
> `reference/evidence-instruments.md` 的配套。**不是排行榜，也不求穷尽**：每条都写明「为何高质量」与「不适合用来做什么」。

**Updated:** 2026-10-20 · Load via `harness skill outlet-map` · live view: `harness sources --group outlets` · machine-readable: `data/sources.json`. Verification: `review/references.md` §K is unrelated (that is the cross-language pass); outlet provenance is each entry's own first-party URL. The itemised survey behind the 2026-10 discovery additions is `review/scholarly-channels-2026-10.md`.

---

## 中文速览

**先看领域，再看来源类型。** 表按**学科门类**分组，每行给：**信息源（一键直达）· 类型 · 为何可信 · 不适合用来做什么**。
`✔` = 本次自动可达性检查（GET，2026-10-19–20）通过；`○` = 规范一手域名已知，但自动检查被反爬/机器人门阻挡（403/405/429/SSL/Anubis），**列为「已知，未在本次确认」**。
用法：① 按领域找到对应小节；② 优先预印本服务器/权威索引定位文献，再到登记库/数据仓储取数据；③ **永远回到一手来源**——聚合器/媒体只用来发现，不用来引用；④ 与 `reference/evidence-instruments.md` 配合，确定「用什么仪器观察该主张」；⑤ 跨语言搬运时按 `reference/cross-language.md` 的意群对齐与回译互证执行（M4.10）。

**与既有分组的关系。** `sources.json` 的 `venues`/`media` 组记录 **AI/ML 赛道**的期刊与媒体；本 `outlets` 组补的是**各学科门类**的信息源，二者不重复。`libraries` 组（Gutenberg、HathiTrust 等）覆盖公共领域文本，与本组的学术门户互补。

---

## How to use · 用法

1. Find your **field** section; scan the `why` column and pick the *primary* outlet for the claim type.
2. Prefer, in order: **first-party registry/database → reviewed index → preprint server → media explainer**.
3. Read the `NOT for` column before you cite: a preprint is not a verdict, an aggregator is not a source, a Q&A answer is not citable.
4. Pair with `reference/evidence-instruments.md`: this map says *where*, that doc says *with what instrument and gate*.
5. When the outlet's language differs from the deliverable's, apply `reference/cross-language.md` (M4.10) — align by meaning unit, corroborate, gloss terms.

**Retrieval routes when the canonical domain is unreachable · 规范域不可达时的取数路径.** Some hosts are blocked from some environments (measured 2026-10-19: `*.substack.com` and `x.com`). Three routes normally still answer: a publication's **own domain** (including its `/feed`, and for Substack-hosted publications the paginated `/api/v1/archive`), the article mirror at `api.fxtwitter.com/<user>/status/<id>` for the X form, and the field's first-party API (e.g. the arXiv `id_list` batch endpoint). A mirror or aggregator remains **discovery only** — always cite through to the primary artifact. Per-entity reachability notes live in `data/sources.json`.

**Verification · 核验.** `✔` = the outlet URL answered an automated HEAD/GET (2026-10-19). `○` = canonical
first-party domain, but the automated check was blocked (403/405) or did not complete; these are recorded
**listed, not confirmed this session** and carry a `note` in `data/sources.json`. The `why` text is the
editor's one-line appraisal (kind + owner) — it is not a substitute for reading the outlet's own policy page.

---

## Cross-field infrastructure · 跨领域基础设施

Fields in every discipline depend on the same registries, repositories and integrity services.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [arXiv](https://arxiv.org/) | preprint | Canonical multi-field preprint server (math, physics, CS, statistics, q-bio, econ). | Not peer-reviewed and versioned; cite the published version when one exists. |
| ○ [DOAJ — Directory of Open Access Journals](https://doaj.org/) | index | Curated directory of vetted open-access journals across fields. | Inclusion is a quality floor, not a ranking; still appraise the article. |
| ✔ [ORCID](https://orcid.org/) | registry | Researcher identifier registry; disambiguates authors across venues. | Identity only — it asserts nothing about the work. |
| ✔ [Zenodo](https://zenodo.org/) | repository | CERN-operated general-purpose repository; assigns DOIs to data, code and papers. | A deposit is not a review — judge the artifact on its own evidence. |
| ✔ [Dryad](https://datadryad.org/) | repository | Curated repository for research data underlying published papers. | Coverage is uneven by field; not a general archive. |
| ✔ [Retraction Watch](https://retractionwatch.com/) | media | Tracks retractions and research-integrity cases; the database is the citable part. | News/commentary; verify each case against the notice itself. |
| ✔ [Google Scholar](https://scholar.google.com/) | index | Broad scholarly index across languages and fields; useful for coverage. | Uncurated — mixes predatory venues, duplicates and grey literature; never treat a hit as peer review. |

---

## Scholarly discovery & citation infrastructure · 学术检索与引用基础设施

The layer that sits *above* a field index: it finds **identifiers**, it does not produce evidence (added 2026-10-20; survey in `review/scholarly-channels-2026-10.md`). Cross-field services already registered elsewhere are **not duplicated here** — `semantic-scholar`, `crossref`, `core`, `scite` and `europepmc` live in the `tools` group, `openalex` in `projects`; use those records for the API endpoints. The rows below are the channels that had no registry entry.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [OpenAIRE](https://www.openaire.eu/) | portal | EC-funded open-science graph linking publications, datasets and CRIS metadata across European repositories. | Graph metadata, not the artefacts — follow each record to the depositing repository or publisher. |
| ○ [DataCite](https://datacite.org/) | registry | DOI registration agency for datasets, software and preprints; the identifier layer for research data. | Identity and persistence only — no quality signal. Landing unreachable here (SSL/502); `api.datacite.org/dois` answered 200. |
| ○ [ROR](https://ror.org/) | registry | Open registry of stable identifiers for research organisations; disambiguates affiliations. | Organisation identity only — no statement about merit. Landing behind a 429 bot checkpoint; `api.ror.org/organizations` answered 200. |
| ○ [BASE](https://www.base-search.net/) | index | Large open-access meta-index harvested from institutional and subject repositories (Bielefeld UL). | Aggregation layer — cite the depositing repository; coverage is repository-dependent. Bot-gated landing here; the search API needs IP registration. |
| ✔ [Connected Papers](https://www.connectedpapers.com/) | index | Builds a citation-similarity graph from one seed paper; good for finding adjacent literatures. | Discovery only, no public API, and similarity is not relevance — verify every node against its own record. |
| ✔ [ResearchRabbit](https://www.researchrabbit.ai/) | index | Citation-network exploration and alerts over public metadata. | Discovery only; client-rendered with no public API, so nothing here is scriptable or reproducible. |
| ✔ [OpenReview](https://openreview.net/) | portal | Publishes submissions, reviews and decisions for venues that review in the open (ICLR and others). | Reviews are opinions, not findings; the accepted paper is the citable artefact. `/notes` is challenge-gated, so paper search is not scriptable here. |
| ✔ [PubPeer](https://pubpeer.com/) | qa | Post-publication comment threads on specific papers — a signal that an integrity question exists. | Anonymous threads are **leads**, not evidence: cite the published notice or the article, never the thread. |

---

## Multilingual & regional scholarship · 多语种与区域学术

English-language indexes systematically under-cover scholarship published in Chinese, Japanese, Korean, French, Spanish and Portuguese. These are the first-party regional platforms that fill that gap (added 2026-10-20); they are **not** interchangeable with a field index.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [SciELO](https://www.scielo.org/) | repository | Open-access network of Latin-American, Iberian and African journals with full text. | Regional scope; quality is per-journal — appraise the journal and the article. |
| ✔ [Redalyc](https://www.redalyc.org/) | repository | Ibero-American open-access journal platform (UAEMex). | Largely Spanish/Portuguese; not a substitute for a field index. |
| ○ [HAL Open Science](https://hal.science/) | repository | French national multidisciplinary open repository; strong for French-language scholarship. | A deposit is not a review — check whether a published version exists. Landing intermittently bot-gated; `api.archives-ouvertes.fr/search/` answered 200. |
| ✔ [CiNii Research](https://cir.nii.ac.jp/) | index | National Institute of Informatics index of Japanese-language articles, books and data. | Index metadata only; effective retrieval needs Japanese-language queries. |
| ✔ [J-STAGE](https://www.jstage.jst.go.jp/) | publisher | JST platform hosting Japanese sci-tech society journals. | Mixed access and language; society-run titles vary — appraise the specific journal. |
| ✔ [CNKI](https://www.cnki.net/) | portal | China National Knowledge Infrastructure: the dominant index for Chinese-language journals and theses. | Licensed/paywalled full text; coverage is opaque — corroborate important claims. |
| ✔ [Wanfang Data](https://www.wanfangdata.com.cn/) | portal | Chinese journals, dissertations and standards (ISTIC-affiliated). | Paywalled; a second Chinese index, not an independent verification of CNKI. |
| ✔ [EThOS](https://ethos.bl.uk/) | repository | UK doctoral theses, now on a Hyku-based platform after the British Library outage. | Theses are examined, not peer-reviewed articles — check for a published paper. |

---

## Publishers of record & proceedings · 版本记录与会议论文集

The version of record for a claim, when the field sections above point to an index. Field-specific publishers already appear in their own sections; AI/ML **venue** indices (NeurIPS, ACL, ICML, ICLR, TMLR) are tracked in the `venues` group and are deliberately not duplicated here.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [PMLR](https://proceedings.mlr.press/) | publisher | Free, citable proceedings for ICML, AISTATS and other ML conferences. | ML scope only; a proceedings paper is not a journal article. |
| ✔ [SpringerLink](https://link.springer.com/) | publisher | Springer Nature journals and books — the version of record for a large share of STM literature. | Largely subscription-gated; the landing page is not the article's evidence. |
| ✔ [Cambridge Core](https://www.cambridge.org/core) | publisher | Cambridge University Press journals and books, strong in the humanities and social sciences. | Largely gated; check the licence per article. |
| ✔ [PLOS](https://plos.org/) | publisher | Open-access publisher with a full search API (`api.plos.org/search`), usable from a script. | PLOS ONE is broad and volume-driven — appraise the specific article, not the brand. |

---

## Physics & astronomy · 物理与天文

Preprint server first, then curated indexes and society publishers.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [NASA ADS](https://ui.adsabs.harvard.edu/) | index | Astronomy/astrophysics literature and data system (NASA). | Strongest in astro; weaker elsewhere. |
| ✔ [INSPIRE-HEP](https://inspirehep.net/) | index | Curated high-energy-physics literature and author database. | HEP-only scope. |
| ✔ [APS Journals](https://journals.aps.org/) | publisher | American Physical Society journals (Physical Review family, PRL). | Subscription-gated in part; some open access. |
| ✔ [IOPscience](https://iopscience.iop.org/) | publisher | Institute of Physics publishing platform (peer-reviewed physics). | Mixed access; check the licence per article. |
| ○ [AIP Publishing](https://pubs.aip.org/) | publisher | American Institute of Physics journals (applied/physical sciences). | Automated check blocked (403) — listed, not confirmed this session. |

---

## Chemistry · 化学

Structures and properties from first-party chemical databases; preprints for early work.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [PubChem](https://pubchem.ncbi.nlm.nih.gov/) | database | NIH chemical database: structures, properties, bioactivity. | Aggregates depositor data — trace each fact to its depositor record. |
| ○ [ChemRxiv](https://chemrxiv.org/) | preprint | Chemistry preprint server (ACS/RSC/GDCh-backed). | Preprints; not peer-reviewed — check for the published version. |
| ✔ [CAS Common Chemistry](https://commonchemistry.cas.org/) | database | Open subset of the CAS Registry of chemical substances. | Subset only; the full registry is proprietary. |

---

## Biology · 生物学

Sequence, expression and genome resources; preprints screened but not reviewed.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [NCBI](https://www.ncbi.nlm.nih.gov/) | database | US National Center for Biotechnology Information; portal to GenBank, PubMed, GEO and more. | Portal — each resource has its own currency and licence. |
| ✔ [bioRxiv](https://www.biorxiv.org/) | preprint | Life-science preprint server (CSHL). | Preprints; screening is minimal — appraise and check publication status. |
| ✔ [Ensembl](https://www.ensembl.org/) | database | Genome browser and annotation database (EMBL-EBI/Wellcome Sanger). | Release-versioned — cite the release used. |
| ✔ [GEO — Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/) | database | NCBI archive of gene-expression datasets. | Depositor-submitted; check the study design before reuse. |

---

## Medicine & health · 医学与健康

Indexes, systematic reviews, trial registries and public-health agencies.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [PubMed](https://pubmed.ncbi.nlm.nih.gov/) | index | US National Library of Medicine index of biomedical literature (MEDLINE). | Index, not full text; an abstract is not the study. |
| ✔ [PubMed Central](https://pmc.ncbi.nlm.nih.gov/) | repository | Free full-text archive of biomedical literature (NIH). | Coverage is partial; the licence varies by article. |
| ○ [Cochrane Library](https://www.cochranelibrary.com/) | database | Systematic reviews and meta-analyses of health interventions; GRADE-graded. | Automated check blocked (403) — listed, not confirmed this session. |
| ✔ [ClinicalTrials.gov](https://clinicaltrials.gov/) | registry | US registry of clinical trials; results often posted here first. | Registration/self-reported results — reconcile with the publication. |
| ✔ [World Health Organization](https://www.who.int/) | portal | WHO guidance, statistics and global-health data. | Guidance documents are normative statements, not primary trials. |
| ○ [US CDC](https://www.cdc.gov/) | portal | US Centers for Disease Control: surveillance, guidance, data. | Automated check blocked (403) — listed, not confirmed this session. |
| ✔ [medRxiv](https://www.medrxiv.org/) | preprint | Health-sciences preprint server (BMJ/Yale/CSHL). | Preprints: screened but not peer-reviewed — never cite as settled clinical evidence. |

---

## Earth & environment · 地球与环境

National survey agencies and Copernicus data services.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [USGS](https://www.usgs.gov/) | portal | US Geological Survey: earth-science data, maps and publications. | National scope; check version/date of datasets. |
| ○ [NASA Earthdata](https://www.earthdata.nasa.gov/) | portal | NASA Earth-observation data and tools. | Automated check blocked; use the data portals (Earthdata Login). |
| ✔ [NOAA](https://www.noaa.gov/) | portal | US National Oceanic and Atmospheric Administration: climate, ocean and weather data. | Cite the specific dataset/station and its version, not the portal. |
| ✔ [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) | database | EU Copernicus climate reanalysis and projections (ERA5 et al.). | Reanalysis is a model product — respect its uncertainty. |

---

## Mathematics & statistics · 数学与统计

Reviewed indexes for mathematics; a community Q&A for statistics references.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ○ [zbMATH Open](https://zbmath.org/) | index | Comprehensive reviewed index of mathematical literature (now open). | Automated check blocked (403) — listed, not confirmed this session. |
| ✔ [MathSciNet](https://mathscinet.ams.org/) | index | American Mathematical Society reviews database (Mathematical Reviews). | Subscription-gated. |
| ✔ [Project Euclid](https://projecteuclid.org/) | publisher | Mathematics and statistics journal platform (open access core). | Coverage is selective, not a full index. |
| ✔ [Cross Validated](https://stats.stackexchange.com/) | qa | Statistics Q&A community; good for finding the canonical reference. | Community answers are not citable — follow them to the primary source. |

---

## Computing · 计算

Curated bibliography plus the two big professional publishers and one diamond-OA journal.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [dblp](https://dblp.org/) | index | Curated computer-science bibliography (author/venue metadata). | Bibliographic metadata only — no full text or quality judgement. |
| ○ [ACM Digital Library](https://dl.acm.org/) | publisher | ACM journals and conference proceedings (peer-reviewed CS). | Automated check blocked (403) — listed, not confirmed this session. |
| ✔ [IEEE Xplore](https://ieeexplore.ieee.org/) | publisher | IEEE journals, conference papers and standards. | Mixed quality across venues; check the specific venue. |
| ✔ [Journal of Machine Learning Research](https://jmlr.org/) | journal | Diamond open-access ML journal with rigorous reviewing. | ML scope only. |

---

## Economics & finance · 经济与金融

Index, working papers, macro data and cross-country statistics.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ○ [RePEc](https://repec.org/) | index | Volunteer-built index of economics research (papers, articles, software). | Automated check did not complete (transport) — listed, not confirmed this session. |
| ✔ [NBER](https://www.nber.org/) | portal | US National Bureau of Economic Research working papers. | Working papers are pre-publication — check the final version. |
| ○ [SSRN](https://www.ssrn.com/) | repository | Large preprint/postprint repository across economics, law and social science. | Automated check blocked (403); and preprints are not peer-reviewed — verify status. |
| ✔ [FRED](https://fred.stlouisfed.org/) | database | Federal Reserve Economic Data: sourced macroeconomic time series. | Series are aggregates — trace to the originating agency release. |
| ✔ [World Bank Open Data](https://data.worldbank.org/) | database | World Bank development indicators and datasets. | Estimates and model-based for some series — read the metadata. |
| ○ [International Monetary Fund](https://www.imf.org/) | portal | IMF macro data, forecasts and surveillance publications. | Forecasts are projections; label them as such. |
| ○ [OECD](https://www.oecd.org/) | portal | OECD statistics, policy analysis and education data. | Automated check blocked (403) — listed, not confirmed this session. |

---

## Psychology & social science · 心理与社会科学

Abstract indexes, preprints, data archives and survey research.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [APA PsycNet](https://psycnet.apa.org/) | index | American Psychological Association index of psychology literature. | Subscriptions gate full text; cite through the DOI/record. |
| ✔ [PsyArXiv](https://osf.io/preprints/psyarxiv) | preprint | Psychology preprint server hosted on OSF. | Preprints; not peer-reviewed — appraise and check publication status. |
| ✔ [ICPSR](https://www.icpsr.umich.edu/) | repository | University of Michigan social-science data archive. | Access tiers vary by membership. |
| ✔ [Pew Research Center](https://www.pewresearch.org/) | portal | Non-partisan survey research on social trends and public opinion. | Reports, not raw data (datasets are separately released) — cite the report. |
| ✔ [Our World in Data](https://ourworldindata.org/) | portal | Curated, sourced long-run data and visual essays. | A secondary curator — always follow through to the underlying dataset. |

---

## Law · 法律

Official portals and free case-law databases — verify against the official reporter.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [EUR-Lex](https://eur-lex.europa.eu/) | portal | Official EU law portal (treaties, legislation, case law). | Authoritative for EU law; check consolidation/version dates. |
| ✔ [CourtListener](https://www.courtlistener.com/) | database | Free Law Project's US case-law and docket database. | Unofficial copies — verify against the official reporter. |
| ✔ [Cornell Legal Information Institute](https://www.law.cornell.edu/) | portal | Free legal encyclopedia and codes (Wex, US Code, CFR). | Educational summaries — verify against the official text. |
| ○ [WorldLII](https://www.worldlii.org/) | portal | Global network of free legal-information institutes. | Automated check blocked (403) — listed, not confirmed this session. |

---

## Humanities · 人文

Digitised journals, reference works and cultural-heritage collections.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [JSTOR](https://www.jstor.org/) | repository | Digitised scholarly journals and books across the humanities and social sciences. | Access is largely gated; some open collections. |
| ✔ [Project MUSE](https://muse.jhu.edu/) | publisher | University-press journals and books (humanities/social sciences). | Subscription-gated. |
| ✔ [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/) | portal | Peer-reviewed, continuously updated reference encyclopedia of philosophy. | A reference work — cite the entry/version, and follow it to primary texts. |
| ○ [PhilPapers](https://philpapers.org/) | index | Comprehensive philosophy bibliography and repository. | Automated check blocked (403) — listed, not confirmed this session. |
| ○ [Gallica](https://gallica.bnf.fr/) | repository | Bibliothèque nationale de France digital library (books, manuscripts, images). | Automated check blocked; OCR quality varies by item. |
| ✔ [Perseus Digital Library](https://www.perseus.tufts.edu/) | repository | Classical Greek and Latin texts with translations and tools. | Editions are dated — record the edition used. |
| ○ [Digital Public Library of America](https://dp.la/) | portal | US aggregator of digitised library, museum and archive collections. | Aggregation layer — cite the holding institution, not the aggregator. |
| ○ [Europeana](https://www.europeana.eu/) | portal | EU aggregator of cultural-heritage collections. | Aggregation layer — cite the holding institution; rights vary per item. |

---

## Knowledge & cultural-heritage infrastructure · 知识与文化遗产基础设施

Standards, authorities and vocabulary services — the *first-party norms* a knowledge base, an edition or a heritage record is built against (added 2026-10-19; cf. `domains/digital-humanities/README.md`, `review/knowledge-and-dh-crosswalk-2026-10.md`).

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [W3C specifications](https://www.w3.org/TR/) | registry | The normative Recommendations themselves (RDF, OWL, SKOS, SHACL, PROV-O). | Terse and precise — read the primer for orientation. |
| ✔ [IIIF specifications](https://iiif.io/api/) | registry | Image/Presentation APIs for publishing digitised cultural heritage interoperably. | Defines the model, not a content repository. |
| ✔ [CIDOC-CRM](https://www.cidoc-crm.org/) | registry | ICOM's event-centric ontology for cultural heritage and museum documentation. | Heavy for a small collection; a flat Dublin Core record often suffices. |
| ✔ [Library of Congress standards](https://www.loc.gov/standards/) | registry | Maintains the archival/bibliographic encodings (EAD3, MARC, METS). | Library-centric; for research data prefer Dublin Core/DataCite. |
| ✔ [Getty vocabularies (AAT, TGN, ULAN)](https://www.getty.edu/research/tools/vocabularies/) | database | Authoritative controlled vocabularies with stable ids for places, agents, concepts. | Western/art-historical weighting; not a global gazetteer. |
| ✔ [Text Encoding Initiative Consortium](https://tei-c.org/) | registry | Publishes TEI P5, the XML standard for critical editions and transcribed text. | Encoding-heavy; a plain corpus may want a lighter schema. |
| ✔ [Wikidata data model](https://www.wikidata.org/wiki/Wikidata:Data_model) | database | Item/property/statement model with qualifiers, references and ranks — per-statement provenance in practice. | Crowd-edited; reconcile *against* it, do not quote it as ground truth. |

---

## Linguistics · 语言学

Language catalogues and typological databases.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [Glottolog](https://glottolog.org/) | database | Catalogue of the world's languages and language families (curated). | Bibliographic/classification resource, not primary language data. |
| ✔ [WALS Online](https://wals.info/) | database | World Atlas of Language Structures: typological features across languages. | Feature coding is the editors' analysis — check the source chapter. |

---

## Education · 教育

A research index and an explicit evidence-review body.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [ERIC](https://eric.ed.gov/) | index | US Institute of Education Sciences index of education research. | Index and grey literature mix — check the source type. |
| ○ [What Works Clearinghouse](https://ies.ed.gov/wwc/) | portal | US evidence reviews of education interventions against explicit standards. | Reviews, not primary studies. |

---

## Arts & design · 艺术与设计

Museum collections with open-access metadata/images.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ○ [The Metropolitan Museum of Art](https://www.metmuseum.org/) | portal | Met museum collection with open-access images and metadata (CC0 where noted). | Automated check blocked (403); cite the object record and its rights statement. |

---

## Science media & journalism · 科学媒体

Secondary explainers — always follow through to the primary paper.

| Outlet | kind | why it is high-quality | NOT for |
|---|---|---|---|
| ✔ [Quanta Magazine](https://www.quantamagazine.org/) | media | High-quality science journalism on math, physics, biology and CS. | Secondary reporting — always follow through to the primary paper. |

---

## Deliberate non-entries · 有意不收录

- **Predatory / pay-to-publish venues and SEO content farms.** Inclusion would launder low quality.
- **Uncurated auto-generated aggregators** presented as primary sources (they are *discovery* only).
- **AI-generated content farms and undisclosed-LLM blogs** — no accountable author or editorial standard.
- **Paywalled indexes without a public record of scope** (a URL alone cannot be appraised).
- **Duplication of `venues`/`media`** (AI/ML journals and media already tracked there) and of `libraries` (public-domain corpora).
- **Aggregator digests as outlets** — a curated "top papers of the week" newsletter (e.g. `nlp.elvissaravia.com`) is **discovery only**, and the publication is already tracked in the `media` group; listing it here again would duplicate and would launder a second-hand index into a citable outlet. Enter individual papers through their own primary record (preprint/publisher).
- **A machine-translation metric as a fidelity gate** — see `reference/cross-language.md` §6 (BLEU/COMET rank candidates; they do not certify meaning).
- **AI/ML venue indices as outlets** (NeurIPS, ACL, ICML, ICLR, TMLR) — they already live in the `venues` group; listing them again here would duplicate the registry and blur the *field-conference* with the *field-outlet*.
- **High-volume OA mega-publishers as single outlets** (MDPI, Frontiers, and similar) — this is a **granularity** decision, not a verdict on quality: their titles differ too much for one row to appraise, so cite the specific journal's indexing and the article itself.
- **LLM literature assistants with no auditable record** (Elicit, Consensus, SciSpace and similar) — their answer is not reproducible, not versioned and not accountable to an author; use them as a lead generator only, and never as the cited channel.
- **A search-hit count as evidence** — "N results on Google Scholar" measures an index, not the literature; citation counts from any aggregator are index artefacts that differ by source (if used at all, name the source and the date).

---

## See also · 另见

- `data/sources.json` — the machine-readable `outlets` group (`harness sources --group outlets`).
- `reference/evidence-instruments.md` — claim type ⇒ instrument ⇒ tool ⇒ gate (M3.10).
- `reference/methodology-map.md` — field ⇒ methodology system ⇒ what the harness enforces (M3.13).
- `reference/cross-language.md` — meaning-unit alignment for cross-language work (M4.10).
- `sources/source-map.md` — how each shipped pattern/outlet set traces to primary sources.
- `review/integration-map-2026-10.md` — scope/status board (what P11 integrated).
- `review/scholarly-channels-2026-10.md` — the 2026-10 survey: ~95 channels with observed HTTP statuses, first-party-vs-aggregator marks, and the seven no-laundering rules.

## Answer (EN)

The primary metric used for the STS tasks is **Spearman's rank correlation (ρ / rho)** between the cosine-similarity of sentence embeddings and the gold labels. In Table 1 the paper reports results across STS12–STS16, STS benchmark (STSb), and SICK-R as Spearman rank correlation, "by convention as ρ × 100" (arXiv:1908.10084). Pearson correlation is explicitly rejected for standard STS because it is "badly suited," and is only additionally provided for the Argument Facet Similarity (AFS) corpus to remain comparable to Misra et al. (e.g., Tables 2 and 3 report Spearman ρ; AFS, Table 3, reports both Pearson r and Spearman ρ) (arXiv:1908.10084).

## 中文速览

STS 任务使用的主要评估指标是 **Spearman 秩相关系数 (ρ)**，即句子嵌入的余弦相似度与金标之间的 Spearman 相关，按惯例以 ρ×100 报告（Table 1，覆盖 STS12–16、STS benchmark、SICK-R）。论文明确认为 Pearson 相关不适用于 STS，仅在 Argument Facet Similarity（AFS）语料上额外给出 Pearson r 以与 Misra et al. 的结果可比（Table 3）。

## Source evidence

> "We compute the Spearman's rank correlation between the cosine-similarity of the sentence embeddings and the gold labels." (arXiv:1908.10084)

> "Performance is reported by convention as ρ × 100." (arXiv:1908.10084, Table 1 caption)

> "We also provide the Pearson correlation r to make the results comparable to Misra et al. However, we showed (Reimers et al., 2016) that Pearson correlation has some serious drawbacks and should be avoided for comparing STS systems." (arXiv:1908.10084)
## Answer (EN)

The paper evaluates MPAD on **10 document classification datasets** covering topic identification, coarse and fine sentiment analysis / opinion mining, and subjectivity detection (arXiv:1908.06267). The datasets introduced in Section 4.1 (and reported in Table 1) are:

1. **Reuters** (ModApte split, 8 classes)
2. **Snippets**
3. **BBCSport** (cross-validation)
4. **Polarity** (Rotten Tomatoes snippets)
5. **Subjectivity** (movie review snippets + IMDB plot summaries)
6. **MPQA** (positive/negative opinion phrases)
7. **IMDB** (polarized movie reviews)
8. **TREC** (question classification, 6 categories)
9. **SST-1** (fine-grained, 5 classes)
10. **SST-2** (binary, neutral removed)
11. **Yelp2013** (2013 Yelp Dataset Challenge)

(Note: Table 1 lists 11 rows even though the text states "10"; the paper's own wording is 10 datasets.) All nodes are initialized with 300-d Google News vectors except Yelp2013, where word vectors are learned with word2vec (arXiv:1908.06267).

## 中文速览

论文在 **10 个文档分类数据集**上评估 MPAD：Reuters、Snippets、BBCSport、Polarity、Subjectivity、MPQA、IMDB、TREC、SST-1、SST-2、Yelp2013（Table 1 实际列了 11 项，但行文均称 10 个）。除 Yelp2013 自行训练 word2vec 向量外，其余均用 300 维 Google News 预训练向量初始化 (arXiv:1908.06267)。

## Source evidence

"We evaluate the quality of the document embeddings learned by MPAD on 10 document classification datasets, covering the topic identification, coarse and fine sentiment analysis and opinion mining, and subjectivity detection tasks." — "Experiments conducted on 10 standard text classification datasets show that our architectures are competitive with the state-of-the-art." (arXiv:1908.06267)
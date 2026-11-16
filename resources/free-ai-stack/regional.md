# Regional & Global Coverage · 区域与全球覆盖
> China/Asia, EU, and global provider leads — explicitly marked where unverified.
> 中国/亚洲、欧盟与全球 provider 线索——未核验处已明确标注。
**Updated:** 2026-11-08 · This page is a **coverage map**, not a verified price list.

---

## 中文速览
“全球全网”不能只看美国 provider。本页列出**中国/亚洲、欧盟、全球**的主要候选，但除已在本目录其他页面核验的条目外，均标 `⚪`：**免费额度、是否需要实名、是否支持境外访问、数据是否出境**都必须在官方页面重新核验。中国 provider 常有**新用户赠送额度/限时免费模型**，但变化快、条款多；涉及个人信息或跨境数据时，先做合规判断，不要直接上免费层。

> **Status rule:** ✅ verified in this snapshot · 🟡 partially verified · ⚪ lead, not verified · ⛔ avoid.

---

## China / Asia · 中国与亚洲
| Provider | What it offers | Official starting point | Status | Verify before use |
|---|---|---|---|---|
| **DeepSeek** | Chat/reasoning API; low-cost paid API | https://platform.deepseek.com/ | ⚪ | Free quota? Current pricing? Data policy? |
| **Alibaba Cloud Model Studio (Qwen)** | Qwen models; API + model studio | https://www.alibabacloud.com/en/product/modelstudio | ⚪ | New-user free quota? Region/real-name? |
| **Zhipu AI (GLM)** | GLM chat/embedding API | https://open.bigmodel.cn/ | ⚪ | Free tier? Rate limits? |
| **Moonshot AI (Kimi)** | Kimi chat API | https://platform.moonshot.cn/ | ⚪ | Free trial? Pricing? |
| **Baidu Qianfan (ERNIE)** | ERNIE models; API | https://cloud.baidu.com/product/wenxinworkshop | ⚪ | Free quota? Real-name? |
| **Tencent Hunyuan** | Hunyuan models; API | https://cloud.tencent.com/product/hunyuan | ⚪ | Free quota? Region? |
| **iFlytek Spark** | Spark models; API | https://www.xfyun.cn/ | ⚪ | Free quota? Real-name? |
| **MiniMax** | Chat/audio/video models | https://www.minimaxi.com/ | ⚪ | Free trial? Pricing? |
| **SiliconFlow** | Hosted open models; OpenAI-compatible | https://siliconflow.cn/ | ⚪ | Free models? Rate limits? |
| **ModelScope** | Model/dataset hub; hosted inference | https://modelscope.cn/ | ⚪ | Free inference? Model licenses? |

**China-specific safety checks:** real-name verification, data residency, cross-border transfer rules, content moderation requirements, and whether the free tier trains on your data. Do not send PII or regulated data to an unverified regional free tier.

---

## EU / Global · 欧盟与全球
| Provider | What it offers | Official starting point | Status | Verify before use |
|---|---|---|---|---|
| **Mistral AI** | EU models; Vibe product; API | https://mistral.ai/pricing | 🟡 (Vibe Free verified; API free tier not) | API free tier? Data residency? |
| **Cohere** | Chat/embed/rerank; trial key | https://cohere.com/pricing | ✅ (trial limits verified) | Production pricing; data policy |
| **AI21 Labs** | Jamba models; API | https://www.ai21.com/ | ⚪ | Free tier? |
| **Aleph Alpha** | EU sovereign AI | https://aleph-alpha.com/ | ⚪ | Free tier? |
| **NVIDIA NIM** | Hosted model APIs; trial credits | https://build.nvidia.com/ | ⚪ | Free credits? Expiry? |
| **Together AI** | Open-model inference | https://www.together.ai/pricing | ⚪ | Free credits? |
| **Fireworks AI** | Open-model inference | https://fireworks.ai/pricing | ⚪ | Free credits? |
| **Cerebras** | Fast inference | https://www.cerebras.ai/ | ⚪ | Free tier? |
| **SambaNova** | Fast inference | https://sambanova.ai/ | ⚪ | Free tier? |
| **Azure AI Foundry** | Model catalog (GitHub Models successor) | https://ai.azure.com/ | ⚪ | Free credits? Terms? |
| **AWS Bedrock** | Managed model access | https://aws.amazon.com/bedrock/pricing/ | ⚪ | Free tier? |
| **Google Vertex AI** | Managed model access | https://cloud.google.com/vertex-ai/pricing | ⚪ | Free trial credits? |

---

## Coverage map · 覆盖地图
| Region | Verified in this snapshot | Leads (`⚪`) | Gap |
|---|---|---|---|
| US/global | Gemini, Groq, OpenRouter, Cohere, Cloudflare, GitHub Copilot, Gemini Code Assist, Amazon Q, Ollama, Cline, Gemini CLI | NVIDIA NIM, Together, Fireworks, Cerebras, SambaNova, Azure AI Foundry, AWS Bedrock, Vertex AI | Paid-tier pricing, regional availability |
| EU | Mistral (Vibe Free); Cohere trial | AI21, Aleph Alpha, Mistral API | EU data residency, DPA, free API tier |
| China/Asia | — | DeepSeek, Qwen/Model Studio, Zhipu, Moonshot, Baidu, Tencent, iFlytek, MiniMax, SiliconFlow, ModelScope | Free quotas, real-name, cross-border data |
| Other regions | — | Provider-specific student/startup programs | Region-locked programs |

**Honesty:** a blank cell is a **coverage gap**, not a claim that no resource exists. Add verified rows as they are fetched.

---

## How to add a regional provider · 如何增补区域 provider
1. Fetch the provider's **official pricing/rate-limit page** in the target region.
2. Record: free quota, expiry, model list, rate limits, data policy, real-name requirement, region availability.
3. Check the **terms** for commercial use and cross-border data.
4. Add the row with `✅`/`🟡`/`⚪` and an access date.
5. If the provider cannot be verified from this network, keep `⚪` and note the failure.

**Do not** infer a free tier from a blog, a GitHub list, or a model's open weights. The provider's page is the source of truth.
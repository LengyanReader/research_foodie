# Changelog · 变更日志
> All notable changes to the free-AI-stack catalog.
> 免费 AI 栈目录的重要变更。
Format: keep it short; every entry names the source and access date.

---

## 2026-11-08 · v1.1 audit — coverage gaps filled
- **Added `free-app-infra.md`** — verified free hosting, DB/auth, search, vector DB, and observability:
  - Vercel Hobby, Cloudflare Pages Free, Supabase Free, Tavily, Qdrant Cloud Free, Langfuse Hobby.
  - Source pages fetched 2026-11-08; numbers recorded with caveats.
- **Added `regional.md`** — China/Asia, EU, and global provider leads, all `⚪` unless verified elsewhere. No numbers quoted for unverified providers.
- **Added `MAINTENANCE.md`** — monthly/quarterly/pre-adoption cadence, update procedure, entry template, status board.
- **Added `CHANGELOG.md`** — this file.
- **Extended `llm-apis.md`** — multimodal free tiers (Gemini Transcribe/Live, Groq Whisper, Cloudflare Whisper/Flux), embeddings note, model/dataset links.
- **Extended `README.md`** — coverage map, explicit out-of-scope, update status.
- **Extended `sources.md`** — Vercel, Supabase, Tavily, Langfuse, Qdrant, Cloudflare Pages; regional leads.

## 2026-11-08 · v1 — initial catalog
- Created `resources/README.md` and `resources/free-ai-stack/` with:
  - `README.md`, `llm-apis.md`, `vibe-coding.md`, `github-lists.md`, `safety.md`, `sources.md`.
- Verified from official pages: Gemini, Groq, OpenRouter, Cohere, Cloudflare Workers AI, Hugging Face, GitHub Models retirement, Mistral Vibe, GitHub Copilot Free, Gemini Code Assist, Amazon Q Developer.
- Verified from GitHub API: Ollama (MIT), Cline (Apache-2.0), Gemini CLI (Apache-2.0), three meta-lists, two red-flag repos, `cheahjs` 404.
- Safety-first exclusions: credential-sharing/proxy APIs, “no key/unlimited” claims, ToS-violating gateways.

---

## Template for future entries
```md
## YYYY-MM-DD · vX.Y — short title
- **Added/Updated/Retired:** what changed.
- **Evidence:** official URL + access date.
- **Impact:** which recommendation changed.
- **Next review:** YYYY-MM-DD.
```
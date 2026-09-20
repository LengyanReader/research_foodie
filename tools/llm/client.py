"""
Unified LLM client for research_foodie.

Backends
--------
- **opencode**: calls the opencode CLI headlessly (`opencode run --format json`)
  using opencode's hosted free models (default `opencode/big-pickle`). The
  primary backend since 2026-09-16.
- **openai**: calls any OpenAI-compatible endpoint (`POST /v1/chat/completions`), which covers:
  - DeepSeek API  (https://api.deepseek.com/v1)
  - DashScope/Qwen (https://dashscope.aliyuncs.com/compatible-mode/v1)
  - OpenRouter     (https://openrouter.ai/api/v1)
  - Moonshot/Kimi  (https://api.moonshot.cn/v1)
  - OpenAI         (https://api.openai.com/v1)
  - any local server that implements the same schema.

The local **Ollama** backend was removed on 2026-09-16 (user decision); local
models are no longer part of the pipeline. Fall back to `openai` if a local
OpenAI-compatible server is ever needed.

Configuration (env vars / constructor kwargs):
  LLM_BACKEND          opencode | openai
  OPENCODE_MODEL       opencode/big-pickle        (hosted free model, via opencode CLI)
  OPENAI_BASE_URL      https://api.openai.com/v1
  OPENAI_MODEL         gpt-4o-mini
  OPENAI_API_KEY       (required for openai backend)

Usage:
    from tools.llm.client import LLMClient, Message
    c = LLMClient(backend="opencode")
    r = c.chat([Message(role="user", content="hello")])
    print(r.text)

No external deps — stdlib only (urllib, json, os, dataclasses, subprocess).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatResponse:
    text: str
    model: str
    usage: Dict[str, Any]
    raw: Dict[str, Any]


class OpencodeError(RuntimeError):
    """A headless `opencode run` failure. `retryable` is False for hard account
    errors (e.g. opencode.ai 401 'No payment method' / CreditsError) so the
    caller fails fast with an actionable message instead of hanging on retries."""

    def __init__(self, message: str, *, retryable: bool = True):
        super().__init__(message)
        self.retryable = retryable


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class LLMClient:
    """Unified interface to the opencode CLI or any OpenAI-compatible API."""

    def __init__(
        self,
        backend: str = "opencode",  # "opencode" | "openai"
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        default_temperature: float = 0.0,
        timeout: int = 600,
    ):
        self.backend = backend
        self.timeout = timeout

        if backend == "opencode":
            self.base_url = None
            self.model = model or os.getenv("OPENCODE_MODEL", "opencode/big-pickle")
            self.api_key = None
            self._binary = shutil.which("opencode") or "opencode"
        elif backend == "openai":
            self.base_url = (
                base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            ).rstrip("/")
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        elif backend == "ollama":
            raise ValueError(
                "backend 'ollama' was removed on 2026-09-16 (user decision) — "
                "use 'opencode' or 'openai'"
            )
        else:
            raise ValueError(f"Unknown backend: {backend!r} (expected 'opencode' or 'openai')")

        self.default_temperature = default_temperature

    # ----- public -----------------------------------------------------------

    def chat(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        json_mode: bool = False,
        max_tokens: Optional[int] = None,
    ) -> ChatResponse:
        """Send a chat request; return a ChatResponse."""
        if self.backend == "opencode":
            return self._chat_opencode(messages, json_mode, max_tokens)
        return self._chat_openai(messages, temperature, json_mode, max_tokens)

    def complete(self, prompt: str, **kw) -> ChatResponse:
        """Convenience wrapper: single user-prompt → response."""
        return self.chat([Message(role="user", content=prompt)], **kw)

    def is_reachable(self) -> bool:
        """True if the backend responds to a lightweight ping."""
        try:
            if self.backend == "opencode":
                return subprocess.run(
                    [self._binary, "--version"], capture_output=True, timeout=10
                ).returncode == 0
            # openai: /models is a lightweight GET
            req = urllib.request.Request(f"{self.base_url}/models")
            if self.api_key:
                req.add_header("Authorization", f"Bearer {self.api_key}")
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status == 200
        except Exception:
            return False

    # ----- internals --------------------------------------------------------

    def _chat_opencode(self, messages, json_mode=False, max_tokens=None):
        """Run a headless `opencode run --format json` call and parse the reply."""
        rendered = [
            (f"[{m.role}]\n{m.content}" if m.role == "system" else f"{m.role}:\n{m.content}")
            for m in messages
        ]
        prompt = "\n\n".join(rendered)
        if json_mode:
            prompt += "\n\nIMPORTANT: output ONLY valid JSON (no prose, no markdown fences)."
        text, usage = None, None
        for attempt in range(3):  # opencode CLI hiccups return empty sessions
            try:
                text, usage = self._run_opencode(prompt)
                break
            except OpencodeError as e:
                if not e.retryable:
                    raise  # billing/auth/config error — retrying only wastes time
                if attempt == 2:
                    raise
                time.sleep(2 + 2 * attempt)
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(2 + 2 * attempt)
        return ChatResponse(
            text=text,
            model=self.model,
            usage=usage,
            raw={"backend": "opencode", "events_source": "opencode run --format json"},
        )

    def _run_opencode(self, prompt: str):
        """Spawn `opencode run`; return (text, usage-from-step_finish).

        The prompt is ALWAYS written to a temp file and attached via `-f`:
        passing it as a CLI argument breaks on Windows when it contains double
        quotes (arg quoting mangles the message → empty greeting reply).
        """
        tmp = None
        try:
            tmp = tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", suffix=".txt", delete=False
            )
            tmp.write(prompt)
            tmp.close()
            cmd = [
                self._binary, "run", "--format", "json", "--pure", "-m", self.model,
                "--auto",
                "Follow the instructions in the attached file; reply with your final answer only.",
                "-f", tmp.name,
            ]
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8", timeout=self.timeout
            )
        finally:
            if tmp is not None:
                try:
                    os.unlink(tmp.name)
                except OSError:
                    pass

        if proc.returncode != 0:
            err = self._first_opencode_error(proc.stdout)
            if err:
                code = err.get("statusCode")
                raise OpencodeError(
                    f"opencode model call failed"
                    + (f" [HTTP {code}]" if code else "")
                    + f": {err.get('message') or 'unknown opencode error'}"
                    + " — free hosted models need credits on this opencode.ai account;"
                      " add a payment method, or run the pipeline via an OpenAI-compatible"
                      " endpoint (LLM_PROFILE=openai-compat) instead.",
                    retryable=bool(err.get("isRetryable", False)),
                )
            tail = (proc.stderr or proc.stdout or "")[-800:]
            raise OpencodeError(f"opencode run failed (rc={proc.returncode}): {tail}")
        text, usage = self._parse_events(proc.stdout)
        if not text:
            err = self._first_opencode_error(proc.stdout)
            if err:
                raise OpencodeError(
                    f"opencode model call failed: {err.get('message') or 'error'}",
                    retryable=bool(err.get("isRetryable", False)),
                )
            raise RuntimeError(f"opencode returned no text; stderr tail: {(proc.stderr or '')[-400:]}")
        return text, usage

    @staticmethod
    def _first_opencode_error(stdout: str):
        """Return the first structured `{"type":"error"}` event from `--format
        json` output as {message, statusCode, isRetryable}, else None. opencode
        reports account/billing failures (e.g. HTTP 401 'No payment method') as
        an error event on stdout even when stderr is empty."""
        for line in (stdout or "").splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "error":
                e = ev.get("error") or {}
                data = e.get("data") or {}
                return {
                    "message": data.get("message") or e.get("name") or "opencode error",
                    "statusCode": data.get("statusCode"),
                    "isRetryable": data.get("isRetryable", False),
                }
        return None

    @staticmethod
    def _parse_events(stdout: str):
        """Extract assistant text + token usage from `--format json` event lines."""
        texts: List[str] = []
        deltas: List[str] = []
        usage: Dict[str, Any] = {}
        for line in stdout.splitlines():
            if not line.strip().startswith("{"):
                continue  # skip non-JSON lines (rate warnings etc.)
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            part = ev.get("part") or {}
            if t == "text":
                texts.append(part.get("text", ""))
            elif t == "text.delta":
                deltas.append(part.get("text", ""))
            elif t == "step_finish":
                tk = part.get("tokens") or {}
                if tk:
                    usage = {
                        "prompt_tokens": tk.get("input"),
                        "completion_tokens": tk.get("output"),
                        "total_tokens": tk.get("total"),
                        "reasoning_tokens": tk.get("reasoning"),
                        "cost": tk.get("cost"),
                    }
        return ("".join(texts) or "".join(deltas)).strip(), usage

    def _chat_openai(self, messages, temperature, json_mode, max_tokens=None):
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else self.default_temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read())

        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return ChatResponse(text=text, model=data.get("model", self.model), usage=usage, raw=data)
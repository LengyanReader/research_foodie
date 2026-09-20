"""
Lightweight OpenAI-compatible mock server for smoke-testing tools.llm.client.

Start:  python -m tools.llm.mock_openai_server --port 8199
Use:    Set OPENAI_BASE_URL=http://127.0.0.1:8199/v1 and OPENAI_MODEL=mock-api
        in the smoke test / client.

Returns deterministic canned responses for three prompt categories so the smoke
test can assert exact substrings without any external API key.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import io
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure stdout can handle UTF-8 on Windows consoles (CP1252)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MOCK_MODEL = "mock-api"


_BENCH_16 = [
    "Claim-Level Citation Support", "Reference Faithfulness and Attribution Accuracy",
    "Multi-Reference Synthesis Coverage and Quality", "Citation Distribution Balance and Non-Redundancy",
    "Citation and Reference Presentation Integrity", "Figure/Table Quality and Textual Integration",
    "Layout and Formatting Professionalism", "Manuscript Component Completeness",
    "Research-Space Coverage", "Taxonomy Clarity and Boundary Control",
    "Survey Organization and Functional Coherence", "Synthesis Insight and Gap Analysis",
    "Multi-Level Goal Alignment", "Paragraph Argument Progression",
    "Atomic Claim Specificity and Technical Concreteness", "Local Synthesis and Non-Enumerative Writing",
]


def _route(content: str) -> str:
    """Pick a canned response based on prompt keywords."""
    lower = content.lower()

    if "grade whether a generated research artifact answers a factual question" in lower:
        return json.dumps(
            {"correctness": 4, "groundedness": 4,
             "feedback": "Mock QA grader: correct answer with inline cites."},
            ensure_ascii=False,
        )

    if "das-bench rubric" in lower:
        return json.dumps({"scores": {c: 4 for c in _BENCH_16}}, ensure_ascii=False)

    if "you are a rigorous research-paper reviewer" in lower:
        return json.dumps(
            {"label": "pass", "score": 5,
             "checks": {"groundedness": True, "structure": True,
                        "bilingual": True, "clarity": True},
             "feedback": "Mock judge: draft is grounded, structured, bilingual."},
            ensure_ascii=False,
        )

    if "reader perspectives" in lower:
        return json.dumps(
            {"perspectives": [
                "practitioner: deployability and cost of detection tooling",
                "methodologist: benchmark validity and metric choices",
                "policy analyst: fairness impact on non-native writers",
            ]},
            ensure_ascii=False,
        )

    if "extract a research outline" in lower:
        return json.dumps(
            {"thesis": "GPT detectors are biased against non-native writers",
             "sections": [
                 {"heading": "Background",
                  "key_points": ["Detectors misclassify non-native prose as AI-generated"]},
                 {"heading": "Mitigation",
                  "key_points": ["Simple prompting can mitigate the bias"]},
             ]},
            ensure_ascii=False,
        )

    if "json extraction" in lower or "extract title and year" in lower:
        return json.dumps(
            {"title": "GPT detectors are biased against non-native English writers", "year": 2023},
            ensure_ascii=False,
        )

    if "list of 2 academic claims" in lower or "list of two academic claims" in lower:
        claims = [
            {"claim": "Transformer self-attention enables parallel sequence processing", "cite": "Vaswani et al. 2017 (arXiv:1706.03762)"},
            {"claim": "Pre-training on large unlabeled corpora improves downstream NLP tasks", "cite": "Devlin et al. 2019 (arXiv:1810.04805)"},
        ]
        return json.dumps(claims, ensure_ascii=False)

    if "evidence-backed claims" in lower:
        claims = [
            {"id": "c1", "claim": "Widely-used GPT detectors consistently misclassify non-native English writing samples as AI-generated.", "quote": "these detectors consistently misclassify non-native English writing samples as AI-generated", "cite": "Liang et al. 2023 (arXiv:2304.02819)", "confidence": "high"},
            {"id": "c2", "claim": "Simple prompting strategies can mitigate the bias and bypass GPT detectors.", "quote": "simple prompting strategies can not only mitigate this bias but also effectively bypass GPT detectors", "cite": "Liang et al. 2023 (arXiv:2304.02819)", "confidence": "high"},
        ]
        return json.dumps(claims, ensure_ascii=False)

    if "Write the INTRO of a bilingual" in lower:
        return "Intro (EN): This survey synthesizes evidence on automatic text detection. 中文导言：本节综述自动文本检测的证据。Sections: Background, Mitigation, Limits, Open questions."

    if "Write ONE section of a bilingual" in lower:
        return ("## Cross-Paper Synthesis\n"
                "Section (EN): GPT detectors misclassify non-native prose "
                "(arXiv:2304.02819), while tool benchmarks stress dependence on "
                "prompting (arXiv:2306.15666). 中文：检测器误判非母语写作者（arXiv:2304.02819），"
                "基准评测强调对提示词的依赖（arXiv:2306.15666）。Open gap: no common eval protocol.")

    if "Write the CONCLUSION of a bilingual" in lower:
        return ("Conclusion (EN): Evidence spans dataset, method and policy "
                "(arXiv:2304.02819; arXiv:1906.04043). 中文结论：证据覆盖数据集、方法与政策。"
                "Remaining gaps: cross-tool calibration.")

    if "extract 2-5 topics" in lower:
        return json.dumps({"topics": ["NLP", "LLM"]}, ensure_ascii=False)

    # Default: bilingual acknowledgement
    return "Mock LLM response (EN): research_foodie is a local-first proactive research pipeline. 回复（中文）：research_foodie 是一套本地优先的主动式学术研究流水线。"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        data = json.loads(body) if body else {}

        # Pull system + user message content for prompt-keyword routing
        messages = data.get("messages", [])
        user_content = "\n".join(
            m.get("content", "")
            for m in messages
            if m.get("role") in ("system", "user")
        )

        reply = _route(user_content)
        resp = {
            "id": "mock-1",
            "object": "chat.completion",
            "created": 1700000000,
            "model": MOCK_MODEL,
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": reply}, "finish_reason": "stop"}
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
        payload = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        # Lightweight /models endpoint for is_reachable()
        if self.path.rstrip("/") in ("/v1/models", "/models"):
            resp = {"object": "list", "data": [{"id": MOCK_MODEL, "object": "model"}]}
        else:
            resp = {"status": "ok"}
        payload = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        print(f"[mock-server] {fmt % args}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="Start a mock OpenAI-compatible server")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8199)
    args = ap.parse_args()
    srv = HTTPServer((args.host, args.port), Handler)
    print(f"[mock-server] listening on http://{args.host}:{args.port} (PID {__import__('os').getpid()})", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()
    print("[mock-server] stopped", flush=True)


if __name__ == "__main__":
    main()

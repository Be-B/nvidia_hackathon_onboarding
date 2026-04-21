"""
NIM Reasoning (Thinking Mode) 예제
- enable_thinking으로 단계별 추론 과정 확인
- reasoning_budget으로 추론 토큰 제어
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("NVIDIA_BASE_URL", "http://localhost:8000/v1")
API_KEY = os.environ.get("NVIDIA_API_KEY", "no-key")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

CHAT_MODEL = "nvidia/nemotron-3-nano-30b-a3b"

print("=== 추론 과정 ===\n")
in_answer = False

stream = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[{"role": "user", "content": "닭과 토끼가 합쳐서 20마리, 다리 합계가 56개일 때 각각 몇 마리?"}],
    temperature=1.0,
    max_tokens=16384,
    extra_body={
        "reasoning_budget": 8192,
        "chat_template_kwargs": {"enable_thinking": True},
    },
    stream=True,
)

for chunk in stream:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    reasoning = getattr(delta, "reasoning_content", None)
    content = delta.content

    if reasoning:
        print(reasoning, end="", flush=True)
    elif content:
        if not in_answer:
            print("\n\n=== 최종 답변 ===\n")
            in_answer = True
        print(content, end="", flush=True)

print()

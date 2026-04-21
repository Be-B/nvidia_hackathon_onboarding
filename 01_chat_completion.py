"""
NIM 기본 Chat Completion 예제
- 단일 턴 & 멀티턴 대화
- 스트리밍 / 일반 응답 전환
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("NVIDIA_BASE_URL", "http://localhost:8000/v1")
API_KEY = os.environ.get("NVIDIA_API_KEY", "no-key")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

CHAT_MODEL = "nvidia/nemotron-3-nano-30b-a3b"
# CHAT_MODEL = "nvidia/nemotron-3-super-120b-a12b"  # 고성능

USE_STREAM = True  # False: 일반 응답, True: 스트리밍

# --- 단일 턴 ---
messages = [
    {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
    {"role": "user",   "content": "NIM이 뭐야? 두 문장으로 설명해줘."},
]

if USE_STREAM:
    stream = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages, temperature=0.5, max_tokens=256, stream=True,
    )
    print("Assistant: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
else:
    response = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages, temperature=0.5, max_tokens=256,
    )
    print(response.choices[0].message.content)
    print(f"\n[토큰] 입력={response.usage.prompt_tokens}, 출력={response.usage.completion_tokens}")

# --- 멀티턴 (히스토리 직접 관리) ---
history = [{"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."}]


def chat(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    resp = client.chat.completions.create(
        model=CHAT_MODEL, messages=history, temperature=0.5, max_tokens=256
    )
    reply = resp.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply


print("\nTurn 1:", chat("내 이름은 준호야."))
print("\nTurn 2:", chat("내 이름이 뭐라고 했지?"))

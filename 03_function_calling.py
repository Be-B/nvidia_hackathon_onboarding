"""
NIM Function Calling (Tool Use) 예제
- 도구 정의 → LLM이 호출 판단 → 실행 → 최종 답변
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

# 1. 도구 정의
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "특정 도시의 현재 날씨를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "도시 이름 (예: 서울, 부산, Tokyo)"}
            },
            "required": ["location"],
        },
    },
}]


# 2. 실제 함수 구현 (Mock)
def get_weather(location: str) -> str:
    mock = {"서울": "맑음, 18°C, 습도 55%", "부산": "흐림, 22°C, 습도 70%"}
    return mock.get(location, f"{location}: 정보 없음")


# 3. 1차 요청
messages = [{"role": "user", "content": "서울 날씨가 어때?"}]
response = client.chat.completions.create(
    model=CHAT_MODEL, messages=messages, tools=tools, tool_choice="auto", max_tokens=256,
)
msg = response.choices[0].message

# 4. tool_calls 처리 → 5. 2차 요청
if msg.tool_calls:
    for tool_call in msg.tool_calls:
        fn_args = json.loads(tool_call.function.arguments)
        result = get_weather(**fn_args)
        print(f"[도구 호출] {tool_call.function.name}({fn_args}) → {result}")
        messages.append(msg)
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
    final = client.chat.completions.create(model=CHAT_MODEL, messages=messages, max_tokens=256)
    print(f"\n최종 답변: {final.choices[0].message.content}")
else:
    print(f"답변 (도구 미사용): {msg.content}")

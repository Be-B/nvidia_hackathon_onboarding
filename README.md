# NVIDIA NIM 온보딩

NIM (NVIDIA Inference Microservices)을 사용한 AI 모델 추론 Quick Start 프로젝트.

## 사전 준비

- Python 3.10+
- NVIDIA GPU + Docker + NVIDIA Container Toolkit (온프레미스)
- [NVIDIA Developer 계정](https://developer.nvidia.com/) & API Key

## 설치

```bash
uv sync
```

## .env 설정

```bash
# .env
NVIDIA_API_KEY=nvapi-xxxx...
```

## NIM 컨테이너 실행 (온프레미스)

```bash
source .env
docker login nvcr.io -u '$oauthtoken' -p $NVIDIA_API_KEY

docker run -it --rm --gpus all \
  -e NGC_API_KEY=$NVIDIA_API_KEY \
  -v ~/.cache/nim:/opt/nim/.cache \
  -p 8000:8000 \
  nvcr.io/nim/nvidia/nemotron-3-nano-30b-a3b:latest
```

## 예제 파일

### NIM 기본 (Chat API)

| 파일 | 내용 |
|------|------|
| `01_chat_completion.py` | 단일턴 + 멀티턴 대화, 스트리밍 |
| `02_reasoning.py` | Thinking Mode (추론 과정 출력) |
| `03_function_calling.py` | Function Calling (Tool Use) |
| `nim_quickstart.ipynb` | 위 예제를 한 노트북에서 실행 |

### Track C: NeMo Data Designer (합성 데이터 생성)

| 파일 | 내용 |
|------|------|
| `data_designer_trackc.ipynb` | 한국어 수학 CoT 데이터셋 생성 파이프라인 전체 |
| `scripts/launch_nemotron_super.sh` | Nemotron 3 Super vLLM 실행 (bf16/fp8/nvfp4) |
| `scripts/launch_nemotron_nano.sh` | Nemotron 3 Nano vLLM 실행 (bf16/fp8/nvfp4) |

#### vLLM 실행 (별도 터미널)

```bash
# Nano (단일 GPU)
bash scripts/launch_nemotron_nano.sh bf16

# Super (멀티 GPU)
bash scripts/launch_nemotron_super.sh fp8
```

## 사용 모델

| 모델 | 파라미터 | 활성 파라미터 | 용도 |
|------|---------|-------------|------|
| Nemotron-3-Nano-30B | 31.6B | 3.2B (MoE) | 경량, 빠른 프로토타이핑 |
| Nemotron-3-Super-120B | 120B | 12B (LatentMoE) | 고성능 추론, 복잡한 에이전트 |

## Cloud API 사용 (GPU 없는 경우)

각 예제에서 client 설정을 아래로 교체:

```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)
```

## 참고 자료

- [NIM 공식 문서](https://docs.nvidia.com/nim/)
- [NIM API 레퍼런스](https://docs.api.nvidia.com)
- [NVIDIA API Catalog](https://build.nvidia.com/explore)
- [NeMo Data Designer 문서](https://nvidia-nemo.github.io/DataDesigner/latest/)
- [NeMo Data Designer GitHub](https://github.com/NVIDIA-NeMo/DataDesigner)
- [vLLM 문서](https://docs.vllm.ai)

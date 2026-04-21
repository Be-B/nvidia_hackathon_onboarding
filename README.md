# NVIDIA NIM & NeMo Data Designer 온보딩

Nemotron 해커톤 Track C를 위한 온보딩 프로젝트.
NIM Chat API 기본 예제 + NeMo Data Designer로 한국어 수학 CoT 합성 데이터셋 생성 파이프라인.

## Quick Start (Brev GPU 서버)

모든 작업은 Brev GPU 서버에서 실행합니다.

### Brev 서버 셋업

```bash
# 1. SSH 접속
ssh <brev-서버>

# 2. 클론 & 환경 설정
git clone https://github.com/Be-B/nvidia_hackathon_onboarding.git
cd nvidia_hackathon_onboarding
cp .env.example .env
nano .env  # NVIDIA_API_KEY 입력

# 3. 한 줄로 전부 실행 (vLLM + Jupyter + Curator)
docker-compose up gpu
```

### 접속 방법

Brev 대시보드에서 포트 8888을 Shareable URL로 등록하면 브라우저에서 바로 접속 가능:

```
https://jupyter0-nyvku23py.brevlab.com
```

또는 SSH 포트 포워딩:

```bash
# 맥 터미널에서 실행
ssh -L 8888:localhost:8888 <brev-서버>
```

이후 맥 브라우저에서 `http://localhost:8888` 접속.

### Docker Compose 서비스

| 명령어 | 환경 | 포함 |
|--------|------|------|
| `docker-compose up gpu` | Brev (GPU) | vLLM + Jupyter + Data Designer + Curator |
| `docker-compose up notebook` | 맥 (CPU) | Jupyter + Data Designer (Cloud API) |

## .env 설정

```bash
NVIDIA_API_KEY=nvapi-xxxx...

# Cloud API (맥에서 테스트용)
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# Brev GPU 서버 — docker-compose up gpu 시 자동 설정됨
# 수동 실행 시: NVIDIA_BASE_URL=http://localhost:5000/v1
```

## 프로젝트 구조

```
.
├── .env.example                 # 환경변수 템플릿
├── Dockerfile                   # Docker 이미지 (CPU, 맥용)
├── Dockerfile.gpu               # Docker 이미지 (GPU, Brev용)
├── docker-compose.yaml          # Docker Compose (notebook / gpu / vllm)
├── pyproject.toml               # 의존성 (uv)
├── HACKATHON_INFO.md            # 해커톤 심사 기준 & 제출물 정리
│
├── 01_chat_completion.py        # NIM 기본: 단일턴 + 멀티턴 + 스트리밍
├── 02_reasoning.py              # NIM 기본: Thinking Mode
├── 03_function_calling.py       # NIM 기본: Function Calling (Tool Use)
├── nim_quickstart.ipynb         # 위 예제를 노트북에서 실행
│
├── data_designer_trackc.ipynb   # Track C 전체 파이프라인 (Step 0~7)
└── scripts/
    ├── launch_nemotron_super.sh # vLLM Nemotron 3 Super (수동 실행용)
    ├── launch_nemotron_nano.sh  # vLLM Nemotron 3 Nano (수동 실행용)
    └── setup_brev.sh            # Brev 원클릭 셋업 (Docker 없이 사용 시)
```

## 온보딩 순서

### Step 1: NIM API 익히기

`nim_quickstart.ipynb`를 열어 셀 순서대로 실행:

| 섹션 | 내용 |
|------|------|
| Chat Completion | 기본 대화, 토큰 사용량 확인 |
| 스트리밍 | 실시간 응답 출력 |
| 멀티턴 | 대화 히스토리 관리 |
| Reasoning | Thinking Mode (추론 과정 출력) |
| Function Calling | Tool Use (외부 함수 호출) |

### Step 2: Track C 파이프라인 실행

`data_designer_trackc.ipynb`를 열어 셀 순서대로 실행:

| Step | 내용 | 결과 |
|------|------|------|
| 0 | 환경 설정 & vLLM 연결 | `.env`에서 자동 설정 |
| 1 | 데이터 스키마 정의 | 학년/주제/난이도 + LLM 컬럼 |
| 2 | 미리보기 | 5개 샘플 생성 & 품질 확인 |
| 3 | 대규모 생성 | 30개 (프로덕션: 500+) |
| 4 | LLM Judge 필터링 | 저품질 데이터 제거 |
| 4.5 | NeMo Curator | 중복 제거 + 한국어 필터 |
| 5 | 내보내기 | JSONL + Parquet |

### 생성되는 파일

```
output/
├── korean_math_cot_sft.jsonl      # SFT 학습용 (대화 형식)
└── korean_math_cot_full.parquet   # 전체 데이터셋 (메타데이터 포함)
```

## 수동 실행 (Docker 없이)

Docker 대신 직접 실행할 수도 있습니다:

```bash
# Brev에서 원클릭 셋업
bash scripts/setup_brev.sh

# API 키 입력
nano .env

# 터미널 1: vLLM 실행
bash scripts/launch_nemotron_nano.sh bf16

# 터미널 2: 노트북 실행
uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

## GPU 요구사항

| 모델 | 변형 | 필요 GPU |
|------|------|----------|
| Nemotron 3 Nano (30B) | BF16 | 1x H100/A100 80GB |
| Nemotron 3 Nano (30B) | FP8 | 1x H100 80GB |
| Nemotron 3 Super (120B) | BF16 | 4x H100 80GB |
| Nemotron 3 Super (120B) | FP8 | 2x H100 80GB |

## 참고 자료

- [NIM 공식 문서](https://docs.nvidia.com/nim/)
- [NIM API 레퍼런스](https://docs.api.nvidia.com)
- [NVIDIA API Catalog](https://build.nvidia.com/explore)
- [NeMo Data Designer 문서](https://nvidia-nemo.github.io/DataDesigner/latest/)
- [NeMo Data Designer GitHub](https://github.com/NVIDIA-NeMo/DataDesigner)
- [NeMo Curator 문서](https://docs.nvidia.com/nemo/curator/latest/)
- [vLLM 문서](https://docs.vllm.ai)

# NVIDIA NIM & NeMo Data Designer 온보딩

Nemotron 해커톤 Track C를 위한 온보딩 프로젝트.
NIM Chat API 기본 예제 + NeMo Data Designer로 한국어 수학 CoT 합성 데이터셋 생성 파이프라인.

## Quick Start

### 1. 레포 클론 & 환경 설정

```bash
git clone https://github.com/Be-B/nvidia_hackathon_onboarding.git
cd nvidia_hackathon_onboarding
cp .env.example .env
# .env 파일을 열어 NVIDIA_API_KEY를 본인 키로 변경
```

### 2. 실행 방법 선택

#### Option A: Docker (NeMo Curator 포함, 권장)

```bash
docker-compose up --build
```

브라우저에서 `http://localhost:8888` 접속 → Jupyter Lab에서 노트북 실행.

#### Option B: 로컬 (Mac/Linux, Curator 제외)

```bash
uv sync
uv run jupyter lab
```

### 3. .env 설정

```bash
NVIDIA_API_KEY=nvapi-xxxx...

# Cloud API (맥/GPU 없는 환경)
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# 온프레미스 vLLM (GPU 서버) — 사용 시 위를 주석 처리
# NVIDIA_BASE_URL=http://localhost:8000/v1
```

`.env` 하나로 Cloud API ↔ 로컬 vLLM 전환 가능. 코드 수정 불필요.

## 프로젝트 구조

```
.
├── .env.example                 # 환경변수 템플릿
├── Dockerfile                   # Docker 이미지 (NeMo Curator 포함)
├── docker-compose.yaml          # Docker Compose 설정
├── pyproject.toml               # 의존성 (uv)
├── README.md
├── HACKATHON_INFO.md            # 해커톤 심사 기준 & 제출물 정리
│
├── 01_chat_completion.py        # NIM 기본: 단일턴 + 멀티턴 + 스트리밍
├── 02_reasoning.py              # NIM 기본: Thinking Mode
├── 03_function_calling.py       # NIM 기본: Function Calling (Tool Use)
├── nim_quickstart.ipynb         # 위 예제를 노트북에서 실행
│
├── data_designer_trackc.ipynb   # Track C 전체 파이프라인 (Step 0~7)
└── scripts/
    ├── launch_nemotron_super.sh # vLLM Nemotron 3 Super 실행
    └── launch_nemotron_nano.sh  # vLLM Nemotron 3 Nano 실행
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

## GPU 서버 (Brev) 에서 실행

```bash
# 1. .env에서 로컬 모드로 전환
NVIDIA_BASE_URL=http://localhost:5000/v1

# 2. vLLM으로 Nemotron 배포 (별도 터미널)
bash scripts/launch_nemotron_nano.sh bf16    # 1x H100/A100
bash scripts/launch_nemotron_super.sh fp8    # 2x H100

# 3. 노트북 실행
docker-compose up --build
```

### GPU 요구사항

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

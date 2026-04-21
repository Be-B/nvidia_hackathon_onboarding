#!/usr/bin/env bash
# Brev GPU 서버 원클릭 셋업 스크립트
# 사용법: bash scripts/setup_brev.sh
set -euo pipefail

echo "=== Brev GPU 서버 셋업 시작 ==="

# 1. uv 설치
if ! command -v uv &> /dev/null; then
    echo "[1/5] uv 설치 중..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
else
    echo "[1/5] uv 이미 설치됨"
fi

# 2. Python & 프로젝트 의존성 설치
echo "[2/5] Python & 프로젝트 의존성 설치 중..."
uv sync

# 3. vLLM 설치 (GPU 전용 패키지)
echo "[3/5] vLLM 설치 중 (시간이 좀 걸립니다)..."
uv pip install vllm==0.17.1 torch==2.10.0 flashinfer-python==0.6.4 \
    flashinfer-cubin==0.6.4 'nvidia-cutlass-dsl>=4.4.0.dev1' \
    --extra-index-url https://download.pytorch.org/whl/cu128

# 4. .env 설정
if [ ! -f .env ]; then
    echo "[4/5] .env 파일 생성 중..."
    cp .env.example .env
    sed -i 's|^NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1|# NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1|' .env
    sed -i 's|^# NVIDIA_BASE_URL=http://localhost|NVIDIA_BASE_URL=http://localhost|' .env
    echo "⚠️  .env에 NVIDIA_API_KEY를 입력하세요: nano .env"
else
    echo "[4/5] .env 이미 존재함"
fi

# 5. GPU 확인
echo "[5/5] GPU 확인..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

echo ""
echo "=== 셋업 완료 ==="
echo ""
echo "다음 단계:"
echo "  1. API 키 설정:  nano .env"
echo "  2. vLLM 실행:    bash scripts/launch_nemotron_nano.sh bf16"
echo "  3. 노트북 실행:  uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
echo ""

#!/usr/bin/env bash
# GPU 컨테이너 엔트리포인트: vLLM 백그라운드 + Jupyter 포그라운드
set -euo pipefail

echo "=== vLLM 서버 시작 (백그라운드) ==="
uv run python -m vllm.entrypoints.openai.api_server \
    --model nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 \
    --dtype auto \
    --trust-remote-code \
    --served-model-name nemotron \
    --host 0.0.0.0 \
    --port 5000 &

echo "=== Jupyter Lab 시작 ==="
exec uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

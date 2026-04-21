FROM python:3.10-slim

WORKDIR /app

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 의존성 먼저 복사 (캐시 활용)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# 소스 복사
COPY . .

# Jupyter 포트
EXPOSE 8888

CMD ["uv", "run", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

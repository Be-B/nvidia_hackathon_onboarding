---
name: Brev GPU Server Info
description: Hackathon Brev H100 server details - instance ID, specs, cost
type: project
---

Brev GPU 서버 할당됨 (2026-04-21).

- Instance: jerryisgood-h100-80gib-vram-sxm5
- ID: nyvku23py
- User: baenokyng-0
- Region: montreal-canada-2
- GPU: 1x NVIDIA H100 80GB SXM5
- CPU: 28 cores, 180GB RAM, 850GB storage
- Provider: Hyperstack
- Cost: $2.28/hr
- Status: Running, Shared

**Why:** 해커톤 Track C 파이프라인(vLLM + Data Designer + Curator)을 이 서버에서 실행.
**How to apply:** vLLM Nano BF16 또는 FP8로 배포 가능 (1x H100). Super는 불가 (4x 필요).

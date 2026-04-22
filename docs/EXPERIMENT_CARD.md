# Experiment Card: MD-Retrieval

## task_type
`md_retrieval`

## 목적
질문에 맞는 MD 파일과 근거 문단을 정확히 찾고, grounded answer를 생성하는 retrieval 레이어를 구축한다.

## 핵심 지표
- file_hit_at_1 — top-1 문서 적중률 (0/1)
- file_hit_at_3 — top-3 문서 적중률 (0/1)
- span_recall — 근거 스팬 커버리지 (0~1)
- answer_f1 — 정답 포함 여부 (0/1)

## 평가 실행
```bash
bash eval/run_phase1.sh
bash eval/run_phase2.sh
```

## 평가 모델
- Phase 1: 8개 모델
- Phase 2: Qwen3.6-27B + LFM 모델

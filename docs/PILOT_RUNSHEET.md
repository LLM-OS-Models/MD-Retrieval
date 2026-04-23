# Pilot Run Sheet: MD-Retrieval

## Objective

- generator FT만으로 exact span answer와 formatting 병목을 줄일 수 있는지 확인한다.
- retrieval 문제와 generation 문제를 분리해서 본다.

## Run IDs

- `MD-P0`: corpus 복구 및 oracle split 설계
- `MD-P1`: `Qwen3-4B` extractive generator pilot
- `MD-P2`: `Qwen3-8B` comparator
- `MD-P3`: oracle docs vs retrieved docs ablation

## Dataset Gate

- missing corpus assets `0`
- query / candidate docs / gold docs 분리 저장
- answer style split:
  - extractive
  - compressed

## Model Matrix

| Run ID | Model | Context | Rank | Retrieval Input | Purpose |
|---|---|---:|---:|---|---|
| MD-P1 | `Qwen3-4B` | 4096 | 16 | oracle docs | generation pilot |
| MD-P2 | `Qwen3-8B` | 4096 | 16 | oracle docs | medium comparator |
| MD-P3 | `Qwen3-4B` | 4096 | 16 | retrieved docs | retrieval sensitivity |

## Fixed Decisions

- answer style: extractive 우선
- output contract: `DOC_IDS` + `ANSWER`
- first stage: generator SFT only

## Primary Metrics

- `file_hit_at_3`
- `span_recall`
- `faithfulness`
- `answer_f1`

## Slice Metrics

- oracle docs split
- retrieved docs split
- exact span split
- long doc split

## Accept

- `span_recall >= 0.80`
- `faithfulness >= 0.90`
- oracle split에서 baseline 대비 formatting regression 없음

## Reject

- extractive style보다 paraphrase가 늘어남
- oracle split도 못 버티면 retrieval 이전 단계에서 탈락
- `DOC_IDS` formatting이 흔들림

## Review Questions

1. retrieval miss와 answer generation miss를 명확히 분리할 수 있는가
2. 4B가 exact span behavior를 충분히 유지하는가
3. reranker FT를 generator보다 먼저 해야 하는가

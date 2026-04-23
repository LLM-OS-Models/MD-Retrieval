# Finetuning Plan: MD-Retrieval

## Current State

- 현재 `v0`에서는 문서 본문이 sample 안에 inline으로 들어가 retrieval이 지나치게 쉽다.
- `v1` corpus 자산은 228/228 누락이다.
- 현재 병목은 retrieval보다 exact span style과 answer formatting이다.

## Priority

- 우선순위: 중상
- 이유: corpus 복구 후 generator SFT만으로도 answer 품질을 빠르게 올릴 수 있다.

## Base Models

- Primary: `Qwen/Qwen3-8B`
- Small pilot: `Qwen/Qwen3-4B`
- Comparator: `google/gemma-4-E2B-it`

## Phase 0

1. `corpus/` 전체 문서를 먼저 복구한다.
2. retrieval task와 generation task를 분리한 dataset을 만든다.
   - query -> top-k doc ids
   - query + gold doc -> extractive answer
3. teacher answer는 paraphrase가 아니라 exact span 중심으로 다시 생성한다.
4. `DOC_IDS` 순서와 `ANSWER` 형식을 고정한다.

## Phase 1

- 목표: generator가 exact span을 놓치지 않게 SFT
- 권장 시작점
  - `max_seq_length=4096`
  - `per_device_train_batch_size=2`
  - `gradient_accumulation_steps=4`
  - `learning_rate=1e-4`
  - `lora_r=16`

## Phase 2

- reward 또는 pairwise preference를 붙일 경우 다음을 본다.
  - relevant doc hit
  - exact span overlap
  - unsupported sentence penalty
  - verbosity penalty

## Phase 3

- retrieval encoder / reranker를 따로 미세조정한다.
- 이 프로젝트는 generator FT와 embedding FT를 분리해서 봐야 한다.

## Model Notes

- `Qwen3`는 문서 압축과 exact answer formatting에 안정적이다.
- 이 프로젝트는 reasoning 강화보다 extractive behavior 강화가 더 중요하다.

## Exit Criteria

- `file_hit_at_3 >= 0.95`
- `span_recall >= 0.8`
- `faithfulness >= 0.9`
- `answer_f1 >= 0.7`

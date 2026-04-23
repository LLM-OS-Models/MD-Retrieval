# MD-Retrieval

MD 문서 기반 정보 검색 및 근거 기반 응답(RAG) 평가 트랙.

질문이 주어지면 후보 MD 문서 목록에서 관련 문서를 검색하고, 해당 문서의 구절(span)을 근거로 삼아 정답을 생성하는 능력을 평가한다. Retrieval 단계와 Answer 단계를 분리하여 어느 쪽에 문제가 있는지 진단할 수 있다.

## 평가 메트릭

| 메트릭 | 설명 |
|--------|------|
| `file_hit_at_1` | 첫 번째로 선택한 문서가 정답 문서인지 (0/1) |
| `file_hit_at_3` | 상위 3개 문서 중 정답 문서 포함 여부 (0/1) |
| `span_recall` | gold span 중 모델 응답에 포함된 비율 (0~1) |
| `answer_f1` | gold answer가 모델 응답에 부분문자열로 포함되는지 (0/1) |
| `faithfulness` | 답변의 각 문장이 문서 내용에 근거하는지 비율 (0~1) |

**성공 조건**: `file_hit_at_3 > 0 AND span_recall >= 0.5 AND faithfulness >= 0.5`

**실패 단계**: `retrieval` (문서检索 실패) 또는 `answer` (문서는 찾았으나 답변 불량)

## 샘플 데이터 형식

```json
{
  "sample_id": "md_0001",
  "task_type": "md_retrieval",
  "user_query": "기업 고객 환불 예외 조항이 무엇인지 알려줘.",
  "artifacts": {
    "documents": [
      {"doc_id": "refund_policy_v3.md", "path": "corpus/policies/refund_policy_v3.md"},
      {"doc_id": "enterprise_terms.md", "path": "corpus/contracts/enterprise_terms.md"},
      {"doc_id": "faq.md", "path": "corpus/support/faq.md"}
    ]
  },
  "gold": {
    "relevant_doc_ids": ["enterprise_terms.md"],
    "relevant_spans": ["별도 계약 조항이 우선 적용되며", "일반 환불 규정의 예외를 인정한다"],
    "expected_answer": "기업 고객은 별도 계약 조항이 우선 적용되며..."
  }
}
```

## 모델 출력 형식

모델은 다음 형식으로 응답해야 한다:

```
DOC_IDS: [doc_id1, doc_id2]
ANSWER: 질문에 대한 답변
```

## 프로젝트 구조

```
MD-Retrieval/
├── README.md
├── pyproject.toml          # uv 프로젝트 설정 (llm-os-eval-core 의존)
├── eval/
│   ├── internal/
│   │   └── v0.jsonl        # 평가 데이터셋 (현재 2샘플)
│   └── results/            # 모델별 결과 ({model}_v0.jsonl)
├── tests/
│   └── test_eval.py        # 그레이더 단위 테스트
└── data/                   # SFT 학습 데이터 (선택)
    └── sft/
```

## 실행

```bash
# 의존성 설치
uv sync

# 스키마 검증
llm-os-eval validate eval/internal/v0.jsonl

# 단일 모델 평가 (vLLM 서버 필요)
llm-os-eval run md_retrieval \
  --model Qwen/Qwen3-4B \
  --samples eval/internal/v0.jsonl \
  --output eval/results/Qwen3-4B_v0.jsonl \
  --base-url http://localhost:8001/v1

# 결과 요약
llm-os-eval summarize eval/results/Qwen3-4B_v0.jsonl
```

## 8-GPU 병렬 평가

```bash
# run_phase1.sh: 8개 모델을 8개 GPU에서 동시 실행
bash eval/run_phase1.sh
```

## 벤치마크 결과 (2026-04-23, Round 3)

| 모델 | Size | file_hit_at_3 | span_recall | 성공률 |
|------|------|---------------|-------------|--------|
| Llama-3.1-8B-Instruct | 8B | **100%** | 0% | 0% |
| Qwen2.5-14B-Instruct | 14B | **100%** | 0% | 0% |
| Qwen3-4B | 4B | **100%** | 0% | 0% |
| gemma-4-E2B-it | MoE | **100%** | 0% | 0% |
| Nemotron-Terminal-8B | 8B | 50% | 0% | 0% |
| Qwen3-8B | 8B | 50% | 0% | 0% |
| Qwen3-0.6B | 0.6B | 0% | 0% | 0% |
| gemma-4-31B-it | 31B | 0% | 0% | 0% |

다수 모델이 문서 검색(file_hit_at_3)은 성공하지만, 정확한 span 인용(span_recall)에는 실패한다. 이는 모델이 문서 내용을 의역하기 때문이며, 원문 구절을 직접 인용하는 능력이 부족함을 시사한다.

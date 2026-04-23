# Labeling Guide: MD-Retrieval

## Goal

- retrieval 대상 문서와 answer generation target을 분리해서 저장한다.
- gold answer는 가능하면 exact span 기준으로 유지한다.

## Required Fields

- `query`
- `candidate_doc_paths`
- `gold_doc_paths`
- `gold_answer`
- `answer_style`

## Labeling Rules

- `candidate_doc_paths`와 `gold_doc_paths`를 섞지 않는다.
- gold answer가 source span과 일치하면 `extractive`로 태깅한다.
- 요약형 답변은 `compressed`로 별도 관리한다.
- unsupported 문장은 gold answer에 넣지 않는다.

## Verification

1. candidate docs 존재 확인
2. gold docs 존재 확인
3. answer evidence span 확인
4. `DOC_IDS` 순서 계약 확인
5. answer style 태그 확인

## Common Mistakes

- retrieval hit와 generation correctness를 같은 필드로 섞음
- exact span인데 annotator paraphrase를 gold로 저장
- long doc 샘플을 easy로 둠

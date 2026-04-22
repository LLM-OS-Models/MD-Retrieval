from __future__ import annotations


from pathlib import Path
from unittest.mock import MagicMock

from llm_os_eval.schemas.sample import EvalSample
from llm_os_eval.schemas.result import EvalResult
from llm_os_eval.graders.md_retrieval import MDRetrievalEvaluator

SAMPLES_PATH = Path(__file__).parent.parent / "eval" / "internal" / "v0.jsonl"


def _load_samples():
    samples = []
    with open(SAMPLES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(EvalSample.model_validate_json(line))
    return samples


def _make_runner_mock(response_text=""):
    runner = MagicMock()
    runner.generate.return_value = {
        "text": response_text,
        "tool_calls": [],
        "latency_ms": 100,
        "input_tokens": 10,
        "output_tokens": 20,
    }
    return runner


class TestSchemaValidation:
    def test_jsonl_schema_valid(self):
        samples = _load_samples()
        assert len(samples) >= 2
        for s in samples:
            assert s.task_type == "md_retrieval"
            assert s.difficulty in ("easy", "medium", "hard")
            assert s.user_query


class TestGraderIntegration:
    def setup_method(self):
        self.samples = _load_samples()
        self.runner = _make_runner_mock()
        self.evaluator = MDRetrievalEvaluator(
            runner=self.runner, model_name="test", checkpoint_name="base"
        )

    def test_build_prompt(self):
        for sample in self.samples:
            sys_prompt, user_prompt = self.evaluator.build_prompt(sample)
            assert sample.user_query in user_prompt

    def test_grade_returns_metrics(self):
        sample = self.samples[0]
        self.runner.generate.return_value = {
            "text": "DOC_IDS: [enterprise_terms.md]\nANSWER: 기업 고객은 별도 계약 조항이 우선 적용된다.",
            "tool_calls": [],
            "latency_ms": 100,
            "input_tokens": 10,
            "output_tokens": 20,
        }
        result = self.evaluator.run_one(sample)

        assert "file_hit_at_1" in result.metric_values
        assert "file_hit_at_3" in result.metric_values
        assert "span_recall" in result.metric_values
        assert "answer_f1" in result.metric_values
        assert result.metric_values["file_hit_at_1"] == 1.0
        assert result.metric_values["file_hit_at_3"] == 1.0

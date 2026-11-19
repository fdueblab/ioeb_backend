from app.services.clinical_reproduction import reproduction_gaps


def test_missing_evidence_cannot_pass():
    assert reproduction_gaps({"generated_code": "def main_process(): return 0"})


def test_rule_requires_traceable_source():
    evidence = {"method_type": "score", "population": "adults", "outcome": "score",
                "horizon": "at assessment", "rules": [{"input": "age", "rule": "age >= 60: 1"}]}
    result = {"reproduction": {"evidence": evidence}}
    assert reproduction_gaps(result)

    evidence["rules"][0]["source"] = {"page": 2, "location": "Table 1", "quote": "60 or more"}
    assert reproduction_gaps(result) == []
    evidence["method_type"] = "trained_model"
    assert reproduction_gaps(result)


def test_runtime_verification_replaces_model_claims(tmp_path, monkeypatch):
    from app.services import clinical_algorithm
    from app.services.clinical_reproduction import verify_candidate
    calls = []
    def runner(path, values):
        calls.append((path, values))
        return {"total_score": 1}
    monkeypatch.setattr(clinical_algorithm, "run_isolated", runner)
    result = {"generated_code": "def main_process(age): return {'total_score': 1}",
              "algorithm_spec": {"inputs": [{"name": "age", "type": "integer"}], "output": {"type": "object"}},
              "smoke_input": {"age": 60}, "reproduction": {},
              "test_results": [{"name": "fake clinical validation", "status": "passed"}]}
    assert verify_candidate(result, tmp_path) == {"total_score": 1}
    assert len(calls) == 1
    assert result["reproduction"]["verification"]["clinical_validation"] == "not_performed"
    assert "fake" not in str(result["test_results"])

"""Structural evidence checks; these do not certify medical correctness."""


def verify_candidate(result, folder):
    """Execute the candidate only in the existing restricted clinical runner."""
    from pathlib import Path
    from app.services.clinical_algorithm import normalize_spec, validate_input, validate_output, run_isolated
    code = result.get("generated_code") or ""
    spec = normalize_spec(result.get("algorithm_spec") or {}, code)
    values = validate_input(spec, result.get("smoke_input") or {})
    path = Path(folder) / "candidate.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(code, encoding="utf-8")
    actual = validate_output(spec, run_isolated(path, values))
    result["test_results"] = [
        {"name": "平台输入契约", "status": "passed", "details": "函数签名与输入规格检查通过"},
        {"name": "平台隔离样例运行", "status": "passed", "details": "实际执行通过；不代表独立分值验证或临床有效性"},
    ]
    result["reproduction"]["verification"] = {"basis": "platform_smoke_run", "actual": actual,
                                             "clinical_validation": "not_performed"}
    result["reproduction"]["status"] = "runtime_checked"
    return actual


def reproduction_gaps(result):
    reproduction = result.get("reproduction")
    if not isinstance(reproduction, dict):
        return ["缺少结构化复现证据"]
    evidence = reproduction.get("evidence")
    if not isinstance(evidence, dict):
        return ["缺少论文规则与出处"]
    gaps = list(reproduction.get("gaps") or []) + list(evidence.get("gaps") or [])
    if evidence.get("method_type") not in {"score", "formula"}:
        gaps.append("当前在线流程仅支持明确的评分和公式；训练模型需单独配置")
    for key, label in [("population", "适用人群"), ("outcome", "预测结局"), ("horizon", "时间窗")]:
        if not evidence.get(key):
            gaps.append("缺少" + label)
    rules = evidence.get("rules")
    if not isinstance(rules, list) or not rules:
        gaps.append("未提供可核对的计算规则")
    else:
        for index, rule in enumerate(rules, 1):
            source = rule.get("source", {}) if isinstance(rule, dict) else {}
            if not (isinstance(rule, dict) and rule.get("rule") and rule.get("input")
                    and isinstance(source, dict) and type(source.get("page")) is int
                    and source["page"] > 0 and source.get("location") and source.get("quote")):
                gaps.append(f"第 {index} 条规则缺少内容或有效出处")
    return list(dict.fromkeys(str(g) for g in gaps))

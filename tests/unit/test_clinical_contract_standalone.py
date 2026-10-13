"""Contract checks that run without the optional Flask integration environment."""

import ast
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest


SOURCE = Path(__file__).resolve().parents[2] / "app" / "services" / "clinical_algorithm.py"
TREE = ast.parse(SOURCE.read_text(encoding="utf-8"))
NAMES = {"normalize_spec", "describe_parameters", "validate_input", "validate_output"}
selected = [node for node in TREE.body if isinstance(node, ast.FunctionDef) and node.name in NAMES]
runner = next(ast.literal_eval(node.value) for node in TREE.body
              if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "_RUNNER" for target in node.targets))
namespace = {"ast": ast, "json": json, "math": math, "_TYPES": {"number", "integer", "string", "boolean"}}
exec("class ClinicalAlgorithmError(ValueError): pass", namespace)
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE), "exec"), namespace)


class ClinicalContractTests(unittest.TestCase):
    def test_source_parameters_and_optional_default(self):
        code = "def main_process(age, note=''):\n    return age\n"
        self.assertEqual(namespace["describe_parameters"](code), [
            {"name": "age", "required": True}, {"name": "note", "required": False},
        ])
        spec = {"inputs": [
            {"name": "age", "type": "integer"},
            {"name": "note", "type": "string", "required": False},
        ]}
        self.assertEqual(len(namespace["normalize_spec"](spec, code)["inputs"]), 2)

    def test_reject_optional_without_python_default(self):
        spec = {"inputs": [{"name": "age", "type": "integer", "required": False}]}
        with self.assertRaisesRegex(namespace["ClinicalAlgorithmError"], "默认值"):
            namespace["normalize_spec"](spec, "def main_process(age):\n    return age\n")

    def test_input_size_uses_utf8_bytes(self):
        spec = {"inputs": [{"name": "note", "type": "string", "required": True, "label": "note", "options": []}]}
        with self.assertRaisesRegex(namespace["ClinicalAlgorithmError"], "16 KB"):
            namespace["validate_input"](spec, {"note": "医" * 5500})

    def test_runner_executes_only_submitted_source_and_inputs(self):
        payload = {"code": "def main_process(age):\n    return {'score': age + 1}\n", "inputs": {"age": 41}}
        process = subprocess.run([sys.executable, "-c", runner], input=json.dumps(payload),
                                 text=True, capture_output=True, check=True, timeout=5)
        self.assertEqual(json.loads(process.stdout), {"score": 42})

    def test_output_type_is_enforced(self):
        spec = {"output": {"type": "object"}}
        self.assertEqual(namespace["validate_output"](spec, {"score": 1}), {"score": 1})
        with self.assertRaisesRegex(namespace["ClinicalAlgorithmError"], "类型不一致"):
            namespace["validate_output"](spec, 1)


if __name__ == "__main__":
    unittest.main()

import ast
import re
from typing import List, Tuple


class CodeStandardIssue:
    """代码规范问题类"""

    def __init__(self, line: int, message: str, severity: str = "error"):
        self.line = line
        self.message = message
        self.severity = severity  # error, warning, info

    def __str__(self):
        return f"第 {self.line} 行: [{self.severity.upper()}] {self.message}"


def check_function_encapsulation(tree: ast.Module) -> List[CodeStandardIssue]:
    """
    检查代码是否将所有核心功能封装成函数

    Args:
        tree: AST语法树

    Returns:
        List[CodeStandardIssue]: 发现的问题列表
    """
    issues = []

    # 获取函数定义和顶层代码
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    toplevel_code = [
        node
        for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))
    ]

    # 检查顶层执行代码是否太多（超过简单的初始化或main调用）
    executable_nodes = [
        node
        for node in toplevel_code
        if isinstance(node, (ast.Assign, ast.Expr, ast.Call, ast.For, ast.While, ast.If))
    ]

    if len(executable_nodes) > 5:  # 超过5个执行语句认为有问题
        issues.append(
            CodeStandardIssue(1, "代码中存在过多未封装到函数中的执行代码，请将核心逻辑封装为函数")
        )

    # 检查是否存在函数定义
    if not functions:
        issues.append(CodeStandardIssue(1, "未发现任何函数定义，请将核心功能封装为函数"))

    return issues


def check_function_docstrings(tree: ast.Module) -> List[CodeStandardIssue]:
    """
    检查函数是否包含Google风格的详细注释

    Args:
        tree: AST语法树

    Returns:
        List[CodeStandardIssue]: 发现的问题列表
    """
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 检查是否有文档字符串
            docstring = ast.get_docstring(node)
            if not docstring:
                issues.append(CodeStandardIssue(node.lineno, f"函数 '{node.name}' 缺少文档字符串"))
                continue

            # 检查Google风格注释格式
            # 至少应包含函数描述和Args部分
            has_args_section = bool(re.search(r"Args:|Arguments:", docstring))
            has_returns_section = bool(re.search(r"Returns:", docstring))

            arg_count = len(node.args.args)
            has_return = any(isinstance(stmt, ast.Return) and stmt.value for stmt in node.body)

            if arg_count > 0 and not has_args_section:
                issues.append(
                    CodeStandardIssue(
                        node.lineno, f"函数 '{node.name}' 文档缺少Args部分，应使用Google风格注释"
                    )
                )

            if has_return and not has_returns_section:
                issues.append(
                    CodeStandardIssue(
                        node.lineno, f"函数 '{node.name}' 文档缺少Returns部分，应使用Google风格注释"
                    )
                )

    return issues


def check_type_annotations(tree: ast.Module) -> List[CodeStandardIssue]:
    """
    检查函数的输入输出是否包含类型注解

    Args:
        tree: AST语法树

    Returns:
        List[CodeStandardIssue]: 发现的问题列表
    """
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 检查参数类型注解
            for i, arg in enumerate(node.args.args):
                if i == 0 and arg.arg == "self":
                    # 跳过类方法的self参数
                    continue

                if arg.annotation is None:
                    issues.append(
                        CodeStandardIssue(
                            arg.lineno, f"函数 '{node.name}' 的参数 '{arg.arg}' 缺少类型注解"
                        )
                    )

            # 检查返回值类型注解
            has_return_stmt = any(isinstance(stmt, ast.Return) and stmt.value for stmt in node.body)
            if has_return_stmt and node.returns is None:
                issues.append(
                    CodeStandardIssue(node.lineno, f"函数 '{node.name}' 缺少返回值类型注解")
                )

    return issues


def check_code_standards(code: str) -> Tuple[bool, List[CodeStandardIssue]]:
    """
    检查代码是否符合规范要求

    Args:
        code: 源代码字符串

    Returns:
        Tuple[bool, List[CodeStandardIssue]]: 是否通过检查，问题列表
    """
    issues = []

    try:
        tree = ast.parse(code)

        # 运行各项检查
        issues.extend(check_function_encapsulation(tree))
        issues.extend(check_function_docstrings(tree))
        issues.extend(check_type_annotations(tree))

        # 如果有任何问题，则检查不通过
        passed = len(issues) == 0
        return passed, issues

    except SyntaxError as e:
        return False, [CodeStandardIssue(e.lineno, f"语法错误: {str(e)}")]

    except Exception as e:
        return False, [CodeStandardIssue(1, f"检查代码时发生错误: {str(e)}")]


def generate_code_review_report(issues: List[CodeStandardIssue]) -> str:
    """
    生成代码审查报告

    Args:
        issues: 问题列表

    Returns:
        str: 格式化的报告
    """
    if not issues:
        return "代码符合所有规范要求，未发现问题。"

    report = ["代码规范审查发现以下问题：\n"]

    # 按严重程度分组
    by_severity = {"error": [], "warning": [], "info": []}

    for issue in issues:
        by_severity[issue.severity].append(issue)

    # 添加错误
    if by_severity["error"]:
        report.append("错误 (必须修复):")
        for issue in by_severity["error"]:
            report.append(f"  - {issue}")

    # 添加警告
    if by_severity["warning"]:
        report.append("\n警告 (建议修复):")
        for issue in by_severity["warning"]:
            report.append(f"  - {issue}")

    # 添加信息
    if by_severity["info"]:
        report.append("\n提示:")
        for issue in by_severity["info"]:
            report.append(f"  - {issue}")

    return "\n".join(report)

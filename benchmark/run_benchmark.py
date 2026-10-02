import argparse
import ast
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from tasks.coding_tasks import TASKS


def extract_code(output: str) -> str:
    """
    Extract Python function code from llama-cli output.
    """

    # 1. Prefer Python code block:
    # ```python
    # def ...
    # ```
    match = re.search(
        r"```(?:python|py)?\s*(.*?)```",
        output,
        re.DOTALL | re.IGNORECASE,
    )

    if match:
        code = match.group(1).strip()

    else:
        # 2. If no code block, find the first line starting with "def "
        lines = output.splitlines()

        start = None

        for i, line in enumerate(lines):
            if line.strip().startswith("def "):
                start = i
                break

        if start is None:
            return output.strip()

        code = "\n".join(lines[start:]).strip()

    # 3. Remove llama-cli output after generated code
    cleaned_lines = []

    for line in code.splitlines():
        stripped = line.strip()

        # llama-cli timing
        if stripped.startswith("[ Prompt:"):
            break

        # llama-cli exit message
        if stripped == "Exiting...":
            break

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def run_llama(
    model_path: str,
    prompt: str,
    threads: int = 8,
    ngl: int = 0,
    max_tokens: int = 1024,
) -> tuple[str, float]:
    """
    Run llama-cli and return:

        generated_text,
        generation_speed_tokens_per_sec
    """

    command = [
        "llama-cli",
        "-m",
        model_path,
        "-p",
        prompt,
        "--temp",
        "0",
        "-n",
        str(max_tokens),
        "-t",
        str(threads),
        "-ngl",
        str(ngl),
        "--single-turn",
        "--no-display-prompt",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"llama-cli failed:\n{result.stderr}"
        )

    # Example:
    #
    # [ Prompt: 1121.6 t/s | Generation: 69.7 t/s ]
    #
    # We want Generation speed.

    timing_output = result.stdout + "\n" + result.stderr

    tokens_per_sec = 0.0

    match = re.search(
        r"\[\s*Prompt:\s*[\d.,]+\s*t/s\s*\|\s*"
        r"Generation:\s*([\d.,]+)\s*t/s\s*\]",
        timing_output,
        re.IGNORECASE,
    )

    if match:
        speed_text = match.group(1).replace(",", ".")
        tokens_per_sec = float(speed_text)

    return result.stdout, tokens_per_sec


# -----------------------------------------------------------------------------
# Isolated Test Runner Script (Executed via Subprocess for Safety & Timeout)
# -----------------------------------------------------------------------------
RUNNER_SCRIPT = r"""
import ast
import json
import sys

def execute():
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(json.dumps({"passed": 0, "total": 0, "details": [f"TEST_RUNNER_ERROR: {e}"]}))
        return

    code = data["code"]
    tests = data["tests"]

    # 1. Parse tests to get total assert count first
    try:
        test_tree = ast.parse(tests)
        assert_nodes = [node for node in test_tree.body if isinstance(node, ast.Assert)]
        total_tests = len(assert_nodes)
    except Exception as exc:
        print(json.dumps({"passed": 0, "total": 0, "details": [f"TEST_SYNTAX_ERROR: {exc}"]}))
        return

    if total_tests == 0:
        print(json.dumps({"passed": 0, "total": 0, "details": ["NO_ASSERT_TESTS_FOUND"]}))
        return

    # 2. Parse and validate generated code syntax
    try:
        code_tree = ast.parse(code)
    except SyntaxError as exc:
        # Crucial fix: return 0 passed out of total_tests instead of (0, 0)
        details = [f"SYNTAX_ERROR: {exc}"] + [f"TEST {i+1}: FAIL - SyntaxError" for i in range(total_tests)]
        print(json.dumps({"passed": 0, "total": total_tests, "details": details}))
        return

    # 3. Execute generated code in isolated namespace
    namespace = {}
    try:
        compiled_code = compile(code_tree, "", "exec")
        exec(compiled_code, namespace)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        details = [f"TEST {i+1}: FAIL - {error}" for i in range(total_tests)]
        print(json.dumps({"passed": 0, "total": total_tests, "details": details}))
        return

    # 4. Evaluate each assert independently
    passed_count = 0
    details = []

    for index, assert_node in enumerate(assert_nodes, start=1):
        try:
            expr = ast.Expression(body=assert_node.test)
            compiled_test = compile(expr, f"", "eval")
            result = eval(compiled_test, namespace)
            if result:
                passed_count += 1
                details.append(f"TEST {index}: PASS")
            else:
                details.append(f"TEST {index}: FAIL - assertion returned False")
        except Exception as exc:
            details.append(f"TEST {index}: FAIL - {type(exc).__name__}: {exc}")

    print(json.dumps({"passed": passed_count, "total": total_tests, "details": details}))

if __name__ == "__main__":
    execute()
"""


def run_tests(
    code: str,
    tests: str,
    timeout_sec: int = 5,
) -> tuple[int, int, list[str]]:
    """
    Run generated code against every assert in a separate subprocess with timeout.
    """
    # Pre-calculate total tests from tests string for fallback
    fallback_total = 0
    try:
        tree = ast.parse(tests)
        fallback_total = sum(1 for node in tree.body if isinstance(node, ast.Assert))
    except Exception:
        pass

    with tempfile.TemporaryDirectory() as tmpdir:
        input_data = {"code": code, "tests": tests}
        input_file = Path(tmpdir) / "payload.json"
        runner_file = Path(tmpdir) / "runner.py"

        input_file.write_text(json.dumps(input_data), encoding="utf-8")
        runner_file.write_text(RUNNER_SCRIPT, encoding="utf-8")

        try:
            proc = subprocess.run(
                [sys.executable, str(runner_file), str(input_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout_sec,
            )

            if proc.returncode != 0:
                return (
                    0,
                    fallback_total,
                    [f"CRASH_ERROR: {proc.stderr.strip()}"],
                )

            data = json.loads(proc.stdout.strip())
            return (data["passed"], data["total"], data["details"])

        except subprocess.TimeoutExpired:
            return (
                0,
                fallback_total,
                [f"TIMEOUT_ERROR: Execution exceeded {timeout_sec}s"],
            )
        except Exception as e:
            return (
                0,
                fallback_total,
                [f"RUNNER_EXCEPTION: {e}"],
            )


def benchmark_model(
    model_name: str,
    model_path: str,
    output_dir: Path,
    threads: int = 8,
    ngl: int = 0,
    max_tokens: int = 1024,
):
    print()
    print("=" * 70)
    print(f"MODEL  : {model_name}")
    print(f"PATH   : {model_path}")
    print(f"CONFIG : -t {threads} | -ngl {ngl} | -n {max_tokens}")
    print("=" * 70)

    results = []

    model_output_dir = output_dir / model_name

    model_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for task in TASKS:

        task_id = task["id"]
        task_name = task["name"]

        print(
            f"\n[{task_id}/{len(TASKS)}] "
            f"{task_name}"
        )

        tokens_per_sec = 0.0

        try:

            # -------------------------------------------------
            # 1. Run LLM với cấu hình cố định
            # -------------------------------------------------

            raw_output, tokens_per_sec = run_llama(
                model_path,
                task["prompt"],
                threads=threads,
                ngl=ngl,
                max_tokens=max_tokens,
            )

            # -------------------------------------------------
            # 2. Extract generated Python code
            # -------------------------------------------------

            code = extract_code(raw_output)

            # -------------------------------------------------
            # 3. Save generated code
            # -------------------------------------------------

            code_file = (
                model_output_dir
                / f"{task_id:02d}_{task_name}.py"
            )

            code_file.write_text(
                code,
                encoding="utf-8",
            )

            # -------------------------------------------------
            # 4. Run individual tests (đã có timeout & subprocess)
            # -------------------------------------------------

            (
                test_passed,
                test_total,
                test_details,
            ) = run_tests(
                code,
                task["tests"],
                timeout_sec=5,
            )

            # -------------------------------------------------
            # 5. Calculate task pass rate
            # -------------------------------------------------

            if test_total > 0:
                task_pass_rate = (
                    test_passed
                    / test_total
                    * 100
                )
            else:
                task_pass_rate = 0.0

            # A task is considered fully passed
            # only when ALL tests pass.

            if (
                test_total > 0
                and test_passed == test_total
            ):
                status = "PASS"
            else:
                status = "FAIL"

            message = "; ".join(
                test_details
            )

        except Exception as exc:

            code = ""

            code_file = (
                model_output_dir
                / f"{task_id:02d}_{task_name}.py"
            )

            code_file.write_text(
                "",
                encoding="utf-8",
            )

            status = "ERROR"

            message = str(exc)[:500]

            test_passed = 0

            # SỬA LỖI MẪU SỐ: Đếm số lượng assert thực tế để tính phạt đúng
            try:
                task_tree = ast.parse(task["tests"])
                test_total = sum(
                    1
                    for node in task_tree.body
                    if isinstance(node, ast.Assert)
                )
            except Exception:
                test_total = 0

            task_pass_rate = 0.0
            test_details = [f"TASK_ERROR: {message}"]

        # -----------------------------------------------------
        # Print task result
        # -----------------------------------------------------

        print(
            f"    Tests : "
            f"{test_passed}/{test_total}"
        )

        print(
            f"    Rate  : "
            f"{task_pass_rate:.1f}%"
        )

        print(
            f"    Status: {status}"
        )

        print(
            f"    Speed : "
            f"{tokens_per_sec:.2f} tokens/s"
        )

        # Show failed test details
        if status != "PASS":

            failed_tests = [
                detail
                for detail in test_details
                if "FAIL" in detail or "ERROR" in detail
            ] if "test_details" in locals() else []

            for detail in failed_tests[:5]:
                print(
                    f"    {detail}"
                )

        # -----------------------------------------------------
        # Save result
        # -----------------------------------------------------

        results.append(
            {
                "task_id": task_id,
                "task": task_name,
                "status": status,
                "test_passed": test_passed,
                "test_total": test_total,
                "test_pass_rate": task_pass_rate,
                "tokens_per_sec": tokens_per_sec,
                "details": message,
            }
        )

    # =========================================================
    # Overall statistics
    # =========================================================

    # Number of fully passed tasks
    fully_passed_tasks = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    task_pass_rate = (
        fully_passed_tasks
        / len(TASKS)
        * 100
    ) if TASKS else 0.0

    # Total test cases
    total_tests = sum(
        result["test_total"]
        for result in results
    )

    total_test_passed = sum(
        result["test_passed"]
        for result in results
    )

    # Overall test-case pass rate
    if total_tests > 0:
        overall_test_pass_rate = (
            total_test_passed
            / total_tests
            * 100
        )
    else:
        overall_test_pass_rate = 0.0

    # Average generation speed
    valid_speeds = [
        result["tokens_per_sec"]
        for result in results
        if result["tokens_per_sec"] > 0
    ]

    if valid_speeds:
        average_tokens_per_sec = (
            sum(valid_speeds)
            / len(valid_speeds)
        )
    else:
        average_tokens_per_sec = 0.0

    # =========================================================
    # Print summary
    # =========================================================

    print()

    print("-" * 70)

    print(f"MODEL: {model_name}")

    print(
        f"Fully passed tasks : "
        f"{fully_passed_tasks}/{len(TASKS)}"
    )

    print(
        f"Task pass rate     : "
        f"{task_pass_rate:.1f}%"
    )

    print(
        f"Test cases passed  : "
        f"{total_test_passed}/{total_tests}"
    )

    print(
        f"Overall test rate  : "
        f"{overall_test_pass_rate:.1f}%"
    )

    print(
        f"Average speed      : "
        f"{average_tokens_per_sec:.2f} tokens/s"
    )

    print("-" * 70)

    return (
        results,
        fully_passed_tasks,
        task_pass_rate,
        total_test_passed,
        total_tests,
        overall_test_pass_rate,
        average_tokens_per_sec,
    )


def save_results(
    results,
    output_file: Path,
):
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "task_id",
                "task",
                "status",
                "test_passed",
                "test_total",
                "test_pass_rate",
                "tokens_per_sec",
                "details",
            ],
        )

        writer.writeheader()

        writer.writerows(results)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Day 3 coding benchmark "
            "for local LLMs."
        )
    )

    parser.add_argument(
        "--model-name",
        required=True,
        help=(
            "Short model name used "
            "for result folders."
        ),
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to GGUF model.",
    )

    parser.add_argument(
        "--output",
        default="results",
        help="Output directory.",
    )

    args = parser.parse_args()

    output_dir = Path(
        args.output
    )

    (
        results,
        fully_passed_tasks,
        task_pass_rate,
        total_test_passed,
        total_tests,
        overall_test_pass_rate,
        average_tokens_per_sec,
    ) = benchmark_model(
        args.model_name,
        args.model,
        output_dir,
    )

    result_file = (
        output_dir
        / f"{args.model_name}_results.csv"
    )

    save_results(
        results,
        result_file,
    )

    print()

    print(
        f"Results saved to: "
        f"{result_file}"
    )

    print(
        f"Task pass rate: "
        f"{task_pass_rate:.1f}%"
    )

    print(
        f"Overall test pass rate: "
        f"{overall_test_pass_rate:.1f}%"
    )


if __name__ == "__main__":
    main()
    
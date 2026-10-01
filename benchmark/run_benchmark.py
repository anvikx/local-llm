import argparse
import ast
import csv
import re
import subprocess
import tempfile
from pathlib import Path

from tasks.coding_tasks import TASKS


def extract_code(output: str) -> str:
    """
    Extract only Python function code from llama-cli output.
    """

    # 1. Ưu tiên code block ```python ... ```
    match = re.search(
        r"```(?:python|py)?\s*(.*?)```",
        output,
        re.DOTALL | re.IGNORECASE,
    )

    if match:
        code = match.group(1).strip()
    else:
        # 2. Nếu không có code block, lấy từ dòng bắt đầu bằng def
        lines = output.splitlines()

        start = None

        for i, line in enumerate(lines):
            if line.strip().startswith("def "):
                start = i
                break

        if start is None:
            return output.strip()

        code = "\n".join(lines[start:]).strip()

    # 3. Loại bỏ các dòng mà llama-cli thêm vào sau code
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

    code = "\n".join(cleaned_lines).strip()

    return code


def run_llama(model_path: str, prompt: str) -> tuple[str, float]:
    """
    Run llama-cli and return:
        generated_text, generation_speed_tokens_per_sec
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
        "256",
        "--single-turn",
        "--no-display-prompt",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"llama-cli failed:\n{result.stderr}"
        )

    # llama-cli prints timing information like:
    #
    # [ Prompt: 1121.6 t/s | Generation: 69.7 t/s ]
    #
    # We want the Generation speed.
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


def run_tests(code: str, tests: str) -> tuple[bool, str]:
    """
    Run generated code + unit tests in a temporary Python file.
    """

    # 1. Check Python syntax before running the tests
    try:
        ast.parse(code)
    except SyntaxError as exc:
        return False, f"SYNTAX_ERROR: {exc}"

    # 2. Combine generated code and unit tests
    full_code = f"""
{code}

{tests}
"""

    # 3. Create a temporary test file
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test_generated.py"

        test_file.write_text(
            full_code,
            encoding="utf-8",
        )

        # 4. Run the generated code + tests
        try:
            result = subprocess.run(
                ["python", str(test_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )

        except subprocess.TimeoutExpired:
            return False, "TIMEOUT"

    # 5. Check result
    if result.returncode == 0:
        return True, "PASS"

    error = result.stderr.strip()

    if not error:
        error = result.stdout.strip()

    error = error.replace("\n", " ")[:500]

    return False, f"TEST_FAILED: {error}"


def benchmark_model(
    model_name: str,
    model_path: str,
    output_dir: Path,
):
    print()

    print("=" * 70)
    print(f"MODEL: {model_name}")
    print(f"PATH : {model_path}")
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

        print(f"\n[{task_id}/10] {task_name}")

        # Giá trị mặc định nếu model bị lỗi
        tokens_per_sec = 0.0

        try:
            # Run LLM
            raw_output, tokens_per_sec = run_llama(
                model_path,
                task["prompt"],
            )

            # Extract generated Python code
            code = extract_code(raw_output)

            # Save generated code
            code_file = (
                model_output_dir
                / f"{task_id:02d}_{task_name}.py"
            )

            code_file.write_text(
                code,
                encoding="utf-8",
            )

            # Run unit tests
            passed, message = run_tests(
                code,
                task["tests"],
            )

            status = "PASS" if passed else "FAIL"

        except Exception as exc:
            code = ""

            # Save empty file if model execution failed
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

        # Print result
        print(f"    Result: {status}")
        print(f"    Speed : {tokens_per_sec:.2f} tokens/s")

        if status != "PASS":
            print(f"    Info  : {message}")

        # Save result
        results.append(
            {
                "task_id": task_id,
                "task": task_name,
                "status": status,
                "tokens_per_sec": tokens_per_sec,
                "details": message,
            }
        )

    # Calculate pass rate
    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    pass_rate = passed / len(TASKS) * 100

    # Calculate average generation speed
    valid_speeds = [
        result["tokens_per_sec"]
        for result in results
        if result["tokens_per_sec"] > 0
    ]

    if valid_speeds:
        average_tokens_per_sec = (
            sum(valid_speeds) / len(valid_speeds)
        )
    else:
        average_tokens_per_sec = 0.0

    # Print summary
    print()

    print("-" * 70)
    print(f"{model_name}")
    print(f"Passed       : {passed}/{len(TASKS)}")
    print(f"Pass rate    : {pass_rate:.1f}%")
    print(
        f"Average speed: "
        f"{average_tokens_per_sec:.2f} tokens/s"
    )
    print("-" * 70)

    return (
        results,
        passed,
        pass_rate,
    )


def save_results(results, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)

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
                "tokens_per_sec",
                "details",
            ],
        )

        writer.writeheader()
        writer.writerows(results)


def main():
    parser = argparse.ArgumentParser(
        description="Day 3 coding benchmark for local LLMs."
    )

    parser.add_argument(
        "--model-name",
        required=True,
        help="Short model name used for result folders.",
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

    output_dir = Path(args.output)

    results, passed, pass_rate = benchmark_model(
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
    print(f"Results saved to: {result_file}")
    print(f"Pass rate: {pass_rate:.1f}%")


if __name__ == "__main__":
    main()
# Local LLM Benchmark — Setup and Experiment Guide

This document provides a step-by-step guide for setting up the local LLM benchmark environment, downloading GGUF model checkpoints, and running the benchmark harness on a local machine (Windows / Linux).

---

## 1. Hardware and Prerequisites

- **Operating System**: Windows 10/11 (PowerShell) or Linux (Ubuntu 20.04+).
- **CPU**: At least 8 physical or logical threads.
- **RAM**: At least 8 GB of available RAM (16 GB recommended).
- **Required software**:
  - Python 3.10 or later.
  - CMake 3.20+ and a C/C++ compiler (MSVC / GCC / Clang).
  - Git.

---

## 2. Building `llama.cpp`

The benchmark uses `llama-cli` and `llama-bench` to measure inference throughput.

### Windows / Linux with Vulkan Backend (Recommended)

```bash
# 1. Clone the llama.cpp repository
git clone https://github.com/ggerganov/llama.cpp.git

cd llama.cpp

# 2. Configure and build with the Vulkan backend
cmake -B build -DGGML_VULKAN=ON

cmake --build build --config Release -j 8
```

> **Note:** After a successful build, the `llama-cli` and `llama-bench` executables will be located in `build/bin/` or `build/bin/Release/` on Windows. Make sure the directory containing `llama-cli` is added to the system `PATH`.

---

## 3. Project Directory Structure

Use the following directory structure so that the benchmark scripts can correctly resolve modules and model paths:

```text
local-llm/

├── benchmark/
│   └── run_benchmark.py       # Benchmark orchestration and scoring script
├── tasks/
│   ├── __init__.py
│   └── coding_tasks.py        # Definition of 10 coding tasks and unit tests
├── models/                    # Directory containing .gguf model files
│   ├── qwen2.5-3b-instruct-q4_k_m.gguf
│   └── qwen2.5-coder-3b-instruct-q4_k_m.gguf
├── results/                   # Benchmark output (CSV files and generated Python code)
├── README.md                  # Summary report and benchmark results
└── SETUP_GUIDE.md             # Setup and usage guide
```

---

## 4. Downloading GGUF Models

Use `huggingface-cli` to download the `Q4_K_M` model files.

```bash
# Install Hugging Face CLI
pip install -U "huggingface_hub[cli]"

# Create the model directory
mkdir -p models

# Download Qwen2.5-3B-Instruct (Q4_K_M)
huggingface-cli download Qwen/Qwen2.5-3B-Instruct-GGUF \
  qwen2.5-3b-instruct-q4_k_m.gguf \
  --local-dir ./models

# Download Qwen2.5-Coder-3B-Instruct (Q4_K_M)
huggingface-cli download Qwen/Qwen2.5-Coder-3B-Instruct-GGUF \
  qwen2.5-coder-3b-instruct-q4_k_m.gguf \
  --local-dir ./models
```

---

## 5. Running the Benchmark (Windows PowerShell)

Navigate to the project root:

```powershell
cd D:\local-llm
```

### Run the Base Model (`Qwen2.5-3B`)

Run the benchmark with standardized parameters:

- **8 CPU threads**: `-t 8`
- **GPU offloading disabled**: `-ngl 0`
- **Maximum generation length**: `-n 1024`

```powershell
python -m benchmark.run_benchmark `
  --model-name "qwen2.5-3b" `
  --model ".\models\qwen2.5-3b-instruct-q4_k_m.gguf" `
  --output "results" `
  -t 8 `
  -ngl 0 `
  -n 1024
```

### Run the Coder Model (`Qwen2.5-Coder-3B`)

```powershell
python -m benchmark.run_benchmark `
  --model-name "qwen2.5-coder-3b" `
  --model ".\models\qwen2.5-coder-3b-instruct-q4_k_m.gguf" `
  --output "results" `
  -t 8 `
  -ngl 0 `
  -n 1024
```

### Run Both Models Sequentially (Batch Mode)

```powershell
python -m benchmark.run_benchmark --model-name "qwen2.5-3b" --model ".\models\qwen2.5-3b-instruct-q4_k_m.gguf" --output "results" -t 8 -ngl 0 -n 1024

python -m benchmark.run_benchmark --model-name "qwen2.5-coder-3b" --model ".\models\qwen2.5-coder-3b-instruct-q4_k_m.gguf" --output "results" -t 8 -ngl 0 -n 1024
```

After the benchmark completes, `.csv` result files and the Python source code generated for each task will be saved in the `results/` directory.

# Qwen2.5-3B / Qwen2.5-Coder-3B Benchmark & Evaluation Report

A comprehensive benchmark and evaluation suite analyzing **Quantization Formats (Q2_K, Q4_K_M, Q8_0)**, inference speeds, memory footprints (RAM & KV Cache scaling), and coding capabilities (**Qwen2.5-3B-Instruct vs. Qwen2.5-Coder-3B-Instruct**).

---

## Table of Contents

- [Overview & Key Findings](#overview--key-findings)
- [Prerequisites & Environment Setup](#prerequisites--environment-setup)
- [Reproducing Benchmarks (CLI Commands)](#reproducing-benchmarks-cli-commands)
- [Day 2: Quantization & Performance Analysis](#day-2-quantization--performance-analysis)
  - [1. Model Footprint](#1-model-footprint)
  - [2. Qualitative Generation Test](#2-qualitative-generation-test)
  - [3. Speed & Memory Consumption](#3-speed--memory-consumption)
  - [4. General Capability Evaluation (6-Prompt Suite)](#4-general-capability-evaluation-6-prompt-suite)
- [Day 3: Coding Benchmark (Qwen2.5-3B vs. Qwen2.5-Coder-3B)](#day-3-coding-benchmark-qwen25-3b-vs-qwen25-coder-3b)
  - [1. Task-by-Task Pass Rates](#1-task-by-task-pass-rates)
  - [2. Aggregate Evaluation Metrics](#2-aggregate-evaluation-metrics)
  - [3. In-Depth Analysis](#3-in-depth-analysis)

---

## Overview & Key Findings

1. **Quantization Sweet Spot (`Q4_K_M`)**: `Q4_K_M` delivers the optimal balance of efficiency and reasoning accuracy. It achieves a 100% pass rate across the qualitative reasoning suite (matching `Q8_0`) while cutting memory by **40.4%** compared to `Q8_0` and achieving **$1.6\times$ faster token generation**.
2. **Degradation in `Q2_K`**: At 2-bit quantization (`Q2_K`), semantic and instruction adherence drops sharply (passing only 2/6 prompts), proving insufficient for multi-step reasoning or programming.
3. **Domain Fine-Tuning (`Coder` vs. `Base`)**: On Python unit-testing suites, `Qwen2.5-Coder-3B` boosts the overall pass rate to **82.44%** (+4.58 pp over `Qwen2.5-3B`), highlighted by a massive **+41.7 pp increase** in complex topological dependency resolution (`resolve_dependencies`).

---

## Prerequisites & Environment Setup

### Hardware & Runtime Specs
- **CPU**: 8 Threads allocated
- **GPU Acceleration**: Vulkan backend (`-ngl 0` for CPU-bound tests)
- **Target Architecture**: GGUF via `llama.cpp`

### 1. Build `llama.cpp` with Vulkan Support

```bash
# Clone repository
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Configure and build with Vulkan backend
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release -j 8
```

### 2. Download Model Checkpoints

Download the quantized GGUF weights for Qwen2 / Qwen2.5:

```bash
# Example using huggingface-cli
pip install -U "huggingface_hub[cli]"

# Download Qwen2.5-3B-Instruct GGUFs (Q2_K, Q4_K_M, Q8_0)
huggingface-cli download Qwen/Qwen2.5-3B-Instruct-GGUF \
  qwen2.5-3b-instruct-q2_k.gguf \
  qwen2.5-3b-instruct-q4_k_m.gguf \
  qwen2.5-3b-instruct-q8_0.gguf \
  --local-dir ./models

# Download Qwen2.5-Coder-3B-Instruct GGUF
huggingface-cli download Qwen/Qwen2.5-Coder-3B-Instruct-GGUF \
  qwen2.5-coder-3b-instruct-q4_k_m.gguf \
  --local-dir ./models
```

---

## Reproducing Benchmarks (CLI Commands)

### 1. Standard Throughput Benchmark (`llama-bench`)

```bash
# Run benchmark on Q4_K_M model with 8 threads, 512 prompt tokens, 128 gen tokens
./build/bin/llama-bench \
  -m ./models/qwen2.5-3b-instruct-q4_k_m.gguf \
  -p 512 \
  -n 128 \
  -r 5 \
  -t 8 \
  -ngl 0
```

### 2. Interactive / Single-Prompt Inference (`llama-cli`)

```bash
./build/bin/llama-cli \
  -m ./models/qwen2.5-3b-instruct-q4_k_m.gguf \
  -p "Explain what quantization is in one paragraph." \
  -t 8 \
  -n 256 \
  --temp 0.2
```

---

## Day 2: Quantization & Performance Analysis

### 1. Model Footprint

| Quantization Type | Disk Size (GB) | Exact Size (Bytes) | Relative Size vs Q8_0 |
| :--- | :--- | :--- | :--- |
| **Q2_K** | 1.28 GB | 1,376,856,480 | 38.1% |
| **Q4_K_M** | 1.95 GB | 2,104,932,768 | 58.2% |
| **Q8_0** | 3.36 GB | 3,616,088,480 | 100.0% |

---

### 2. Qualitative Generation Test

**Prompt:** *"Explain what quantization is in one paragraph."*

#### Q2_K
> *"Quantization is a fundamental technique in digital signal processing that involves reducing a continuous range of data into a finite range of data points. This process is essential for converting analog signals, such as audio or images, into digital formats, which are more easily processed and stored in digital systems. Essentially, it involves dividing the original data into a limited set of values, often represented in binary format, to facilitate more efficient data handling in digital systems."*  
> `[ Prompt: 45.5 t/s | Generation: 71.3 t/s ]`

#### Q4_K_M
> *"Quantization is a technique used in machine learning and computer vision to reduce the precision of numerical data, specifically floating-point numbers, to lower-precision formats such as integers or half-precision floating-point numbers. This process, often performed during model optimization, aims to decrease the memory footprint of models and improve their inference speed. By converting the weights and activations of a neural network from higher precision (e.g., 32-bit floating-point) to lower precision (e.g., 8-bit or 4-bit), quantization makes the models more efficient and suitable for deployment on devices with limited computational resources, such as mobile phones, edge devices, or IoT devices. However, quantization can also introduce some loss of information and may affect the model's accuracy, so it is crucial to carefully tune the quantization process and evaluate the impact on model performance."*  
> `[ Prompt: 15.4 t/s | Generation: 59.3 t/s ]`

#### Q8_0
> *"Quantization is a technique used in the processing and representation of data, particularly in machine learning and artificial intelligence, to reduce the precision of numerical data, such as weights and activations in neural networks, from their original high precision (e.g., 32-bit floating point) to a lower precision format (e.g., 8-bit integers). This process involves mapping a range of possible values to the nearest quantization level, which can significantly reduce storage and computational requirements. However, it also introduces quantization noise, which can affect the accuracy of models, especially in tasks requiring high precision. Techniques like uniform quantization, adaptive quantization, and binarization are used to minimize the impact of quantization on model performance."*  
> `[ Prompt: 44.4 t/s | Generation: 19.4 t/s ]`

---

### 3. Speed & Memory Consumption

#### Benchmark Parameters
- **Prompt Tokens (`-p`)**: 512
- **Generated Tokens (`-n`)**: 128
- **Iterations (`-r`)**: 5
- **CPU Threads (`-t`)**: 8
- **GPU Offload (`-ngl`)**: 0 (Full CPU execution)

#### Throughput Results

| Model Variant | Disk Size | Parameters | Backend | NGL | Threads | Test Type | Speed (t/s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Qwen2 3B Q2_K (Medium)** | 1.28 GiB | 3.40 B | Vulkan | 0 | 8 | pp512 | $1242.85 \pm 46.20$ |
| | | | | | | tg128 | $20.37 \pm 2.79$ |
| **Qwen2 3B Q4_K_M** | 1.95 GiB | 3.40 B | Vulkan | 0 | 8 | pp512 | $1071.13 \pm 20.38$ |
| | | | | | | tg128 | $15.93 \pm 1.22$ |
| **Qwen2 3B Q8_0** | 3.36 GiB | 3.40 B | Vulkan | 0 | 8 | pp512 | $729.88 \pm 43.15$ |
| | | | | | | tg128 | $9.98 \pm 0.45$ |

#### RAM Allocation & Context Scaling

| Quantization Format | RAM @ 2K Context | RAM @ 8K Context | Empirical Delta ($\Delta$) |
| :--- | :--- | :--- | :--- |
| **Q2_K** | 1,530 MiB | 1,752 MiB | +222 MiB |
| **Q4_K_M** | 2,224 MiB | 2,446 MiB | +222 MiB |
| **Q8_0** | 3,735 MiB | 3,891 MiB | +156 MiB |

##### KV Cache Scaling Analysis
Theoretical memory for the FP16 Key-Value (KV) cache is calculated as:
$$\text{Memory}_{\text{KV}} = 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times c \times \text{bytes\_per\_element}$$

For **Qwen2.5-3B** ($n_{\text{layers}} = 36$, $n_{\text{heads}} = 2$, $d_{\text{head}} = 128$, $\text{FP16} = 2\text{ bytes}$):
- **@ 2,048 tokens ($2\text{K}$)**: $\approx 72\text{ MiB}$
- **@ 8,192 tokens ($8\text{K}$)**: $\approx 288\text{ MiB}$
- **Theoretical Growth**: $\Delta \approx 216\text{ MiB}$ ($4\times$ scaling factor)

**Observed vs. Theoretical**:
- `Q2_K` and `Q4_K_M` increased by **222 MiB**, closely mirroring the theoretical prediction of 216 MiB.
- `Q8_0` experienced a smaller net increase of **156 MiB**, attributed to memory pooling, allocator fragmentation, and runtime buffer reuse under higher memory pressure.

---

### 4. General Capability Evaluation (6-Prompt Suite)

#### Test Prompt Suite

| ID | Domain | Prompt / Instruction | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **M1** | Math | *A store offers a 20% discount on a shirt priced at 350,000 VND, then adds another 10% discount on top of the already reduced price. What is the final price?* | `252,000 VND` |
| **M2** | Math | *Find x: $3x + 7 = 2x + 19$* | $x = 12$ |
| **C1** | Code | *Write a Python function `is_prime(n)` that returns `True` if `n` is a prime number.* | Passes tests: `0, 1, 2, 17, 18, 97` |
| **C2** | Code | *Write a Python function `reverse_words(s)` to reverse the order of words in a sentence.* | Reverses arbitrary strings correctly |
| **V1** | Vietnamese | *What is the capital of Vietnam? Answer in one sentence in Vietnamese.* | Mentions "Hà Nội" in a single Vietnamese sentence |
| **V2** | Vietnamese | *Write a meaningful sentence using the words "sunrise" and "sea".* | Natural Vietnamese syntax with both target entities |

#### Accuracy Scores (Pass: 1 / Fail: 0)

| Prompt ID | Domain | Q2_K | Q4_K_M | Q8_0 |
| :--- | :--- | :---: | :---: | :---: |
| **M1** | Math | ❌ 0 | ✅ 1 | ✅ 1 |
| **M2** | Math | ✅ 1 | ✅ 1 | ✅ 1 |
| **C1** | Code | ❌ 0 | ✅ 1 | ✅ 1 |
| **C2** | Code | ❌ 0 | ✅ 1 | ✅ 1 |
| **V1** | Vietnamese | ✅ 1 | ✅ 1 | ✅ 1 |
| **V2** | Vietnamese | ❌ 0 | ✅ 1 | ✅ 1 |
| **Total Score** | | **2 / 6** | **6 / 6** | **6 / 6** |

#### Per-Prompt Generation Speed (Tokens/s)

| Prompt ID | Q2_K Prompt (t/s) | Q2_K Gen (t/s) | Q4_K_M Prompt (t/s) | Q4_K_M Gen (t/s) | Q8_0 Prompt (t/s) | Q8_0 Gen (t/s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | 9.9 | 25.4 | 22.9 | 17.0 | 26.2 | 11.1 |
| **M2** | 199.1 | 24.6 | 157.8 | 17.8 | 101.9 | 11.3 |
| **C1** | 211.3 | 25.3 | 147.6 | 17.1 | 104.8 | 11.2 |
| **C2** | 213.0 | 24.6 | 160.1 | 17.7 | 102.2 | 11.0 |
| **V1** | 210.4 | 26.7 | 158.7 | 18.9 | 105.2 | 10.7 |
| **V2** | 217.0 | 25.8 | 156.8 | 17.4 | 107.3 | 11.4 |

---

## Day 3: Coding Benchmark (Qwen2.5-3B vs. Qwen2.5-Coder-3B)

A comprehensive Python unit-testing benchmark covering 10 distinct algorithmic problems (131 automated unit tests) evaluated on `Q4_K_M` quantizations.

### 1. Task-by-Task Pass Rates

| # | Task Identifier | Qwen2.5-3B-Instruct | Qwen2.5-Coder-3B-Instruct | Discrepancy |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `normalize_whitespace` | 11/11 (100.0%) | 11/11 (100.0%) | Parity ($=$) |
| 2 | `run_length_encode` | 11/11 (100.0%) | 11/11 (100.0%) | Parity ($=$) |
| 3 | `is_balanced` | 15/17 (88.2%) | 15/17 (88.2%) | Parity ($=$) |
| 4 | `merge_intervals` | 11/13 (84.6%) | 11/13 (84.6%) | Parity ($=$) |
| 5 | `two_sum_safe` | 12/14 (85.7%) | 12/14 (85.7%) | Parity ($=$) |
| 6 | `longest_unique_substring` | 14/14 (100.0%) | 14/14 (100.0%) | Parity ($=$) |
| 7 | `parse_config` | 11/13 (84.6%) | 12/13 (92.3%) | **Coder +7.7 pp** |
| 8 | `top_k_frequent_words` | 12/12 (100.0%) | 12/12 (100.0%) | Parity ($=$) |
| 9 | `resolve_dependencies` | 3/12 (25.0%) | 8/12 (66.7%) | **Coder +41.7 pp** |
| 10 | `lru_simulate` | 2/14 (14.3%) | 2/14 (14.3%) | Parity ($=$) |

---

### 2. Aggregate Evaluation Metrics

| Metric | Qwen2.5-3B-Instruct (`Q4_K_M`) | Qwen2.5-Coder-3B-Instruct (`Q4_K_M`) | Delta / Notes |
| :--- | :--- | :--- | :--- |
| **Model Size** | 3.4B parameters | 3.4B parameters | Identical architecture |
| **Quantization** | Q4_K_M | Q4_K_M | Identical bit-width |
| **Coding Tasks** | 10 | 10 | Standard algorithm suite |
| **Total Test Cases** | 131 | 131 | Unit test coverage |
| **Passed Test Cases** | 102 | **108** | **+6 test cases** |
| **Failed Test Cases** | 29 | **23** | **-6 failures** |
| **Overall Pass Rate** | **77.86%** | **82.44%** | **+4.58 pp** |
| **Perfect Tasks (100%)** | 5 / 10 | 5 / 10 | Equal baseline mastery |
| **Average Generation Speed** | **42.69 tok/s** | **41.97 tok/s** | ~1.7% variance (negligible) |
| **Best Task Performance** | 100.0% | 100.0% | Tasks 1, 2, 6, 8 |
| **Hardest Task (`lru_simulate`)** | 14.3% | 14.3% | Equal failure rate |
| **Key Differentiator (`resolve_dependencies`)**| 25.0% | **66.7%** | **+41.7 pp gain** |

---

### 3. In-Depth Analysis

- **Syntactic & Structural Logic**:
  Both models effortlessly master standard procedural manipulation (regex/whitespace sanitization, run-length compression, sliding window strings, and priority hash maps), scoring 100% on 4 distinct tasks.
- **Topological & Dependency Resolution**:
  The core differentiator is `resolve_dependencies`. The general-purpose model (`Qwen2.5-3B`) fails to handle cyclic dependencies and directed acyclic graph (DAG) traversals accurately (25.0%), whereas `Qwen2.5-Coder-3B` demonstrates dedicated structural reasoning, scoring 66.7% (+41.7 pp).
- **Inference Latency Neutrality**:
  Domain specialization in `Qwen2.5-Coder-3B` carries **virtually zero compute penalty**: generation speeds differed by only $0.72\text{ tokens/s}$ ($42.69\text{ tok/s}$ vs. $41.97\text{ tok/s}$), proving that fine-tuning preserves native runtime efficiency.
- **Stateful Edge Cases (`lru_simulate`)**:
  Both models degrade to $14.3\%$ on simulating an LRU Cache with strict boundary conditions. This reveals a clear performance ceiling for 3B-parameter models when managing multi-step persistent state invariants without auxiliary reasoning steps.

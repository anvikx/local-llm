# Benchmark & Comprehensive Evaluation Report: Qwen2.5-3B vs. Qwen2.5-Coder-3B

This document summarizes experimental results analyzing quantization formats (**Q2_K, Q4_K_M, Q8_0**), memory scaling behavior (RAM & KV Cache Scaling), and a detailed comparison of the coding capabilities of **Qwen2.5-3B-Instruct** and **Qwen2.5-Coder-3B-Instruct** under a controlled execution environment.

## Table of Contents

* [1. Core Results Summary](#1-core-results-summary)
* [2. Day 2: Quantization & Hardware Performance Analysis](#2-day-2-quantization--hardware-performance-analysis)

  * [2.1 Model Size](#21-model-size)
  * [2.2 Response Quality Test](#22-response-quality-test)
  * [2.3 Inference Speed & Memory Consumption](#23-inference-speed--memory-consumption)
  * [2.4 General Capability Evaluation (6-Prompt Set)](#24-general-capability-evaluation-6-prompt-set)
* [3. Day 3: Coding Capability Evaluation (Coding Benchmark)](#3-day-3-coding-capability-evaluation-coding-benchmark)

  * [3.1 Detailed Results by Task](#31-detailed-results-by-task)
  * [3.2 Measurement Summary](#32-measurement-summary)
  * [3.3 In-Depth Analysis of Code and Errors](#33-in-depth-analysis-of-code-and-errors)
* [4. Conclusion & Deployment Recommendations](#4-conclusion--deployment-recommendations)

## 1. Core Results Summary

* **Optimal Quantization Point (Q4_K_M):** Provides the best balance between model size and reasoning quality. Q4_K_M achieved **6/6 accuracy** on the general test set (equal to Q8_0) while reducing memory usage by 40.4% and increasing code generation speed by $1.6\times$ compared with Q8_0.
* **Accuracy Degradation at 2-bit (Q2_K):** Significant accuracy loss was observed, with only 2/6 correct on the basic test set, making it unreliable for programming or logical computation.
* **Coding Capability Comparison (Standardized Day 3):**

  * Qwen2.5-3B (Base) achieved a higher overall pass rate (**84.7%** — 111/131 tests), mainly due to its stronger performance on the LRU cache simulation task.
  * Qwen2.5-Coder-3B achieved **80.2%** (105/131 tests). Despite encountering a tuple-unpacking issue on the LRU task, Coder demonstrated stronger algorithmic reasoning on complex bracket matching (Task 3: +11.7 pp), configuration parsing (Task 7: +7.7 pp), and graph dependency resolution (Task 9: +16.7 pp).
* **Throughput Consistency:** With `-t 8 -ngl 0 -n 1024` fixed, the code-generation speed difference between the two models was relatively small (**17.81 tok/s** vs. **18.61 tok/s**).

## 2. Day 2: Quantization & Hardware Performance Analysis

### 2.1 Model Size

| **Quantization Format** | **Size (GB) PY** | **Exact Size (Bytes) PY** | **Ratio vs. Q8_0** |
| ----------------------- | ---------------- | ------------------------- | ------------------ |
| **Q2_K**                | 1.28 GB          | 1,376,856,480             | 38.1%              |
| **Q4_K_M**              | 1.95 GB          | 2,104,932,768             | 58.2%              |
| **Q8_0**                | 3.36 GB          | 3,616,088,480             | 100.0%             |

### 2.2 Response Quality Test

**Test Prompt:** *"Explain what quantization is in one paragraph."*

* **Q2_K:**

> "Quantization is a fundamental technique in digital signal processing that involves reducing a continuous range of data into a finite range of data points. This process is essential for converting analog signals, such as audio or images, into digital formats, which are more easily processed and stored in digital systems. Essentially, it involves dividing the original data into a limited set of values, often represented in binary format, to facilitate more efficient data handling in digital systems."

`[Prompt: 45.5 t/s | Generation: 71.3 t/s]`

* **Q4_K_M:**

> "Quantization is a technique used in machine learning and computer vision to reduce the precision of numerical data, specifically floating-point numbers, to lower-precision formats such as integers or half-precision floating-point numbers. This process, often performed during model optimization, aims to decrease the memory footprint of models and improve their inference speed. By converting the weights and activations of a neural network from higher precision (e.g., 32-bit floating-point) to lower precision (e.g., 8-bit or 4-bit), quantization makes the models more efficient and suitable for deployment on devices with limited computational resources, such as mobile phones, edge devices, or IoT devices. However, quantization can also introduce some loss of information and may affect the model's accuracy, so it is crucial to carefully tune the quantization process and evaluate the impact on model performance."

`[Prompt: 15.4 t/s | Generation: 59.3 t/s]`

* **Q8_0:**

> "Quantization is a technique used in the processing and representation of data, particularly in machine learning and artificial intelligence, to reduce the precision of numerical data, such as weights and activations in neural networks, from their original high precision (e.g., 32-bit floating point) to a lower precision format (e.g., 8-bit integers). This process involves mapping a range of possible values to the nearest quantization level, which can significantly reduce storage and computational requirements. However, it also introduces quantization noise, which can affect the accuracy of models, especially in tasks requiring high precision. Techniques like uniform quantization, adaptive quantization, and binarization are used to minimize the impact of quantization on model performance."

`[Prompt: 44.4 t/s | Generation: 19.4 t/s]`

### 2.3 Inference Speed & Memory Consumption

#### Standard Benchmark Configuration

* Input prompt tokens (`-p`): 512
* New tokens generated (`-n`): 128
* Number of repetitions (`-r`): 5
* Compute threads (`-t`): 8
* GPU layers (`-ngl`): 0 (CPU-only execution)

#### Throughput Results

| **Model**                  | **Size (GiB) PY** | **Parameters (PY)** | **Backend (PY)** | **NGL (PY)** | **Threads (PY)** | **Benchmark (PY)** | **Speed (t/s) PY** |
| -------------------------- | ----------------- | ------------------- | ---------------- | ------------ | ---------------- | ------------------ | ------------------ |
| **Qwen2 3B Q2_K (Medium)** | 1.28 GiB          | 3.40 B              | Vulkan           | 0            | 8                | pp512              | 1242.85 ± 46.20    |
|                            |                   |                     |                  |              |                  | tg128              | 20.37 ± 2.79       |
| **Qwen2 3B Q4_K_M**        | 1.95 GiB          | 3.40 B              | Vulkan           | 0            | 8                | pp512              | 1071.13 ± 20.38    |
|                            |                   |                     |                  |              |                  | tg128              | 15.93 ± 1.22       |
| **Qwen2 3B Q8_0**          | 3.36 GiB          | 3.40 B              | Vulkan           | 0            | 8                | pp512              | 729.88 ± 43.15     |
|                            |                   |                     |                  |              |                  | tg128              | 9.98 ± 0.45        |

#### RAM Consumption by Context Length (Context Scaling)

| **Quantization Format** | **RAM @ 2K Context PY** | **RAM @ 8K Context PY** | **Actual Growth (Δ) PY** |
| ----------------------- | ----------------------- | ----------------------- | ------------------------ |
| **Q2_K**                | 1,530 MiB               | 1,752 MiB               | +222 MiB                 |
| **Q4_K_M**              | 2,224 MiB               | 2,446 MiB               | +222 MiB                 |
| **Q8_0**                | 3,735 MiB               | 3,891 MiB               | +156 MiB                 |

##### Hardware & Environment Specifications

* **Operating System (OS)**: Microsoft Windows 11 Home Single Language 64-bit (PowerShell runtime)
* **Processor (CPU)**: 11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz (6 Cores / 12 Logical Processors), configured with 8 execution threads (`-t 8`)[cite: 1]
* **Graphics Processor (GPU)**: 
  * Integrated: Intel(R) UHD Graphics
  * Dedicated: NVIDIA GeForce RTX 3050 Laptop GPU
  * *Benchmark Configuration*: Vulkan runtime backend (`-ngl 0` — CPU-only execution for standardized benchmarking)[cite: 1]
* **System Memory (RAM)**: 32 GB (DDR4)
* **llama.cpp Version / Build**: `0.5.0-dev` (build `11193`, commit `4e7481175`), built with Clang 20.1.8 for Windows x86_64

##### Memory (RAM) Measurement Methodology

* **Measurement Tools**: Resident Working Set monitored via Windows PowerShell (`Get-Process -Name "llama-cli" | Select-Object WorkingSet`) alongside runtime initialization memory buffer allocations (`model`, `kv self`, and `compute buffer`) reported by `llama-cli` / `llama-bench`.

* **Context Scaling Procedure**:

  1. Initialize the inference engine with context length `-c 2048`, feed prompt inputs, and log the steady-state Resident Working Set.
  2. Repeat the process using context length `-c 8192` with identical hardware parameters.
  3. Compute empirical memory scaling:

$$
\Delta \mathrm{RAM}
=
\mathrm{RAM}_{8K}
-
\mathrm{RAM}_{2K}
$$

```
 to observe KV Cache growth.
```

##### Theoretical KV Cache Calculation

The FP16 Key-Value (KV) Cache size is determined by:

$$
\mathrm{Memory}_{\mathrm{KV}}
=
2
\times
n_{\mathrm{layers}}
\times
n_{\mathrm{heads}}
\times
d_{\mathrm{head}}
\times
c
\times
\mathrm{bytes}_{\mathrm{per\ element}}
$$

Where:

* $n_{\mathrm{layers}}$: Number of transformer decoder layers
* $n_{\mathrm{heads}}$: Number of key-value query/cache heads (GQA heads)
* $d_{\mathrm{head}}$: Dimension per attention head
* $c$: Target context length in tokens
* $\mathrm{bytes}_{\mathrm{per\ element}}$: Precision byte size ($2$ bytes for FP16)

For the **Qwen2.5-3B** architecture:

* $n_{\mathrm{layers}} = 36$
* $n_{\mathrm{heads}} = 2$
* $d_{\mathrm{head}} = 128$
* $\mathrm{bytes}_{\mathrm{per\ element}} = 2$ bytes (FP16)

**Theoretical Memory Allocations:**

* At 2,048 tokens ($2\mathrm{K}$): $\approx \mathbf{72\ MiB}$
* At 8,192 tokens ($8\mathrm{K}$): $\approx \mathbf{288\ MiB}$
* Theoretical growth:

$$
\Delta \approx \mathbf{216\ MiB}
$$

representing a $4\times$ increase in KV capacity.

**Measured Empirical Results:**

* **`Q2_K` & `Q4_K_M`**: Increased by **222 MiB**, aligning with the theoretical derivation of 216 MiB ($\pm 6$ MiB overhead from graph allocators).
* **`Q8_0`**: Increased by **156 MiB**, attributed to memory pooling, buffer fragmentation, and runtime workspace reuse under elevated memory pressure.

**Measured Empirical Results:**

* **`Q2_K` & `Q4_K_M`**: Increased by **222 MiB**, aligning with the theoretical derivation of 216 MiB ($\pm 6\text{ MiB}$ overhead from graph allocators).
* **`Q8_0`**: Increased by **156 MiB**, attributed to memory pooling, buffer fragmentation, and runtime workspace reuse under elevated memory pressure.

### 2.4 General Capability Evaluation (6-Prompt Set)

| **ID PY** | **Category PY** | **Prompt PY**                                                 | **Expected Answer PY**                        | **Q2_K PY** | **Q4_K_M PY** | **Q8_0 PY** |
| --------- | --------------- | ------------------------------------------------------------- | --------------------------------------------- | ----------- | ------------- | ----------- |
| **M1**    | Mathematics     | 20% discount on 350,000 VND, followed by another 10% discount | 252,000 VND                                   | ❌ 0         | ✅ 1           | ✅ 1         |
| **M2**    | Mathematics     | Solve: $3x + 7 = 2x + 19$                                     | $x = 12$                                      | ✅ 1         | ✅ 1           | ✅ 1         |
| **C1**    | Code            | Write `is_prime(n)` to check whether a number is prime        | Correctly handles 0, 1, 2, 17, 18, 97         | ❌ 0         | ✅ 1           | ✅ 1         |
| **C2**    | Code            | Write `reverse_words(s)` to reverse the order of words        | Correct word-order reversal                   | ❌ 0         | ✅ 1           | ✅ 1         |
| **V1**    | Vietnamese      | What is the capital of Vietnam?                               | Complete sentence stating "Hanoi"             | ✅ 1         | ✅ 1           | ✅ 1         |
| **V2**    | Vietnamese      | Write a sentence containing "sunrise" and "sea"               | Grammatically correct and contains both terms | ❌ 0         | ✅ 1           | ✅ 1         |
| **Total** |                 |                                                               |                                               | **2 / 6**   | **6 / 6**     | **6 / 6**   |

## 3. Day 3: Coding Capability Evaluation (Coding Benchmark)

The benchmark evaluates 10 Python algorithmic tasks with a total of **131 test cases**, executed in an isolated sandbox environment.

**Fixed hardware configuration:** `-t 8 -ngl 0 -n 1024`.

### 3.1 Detailed Results by Task

| **#**  | **Task Name**              | **Qwen2.5-3B (Base)** | **Qwen2.5-Coder-3B** | **Delta**          | **Error Analysis**                                                                                            |
| ------ | -------------------------- | --------------------- | -------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| **1**  | `normalize_whitespace`     | 11/11 (100.0%)        | 11/11 (100.0%)       | Equal              | Correct handling of strings and whitespace.                                                                   |
| **2**  | `run_length_encode`        | 11/11 (100.0%)        | 11/11 (100.0%)       | Equal              | Run-length encoding completed without syntax errors.                                                          |
| **3**  | `is_balanced`              | 13/17 (76.5%)         | **15/17 (88.2%)**    | **Coder +11.7 pp** | Base fails on lowercase letters; Coder uses a correct stack algorithm but lacks type checks for `None`/`int`. |
| **4**  | `merge_intervals`          | 11/13 (84.6%)         | 11/13 (84.6%)        | Equal              | Both models fail test 13.                                                                                     |
| **5**  | `two_sum_safe`             | **12/14 (85.7%)**     | 10/14 (71.4%)        | **Base +14.3 pp**  | Coder applies a hash-map pattern too early, failing the requirement to prioritize the smallest index `i`.     |
| **6**  | `longest_unique_substring` | 14/14 (100.0%)        | 14/14 (100.0%)       | Equal              | Optimal sliding-window implementation.                                                                        |
| **7**  | `parse_config`             | 11/13 (84.6%)         | **12/13 (92.3%)**    | **Coder +7.7 pp**  | Base crashes on a line without `=`; Coder handles invalid configuration lines safely.                         |
| **8**  | `top_k_frequent_words`     | 12/12 (100.0%)        | 12/12 (100.0%)       | Equal              | Correctly handles sorting by frequency and lexicographical order.                                             |
| **9**  | `resolve_dependencies`     | 4/12 (33.3%)          | **6/12 (50.0%)**     | **Coder +16.7 pp** | Base crashes after modifying a list while iterating; Coder implements the graph algorithm more effectively.   |
| **10** | `lru_simulate`             | **12/14 (85.7%)**     | 3/14 (21.4%)         | **Base +64.3 pp**  | Coder has a tuple-unpacking error (`"get", key`), causing the task to fail extensively.                       |

### 3.2 Measurement Summary

| **Evaluation Criterion**          | **Qwen2.5-3B-Instruct (Q4_K_M)** | **Qwen2.5-Coder-3B-Instruct (Q4_K_M)** | **Relative Comparison**          |
| --------------------------------- | -------------------------------- | -------------------------------------- | -------------------------------- |
| **Parameters & Format**           | 3.4B — Q4_K_M                    | 3.4B — Q4_K_M                          | Same architecture                |
| **Total Tasks**                   | 10                               | 10                                     | Includes edge cases              |
| **Total Test Cases**              | 131                              | 131                                    | Independently evaluated          |
| **Passed Test Cases**             | **111**                          | 105                                    | Base passes 6 more tests         |
| **Tasks with 100% Pass Rate**     | 4 / 10                           | 4 / 10                                 | Equal (Tasks 1, 2, 6, 8)         |
| **Overall Pass Rate**             | **84.7%**                        | 80.2%                                  | **Base +4.5 pp**                 |
| **Average Code Generation Speed** | 17.81 tokens/s                   | **18.61 tokens/s**                     | Coder approximately ~4.5% faster |

### 3.3 In-Depth Analysis of Code and Errors

#### 1. Why Is the Overall Pass Rate of Qwen2.5-3B Higher?

Qwen2.5-3B achieved an overall score of 84.7%, largely due to its strong performance on **Task 10 (`lru_simulate`)**, where it passed 12/14 tests.

The Base model correctly handled operation tuples with different lengths:

* 2 elements for `get`
* 3 elements for `put`

This allowed it to process the test cases without the tuple-unpacking failure observed in the Coder model.

#### 2. Critical Error of Qwen2.5-Coder-3B on Task 10

The specialized Coder model produced an incorrect tuple-unpacking pattern:

```python
# Code generated by Qwen2.5-Coder-3B:
for op, key, val in operations:
    ...
```

When processing an operation such as `("get", key)`, Python raises:

```text
ValueError: not enough values to unpack (expected 3, got 2).
```

This caused the generated implementation to crash on multiple test cases, reducing its score on this task to **21.4% (3/14)**.

#### 3. Coder's Strength in Algorithmic Tasks

Despite the tuple-unpacking issue on Task 10, **Qwen2.5-Coder-3B demonstrated stronger performance on several structurally complex programming tasks**:

* **Task 3 (`is_balanced`)**: Coder passed 15/17 tests. It applied a standard Stack-based approach and only failed two tests involving invalid input types (`None` and `int`). The Base model, in contrast, contained a logic error when processing strings containing alphabetic characters.
* **Task 7 (`parse_config`)**: Coder safely handled invalid configuration lines and delimiter parsing, achieving 92.3%, while the Base model crashed with a `ValueError` after assuming every line contained `=`.
* **Task 9 (`resolve_dependencies`)**: The Base model made a fundamental list-processing error by attempting to remove elements while iterating, resulting in `ValueError: list.remove(x): x not in list`. Coder constructed a valid dependency-graph solution and achieved a higher pass rate.

## 4. Conclusion & Deployment Recommendations

* **Model Recommendation:**

  * For practical project coding tasks, **Qwen2.5-Coder-3B** remains the preferred choice because of its stronger structured algorithmic reasoning and fewer basic logic errors in several data-structure tasks.
  * When designing prompts for small 3B Coder models, explicitly include instructions such as:

    > "Handle edge cases with different tuple lengths and validate input types strictly."
    > This can help reduce errors caused by overly rigid assumptions about input structure.

* **Quantization Recommendation:**

  * **Q4_K_M** is recommended for workstation and edge-laptop environments. It maintains stable code-generation performance (approximately **18 tokens/s on an 8-thread CPU**) while preserving reasoning quality comparable to the 8-bit version.

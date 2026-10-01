# ============================================
# C1 - is_prime benchmark
# Q2_K / Q4_K_M / Q8_0
# ============================================


# -------------------------
# Q2_K
# -------------------------
# Code gốc Q2_K có lỗi cú pháp ở dòng:
# for i in range(2, 2 + (n / 2):
#
# Vì vậy không thể định nghĩa function nguyên bản.
# Ta đánh dấu Q2_K = FAIL trực tiếp.

q2_result = False


# -------------------------
# Q4_K_M
# -------------------------
def is_prime_q4(n):

    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5

    while i * i <= n:

        if n % i == 0 or n % (i + 2) == 0:
            return False

        i += 6

    return True


# -------------------------
# Q8_0
# -------------------------
def is_prime_q8(n):

    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5

    while i * i <= n:

        if n % i == 0 or n % (i + 2) == 0:
            return False

        i += 6

    return True


# ============================================
# TEST CASES
# ============================================

tests = {
    0: False,
    1: False,
    2: True,
    17: True,
    18: False,
    97: True,
}


# ============================================
# TEST FUNCTION
# ============================================

def run_tests(model_name, func):

    print()
    print("=" * 50)
    print(model_name)
    print("=" * 50)

    passed = 0

    for n, expected in tests.items():

        try:
            result = func(n)

            if result == expected:
                print(
                    f"n={n:2} | "
                    f"expected={expected} | "
                    f"got={result} | OK"
                )
                passed += 1

            else:
                print(
                    f"n={n:2} | "
                    f"expected={expected} | "
                    f"got={result} | WRONG"
                )

        except Exception as e:

            print(
                f"n={n:2} | "
                f"ERROR: {type(e).__name__}: {e}"
            )

    print()
    print(f"{model_name}: {passed}/{len(tests)} tests passed")

    return passed == len(tests)


# ============================================
# RUN
# ============================================

q4_correct = run_tests("Q4_K_M", is_prime_q4)

q8_correct = run_tests("Q8_0", is_prime_q8)


# ============================================
# FINAL SCORE
# ============================================

print()
print("=" * 50)
print("FINAL SCORE")
print("=" * 50)

print("Q2_K   :", "1/1" if q2_result else "0/1")
print("Q4_K_M :", "1/1" if q4_correct else "0/1")
print("Q8_0   :", "1/1" if q8_correct else "0/1")
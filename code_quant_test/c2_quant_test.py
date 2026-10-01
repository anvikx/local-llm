# ============================================
# C2 - reverse_words benchmark
# Q2_K / Q4_K_M / Q8_0
# ============================================


# -------------------------
# Q2_K
# -------------------------
def reverse_words_q2(s: str):

    words = s.split()

    # Code Q2_K sinh ra:
    # reversed_words = [word[::-1] for word in words]
    #
    # Lưu ý: nó đảo từng WORD,
    # chứ không đảo thứ tự các WORD.
    reversed_words = [word[::-1] for word in words]

    return ' '.join(reversed_words)


# -------------------------
# Q4_K_M
# -------------------------
def reverse_words_q4(s):

    words = s.split()

    reversed_words = words[::-1]

    reversed_sentence = ' '.join(reversed_words)

    return reversed_sentence


# -------------------------
# Q8_0
# -------------------------
def reverse_words_q8(s):

    words = s.split()

    reversed_words = words[::-1]

    reversed_sentence = ' '.join(reversed_words)

    return reversed_sentence


# ============================================
# TEST CASES
# ============================================

tests = {
    "hello world": "world hello",
    "I love Python": "Python love I",
    "one two three": "three two one",
    "hello": "hello",
    "": "",
}


# ============================================
# TEST FUNCTION
# ============================================

def run_tests(model_name, func):

    print()
    print("=" * 60)
    print(model_name)
    print("=" * 60)

    passed = 0

    for s, expected in tests.items():

        try:
            result = func(s)

            if result == expected:
                print(
                    f"input={s!r:25} | "
                    f"expected={expected!r:25} | "
                    f"got={result!r:25} | OK"
                )
                passed += 1

            else:
                print(
                    f"input={s!r:25} | "
                    f"expected={expected!r:25} | "
                    f"got={result!r:25} | WRONG"
                )

        except Exception as e:

            print(
                f"input={s!r:25} | "
                f"ERROR: {type(e).__name__}: {e}"
            )

    print()
    print(f"{model_name}: {passed}/{len(tests)} tests passed")

    return passed == len(tests)


# ============================================
# RUN TESTS
# ============================================

q2_correct = run_tests(
    "Q2_K",
    reverse_words_q2
)

q4_correct = run_tests(
    "Q4_K_M",
    reverse_words_q4
)

q8_correct = run_tests(
    "Q8_0",
    reverse_words_q8
)


# ============================================
# FINAL SCORE
# ============================================

print()
print("=" * 60)
print("FINAL SCORE")
print("=" * 60)

print("Q2_K   :", "1/1" if q2_correct else "0/1")
print("Q4_K_M :", "1/1" if q4_correct else "0/1")
print("Q8_0   :", "1/1" if q8_correct else "0/1")
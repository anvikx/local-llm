TASKS = [
    {
        "id": 1,
        "name": "is_even",
        "prompt": """
Write a Python function called is_even(n).

Return True if n is even and False otherwise.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert is_even(2) is True
assert is_even(3) is False
assert is_even(0) is True
assert is_even(-4) is True
assert is_even(-5) is False
""",
    },

    {
        "id": 2,
        "name": "factorial",
        "prompt": """
Write a Python function called factorial(n).

The function should return n!.

Assume n is a non-negative integer.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120
assert factorial(7) == 5040
""",
    },

    {
        "id": 3,
        "name": "reverse_string",
        "prompt": """
Write a Python function called reverse_string(s).

Return the input string reversed.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert reverse_string("hello") == "olleh"
assert reverse_string("abc") == "cba"
assert reverse_string("") == ""
assert reverse_string("a") == "a"
""",
    },

    {
        "id": 4,
        "name": "count_vowels",
        "prompt": """
Write a Python function called count_vowels(s).

Count the number of vowels in the string.
Count a, e, i, o, u regardless of case.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert count_vowels("hello") == 2
assert count_vowels("HELLO") == 2
assert count_vowels("python") == 1
assert count_vowels("") == 0
assert count_vowels("beautiful") == 5
""",
    },

    {
        "id": 5,
        "name": "find_max",
        "prompt": """
Write a Python function called find_max(numbers).

Return the largest number in the list.

Assume the list contains at least one number.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert find_max([1, 2, 3]) == 3
assert find_max([-1, -5, -2]) == -1
assert find_max([10]) == 10
assert find_max([5, 5, 3]) == 5
""",
    },

    {
        "id": 6,
        "name": "remove_duplicates",
        "prompt": """
Write a Python function called remove_duplicates(numbers).

Return a list containing the values from the input list without duplicates.

Preserve the original order.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert remove_duplicates([1, 2, 2, 3]) == [1, 2, 3]
assert remove_duplicates([1, 1, 1]) == [1]
assert remove_duplicates([]) == []
assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]
""",
    },

    {
        "id": 7,
        "name": "is_palindrome",
        "prompt": """
Write a Python function called is_palindrome(s).

Return True if the string reads the same forward and backward.
Otherwise return False.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert is_palindrome("racecar") is True
assert is_palindrome("hello") is False
assert is_palindrome("") is True
assert is_palindrome("a") is True
assert is_palindrome("level") is True
""",
    },

    {
        "id": 8,
        "name": "fibonacci",
        "prompt": """
Write a Python function called fibonacci(n).

Return the nth Fibonacci number.

Use:
F(0) = 0
F(1) = 1

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert fibonacci(0) == 0
assert fibonacci(1) == 1
assert fibonacci(2) == 1
assert fibonacci(5) == 5
assert fibonacci(10) == 55
""",
    },

    {
        "id": 9,
        "name": "two_sum",
        "prompt": """
Write a Python function called two_sum(nums, target).

Return the indices of two numbers whose sum equals target.

Assume exactly one solution exists.

Return the indices as a list.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
""",
    },

    {
        "id": 10,
        "name": "is_prime",
        "prompt": """
Write a Python function called is_prime(n).

Return True if n is a prime number.
Otherwise return False.

Requirements:
- Return only the function code.
- Do not use imports.
- Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert is_prime(2) is True
assert is_prime(3) is True
assert is_prime(4) is False
assert is_prime(17) is True
assert is_prime(1) is False
assert is_prime(0) is False
assert is_prime(-5) is False
""",
    },
]
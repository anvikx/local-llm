# tasks/coding_tasks.py

TASKS = [
{
        "id": 1,
        "name": "normalize_whitespace",
        "prompt": """
Write a Python function called normalize_whitespace(s).

Normalize whitespace in a string:
- Remove leading and trailing whitespace.
- Replace every consecutive whitespace character with a single space.
- Whitespace includes spaces, tabs, and newlines.
- Return an empty string if the input contains only whitespace.
- If s is not a string, return an empty string.

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert normalize_whitespace("hello   world") == "hello world"
assert normalize_whitespace("  hello   world  ") == "hello world"
assert normalize_whitespace("hello\t\tworld") == "hello world"
assert normalize_whitespace("hello\nworld") == "hello world"
assert normalize_whitespace("  hello \t\n world  ") == "hello world"
assert normalize_whitespace("") == ""
assert normalize_whitespace("   \t\n  ") == ""
assert normalize_whitespace("hello") == "hello"
assert normalize_whitespace("hello  world  test") == "hello world test"
assert normalize_whitespace(None) == ""
assert normalize_whitespace(123) == ""
""",
    },
    {
        "id": 2,
        "name": "run_length_encode",
        "prompt": """
Write a Python function called run_length_encode(s).

Return a run-length encoded representation of the string.

For each consecutive group of identical characters, output the character
followed by the number of occurrences.

Examples:
"aaabbc" -> "a3b2c1"
"abc" -> "a1b1c1"

Rules:
- Return an empty string for an empty input.
- Treat uppercase and lowercase characters as different.
- Do not modify the input.
- If s is not a string, return an empty string.

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert run_length_encode("aaabbc") == "a3b2c1"
assert run_length_encode("abc") == "a1b1c1"
assert run_length_encode("aaaa") == "a4"
assert run_length_encode("") == ""
assert run_length_encode("aabbbaaa") == "a2b3a3"
assert run_length_encode("111122") == "1422"
assert run_length_encode(" ") == " 1"
assert run_length_encode("aAa") == "a1A1a1"
assert run_length_encode("aaAA") == "a2A2"
assert run_length_encode(None) == ""
assert run_length_encode(123) == ""
""",
    },
    {
        "id": 3,
        "name": "is_balanced",
        "prompt": """
Write a Python function called is_balanced(s).

Return True if all parentheses, square brackets, and curly brackets
are correctly balanced and properly nested.

Supported brackets:
()
[]
{}

Ignore all non-bracket characters.

Return False for invalid or incorrectly nested brackets.

Examples:
"([])" -> True
"([)]" -> False

Rules:
- An empty string is considered balanced.
- A string containing no brackets is considered balanced.
- If s is not a string, return False.

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert is_balanced("()") is True
assert is_balanced("([])") is True
assert is_balanced("{[()]}") is True
assert is_balanced("") is True
assert is_balanced("hello") is True
assert is_balanced("([{}])") is True
assert is_balanced("abc(def[ghi])") is True

assert is_balanced("(") is False
assert is_balanced(")") is False
assert is_balanced("([)]") is False
assert is_balanced("((())") is False
assert is_balanced("{[}") is False
assert is_balanced(")(") is False
assert is_balanced("[(])") is False
assert is_balanced("(((())))") is True
assert is_balanced(None) is False
assert is_balanced(123) is False
""",
    },
    {
        "id": 4,
        "name": "merge_intervals",
        "prompt": """
Write a Python function called merge_intervals(intervals).

The input is a list of intervals represented as [start, end].

Requirements:
- Merge all overlapping intervals.
- Return the merged intervals sorted by their start value.
- If an interval has start greater than end, treat it as invalid and ignore it.
- Intervals that only touch at the boundary should be merged.
- An empty input should return [].
- Do not modify the input list.
- If intervals is not a list, return [].
- Ignore malformed intervals that do not contain exactly two numeric values.

Examples:
[[1,3], [2,6], [8,10]] -> [[1,6], [8,10]]
[[1,2], [2,3]] -> [[1,3]]

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert merge_intervals([]) == []

assert merge_intervals(
    [[1, 3], [2, 6], [8, 10], [9, 12]]
) == [[1, 6], [8, 12]]

assert merge_intervals(
    [[1, 2], [2, 3]]
) == [[1, 3]]

assert merge_intervals(
    [[5, 7]]
) == [[5, 7]]

assert merge_intervals(
    [[5, 1], [2, 4], [3, 8]]
) == [[2, 8]]

assert merge_intervals(
    [[1, 1], [1, 1]]
) == [[1, 1]]

assert merge_intervals(
    [[10, 1], [5, 3]]
) == []

assert merge_intervals(
    [[8, 10], [1, 3], [2, 6]]
) == [[1, 6], [8, 10]]

assert merge_intervals(
    [[1, 5], [2, 3], [4, 8]]
) == [[1, 8]]

assert merge_intervals(
    [[1, 2], [3, 4]]
) == [[1, 2], [3, 4]]

assert merge_intervals(None) == []
assert merge_intervals("invalid") == []

assert merge_intervals(
    [[1, 3], [4], [5, 6], ["a", 2], [7, 8, 9]]
) == [[1, 3], [5, 6]]
""",
    },
    {
        "id": 5,
        "name": "two_sum_safe",
        "prompt": """
Write a Python function called two_sum_safe(nums, target).

Return the indices of two distinct elements whose values add up to target.

Requirements:
- Return the first valid pair encountered when scanning from left to right.
- Return the indices as a list [i, j].
- If no pair exists, return [].
- Do not use the same element twice.
- If nums is not a list, return [].
- If target is not an int or float, return [].
- The input list may contain duplicate values.
- Preserve the order of the indices.

Examples:
[2,7,11,15], 9 -> [0,1]
[3,2,4], 6 -> [1,2]
[3,3], 6 -> [0,1]

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert two_sum_safe([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_safe([3, 2, 4], 6) == [1, 2]
assert two_sum_safe([3, 3], 6) == [0, 1]

assert two_sum_safe([1, 2, 3], 100) == []
assert two_sum_safe([1], 2) == []
assert two_sum_safe([], 0) == []

assert two_sum_safe([1, 1, 1], 2) == [0, 1]
assert two_sum_safe([0, 4, 3, 0], 0) == [0, 3]

assert two_sum_safe([1, 5, 3, 7], 8) == [0, 3]
assert two_sum_safe([-1, -2, -3, -4], -5) == [0, 3]

assert two_sum_safe(None, 5) == []
assert two_sum_safe("123", 3) == []
assert two_sum_safe([1, 2, 3], "3") == []
assert two_sum_safe([1, 2, 3], None) == []
""",
    },
    {
        "id": 6,
        "name": "longest_unique_substring",
        "prompt": """
Write a Python function called longest_unique_substring(s).

Return the length of the longest substring that contains no repeated
characters.

Requirements:
- The comparison is case-sensitive.
- Return 0 for an empty string.
- A substring must contain consecutive characters.
- If s is not a string, return 0.

Examples:
"abcabcbb" -> 3
"bbbbb" -> 1
"pwwkew" -> 3

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert longest_unique_substring("") == 0
assert longest_unique_substring("a") == 1
assert longest_unique_substring("abcabcbb") == 3
assert longest_unique_substring("bbbbb") == 1
assert longest_unique_substring("pwwkew") == 3
assert longest_unique_substring("abcdef") == 6
assert longest_unique_substring("abba") == 2
assert longest_unique_substring("aAbB") == 4
assert longest_unique_substring(" ") == 1
assert longest_unique_substring("   ") == 1
assert longest_unique_substring("dvdf") == 3
assert longest_unique_substring("tmmzuxt") == 5
assert longest_unique_substring(None) == 0
assert longest_unique_substring(12345) == 0
""",
    },
    {
        "id": 7,
        "name": "parse_config",
        "prompt": """
Write a Python function called parse_config(text).

Parse a simple configuration string into a dictionary.

Each valid line has the format:
key=value

Rules:
- Ignore empty lines.
- Ignore lines whose first non-whitespace character is '#'.
- Strip whitespace around keys and values.
- A key must be non-empty.
- If a line does not contain '=', ignore the line.
- If a key appears multiple times, the last valid value wins.
- Values may contain '=' characters.
- Do not remove '#' characters from values.
- Preserve the value exactly after stripping leading and trailing whitespace.
- If text is not a string, return {}.

Examples:
"name=Alice\\nage=20" -> {"name": "Alice", "age": "20"}

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert parse_config(
    "name=Alice\\nage=20"
) == {
    "name": "Alice",
    "age": "20",
}

assert parse_config(
    " name = Alice \\n age = 20 "
) == {
    "name": "Alice",
    "age": "20",
}

assert parse_config(
    "# comment\\nname=Alice\\n\\nage=20"
) == {
    "name": "Alice",
    "age": "20",
}

assert parse_config(
    "url=https://example.com?a=1=b"
) == {
    "url": "https://example.com?a=1=b",
}

assert parse_config(
    "name=Alice\\nname=Bob"
) == {
    "name": "Bob",
}

assert parse_config(
    "=invalid\\nvalid=yes\\ninvalid_line"
) == {
    "valid": "yes",
}

assert parse_config("") == {}
assert parse_config("   \\n # hello\\n ") == {}

assert parse_config(None) == {}
assert parse_config(123) == {}

assert parse_config(
    "key=value # not a comment"
) == {
    "key": "value # not a comment",
}

assert parse_config(
    "  key  =  value with spaces  "
) == {
    "key": "value with spaces",
}

assert parse_config(
    "a=1\\n\\nb=2\\n# comment\\nc=3"
) == {
    "a": "1",
    "b": "2",
    "c": "3",
}
""",
    },
    {
        "id": 8,
        "name": "top_k_frequent_words",
        "prompt": """
Write a Python function called top_k_frequent_words(words, k).

Return the k most frequent words.

Sorting rules:
1. Frequency descending.
2. Alphabetical order ascending when frequencies are equal.

Requirements:
- Treat words as case-sensitive.
- If k <= 0, return [].
- If k is larger than the number of unique words, return all unique words.
- If words is not a list, return [].
- Assume every element in words is a string. If an element is not a string,
  ignore that element.
- Do not modify the input list.

Examples:
["i","love","leetcode","i","love","coding"], 2
-> ["i","love"]

["a","b","c"], 2
-> ["a","b"]

Return only the function code.
Do not use imports.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert top_k_frequent_words(
    ["i", "love", "leetcode", "i", "love", "coding"],
    2
) == ["i", "love"]

assert top_k_frequent_words(
    ["a", "b", "c"],
    2
) == ["a", "b"]

assert top_k_frequent_words(
    ["b", "a", "b", "a", "c"],
    3
) == ["a", "b", "c"]

assert top_k_frequent_words(
    ["a", "a", "a"],
    1
) == ["a"]

assert top_k_frequent_words(
    ["a", "b"],
    10
) == ["a", "b"]

assert top_k_frequent_words(
    ["a", "b"],
    0
) == []

assert top_k_frequent_words(
    ["a", "b"],
    -1
) == []

assert top_k_frequent_words([], 3) == []

assert top_k_frequent_words(
    ["A", "a", "A", "b"],
    3
) == ["A", "a", "b"]

assert top_k_frequent_words(None, 2) == []

assert top_k_frequent_words(
    ["b", 123, "a", None, "b", "a"],
    2
) == ["a", "b"]

assert top_k_frequent_words(
    ["z", "y", "x", "z", "y"],
    2
) == ["y", "z"]
""",
    },
    {
        "id": 9,
        "name": "resolve_dependencies",
        "prompt": """
Write a Python function called resolve_dependencies(dependencies).

dependencies is a dictionary where each key is a package name and
its value is a list of packages that must be installed before it.

Return a valid installation order containing every package.

Requirements:
- If multiple packages are available at the same time, choose the
  alphabetically smallest package.
- Packages that only appear as dependencies but not as dictionary keys
  must also be included.
- If there is a dependency cycle, return [].
- If dependencies is not a dictionary, return [].
- If a dependency list is invalid, treat it as an empty list.
- Package names are strings.
- Do not use imports.

Examples:
{
    "app": ["db", "api"],
    "api": ["utils"],
    "db": [],
    "utils": []
}
-> ["db", "utils", "api", "app"]

Return only the function code.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert resolve_dependencies({
    "app": ["db", "api"],
    "api": ["utils"],
    "db": [],
    "utils": [],
}) == ["db", "utils", "api", "app"]

assert resolve_dependencies({
    "b": ["a"],
    "c": ["b"],
    "a": [],
}) == ["a", "b", "c"]

assert resolve_dependencies({
    "app": ["external"],
}) == ["external", "app"]

assert resolve_dependencies({
    "a": ["b"],
    "b": ["a"],
}) == []

assert resolve_dependencies({
    "a": ["b"],
    "b": ["c"],
    "c": ["a"],
}) == []

assert resolve_dependencies({}) == []

assert resolve_dependencies({
    "a": [],
    "b": [],
    "c": [],
}) == ["a", "b", "c"]

assert resolve_dependencies(None) == []
assert resolve_dependencies([]) == []

assert resolve_dependencies({
    "app": ["db", "cache"],
    "db": [],
    "cache": [],
}) == ["cache", "db", "app"]

assert resolve_dependencies({
    "z": ["a"],
    "a": [],
    "m": [],
}) == ["a", "m", "z"]

assert resolve_dependencies({
    "app": ["external_a", "external_b"],
}) == ["external_a", "external_b", "app"]
""",
    },
    {
        "id": 10,
        "name": "lru_simulate",
        "prompt": """
Write a Python function called lru_simulate(capacity, operations).

Simulate a Least Recently Used (LRU) cache.

capacity is the maximum number of key-value pairs.

operations is a list containing tuples:
("put", key, value)
("get", key)

For a "put":
- Insert or update the key.
- Updating an existing key makes it most recently used.
- If the cache exceeds capacity, remove the least recently used key.

For a "get":
- If the key exists, return its value and make it most recently used.
- If the key does not exist, return None.

Return a list containing the results of every "get" operation in order.

Additional rules:
- If capacity <= 0, no values can be stored and every get returns None.
- Ignore malformed operations.
- If capacity is not an integer, return [].
- The key can be any hashable value.
- Do not use imports.
- Do not modify the operations list.

Return only the function code.
Do not access files, network, subprocesses, or the operating system.
""",
        "tests": """
assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("put", "b", 2),
        ("get", "a"),
        ("put", "c", 3),
        ("get", "b"),
        ("get", "c"),
    ],
) == [1, None, 3]

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("put", "b", 2),
        ("put", "a", 10),
        ("put", "c", 3),
        ("get", "b"),
        ("get", "a"),
    ],
) == [None, 10]

assert lru_simulate(
    1,
    [
        ("put", "a", 1),
        ("put", "b", 2),
        ("get", "a"),
        ("get", "b"),
    ],
) == [None, 2]

assert lru_simulate(
    0,
    [
        ("put", "a", 1),
        ("get", "a"),
    ],
) == [None]

assert lru_simulate(
    -1,
    [
        ("put", "a", 1),
        ("get", "a"),
    ],
) == [None]

assert lru_simulate(2, []) == []

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("get", "missing"),
        ("put", "b", 2),
        ("get", "a"),
    ],
) == [None, 1]

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("bad", "x", 99),
        ("get", "a"),
        ("invalid",),
        ("get", "missing"),
    ],
) == [1, None]

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("put", "a", 2),
        ("get", "a"),
    ],
) == [2]

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("put", "b", 2),
        ("get", "a"),
        ("put", "c", 3),
        ("get", "b"),
        ("get", "a"),
        ("get", "c"),
    ],
) == [1, None, 1, 3]

assert lru_simulate(
    2,
    [
        ("put", "a", 1),
        ("put", "b", 2),
        ("put", "c", 3),
        ("get", "a"),
        ("get", "b"),
        ("get", "c"),
    ],
) == [None, None, 3]

assert lru_simulate(
    3,
    [
        ("put", 1, "one"),
        ("put", 2, "two"),
        ("put", 3, "three"),
        ("get", 1),
        ("put", 4, "four"),
        ("get", 2),
        ("get", 3),
        ("get", 4),
    ],
) == ["one", None, "three", "four"]

assert lru_simulate(None, [("get", "a")]) == []

assert lru_simulate(
    2,
    None
) == []
""",
    },
]

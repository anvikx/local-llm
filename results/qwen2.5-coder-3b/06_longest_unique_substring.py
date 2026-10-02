def longest_unique_substring(s):
    if not isinstance(s, str):
        return 0
    
    if not s:
        return 0
    
    max_length = 0
    start = 0
    char_index_map = {}
    
    for end, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= start:
            start = char_index_map[char] + 1
        
        char_index_map[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length
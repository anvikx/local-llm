def run_length_encode(s):
    if not isinstance(s, str):
        return ""
    
    if not s:
        return ""
    
    encoded = ""
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            encoded += s[i - 1] + str(count)
            count = 1
    
    # Add the last group
    encoded += s[-1] + str(count)
    
    return encoded
def normalize_whitespace(s):
    if not isinstance(s, str):
        return ""
    
    # Strip leading and trailing whitespace
    s = s.strip()
    
    # Replace every consecutive whitespace character with a single space
    s = ' '.join(s.split())
    
    return s
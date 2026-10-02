def normalize_whitespace(s):
    if not isinstance(s, str):
        return ""
    s = s.strip()
    s = ' '.join(s.split())
    return s if s else ""
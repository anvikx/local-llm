def parse_config(text):
    if not isinstance(text, str):
        return {}
    
    config = {}
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split('=')
        if len(parts) != 2:
            continue
        
        key, value = parts
        key = key.strip()
        value = value.strip()
        
        if key:
            config[key] = value
    
    return config
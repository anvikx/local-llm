def parse_config(text):
    if not isinstance(text, str):
        return {}
    
    config_dict = {}
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if key in config_dict:
            continue
        config_dict[key] = value
    return config_dict
def get_key_default(value, field: str):
    if isinstance(value, dict):
        return value.get(field)
    return ""

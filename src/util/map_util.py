def get_key_or_default(value, field: str):
    if isinstance(value, dict):
        return value.get(field)
    return ""


def get_key_or_zero(value, field: str):
    if not isinstance(value, dict):
        return 0
    val = value.get(field)
    if val:
        return val
    return 0


def get_key_or_empty(value, field: str):
    if isinstance(value, dict):
        val = value.get(field)
        if val:
            return val
    return {}

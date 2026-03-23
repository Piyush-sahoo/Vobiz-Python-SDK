

def map_type(val):
    if isinstance(val, bool):
        return str(val).lower()
    return str(val)

def is_numeric(line: str) -> bool:
    try:
        float(line)
    except:
        return False
    else:
        return True

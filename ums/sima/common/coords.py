def ra_convert_to_float(ra_txt: str) -> float:
    d, m, s = map(float, ra_txt.split())
    return round((abs(d) + m / 60 + s / 3600) * 15, 6)

def ra_convert_to_str(ra_float: float) -> str:
    ra_float /= 15
    d = abs(int(ra_float))
    m_f = abs(ra_float)%1 * 60
    m = int(m_f)
    s = round(m_f%1 * 60, 2)
    if s >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        d += 1
    return f"{d:02d} {m:02d} {s:05.2f}"

def dec_convert_to_float(dec_txt: str) -> float:
    d, m, s = map(float, dec_txt.split())
    sign = -1 if dec_txt[0] == '-' else 1
    return round(sign * (abs(d) + m / 60 + s / 3600), 6)

def dec_convert_to_str(dec: float) -> str:
    sign = '-' if dec < 0 else '+'
    d = abs(int(dec))
    m_f = abs(dec)%1 * 60
    m = int(m_f)
    s = round(m_f%1 * 60, 2)
    if s >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        d += 1
    return f"{sign}{d:02d} {m:02d} {s:05.2f}"
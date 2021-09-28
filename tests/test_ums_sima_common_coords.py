from ums.sima.common.coords import ra_convert_to_float, ra_convert_to_str, dec_convert_to_float, dec_convert_to_str
from random import randint, random

def test_ra_convert():
    values = ['00 00 00.99', '00 00 59.99', '00 59 59.99', '23 59 59.99']
    for value in values:
        float_value = ra_convert_to_float(value)
        covered_value = ra_convert_to_str(float_value)
        assert value == covered_value
    
def test_dec_convert():
    values = ['-89 59 59.99', '+89 59 59.99', '-00 00 00.99', '+00 00 59.99']
    for value in values:
        float_value = dec_convert_to_float(value)
        covered_value = dec_convert_to_str(float_value)
        assert value == covered_value

def test_custom_convert():
    input_data = '12 34 56.78'
    data = ra_convert_to_float(input_data)
    data_sec = data * 3600 / 15
    assert input_data == f"{int(data_sec/3600):02d} {int(data_sec%3600/60):02d} {data_sec%60:02.2f}"
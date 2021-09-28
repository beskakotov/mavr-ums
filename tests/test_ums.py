from ums import __mainversion__, __subversion__, __debugversion__

def test_ums_version():
    assert f'{__mainversion__}.{__subversion__}.{__debugversion__}' == '0.0.1'
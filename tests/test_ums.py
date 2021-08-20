from ums import __mainversion__, __subversion__

def test_ums_version():
    assert f'{__mainversion__}.{__subversion__}' == '0.1'
class __version__:
    __main = 0
    __sub = 0
    __debug = 1

    @classmethod
    def get(cls):
        return f"UMS v{cls.__main}.{cls.__sub}.{cls.__debug}"

class ErrorBase(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._code = args[0] if len(args) else 0
        self._error = args[1] if len(args) > 1 else ''

    def __str__(self):
        return 'err: (%s) %s' % (self._code, self._error)

    @property
    def code(self):
        return self._code

    @property
    def error(self):
        return self._error


class ServerError(ErrorBase):
    pass


class NormalError(ErrorBase):
    pass


class CriticalError(ErrorBase):
    pass


class BasicError(ErrorBase):
    pass

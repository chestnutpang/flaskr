from flask import url_for, redirect


class ErrorCode:
    LOGIN_REQUIRE = 20000, 'unverified'
    COMM_ERROR = 10000, 'common error'
    @classmethod
    def custom(cls, code, msg):
        return code[0], msg

    @classmethod
    def format(cls, code, msg):
        return code[0], code[1].format(msg)


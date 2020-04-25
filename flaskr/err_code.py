from flask import url_for, redirect


class ErrorCode:
    COMM_ERROR = 10000, 'common error'

    LOGIN_REQUIRE = 20000, 'unverified'
    REGISTER_ERROR = 20001, 'register error'
    @classmethod
    def custom(cls, code, msg):
        return code[0], msg

    @classmethod
    def format(cls, code, msg):
        return code[0], code[1].format(msg)


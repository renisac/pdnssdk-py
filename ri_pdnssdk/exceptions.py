
class PdnsException(Exception):
    def __init__(self, msg):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg

class AuthError(PdnsException):
    pass


class TimeoutError(PdnsException):
    pass

class InvalidSearch(PdnsException):
    pass

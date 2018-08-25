class AuthenticationError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class NotImplementedError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

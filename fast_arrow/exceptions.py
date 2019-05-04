class AuthenticationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class NotImplementedError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class TradeExecutionError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

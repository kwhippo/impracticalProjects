class KeyValidationError(Exception):
    def __init__(self, message='The cipher key is invalid'):
        super(KeyValidationError, self).__init__(message)


class IncompleteKeyError(KeyValidationError):
    def __init__(self, message='The cipher key is missing values'):
        super(IncompleteKeyError, self).__init__(message)

class KeyError(Exception):
    def __init__(self, message='Cipher key error'):
        super(KeyError, self).__init__(message)


class KeyValidationError(KeyError):
    def __init__(self, message='The cipher key is invalid'):
        super(KeyValidationError, self).__init__(message)


class IncompleteKeyError(KeyValidationError):
    def __init__(self, message='The cipher key is missing values'):
        super(IncompleteKeyError, self).__init__(message)


class KeyCalculationError(KeyError):
    def __init__(self, message='Error calculating key values'):
        super(KeyCalculationError, self).__init__(message)


class EncryptionError(Exception):
    def __init__(self, message='Error encrypting the plaintext'):
        super(EncryptionError, self).__init__(message)


class DecryptionError(Exception):
    def __init__(self, message='Error decrypting the ciphertext'):
        super(DecryptionError, self).__init__(message)

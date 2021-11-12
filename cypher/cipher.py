import pprint
from cypher.exceptions import KeyValidationError, IncompleteKeyError


class Key:
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, alphabet=ALPHABET):
        self.alphabet = alphabet

    def get(self):
        return self.__dict__

    def validate(self):
        for key_name, key_value in self.__dict__.items():
            if key_value is None:
                raise IncompleteKeyError(f'{key_name} must have a value')

    def random(self):
        for key_name in self.__dict__.keys():
            self.__setattr__(key_name, None)
        self.validate()

    def print(self):
        pprint.pprint(self.__dict__)


class Cipher:
    NAME = 'Generic'

    def __init__(self, plaintext='', ciphertext='', key=None):
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.key = key

    def encrypt(self):
        try:
            self.key.validate()
            self.ciphertext = self.plaintext.upper()
        except Exception:
            self.ciphertext = ''
            raise KeyValidationError

    def decrypt(self):
        try:
            self.key.validate()
            self.plaintext = self.ciphertext.upper()
        except Exception:
            self.plaintext = ''
            raise KeyValidationError

    def print(self):
        print(f'Plaintext:  {self.plaintext}')
        print(f'Ciphertext: {self.ciphertext}')
        print('Key:', end=' ')
        self.key.print()

    def set_key(self, key=Key()):
        self.key = key

    def clear_key(self):
        self.key = Key()

    def get(self):
        cipher_dict = {}
        for key, value in self.__dict__.items():
            if type(value) != Key:
                cipher_dict[key] = value
        cipher_dict['key'] = self.key.get()
        return cipher_dict

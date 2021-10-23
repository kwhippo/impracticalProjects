import pprint


class Key:
    def __init__(self):
        pass

    def validate(self):
        for key_name, key_value in self.__dict__.items():
            if key_value is None:
                raise ValueError(f'{key_name} must have a value')

    def random(self):
        for key_name in self.__dict__.keys():
            self.__setattr__(key_name, None)
        self.validate()

    def print(self):
        pprint.pprint(self.__dict__)


class Cipher:
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NAME = 'Generic'

    def __init__(self, alphabet=ALPHABET, plaintext='', ciphertext='', key=None):
        self.alphabet = alphabet
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.key = key

    def encrypt(self):
        self.key.validate()
        self.ciphertext = self.plaintext.upper()

    def decrypt(self):
        self.key.validate()
        self.plaintext = self.ciphertext.upper()

    def print(self):
        print(f'Alphabet: {self.alphabet}')
        print(f'Plaintext:  {self.plaintext}')
        print(f'Ciphertext: {self.ciphertext}')
        print('Key:', end=' ')
        self.key.print()

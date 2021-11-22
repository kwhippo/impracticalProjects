from cypher.cipher import Key, Cipher
from cypher.substitution import random_alpha_key
from cypher.exceptions import KeyValidationError, EncryptionError, DecryptionError
from cypher.tools.utilities import break_string_to_list, text_upper_strip_non_alphabet


def random_xy_key():
    return random_alpha_key(Key.ALPHABET)[:5]


def validate_cipher_alphabet(cipher_alphabet):
    try:
        alpha_list = break_string_to_list(cipher_alphabet)
        alpha_list.sort()
        sorted_alphabet = ''.join(alpha_list)
        assert PolybiusSquareKey.ALPHABET == sorted_alphabet
    except AssertionError:
        raise KeyValidationError('Cipher Alphabet does not match Polybius Square Alphabet')
    except Exception as e:
        raise KeyValidationError(e)


def validate_xy_key(xy_key):
    try:
        assert isinstance(xy_key, str)
    except Exception as e:
        raise KeyValidationError('X/Y Key must be a string') from e
    try:
        assert len(xy_key) == 5
    except Exception as e:
        raise KeyValidationError('X/Y Key must be 5 characters long') from e
    try:
        test_key = ''
        for character in xy_key:
            if test_key.find(character) == -1:
                test_key += character
            else:
                raise RuntimeError
    except Exception as e:
        raise KeyValidationError('X/Y Key must not contain duplicate values') from e


class PolybiusSquareKey(Key):
    ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

    def __init__(self, cipher_alphabet='', x_key='', y_key=''):
        super(PolybiusSquareKey, self).__init__(alphabet=self.ALPHABET)
        self.cipher_alphabet = cipher_alphabet
        self.x_key = x_key
        self.y_key = y_key

    def random(self):
        self.cipher_alphabet = random_alpha_key(self.alphabet)
        self.x_key = random_xy_key()
        self.y_key = random_xy_key()

    def validate(self):
        try:
            super(PolybiusSquareKey, self).validate()
            validate_cipher_alphabet(self.cipher_alphabet)
            validate_xy_key(self.x_key)
            validate_xy_key(self.y_key)
        except Exception as e:
            raise KeyValidationError(e)


class PolybiusSquareCipher(Cipher):
    NAME = 'Polybius Square Cipher'

    def __init__(self, *args, **kwargs):
        super(PolybiusSquareCipher, self).__init__(*args, **kwargs)

    def encrypt(self):
        try:
            self.key.validate()
            cipher_text = ''
            for character in text_upper_strip_non_alphabet(self.plaintext):
                if character == 'J':
                    character = 'I'
                cipher_index = self.key.cipher_alphabet.find(character)
                if cipher_index >= 0:
                    y_index = cipher_index // 5
                    x_index = cipher_index % 5
                    cipher_text += f'{self.key.y_key[y_index]}{self.key.x_key[x_index]}'
                else:
                    raise EncryptionError
            self.ciphertext = cipher_text
        except Exception as e:
            raise EncryptionError from e

    def decrypt(self):
        try:
            self.key.validate()
            plain_text = ''
            bigram_list = break_string_to_list(self.ciphertext, step=2)
            for bigram in bigram_list:
                y_index = self.key.y_key.find(bigram[0])
                x_index = self.key.x_key.find(bigram[1])
                if y_index == -1 or x_index == -1:
                    raise DecryptionError('Key invalid for cipher text')
                cipher_index = (y_index * 5) + x_index
                plain_text += self.key.cipher_alphabet[cipher_index]
            self.plaintext = plain_text
        except Exception as e:
            raise DecryptionError from e

    def set_key(self, key=PolybiusSquareKey()):
        self.key = key

    def clear_key(self):
        self.key = PolybiusSquareKey()

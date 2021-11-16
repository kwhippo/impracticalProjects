"""
Homophonic substitution cipher.

The Homophonic Substitution cipher is a substitution cipher in which single plaintext letters can
be replaced by any of several different ciphertext letters. They are generally much more difficult
to break than standard substitution ciphers.
The number of characters each letter is replaced by is part of the key, e.g. the letter 'E' might
be replaced by any of 5 different symbols, while the letter 'Q' may only be substituted by 1 symbol.
This cipher ignores punctuation and numbers, converting text to uppercase.
"""
import random
from pprint import pprint

from cypher.cipher import Key, Cipher
from cypher.substitution import crypt
from cypher.exceptions import KeyCalculationError, KeyValidationError, EncryptionError, \
    DecryptionError
from cypher.tools.frequency import calculate_plaintext_frequency

COMMON_FREQUENCY = [
    812,  # A
    149,  # B
    271,  # C
    432,  # D
    1202,  # E
    230,  # F
    203,  # G
    592,  # H
    731,  # I
    10,  # J
    69,  # K
    398,  # L
    261,  # M
    695,  # N
    768,  # O
    182,  # P
    11,  # Q
    602,  # R
    628,  # S
    910,  # T
    288,  # U
    111,  # V
    210,  # W
    17,  # X
    211,  # Y
    7,  # Z
]


def calculate_alpha_keys(alpha_dict_key):
    alpha_plain_key = ''
    alpha_cipher_key = ''
    for key, value in alpha_dict_key.items():
        for character in value:
            alpha_plain_key += key
            alpha_cipher_key += character
    return alpha_plain_key, alpha_cipher_key


def calculate_alpha_text_key(alpha_dict_key):
    # Find longest length
    alpha_text_key = ''
    longest = 0
    for value in alpha_dict_key.values():
        if len(value) > longest:
            longest = len(value)
    for i in range(longest):
        for value in alpha_dict_key.values():
            try:
                alpha_text_key += value[i]
            except IndexError:
                alpha_text_key += ' '
        alpha_text_key += '\n'
    return alpha_text_key


def calculate_alpha_dict(alpha_plain_key, alpha_cipher_key):
    alpha_dict_key = {}
    index = 0
    for character in alpha_plain_key:
        if character in alpha_dict_key:
            alpha_dict_key[character].append(alpha_cipher_key[index])
        else:
            alpha_dict_key[character] = [alpha_cipher_key[index]]
        index += 1
    return alpha_dict_key


def random_alpha_dict_key(alphabet, cipher_alphabet, frequency=None):
    return calculate_alpha_dict(*random_alpha_keys(alphabet, cipher_alphabet, frequency))


# WORKING
def random_alpha_keys(alphabet, cipher_alphabet, frequency=None):
    """
    Generate random alpha keys based on given frequency.

    :param alphabet: string value of plaintext alphabet
    :type alphabet: str
    :param cipher_alphabet: string value of cipher alphabet
    :type cipher_alphabet: str
    :return: calculated alpha_plain_key and alpha_cipher_key
    :param frequency: list of integers with length of len(alphabet)
    :type frequency: list
    :return
        alpha_plain_key: Text of alphabet string with repeated characters
        alpha_cipher_key: Text of cipher alphabet in plain alphabet order
    :rtype: str, str
    """
    try:
        cipher_list = [x for x in cipher_alphabet]
        random.shuffle(cipher_list)
        alpha_cipher_key = ''.join(cipher_list)
        alpha_list = [x for x in alphabet]
        extra_length = len(cipher_alphabet) - len(alphabet)
        extra_alpha = ''.join(random.choices(alpha_list, weights=frequency, k=extra_length))
        alpha_plain_key = ''.join(sorted(alphabet + extra_alpha))

    except Exception as e:
        raise KeyCalculationError from e

    return alpha_plain_key, alpha_cipher_key


def random_frequency(alphabet):
    frequency = []
    for i in range(len(alphabet)):
        frequency.append(random.randint(1, 1000))
    return frequency


class HomophonicKey(Key):
    """The key class manages the key used for cipher encryption and decryption."""

    CIPHER_ALPHABET = Key.ALPHABET + '0123456789'

    OPTIMIZE_OPTIONS = [
        'common',
        'plaintext',
        'random',
    ]

    def __init__(self, alpha_dict_key=None, alpha_plain_key='', alpha_cipher_key='',
                 alpha_text_key='', cipher_alphabet=CIPHER_ALPHABET, alphabet=Key.ALPHABET,
                 optimize='common', frequency=None):
        """
        Initialize key attributes from arguments or default to blank values.

        :param alpha_dict_key: Dictionary of alphabet keys mapped to a list of cipher characters
        :type alpha_dict_key: dict
        :param alpha_plain_key: Text of alphabet string with repeated characters
        :type alpha_plain_key: str
        :param alpha_cipher_key: Text of cipher alphabet in plain alphabet order
        :type alpha_cipher_key: str
        :param alpha_text_key: Formatted text of cipher alphabet
        :type alpha_text_key: str
        :param cipher_alphabet: Text of cipher alphabet in alphabetical order
        :param alphabet: Text of full alphabet
        :type alphabet: str
        :param optimize: An attribute that holds character distribution option
        :type optimize: str
        """
        super().__init__(alphabet=alphabet)
        if alpha_dict_key is None:
            self.alpha_dict_key = {}
            for character in Key.ALPHABET:
                self.alpha_dict_key[character] = ''
        else:
            self.alpha_dict_key = alpha_dict_key
        self.alpha_plain_key = alpha_plain_key
        self.alpha_cipher_key = alpha_cipher_key
        self.cipher_alphabet = cipher_alphabet
        self.alpha_text_key = alpha_text_key
        self.optimize = optimize
        if frequency is None:
            self.frequency = [1] * len(self.alphabet)
        else:
            self.frequency = frequency

    def calculate(self):
        # TODO: Validate alpha_dict_key, optimize, frequency
        self.alpha_plain_key, self.alpha_cipher_key = calculate_alpha_keys(self.alpha_dict_key)
        self.alpha_text_key = calculate_alpha_text_key(self.alpha_dict_key)

    def calculate_frequency(self, plaintext=None):
        try:
            if self.optimize == 'common':
                self.frequency = COMMON_FREQUENCY
            elif self.optimize == 'plaintext':
                assert plaintext is not None
                self.frequency = calculate_plaintext_frequency(plaintext, self.alphabet)
            elif self.optimize == 'random':
                self.frequency = random_frequency(self.alphabet)
            else:
                raise KeyCalculationError('Invalid option for optimize attribute')
        except AssertionError as e:
            raise KeyCalculationError("Plaintext required for plaintext optimization") from e
        except Exception as e:
            raise KeyCalculationError from e

    # def calculate(self, *, string_key=None, list_key=None, numeric_key=None):
    #     """
    #     Calculate and set all key attributes based on key argument.
    #
    #     Calculate method expects a certain set of arguments to calculate values.
    #     :param string_key: Text key variable
    #     :type string_key: str
    #     :param list_key: List key variable
    #     :type list_key: list
    #     :param numeric_key: Integer key variable
    #     :type numeric_key: int
    #     :raises
    #         KeyValidationError: If unable to calculate a key from given arguments
    #     """
    #     try:
    #         if list_key is not None:
    #             assert string_key is None
    #             assert numeric_key is None
    #             self.list_key = list_key
    #             self.string_key = list_key[0]
    #             self.numeric_key = len(list_key)
    #         elif string_key is not None and numeric_key is not None:
    #             assert list_key is None
    #             self.string_key = string_key
    #             self.numeric_key = numeric_key
    #             self.list_key = calculate_list_key(string_key, numeric_key)
    #     except Exception as e:
    #         raise KeyValidationError('Unable to calculate key') from e

    # def validate(self):
    #     """
    #     Check key attributes and raise error or return.
    #
    #     :raises
    #         KeyValidationError: Mismatch in key attributes or value error
    #         IncompleteKeyError: Missing or blank key attributes
    #     """
    #     try:
    #         # Validate key attributes match and values are acceptable
    #         # Implement additional logic here
    #         validate_string_key(self.string_key)
    #         validate_list_key(self.list_key)
    #         validate_numeric_key(self.numeric_key)
    #
    #         super().validate()
    #     except Exception as e:
    #         raise KeyValidationError('Invalid key') from e
    #
    def random(self):
        """Create a random key and set key attributes."""
        self.alpha_plain_key, self.alpha_cipher_key = \
            random_alpha_keys(Key.ALPHABET,
                              HomophonicKey.CIPHER_ALPHABET,
                              frequency=self.frequency)
        self.alpha_dict_key = calculate_alpha_dict(self.alpha_plain_key, self.alpha_cipher_key)
        self.alpha_text_key = calculate_alpha_text_key(self.alpha_dict_key)


class HomophonicCipher(Cipher):
    """The cipher class manages the text, key, encryption and decryption methods."""

    NAME = 'Homophonic Substitution Cipher'

    def __init__(self, *args, **kwargs):
        """
        Homophonic cipher initialization method that inherits from Cipher class.

        :param args: Parent arguments
        :param kwargs: Parent keyword arguments
        """
        super().__init__(*args, **kwargs)

    def encrypt(self):
        """
        Implement the encryption algorithm using the cipher plaintext and setting the ciphertext.

        :raises
            EncryptionError: Unable to encrypt plaintext using key
        """
        try:
            self.key.validate()
            print(f'Alpha Plain Key: {self.key.alpha_plain_key}')
            print(f'Alpha Cipher Key: {self.key.alpha_cipher_key}')
            pprint(self.key.alpha_dict_key)
            plaintext = self.plaintext.upper()
            ciphertext = ''
            for character in plaintext:
                if character in self.key.alphabet:
                    ciphertext += random.choice(self.key.alpha_dict_key[character])
                else:
                    ciphertext += character
            self.ciphertext = ciphertext
        except Exception as e:
            self.ciphertext = ''
            raise EncryptionError from e

    def decrypt(self):
        """
        Implement the decryption algorithm using the ciphertext and setting the plaintext.

        :raises
            DecryptionError: Unable to decrypt ciphertext using key
        """
        try:
            self.key.validate()
            print(f'Alpha Plain Key: {self.key.alpha_plain_key}')
            print(f'Alpha Cipher Key: {self.key.alpha_cipher_key}')
            pprint(self.key.alpha_dict_key)
            self.plaintext = crypt(self.ciphertext, self.key.alpha_cipher_key,
                                   self.key.alpha_plain_key)
        except Exception as e:
            self.plaintext = ''
            raise DecryptionError from e

    def set_key(self, key=HomophonicKey()):
        """
        Set key attribute to a given key.

        :param key: Key object of cipher
        :type key: HomophonicKey
        """
        # Implement additional logic here
        super().set_key(key)

    def clear_key(self):
        """Set key attribute to a new empty key passing original key settings."""
        if self.key.optimize:
            self.key = HomophonicKey(optimize=self.key.optimize)
        else:
            self.key = HomophonicKey()


if __name__ == '__main__':
    c = HomophonicCipher()
    c.set_key()

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
    pass


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


# WORKING
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


# WORKING
def calculate_plaintext_frequency(plaintext, alphabet):
    """
    Calculate the frequency of alphabet characters in plaintext and return frequency list

    :param plaintext: Text body to calculate frequency from
    :type plaintext: str
    :param alphabet: String value of plaintext alphabet
    :return: frequency: List of frequency sorted in alphabet order
    """
    alpha_dict = {}
    for character in alphabet:
        alpha_dict[character] = 1
    for character in plaintext:
        if character in alpha_dict:
            alpha_dict[character] += 1
    frequency_list = [x for x in alpha_dict.values()]
    return frequency_list


def validate_string_key(string_key):
    """
    Validate the string key variable.

    :param string_key: string value of cipher key
    :type string_key: str
    :raises
        KeyValidationError: Key variable is invalid
    """
    try:
        if isinstance(string_key, str):
            raise TypeError
        assert len(string_key) > 0
    except TypeError:
        raise KeyValidationError('String key must be a string') from TypeError
    except AssertionError:
        raise KeyValidationError('String key must not be blank') from AssertionError
    except Exception as e:
        raise Exception('String key is invalid') from e


def validate_list_key(list_key):
    """
    Validate the list key variable.

    :param list_key: list value of cipher key
    :type list_key: list
    :raises
        KeyValidationError: Key variable is invalid
    """
    try:
        if isinstance(list_key, list):
            raise TypeError
        assert len(list_key) > 0
    except TypeError:
        raise KeyValidationError('List key must be a list') from TypeError
    except AssertionError:
        raise KeyValidationError('List key must be greater than 0') from AssertionError
    except Exception as e:
        raise Exception('List key is invalid') from e


def validate_numeric_key(numeric_key):
    """
    Validate the int key variable.

    :param numeric_key: numeric value of cipher key
    :type numeric_key: int
    :raises
        KeyValidationError: Key variable is invalid
    """
    try:
        if isinstance(numeric_key, int):
            raise TypeError
        assert numeric_key > 0
    except TypeError:
        raise KeyValidationError('Numeric key must be an integer') from TypeError
    except AssertionError:
        raise KeyValidationError('Numeric key must be greater than 0') from AssertionError
    except Exception as e:
        raise Exception('Numeric key is invalid') from e


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
                 optimize='common'):
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
            alpha_dict = {}
            for character in Key.ALPHABET:
                alpha_dict[character] = ''
        self.alpha_plain_key = alpha_plain_key
        self.alpha_cipher_key = alpha_cipher_key
        self.cipher_alphabet = cipher_alphabet
        self.alpha_text_key = alpha_text_key
        self.optimize = optimize

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
    def random(self, frequency=None):
        """Create a random key and set key attributes."""
        pk, ck = random_alpha_keys(Key.ALPHABET, HomophonicKey.CIPHER_ALPHABET,
                                   frequency=frequency)
        print(pk)
        print(ck)
        dk = random_alpha_dict_key(Key.ALPHABET, HomophonicKey.CIPHER_ALPHABET, frequency=frequency)
        pprint(calculate_alpha_dict(pk, ck))

    #
    # def set(self, *, string_key=None, list_key=None, numeric_key=None):
    #     """
    #     Set key attributes from keyword arguments.
    #
    #     :param string_key: value of string key attribute
    #     :type string_key: str
    #     :param list_key: value of list key attribute
    #     :type list_key: list
    #     :param numeric_key: value of numeric key attribute
    #     :type numeric_key: int
    #     """
    #     if string_key is not None:
    #         self.string_key = string_key
    #     if list_key is not None:
    #         self.list_key = list_key
    #     if numeric_key is not None:
    #         self.numeric_key = numeric_key


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
            super().encrypt()
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
            super().decrypt()
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
    dk = random_alpha_dict_key(Key.ALPHABET, HomophonicKey.CIPHER_ALPHABET,
                               frequency=COMMON_FREQUENCY)
    pprint(dk)
    print(calculate_alpha_text_key(dk))
    HomophonicKey().print()

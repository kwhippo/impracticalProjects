"""
Cipher Module Template.

The cipher module implements the encryption and decryption algorithms along with necessary helper
functions.
User interfaces are implemented in a separate module.
Functions and methods should follow crypt, calculate, validate, random, set, get, ui order.
They should also generally start with the more broad and complex and end with the more simple and
specific.
"""
import random

from cypher.cipher import Key, Cipher
from cypher.exceptions import KeyCalculationError, KeyValidationError, EncryptionError, \
    DecryptionError


def crypt(text, key_list):
    """
    Define a symmetric encryption algorithm for the cipher and return text string.

    :param text: original text value
    :type text: str
    :param key_list: key list value
    :type key_list: list
    :return: crypted version of original text
    :rtype: str
    """
    crypted_text = ''
    for key in key_list:
        crypted_text += key + text
    return crypted_text


def calculate_list_key(string_value, numeric_value):
    """
    Use input arguments to calculate and return a list key.

    :param string_value: string value of cipher key
    :type string_value: str
    :param numeric_value: numeric value of cipher key
    :type numeric_value: int
    :return: calculated list key value
    :rtype: list
    """
    try:
        list_key = [string_value] * numeric_value
    except Exception as e:
        raise KeyCalculationError from e
    return list_key


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


def random_numeric_key():
    """
    Create a random numeric key value and return result.

    :return: numeric key value
    :rtype: int
    """
    numeric_key = random.randint(1, 10)
    return numeric_key


def random_string_key():
    """
    Create a random string key value and return result.

    :return: string key value
    :rtype: str
    """
    string_start = random.randint(0, 25)
    string_end = random.randint(string_start, 25)
    string_key = Key.ALPHABET[string_start:string_end]
    return string_key


class KeyClass(Key):
    """The key class manages the key used for cipher encryption and decryption."""

    def __init__(self, string_key='', list_key=None, numeric_key=0, alphabet=Key.ALPHABET,
                 setting=False):
        """
        Initialize key attributes from arguments or default to blank values.

        :param string_key: Text key attribute
        :type string_key: str
        :param list_key: List key attribute
        :type list_key: list
        :param numeric_key: Integer key attribute
        :type numeric_key: int
        :param alphabet: Text of full alphabet
        :type alphabet: str
        :param setting: An attribute that holds key options
        :type setting: bool
        """
        super().__init__(alphabet=alphabet)
        self.string_key = string_key
        if list_key is None:
            list_key = []
        self.list_key = list_key
        self.numeric_key = numeric_key
        self.setting = setting
        # TODO: Update template

    def calculate(self, *, string_key=None, list_key=None, numeric_key=None):
        """
        Calculate and set all key attributes based on key argument.

        Calculate method expects a certain set of arguments to calculate values.
        :param string_key: Text key variable
        :type string_key: str
        :param list_key: List key variable
        :type list_key: list
        :param numeric_key: Integer key variable
        :type numeric_key: int
        :raises
            KeyValidationError: If unable to calculate a key from given arguments
        """
        try:
            if list_key is not None:
                assert string_key is None
                assert numeric_key is None
                self.list_key = list_key
                self.string_key = list_key[0]
                self.numeric_key = len(list_key)
            elif string_key is not None and numeric_key is not None:
                assert list_key is None
                self.string_key = string_key
                self.numeric_key = numeric_key
                self.list_key = calculate_list_key(string_key, numeric_key)
        except Exception as e:
            raise KeyValidationError('Unable to calculate key') from e

    def validate(self):
        """
        Check key attributes and raise error or return.

        :raises
            KeyValidationError: Mismatch in key attributes or value error
            IncompleteKeyError: Missing or blank key attributes
        """
        try:
            # Validate key attributes match and values are acceptable
            # Implement additional logic here
            validate_string_key(self.string_key)
            validate_list_key(self.list_key)
            validate_numeric_key(self.numeric_key)

            super().validate()
        except Exception as e:
            raise KeyValidationError('Invalid key') from e

    def random(self):
        """Create a random key and set key attributes."""
        numeric_key = random_numeric_key()
        string_key = random_string_key()
        self.calculate(string_key=string_key, numeric_key=numeric_key)

    def set(self, *, string_key=None, list_key=None, numeric_key=None):
        """
        Set key attributes from keyword arguments.

        :param string_key: value of string key attribute
        :type string_key: str
        :param list_key: value of list key attribute
        :type list_key: list
        :param numeric_key: value of numeric key attribute
        :type numeric_key: int
        """
        if string_key is not None:
            self.string_key = string_key
        if list_key is not None:
            self.list_key = list_key
        if numeric_key is not None:
            self.numeric_key = numeric_key

    def get(self):
        """
        Compile key attributes into dictionary and return a dictionary object.

        :return: Dictionary of key attributes
        :rtype: dict
        """
        super().get()

    def print(self):
        """Print key attributes to the console."""
        super().print()


class CipherClass(Cipher):
    """The cipher class manages the text, key, encryption and decryption methods."""

    NAME = 'Cipher Template'

    def __init__(self, *args, **kwargs):
        """
        Cipher initialization method that inherits from Cipher class.

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
            # Implement additional logic here
            self.ciphertext = crypt(self.plaintext, self.key.list_key)
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
            # Implement additional logic here
            self.plaintext = crypt(self.ciphertext, self.key.list_key)
        except Exception as e:
            self.plaintext = ''
            raise DecryptionError from e

    def set_key(self, key=KeyClass()):
        """
        Set key attribute to a given key.

        :param key: Key object of cipher
        :type key: KeyClass
        """
        # Implement additional logic here
        super().set_key(key)

    def clear_key(self):
        """Set key attribute to a new empty key passing original key settings."""
        if self.key.setting:
            self.key = KeyClass(setting=True)
        else:
            self.key = KeyClass()

    def get(self):
        """
        Compile cipher attributes into dictionary and returns a dictionary object.

        :return: Dictionary of cipher attributes
        :rtype: dict
        """
        super().get()

    def print(self):
        """Print cypher attributes to the console."""
        super().print()

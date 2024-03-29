from cypher.caesar import create_keys
from cypher.cipher import Cipher, Key
from cypher.tools.utilities import get_random_word
from cypher import substitution


def create_key_list(keyword=None, alphabet=Key.ALPHABET):
    if keyword is None:
        keyword = get_random_word('pokemon')
    key_list = []
    for letter in keyword.upper():
        key_list.append(create_keys(letter, alphabet)['alpha_key'])
    return key_list


def crypt(text, source_alphabet, crypted_alphabet):
    crypted_text = ''
    if type(source_alphabet) == list:
        source_list = True
        key_length = len(source_alphabet)
        alphabet = crypted_alphabet
    else:
        source_list = False
        key_length = len(crypted_alphabet)
        alphabet = source_alphabet
    key_index = 0
    for letter in text.upper():
        if source_list:
            crypted_text += substitution.crypt(letter, source_alphabet[key_index], crypted_alphabet)
        else:
            crypted_text += substitution.crypt(letter, source_alphabet, crypted_alphabet[key_index])
        if letter in alphabet:
            key_index += 1
            if key_index == key_length:
                key_index = 0
    return crypted_text


class VigenereKey(Key):
    def __init__(self, keyword='', key_list=None, alphabet=Key.ALPHABET):
        super(VigenereKey, self).__init__(alphabet=alphabet)
        if key_list is None:
            key_list = []
        self.keyword = keyword
        self.key_list = key_list
        self.alphabet = alphabet

    def set(self, *, keyword=None, key_list=None):
        if keyword is not None:
            self.keyword = keyword
        if key_list is not None:
            self.key_list = key_list

    def calculate(self, *, keyword=None):
        self.keyword = keyword
        self.key_list = create_key_list(keyword)

    def random(self):
        self.calculate(keyword=get_random_word())

    def validate(self):
        if self.keyword is None and self.key_list is None:
            self.keyword = get_random_word('pokemon')
        if self.key_list is None:
            self.key_list = create_key_list(self.keyword, self.alphabet)
        if self.keyword is None:
            keyword = ''
            for item in self.key_list:
                keyword += item[0]
            self.keyword = keyword
        assert len(self.key_list) == len(self.keyword)
        for key in self.key_list:
            key_set = set(key)
            assert len(key_set) == len(self.alphabet)
            for character in self.alphabet:
                assert character in key_set
        super().validate()


class VigenereCipher(Cipher):
    NAME = 'Vigenere Cipher'

    def __init__(self, *args, **kwargs):
        super(VigenereCipher, self).__init__(*args, **kwargs)

    def encrypt(self):
        super(VigenereCipher, self).encrypt()
        self.ciphertext = crypt(self.plaintext, self.key.alphabet, self.key.key_list)

    def decrypt(self):
        super(VigenereCipher, self).decrypt()
        self.plaintext = crypt(self.ciphertext, self.key.key_list, self.key.alphabet)

    def set_key(self, key=VigenereKey()):
        super(VigenereCipher, self).set_key(key)

    def clear_key(self):
        self.key = VigenereKey()

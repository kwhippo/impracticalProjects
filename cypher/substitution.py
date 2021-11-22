from cypher.cipher import Key, Cipher
from cypher.tools.alphabet import random_alpha_key


def crypt(text, source_alphabet, crypted_alphabet):
    crypted_text = ''
    for character in text:
        crypted_character = character
        if character in source_alphabet:
            crypted_character = crypted_alphabet[source_alphabet.find(character)]
        crypted_text += crypted_character
    return crypted_text


# Cipher Definition
class SubstitutionKey(Key):

    def __init__(self, alpha_key='', alphabet=Key.ALPHABET):
        super().__init__()
        self.alpha_key = alpha_key
        self.alphabet = alphabet

    def random(self):
        self.alpha_key = random_alpha_key()

    def validate(self):
        try:
            validated = self.alpha_key.upper()
            key_set = set(validated)
            assert len(key_set) == len(self.alphabet)
            for character in self.alphabet:
                assert character in key_set
            self.alpha_key = validated
        except Exception as e:
            raise e
        super(SubstitutionKey, self).validate()


class SubstitutionCipher(Cipher):
    NAME = 'Simple Substitution Cipher'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encrypt(self):
        super(SubstitutionCipher, self).encrypt()
        plaintext = self.plaintext.upper()
        self.ciphertext = crypt(plaintext, self.key.alphabet, self.key.alpha_key)

    def decrypt(self):
        super(SubstitutionCipher, self).decrypt()
        ciphertext = self.ciphertext.upper()
        self.plaintext = crypt(ciphertext, self.key.alpha_key, self.key.alphabet)

    def set_key(self, key=SubstitutionKey()):
        super(SubstitutionCipher, self).set_key(key)

    def clear_key(self):
        self.key = SubstitutionKey()

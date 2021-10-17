import random
from cypher.cipher import Key, Cipher


# Utility Functions
def random_substitution_key():
    key_list = list(Cipher.ALPHABET)
    random.shuffle(key_list)
    alpha_key = ''.join(key_list)
    return alpha_key


def crypt(text, source_alphabet, crypted_alphabet):
    crypted_text = ''
    for character in text:
        crypted_character = character
        if character in crypted_alphabet:
            crypted_character = crypted_alphabet[source_alphabet.find(character)]
        crypted_text += crypted_character
    return crypted_text


# Cipher Definition
class SubstitutionKey(Key):
    def __init__(self, alpha_key=None):
        super().__init__()
        self.alpha_key = alpha_key

    def validate(self, alphabet=Cipher.ALPHABET):
        if self.alpha_key is None:
            self.alpha_key = random_substitution_key()
        try:
            validated = self.alpha_key.upper()
            key_set = set(validated)
            assert len(key_set) == len(alphabet)
            for character in alphabet:
                assert character in key_set
            self.alpha_key = validated
        except Exception as e:
            raise e
        super().validate()


class SubstitutionCipher(Cipher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encrypt(self):
        super(SubstitutionCipher, self).encrypt()
        plaintext = self.plaintext.upper()
        self.ciphertext = crypt(plaintext, self.alphabet, self.key.alpha_key)

    def decrypt(self):
        super(SubstitutionCipher, self).decrypt()
        ciphertext = self.ciphertext.upper()
        self.plaintext = crypt(ciphertext, self.key.alpha_key, self.alphabet)

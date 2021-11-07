import random
from cypher.substitution import SubstitutionKey, SubstitutionCipher
from cypher.cipher import Cipher


def create_keys(input_key=None, alphabet=Cipher.ALPHABET, reverse=False):
    plain_alphabet = alphabet
    if reverse:
        cipher_alphabet = alphabet[::-1]
    else:
        cipher_alphabet = alphabet
    if input_key is None:
        input_key = random.randint(1, len(plain_alphabet) - 1)
    key_string = str(input_key).upper()
    if get_key_type(key_string, cipher_alphabet) == 'numeric_key':
        numeric_key = int(key_string) % 26
        ab_key = plain_alphabet[0] + cipher_alphabet[numeric_key]
        a_key = cipher_alphabet[numeric_key]
        alpha_key = cipher_alphabet[numeric_key:] + cipher_alphabet[:numeric_key]
    elif get_key_type(key_string, cipher_alphabet) == 'ab_key':
        numeric_key = cipher_alphabet.find(key_string[1]) - plain_alphabet.find(key_string[0])
        ab_key = key_string
        a_key = cipher_alphabet[numeric_key]
        alpha_key = cipher_alphabet[numeric_key:] + cipher_alphabet[:numeric_key]
    elif get_key_type(key_string, cipher_alphabet) == 'a_key':
        numeric_key = cipher_alphabet.find(key_string)
        ab_key = plain_alphabet[0] + key_string
        a_key = key_string
        alpha_key = cipher_alphabet[numeric_key:] + cipher_alphabet[:numeric_key]
    elif get_key_type(key_string, cipher_alphabet) == 'alpha_key':
        numeric_key = cipher_alphabet.find(key_string[0])
        a_key = cipher_alphabet[numeric_key]
        ab_key = plain_alphabet[0] + a_key
        alpha_key = cipher_alphabet[numeric_key:] + cipher_alphabet[:numeric_key]
    else:
        raise ValueError('Input key is not a valid key type')
    return {'alpha_key': alpha_key, 'ab_key': ab_key, 'numeric_key': numeric_key, 'a_key': a_key}


def get_key_type(input_key, alphabet=Cipher.ALPHABET):
    try:
        input_key = str(input_key)
        try:
            int(input_key)
            key_type = 'numeric_key'
        except ValueError:
            if input_key.isalpha() and len(input_key) == 2:
                key_type = 'ab_key'
            elif input_key.isalpha() and len(input_key) == 1:
                key_type = 'a_key'
            elif len(input_key) == len(alphabet):
                numeric_key = input_key.find(alphabet[0])
                if numeric_key == -1:
                    raise ValueError('Input alpha key not found in alphabet')
                else:
                    alpha = alphabet[:numeric_key] + alphabet[numeric_key:]
                    if alpha == alphabet:
                        key_type = 'alpha_key'
                    else:
                        raise ValueError('Input alpha key does not match alphabet')
            else:
                raise ValueError
    except ValueError:
        raise ValueError('Input key is not a valid key type')
    return key_type


class CaesarKey(SubstitutionKey):
    def __init__(self, numeric_key=0, ab_key='', a_key='', reverse=False, *args, **kwargs):
        super(CaesarKey, self).__init__(*args, **kwargs)
        self.numeric_key = numeric_key
        self.ab_key = ab_key
        self.a_key = a_key
        self.reverse = reverse

    def set(self, *, alpha_key=None, numeric_key=None, ab_key=None, a_key=None):
        if alpha_key is not None:
            self.alpha_key = alpha_key
        if numeric_key is not None:
            self.numeric_key = numeric_key
        if ab_key is not None:
            self.ab_key = ab_key
        if a_key is not None:
            self.a_key = a_key

    def calculate(self, *, alpha_key=None, numeric_key=None, ab_key=None, a_key=None):
        try:
            if alpha_key is not None:
                assert numeric_key is None
                assert ab_key is None
                assert a_key is None
                keys = create_keys(alpha_key, reverse=self.reverse)
                keys['alpha_key'] = alpha_key
                self.set(**keys)
            elif numeric_key is not None:
                assert alpha_key is None
                assert ab_key is None
                assert a_key is None
                keys = create_keys(numeric_key, reverse=self.reverse)
                keys['numeric_key'] = numeric_key
                self.set(**keys)
            elif ab_key is not None:
                assert alpha_key is None
                assert numeric_key is None
                assert a_key is None
                keys = create_keys(ab_key, reverse=self.reverse)
                keys['ab_key'] = ab_key
                self.set(**keys)
            elif a_key is not None:
                assert alpha_key is None
                assert numeric_key is None
                assert ab_key is None
                keys = create_keys(a_key, reverse=self.reverse)
                keys['a_key'] = a_key
                self.set(**keys)
            else:
                raise AssertionError
        except AssertionError:
            raise AssertionError('Calculate method expects exactly 1 key variable')

    def random(self):
        keys = create_keys(reverse=self.reverse)
        self.set(**keys)

    def validate(self, alphabet=Cipher.ALPHABET):
        for key_name, key_value in self.__dict__.items():
            if key_value and key_name != 'reverse':
                validation_key = key_value
                try:
                    validation_keys = create_keys(validation_key, reverse=self.reverse)
                    for validation_name, validation_value in validation_keys.items():
                        if self.__getattribute__(validation_name):
                            assert self.__getattribute__(validation_name) == validation_value
                        else:
                            self.__setattr__(validation_name, validation_value)
                except AssertionError:
                    raise AssertionError('Keys in caesar key do not match')
                except Exception as e:
                    raise e
        super(CaesarKey, self).validate(alphabet=alphabet)


class CaesarCipher(SubstitutionCipher):
    NAME = 'Caesar Cipher'

    def set_key(self, key=CaesarKey()):
        super(CaesarCipher, self).set_key(key)

    def clear_key(self):
        if self.key.reverse:
            self.key = CaesarKey(reverse=True)
        else:
            self.key = CaesarKey()

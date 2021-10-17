import random
from cypher.substitution import SubstitutionKey, SubstitutionCipher
from cypher.cipher import Cipher


def create_keys(input_key=None, alphabet=Cipher.ALPHABET):
    if input_key is None:
        input_key = random.randint(1, len(alphabet) - 1)
    key_string = str(input_key).upper()
    if get_key_type(key_string, alphabet) == 'numeric_key':
        numeric_key = int(key_string) % 26
        ab_key = alphabet[0] + alphabet[numeric_key]
        a_key = alphabet[numeric_key]
        alpha_key = alphabet[numeric_key:] + alphabet[:numeric_key]
    elif get_key_type(key_string, alphabet) == 'ab_key':
        numeric_key = alphabet.find(key_string[1]) - alphabet.find(key_string[0])
        ab_key = key_string
        a_key = alphabet[numeric_key]
        alpha_key = alphabet[numeric_key:] + alphabet[:numeric_key]
    elif get_key_type(key_string, alphabet) == 'a_key':
        numeric_key = alphabet.find(key_string)
        ab_key = alphabet[0] + key_string
        a_key = key_string
        alpha_key = alphabet[numeric_key:] + alphabet[:numeric_key]
    elif get_key_type(key_string, alphabet) == 'alpha_key':
        numeric_key = alphabet.find(key_string[0])
        a_key = alphabet[numeric_key]
        ab_key = alphabet[0] + a_key
        alpha_key = alphabet[numeric_key:] + alphabet[:numeric_key]
    else:
        raise ValueError('Input key is not a valid key type')
    return {'alpha_key': alpha_key, 'ab_key': ab_key, 'numeric_key': numeric_key, 'a_key': a_key}


def get_key_type(input_key, alphabet=Cipher.ALPHABET):
    try:
        input_key = str(input_key)
        if input_key.isnumeric():
            key_type = 'numeric_key'
        elif input_key.isalpha() and len(input_key) == 2:
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
    def __init__(self, numeric_key=None, ab_key=None, a_key=None, *args, **kwargs):
        super(CaesarKey, self).__init__(*args, **kwargs)
        self.numeric_key = numeric_key
        self.ab_key = ab_key
        self.a_key = a_key

    def validate(self, alphabet=Cipher.ALPHABET):
        validation_key = None
        for key_name, key_value in self.__dict__.items():
            if key_value:
                validation_key = key_value
        try:
            validation_keys = create_keys(validation_key)
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
    pass

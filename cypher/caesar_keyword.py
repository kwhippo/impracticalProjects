from cypher.cipher import Cipher
from cypher.utilities import get_random_word
from cypher.substitution import SubstitutionKey, SubstitutionCipher


def create_caesar_keyword_keys(keyword=None, alphabet=Cipher.ALPHABET):
    key_list = []
    if keyword is None:
        keyword = get_random_word(source='pokemon')
    for letter in keyword.upper():
        if letter in alphabet:
            if letter not in key_list:
                key_list.append(letter)

    ordered_key_list = sorted(key_list)
    key_index = [alphabet.find(key) for key in ordered_key_list]
    key_dict = {}
    wrap = alphabet[:alphabet.find(ordered_key_list[0])]
    wrapped_alphabet = alphabet + wrap
    for index, letter in enumerate(ordered_key_list):
        if index + 1 < len(ordered_key_list):
            next_index = key_index[index + 1]
        else:
            next_index = len(wrapped_alphabet) + 1
        key_dict[letter] = wrapped_alphabet[wrapped_alphabet.find(letter):next_index]

    alpha_key = ''
    for key in key_list:
        alpha_key += key_dict[key]

    return {'alpha_key': alpha_key, 'keyword': keyword}


class CaesarKeywordKey(SubstitutionKey):
    def __init__(self, keyword=None, *args, **kwargs):
        super(CaesarKeywordKey, self).__init__(*args, **kwargs)
        self.keyword = keyword

    def validate(self, alphabet=Cipher.ALPHABET):
        try:
            keys = create_caesar_keyword_keys(self.keyword)
            self.keyword = keys['keyword']
            self.alpha_key = keys['alpha_key']
        except Exception as e:
            raise e
        super(CaesarKeywordKey, self).validate(alphabet=alphabet)


class CaesarKeywordCipher(SubstitutionCipher):
    NAME = 'Caesar Keyword'

import random

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
POLYBIUS_ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
ALPHA_NUMERIC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
QWERTY = 'QWERTYUIOPASDFGHJKLZXCVBNM'


def deranged_alphabet(keyword, alphabet=ALPHABET):
    result_alphabet = ''
    keyword = keyword.upper()
    for character in keyword:
        if character not in result_alphabet:
            if character in alphabet:
                result_alphabet += character
    for character in alphabet:
        if character not in result_alphabet:
            result_alphabet += character
    return result_alphabet


def random_alphabet(alphabet=ALPHABET, no_fixed_point=True):
    fixed_point_test = True
    random_alpha = ''
    while fixed_point_test:
        alpha_list = list(alphabet)
        random.shuffle(alpha_list)
        random_alpha = ''.join(alpha_list)
        if no_fixed_point:
            fixed_point_test = False
            for index, character in enumerate(random_alpha):
                if index == alphabet.find(character):
                    fixed_point_test = True
        else:
            break
    return random_alpha


if __name__ == '__main__':
    pass

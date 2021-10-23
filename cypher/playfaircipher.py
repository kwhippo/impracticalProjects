from cypher.cipher import Cipher, Key
from cypher.utilities import string_remove_duplicates, list_remove_duplicates, get_random_word, break_string


def find_letter(letter, key_table):
    row_num = -1
    col_num = -1
    for row_index, row in enumerate(key_table):
        try:
            col_num = row.index(letter)
            row_num = row_index
        except ValueError:
            continue
    if row_num == -1 or col_num == -1:
        raise ValueError('Letter is not in key table')
    return row_num, col_num


def get_letter(index, key_table):
    return key_table[index[0]][index[1]]


def increment_index(num, slide):
    index = num + slide
    if index == 5:
        index = 0
    elif index == -1:
        index = 4
    return index


def crypt_bigram(bigram, key_table, slide):
    bigram_list = list(bigram)
    try:
        validate_key_table(key_table)
    except Exception as e:
        print('There was an error with the key table')
        raise e
    if type(bigram) != str:
        raise TypeError('Bigram must be a string')
    if len(bigram) != 2:
        raise ValueError('Bigram must be 2 characters')
    for letter in bigram:
        bigram_list.append(letter)
        if letter not in PlayfairCipher.ALPHABET:
            raise ValueError('Bigram must only contain uppercase letters in the alphabet '
                             'excluding "J"')
    if bigram_list[0] == bigram_list[1]:
        raise ValueError('Bigram can not contain duplicate letters')

    letter1 = find_letter(bigram_list[0], key_table)
    letter2 = find_letter(bigram_list[1], key_table)
    if letter1[0] == letter2[0]:
        # Row
        crypted1 = get_letter((letter1[0], increment_index(letter1[1], slide)), key_table)
        crypted2 = get_letter((letter2[0], increment_index(letter2[1], slide)), key_table)
    elif letter1[1] == letter2[1]:
        # Column
        crypted1 = get_letter((increment_index(letter1[0], slide), letter1[1]), key_table)
        crypted2 = get_letter((increment_index(letter2[0], slide), letter2[1]), key_table)
    else:
        # Rectangle
        crypted1 = get_letter((letter1[0], letter2[1]), key_table)
        crypted2 = get_letter((letter2[0], letter1[1]), key_table)

    return f'{crypted1}{crypted2}'


def crypt(text, key_table, slide):
    ciphertext = ''
    for symbol in text:
        if symbol in PlayfairCipher.ALPHABET:
            ciphertext += symbol
    cleaned_list = list(ciphertext)
    bigram_list = [cleaned_list.pop(0)]
    counter = 0
    for letter in cleaned_list:
        if len(bigram_list[counter]) == 1:
            if bigram_list[counter] == letter:
                bigram_list[counter] += 'X'
                counter += 1
                bigram_list.append(letter)
            else:
                bigram_list[counter] += letter
        else:
            counter += 1
            bigram_list.append(letter)
    if len(bigram_list[-1]) == 1:
        bigram_list[-1] += 'X'
    crypted_list = [crypt_bigram(bigram, key_table, slide) for bigram in bigram_list]
    return ''.join(crypted_list)


def create_key_table(keyword):
    keyword = string_remove_duplicates(keyword.replace('J', 'I')).upper()
    key_list = list(keyword) + list(PlayfairCipher.ALPHABET)
    key_list = list_remove_duplicates(key_list)
    key_table = [[], [], [], [], []]
    for row in key_table:
        for i in range(5):
            row.append(key_list.pop(0))
    return key_table


def validate_key_table(key_table):
    if type(key_table) != list:
        raise TypeError('Key table must be a list')
    if len(key_table) != 5:
        raise ValueError('Key table must contain 5 rows')
    alpha_list = []
    for row in key_table:
        if len(row) != 5:
            raise ValueError('Rows in key table must contain 5 columns')
        for letter in row:
            try:
                if not letter.isupper():
                    raise TypeError('Cells in key table must contain only uppercase letters')
            except AttributeError:
                raise AttributeError('Cells in key table must contain only letters')
            alpha_list.append(letter)
    alpha_list.sort()
    if alpha_list != list(PlayfairCipher.ALPHABET):
        raise ValueError('Key table must include all letters in alphabet excluding "J" without duplicates')


class PlayfairKey(Key):
    def __init__(self, keyword=None, key_table=None):
        super(PlayfairKey, self).__init__()
        self.keyword = keyword
        self.key_table = key_table

    def validate(self):
        if self.keyword is None and self.key_table is None:
            self.keyword = get_random_word('pokemon')
        if self.key_table is None:
            self.key_table = create_key_table(self.keyword)
        validate_key_table(self.key_table)
        super(PlayfairKey, self).validate()


class PlayfairCipher(Cipher):
    ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    NAME = 'Playfair'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alphabet = PlayfairCipher.ALPHABET

    def encrypt(self):
        super(PlayfairCipher, self).encrypt()
        plaintext = self.plaintext.upper().replace('J', 'I')
        self.ciphertext = break_string(crypt(plaintext, self.key.key_table, 1))

    def decrypt(self):
        super(PlayfairCipher, self).decrypt()
        self.plaintext = crypt(self.ciphertext, self.key.key_table, -1)

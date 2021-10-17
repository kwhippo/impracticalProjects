from cypher.keyword import Keyword
from cypher.tools import string_remove_duplicates, list_remove_duplicates, break_string


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


def increment_index(num):
    index = num + 1
    if index == 5:
        index = 0
    return index


def crypt(bigram, key_table):
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
        if letter not in Playfair.ALPHABET:
            raise ValueError('Bigram must only contain uppercase letters in the alphabet '
                             'excluding "J"')
    if bigram_list[0] == bigram_list[1]:
        raise ValueError('Bigram can not contain duplicate letters')

    letter1 = find_letter(bigram_list[0], key_table)
    letter2 = find_letter(bigram_list[1], key_table)
    if letter1[0] == letter2[0]:
        # Row
        crypted1 = get_letter((letter1[0], increment_index(letter1[1])), key_table)
        crypted2 = get_letter((letter2[0], increment_index(letter2[1])), key_table)
    elif letter1[1] == letter2[1]:
        # Column
        crypted1 = get_letter((increment_index(letter1[0]), letter1[1]), key_table)
        crypted2 = get_letter((increment_index(letter2[0]), letter2[1]), key_table)
    else:
        # Rectangle
        crypted1 = get_letter((letter1[0], letter2[1]), key_table)
        crypted2 = get_letter((letter2[0], letter1[1]), key_table)

    return f'{crypted1}{crypted2}'


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
    if alpha_list != list(Playfair.ALPHABET):
        raise ValueError('Key table must include all letters in alphabet excluding "J" without duplicates')


class Playfair(Keyword):
    ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys['key_table'] = None
        self.alphabet = Playfair.ALPHABET

    def create_key(self):
        super().create_key()
        self.keys['key'] = string_remove_duplicates(self.keys['key'].replace('J', 'I'))
        key_list = list(self.keys['key']) + list(self.alphabet)
        key_list = list_remove_duplicates(key_list)
        key_table = [[], [], [], [], []]
        for row in key_table:
            for i in range(5):
                row.append(key_list.pop(0))
        self.keys['key_table'] = key_table

    def validate_keys(self):
        validate_key_table(self.keys['key_table'])
        super().validate_keys()

    def encrypt(self):
        self.validate_keys()
        cleaned_decrypted = self.plaintext.upper().replace('J', 'I')
        decrypted = ''
        for symbol in cleaned_decrypted:
            if symbol in Playfair.ALPHABET:
                decrypted += symbol
        cleaned_list = list(decrypted)
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
        self.decrypted_text = decrypted
        crypted_list = [crypt(bigram, self.keys['key_table']) for bigram in bigram_list]
        self.encrypted_text = break_string(''.join(crypted_list))

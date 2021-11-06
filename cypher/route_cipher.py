import random
from cypher.cipher import Key, Cipher
from cypher.tools.utilities import is_prime, get_factors, get_random_word, break_string, SOURCE_FILES


def recommended_grid(text_length):
    factor_list = get_factors(text_length)
    if len(factor_list) == 0:
        text_length += 1
        factor_list = get_factors(text_length)
    if text_length < 6:
        raise ValueError('Text length is too short to generate effective key grid')
    # Choose most square grid and favor more rows over more columns for uneven messages
    if len(factor_list) % 2 == 0:
        first_middle = int(len(factor_list) / 2) - 1
    else:
        first_middle = int(len(factor_list) / 2)
    # If only 2 columns, favor more columns over rows
    if factor_list[first_middle][0] == 2:
        grid = factor_list[first_middle + 1]
    else:
        grid = factor_list[first_middle]
    return grid


def random_key_list(cols):
    plus_minus = (1, -1)
    key_list = []
    for key_int in range(1, cols + 1):
        key_list.append(int(key_int * random.choice(plus_minus)))
    random.shuffle(key_list)
    return key_list


def validate_key_list(input_list):
    try:
        int_list = [abs(int(i)) for i in input_list]
        int_list.sort()
        test_list = [i for i in range(1, len(int_list) + 1)]
        assert int_list == test_list
    except ValueError:
        raise ValueError('Key list must be a list of ints')
    except AssertionError:
        raise AssertionError('Key list must contain all abs values from 1 to length of list')


def validate_key_string(input_string):
    try:
        int_list = input_string.split(' ')
        validate_key_list(int_list)
    except AttributeError:
        raise AttributeError('Key string must be a string')
    except ValueError:
        raise ValueError('Key list must be a list of ints separated by a single space')
    except Exception as e:
        raise e


def validate_columns(input_columns):
    try:
        cols = int(input_columns)
        assert cols > 0
    except ValueError:
        raise ValueError('Columns must be an integer')
    except AssertionError:
        raise AssertionError('Columns must be greater than 0')


class RouteKey(Key):
    BLOCKS = [
        'word',
        'character',
    ]
    NOISE_OPTIONS = SOURCE_FILES

    def __init__(self, key_list=None, key_string=None, columns=None, block='word', noise=None, fudgel='FUDGEL'):
        super(RouteKey, self).__init__()
        self.key_list = key_list
        self.key_string = key_string
        self.columns = columns
        self.block = block
        self.noise = noise
        self.fudgel = fudgel
        if self.block == 'character' and self.fudgel == 'FUDGEL':
            self.fudgel = 'X'

    def calculate(self, *, key_list=None, key_string=None, columns=None, best_fit_length=None):
        try:
            if key_list is not None:
                assert key_string is None
                assert columns is None
                assert best_fit_length is None
                try:
                    validate_key_list(key_list)
                except Exception:
                    raise RuntimeError('Key list validation error')
                self.key_list = key_list
                self.key_string = ' '.join([str(i) for i in key_list])
                self.columns = len(key_list)
            elif key_string is not None:
                assert key_list is None
                assert columns is None
                assert best_fit_length is None
                try:
                    validate_key_string(key_string)
                except Exception:
                    raise RuntimeError('Key string validation error')
                self.key_list = [int(i) for i in key_string.split(' ')]
                self.key_string = key_string
                self.columns = len(self.key_list)
            elif columns is not None:
                assert key_list is None
                assert key_string is None
                assert best_fit_length is None
                try:
                    validate_columns(columns)
                except Exception:
                    raise RuntimeError('Column validation error')
                self.key_list = random_key_list(columns)
                self.key_string = ' '.join([str(i) for i in self.key_list])
                self.columns = columns
            elif best_fit_length is not None:
                assert key_list is None
                assert key_string is None
                assert columns is None
                try:
                    cols = recommended_grid(best_fit_length)[0]
                except Exception:
                    raise RuntimeError('Error calculating recommended grid')
                self.key_list = random_key_list(cols)
                self.key_string = ' '.join([str(i) for i in self.key_list])
                self.columns = cols
            else:
                raise AssertionError
        except AssertionError:
            raise AssertionError('Calculate expects exactly 1 keyword argument')
        except Exception as e:
            raise e

    def validate(self):
        super(RouteKey, self).validate()


class RouteCipher(Cipher):
    NAME = 'Route Cipher'

    def __init__(self, *args, **kwargs):
        super(RouteCipher, self).__init__(*args, **kwargs)

    def encrypt(self):
        if self.key.block == 'word':
            plaintext_list = self.plaintext.split()
        else:
            plaintext_list = break_string(self.plaintext, step=self.key.block).split()
        # Split plain text into list converting text to upper and stripping punctuation
        for index, word in enumerate(plaintext_list):
            if not word.isalnum():
                clean_word = ''
                for letter in word:
                    if letter.isalnum():
                        clean_word += letter
                plaintext_list[index] = clean_word.upper()
            else:
                plaintext_list[index] = word.upper()
        while '' in plaintext_list:
            plaintext_list.remove('')
        # Make sure length of list can be split evenly into columns adding filler word if required
        if is_prime(len(plaintext_list)):
            plaintext_list.append('FUDGEL')
        # Check that the message is long enough to effectively encode
        if len(plaintext_list) < 6:
            raise Exception('That message is not long enough to encrypt')
        # Select appropriately sized grid
        grid = recommended_grid(len(plaintext_list))
        cols = grid[0]
        rows = grid[1]
        # Build list of columns with noise added on last row
        col_list = []
        for c in range(cols):
            col_items = []
            for r in range(rows):
                col_items.append(plaintext_list[c + (r * cols)])
            filler_word = get_random_word().upper()
            col_items.append(filler_word)
            col_list.append(col_items)
        # Create the key and build shuffled list
        key_list = random_key_list(cols)
        route_key = ' '.join(str(key) for key in key_list)
        cipher_list = []
        for key in key_list:
            if key < 0:
                cipher_row = col_list[(abs(key) - 1)]
                cipher_list.append(cipher_row[::-1])
            else:
                cipher_row = col_list[key - 1]
                cipher_list.append(cipher_row)
        # Convert shuffled list to final cipher text
        cipher_text_list = []
        for chunk in cipher_list:
            for word in chunk:
                cipher_text_list.append(word)
        cipher_text = ' '.join(cipher_text_list)

        return cipher_text, route_key

    def decrypt(self):
        # Convert inputs into usable values
        cipher_list = list(self.ciphertext.split())
        key_int = [int(i) for i in self.key.key_list]
        # Determine the number of rows and columns
        cols = len(key_int)
        rows = int(len(cipher_list) / len(key_int))
        # Build the decrypted list
        translation_matrix = list([None] * cols)
        start = 0
        stop = rows
        for key in key_int:
            col_items = []
            if key < 0:
                col_items = cipher_list[start:stop]
            elif key > 0:
                col_items = list(reversed(cipher_list[start:stop]))
            translation_matrix[abs(key) - 1] = col_items
            start += rows
            stop += rows
        translation_list = []
        for i in range(rows):
            for col_items in translation_matrix:
                word = str(col_items.pop())
                translation_list.append(word)
        # Remove noise from cipher text
        plain_list = translation_list[:-cols]
        if plain_list[-1] == 'FUDGEL':
            plaintext = ' '.join(plain_list[:-1])
        else:
            plaintext = ' '.join(plain_list)

        return plaintext


if __name__ == '__main__':
    # PLAINTEXT = "All the world's a stage, And & all the men and women merely players;"
    # CIPHERTEXT = 'PLANE WOMEN A ALL FUDGEL FISH WORLDS AND EDGE CROSS PLAYERS AND ALL THE FLOW THICK' \
    #              ' MERELY STAGE DURING MEN THE'
    # KEY_STRING = '-4 7 3 -6 1 -5 -2'
    # k = RouteKey(key_string=KEY_STRING, block='word', noise=True)
    # c = RouteCipher(plaintext=PLAINTEXT, key=k)
    # c.encrypt()
    # if CIPHERTEXT == c.ciphertext:
    #     print('Successful encryption!')
    # else:
    #     print('Failed encryption :(')
    # c.decrypt()
    # if PLAINTEXT.upper() == c.plaintext:
    #     print('Successful decryption!')
    # else:
    #     print('Failed decryption :(')
    ks = '-1 2'
    validate_key_string(ks)

# -------------------------------------------------------------------------------------------------
# Impractical Python Projects
# Chapter 4
# Civil War Ciphers by Kevin Wares
# -------------------------------------------------------------------------------------------------
# Objective:
# Design an algorithm that will decrypt a route cipher based on an assumed encryption matrix and
# path. In the spirit of General Anson Stager, write a user-friendly program that will reduce
# human error.
# -------------------------------------------------------------------------------------------------
# Pseudocode:
# 1. Load the ciphertext string
# 2. Convert ciphertext into a cipher list to split out individual words
# 3. Get input for the number of columns and rows
# 4. Get input for the key
# 5. Convert key into a list to split out individual numbers
# 6. Create a new list for the translation matrix
# 7. For every number in the key:
#   1. Create a new list and append every n items (n = # of rows) from the cipher list
#   2. Use the sign of key number to decide whether to read the row forward or backward
#   3. Using the chose direction, add the new list to the matrix with the index based on the
#       column number used in the key
# 8. Create a new string to hold translation results
# 9. For range of rows:
#   1. For the nested list in translation matrix:
#       1. Remove the last word in nested list
#       2. Add the word to the translation string
# 10. Print the translation string
# -------------------------------------------------------------------------------------------------
# Notes:
# The bottom row of a route cipher is filler words
"""
Decrypt or encrypt route cipher code.

Decrypt: Take a message encrypted with the route cipher, the number of columns and rows in the
transposition matrix, and a key, then display the translated plaintext.
"""
import random

import cypher.cipher
import cypher.tools
import tools

# Encoder
PLAIN_TEXT = "All the world's a stage, And & all the men and women merely players;"


def encrypt(plain_text=PLAIN_TEXT):
    word_list = plain_text.split()

    # Split plain text into list converting text to upper and stripping punctuation
    for index, word in enumerate(word_list):
        if not word.isalnum():
            clean_word = ''
            for letter in word:
                if letter.isalnum():
                    clean_word += letter
            word_list[index] = clean_word.upper()
        else:
            word_list[index] = word.upper()
    while '' in word_list:
        word_list.remove('')

    # Make sure length of list can be split evenly into columns adding filler word if required
    if cypher.utilities.is_prime(len(word_list)):
        word_list.append('FUDGEL')

    # Check that the message is long enough to effectively encode
    if len(word_list) < 6:
        raise Exception('That message is not long enough to encrypt')

    # Select appropriately sized grid
    factors = cypher.utilities.get_factors(len(word_list))
    grid = recommended_grid(factors)
    cols = grid[0]
    rows = grid[1]

    # Build list of columns with noise added on last row
    col_list = []
    for c in range(cols):
        col_items = []
        for r in range(rows):
            col_items.append(word_list[c + (r * cols)])
        filler_word = cypher.utilities.get_random_word().upper()
        col_items.append(filler_word)
        col_list.append(col_items)

    # Create the key and build shuffled list
    key_list = generate_key(cols)
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


def recommended_grid(factor_list):
    # Choose most square grid
    if len(factor_list) % 2 == 0:
        first_middle = int(len(factor_list) / 2) - 1
    else:
        first_middle = int(len(factor_list) / 2)

    # Favor more columns over more rows for uneven messages
    if factor_list[first_middle][0] == 2:
        grid = factor_list[first_middle + 1]
    else:
        grid = factor_list[first_middle]

    return grid


def generate_key(cols):
    plus_minus = (1, -1)
    key_list = []
    for key_int in range(1, cols + 1):
        key_list.append(int(key_int * random.choice(plus_minus)))
    random.shuffle(key_list)
    return key_list


# Decoder
CIPHERTEXT = 'PLANE WOMEN A ALL FUDGEL FISH WORLDS AND EDGE CROSS PLAYERS AND ALL THE FLOW THICK' \
             ' MERELY STAGE DURING MEN THE'
CIPHER_KEY = '-4 7 3 -6 1 -5 -2'


def decrypt(cipher_text=CIPHERTEXT, key=CIPHER_KEY):
    # Convert inputs into usable values
    cipher_list = list(cipher_text.split())
    key_int = [int(i) for i in key.split()]

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


def main():
    print('Welcome to the Route Cipher')
    while True:
        options = ['encrypt message', 'decrypt message', 'exit']
        option = cypher.utilities.prompt_options(options, prompt='What would you like to do?')
        if option == 'encrypt message':
            print('Please enter your message or press enter for a random message.')
            try:
                message = input('Enter message:')
                if message == '':
                    message = PLAIN_TEXT
                encrypted_message, key = encrypt(message)
                print(f'Encrypted message: {encrypted_message}')
                print(f'Key: {key}')
            except Exception as e:
                print('There was an error:')
                print(e)
                print('Please try again.')
        elif option == 'decrypt message':
            print('Please enter your message and key.')
            try:
                message = input('Message to decrypt:')
                key = input('Key:')
                print(f'Decrypted text: {decrypt(message, key)}')
            except Exception as e:
                print('There was an error:')
                print(e)
                print('Please try again.')
        else:
            break


if __name__ == '__main__':
    main()

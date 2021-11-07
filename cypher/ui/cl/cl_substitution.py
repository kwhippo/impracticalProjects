import random

import cypher.tools
from cypher.caesar import input_caesar_key, create_caesar_key
from cypher.caesar_keyword import input_keyword_key, create_keyword_key
from cypher.substitution import encrypt, decrypt, ALPHABET, CIPHERS, random_alpha_key


def cl_encrypt_text():
    keys, cipher, known = cl_input_cipher_key()
    input_text, random_word = cypher.utilities.input_text()
    encrypted_text, key = encrypt(input_text, keys['key'])
    decrypted_text = decrypt(encrypted_text, keys['key'])
    print(f'Cipher: {cipher.title()}')
    if cipher == 'keyword':
        print(f"Keyword: {keys['keyword']}")
    if cipher == 'caesar':
        print(f"AB Key: {keys['ab_key']}")
        print(f"Numeric Key: {keys['numeric_key']}")
    print(f"Key: {keys['key']}")
    print(f'Input Text: {input_text}')
    print(f'Encrypted: {encrypted_text}')
    print(f'Decrypted: {decrypted_text}')


def cl_decrypt_text():
    input_text, random_word = cl_input_encrypted_text()
    if random_word:
        print(f'Encrypted: {input_text}')
    keys, cipher, known = cl_input_cipher_key()
    if known:
        decrypted_text = decrypt(input_text, keys['key'])
        print(f'Decrypted: {decrypted_text}')
    else:
        print("Unfortunately I can't decrypt a message without a key yet.")


def cl_main():
    print('Welcome to the Substitution Cipher!')
    while True:
        options = ['encrypt text', 'decrypt text', 'exit']
        option = cypher.utilities.prompt_options(options, prompt='What would you like to do?')
        if option == 'encrypt text':
            cl_encrypt_text()
            continue
        elif option == 'decrypt text':
            cl_decrypt_text()
            continue
        else:
            break


def cl_input_encrypted_text(prompt="Please input encrypted text or press enter for random word:"):
    unencrypted_text, is_random = cypher.utilities.input_text(prompt=prompt)
    if is_random:
        encrypted_text, key = encrypt(unencrypted_text)
    else:
        encrypted_text = unencrypted_text
    return encrypted_text, is_random


def cl_input_cipher_key():
    prompt = "Please input key or press enter for more options:"
    keys = {'key': None}
    cipher = None
    known = True
    while keys['key'] is None:
        key_input = input(prompt)
        if key_input:
            try:
                keys['key'] = valid_key(key_input)
                known = False
            except Exception as e:
                print(f'Invalid key: {key_input}')
                print(f'Error: {e}')
                print(f'Key must be an alphabetical string containing all characters in'
                      f' {ALPHABET} with no duplicates')
                continue
        else:
            ciphers = CIPHERS + ['unknown']
            cipher = cypher.utilities.prompt_options(ciphers, prompt='Please choose a cypher.')
            if cipher == 'caesar':
                keys = input_caesar_key()
            elif cipher == 'keyword':
                keys = input_keyword_key()
            elif cipher == 'random':
                keys = random_alpha_key()
            else:
                cipher = random.choice(CIPHERS)
                known = False
                if cipher == 'caesar':
                    keys = create_caesar_key()
                elif cipher == 'keyword':
                    keys = create_keyword_key()
                else:
                    keys = random_alpha_key()

    return keys, cipher, known
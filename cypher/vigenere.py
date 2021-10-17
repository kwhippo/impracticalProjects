import cypher.caesar
import cypher.cipher
import cypher.tools
import substitution


def create_vigenere_key(keyword=None):
    if keyword is None:
        keyword = cypher.utilities.get_random_word(source='pokemon')
    keys = {'keyword': keyword}
    try:
        for index, letter in enumerate(keyword.upper()):
            keys[index] = cypher.caesar.create_caesar_key(letter)
    except ValueError:
        print('Invalid keyword')
    return keys


def encrypt(text, key=None):
    encrypted_text = ''
    if type(key) is dict:
        keys = key
    else:
        keys = create_vigenere_key(key)
    for text_index, letter in enumerate(text.upper()):
        keyword_index = text_index
        if text_index >= len(keys['keyword']):
            keyword_index = keyword_index % len(keys['keyword'])
        encrypted_text += substitution.encrypt(letter, keys[keyword_index]['key'])[0]
    return encrypted_text, keys


def decrypt(text, keys):
    decrypted_text = ''
    for text_index, letter in enumerate(text.upper()):
        keyword_index = text_index
        if text_index >= len(keys['keyword']):
            keyword_index = keyword_index % len(keys['keyword'])
        decrypted_text += substitution.decrypt(letter, keys[keyword_index]['key'])[0]
    return decrypted_text

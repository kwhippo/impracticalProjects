"""
Translate English to Pig Latin.

Pig Latin translation works by moving the initial consonant or consonant cluster to the end of the
word suffixed by 'ay'. If the word starts with a vowel suffix with 'yay'.
"""
from cypher.cipher import Cipher

VOWELS = 'AEIOUaeiou'
PUNCTUATION = '",.;?!'


def word_to_pig_latin(word):
    """Convert a word to Pig Latin."""
    beginning_punctuation_removed = word
    beginning_punctuation = ''
    for index, character in enumerate(word):
        if character in PUNCTUATION:
            beginning_punctuation = beginning_punctuation + character
            beginning_punctuation_removed = word[index + 1:]
        else:
            break
    punctuation_removed = beginning_punctuation_removed
    ending_punctuation = ''
    for index, character in enumerate(beginning_punctuation_removed[::-1]):
        if character in PUNCTUATION:
            ending_punctuation = character + ending_punctuation
            punctuation_removed = beginning_punctuation_removed[:-(index + 1)]
        else:
            break

    no_apostrophe_hyphens = punctuation_removed.replace("'", "").replace("-", "")
    if not no_apostrophe_hyphens.isalpha():
        return word

    # If the word contains no vowels, treat the last letter as the first vowel
    first_vowel_index = -1
    for letter in punctuation_removed:
        if punctuation_removed.index(letter) != 0 and letter in VOWELS + 'Yy':
            if first_vowel_index == -1:
                first_vowel_index = punctuation_removed.index(letter)
        elif letter in VOWELS:
            if first_vowel_index == -1:
                first_vowel_index = punctuation_removed.index(letter)
        else:
            continue

    onset = punctuation_removed[:first_vowel_index]
    offset = punctuation_removed[first_vowel_index:]

    suffix = 'ay'
    if onset == '':
        suffix = 'yay'

    return beginning_punctuation + offset + onset + suffix + ending_punctuation


class PigLatinCipher(Cipher):
    def __init__(self, *args, **kwargs):
        super(PigLatinCipher, self).__init__(*args, **kwargs)

    def encrypt(self):
        """Convert phrase to Pig Latin."""
        words = self.plaintext.split()
        translated_words = []
        for word in words:
            translated_words.append(word_to_pig_latin(word))
        self.ciphertext = ' '.join(translated_words)

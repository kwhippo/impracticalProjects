# -------------------------------------------------------------------------------------------------
# Impractical Python Projects
# Chapter 1
# Pig Latin Translator by Kevin Wares
# -------------------------------------------------------------------------------------------------
# Objective:
# Create a program that translates an English word or phrase to Pig Latin
# -------------------------------------------------------------------------------------------------
# Pseudocode:
# 1. Define vowels
# 2. Define word to pig latin function
#   1. Step forward over word to remove beginning punctuation to add back later
#   2. Step backward over cleaned word to remove ending punctuation to add back later
#   3. Validate cleaned word allowing contractions and hyphenated words, return invalid words as-is
#   4. Find the first vowel
#   5. If y is not the first letter but comes before the first vowel treat as vowel
#   6. Define word parts
#       1. Define onset (or the first consonant or consonant cluster)
#       2. Define offset (the remainder of the word starting with the first vowel)
#       3. Define suffix ('ay' for words starting with a consonant and 'yay' for words starting
#           with a vowel
#   5. Return translated word with beginning and ending punctuation added back in
# 3. Define phrase to pig latin function
#   1. Split phrase into individual words
#   2. Translate each word
#   3. Return translated phrase
# 4. Define main function (user interface)
#   1. Prompt user for word or phrase
#   2. If user enters an empty string, exit
#   3. Translate user input
# -------------------------------------------------------------------------------------------------
# Additional functionality to add:
# 1. Add file input to user interface
"""
Translate English to Pig Latin.

Pig Latin translation works by moving the initial consonant or consonant cluster to the end of the
word suffixed by 'ay'. If the word starts with a vowel suffix with 'yay'.
"""
import cypher.cipher
import cypher.tools

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


def phrase_to_pig_latin(phrase):
    """Convert phrase to Pig Latin."""
    words = phrase.split()
    translated_words = []
    for word in words:
        translated_words.append(word_to_pig_latin(word))
    return ' '.join(translated_words)


def file_to_pig_latin(file):
    """Convert file to Pig Latin and save as file_translated.txt"""
    # TODO: Add error handling
    with open(file, 'r') as original:
        lines = original.readlines()
        with open(f'{file[:-4]}_piglatin.txt', 'w+') as translated:
            for line in lines:
                translated.write(phrase_to_pig_latin(line))
                translated.write('\n')


def main():
    """Provide user interface for Pig Latin Translator."""
    print('Welcome to the Pig Latin Translator')
    while True:
        options = ['translate message', 'exit']
        option = cypher.utilities.prompt_options(options)
        if option == 'translate message':
            user_input, random_word = cypher.utilities.input_text()
            if random_word:
                print(f'Input text: {user_input}')
            print(f'Translated text: {phrase_to_pig_latin(user_input)}')
            continue
        else:
            break


if __name__ == '__main__':
    main()

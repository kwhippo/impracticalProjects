# import random
from pprint import pprint

len_dist = {1: 26,
            2: 396,
            3: 678,
            4: 1127,
            5: 1379,
            6: 1504,
            7: 1468,
            8: 1162,
            9: 909,
            10: 610,
            11: 379,
            12: 208,
            13: 101,
            14: 38,
            15: 10,
            16: 3,
            18: 1}


def find_words(source):
    text = source
    phrase_candidates = []

    with open('../text_sources/words_alpha.txt', 'r') as p:
        lines = p.readlines()
        words = [line.strip() for line in lines]

    if len(text) > 18:
        max_length = 18
    else:
        max_length = len(text)

    trial_length = max_length
    phrase_candidate = []

    for i in range(max_length):
        while len(text) > 0:
            print(f'Trying to find: {text[:trial_length]}')
            if text[:trial_length] in words:
                phrase_candidate.append(text[:trial_length])
                print(f'Found: {text[:trial_length]}')
                text = text[trial_length:]
                trial_length = len(text)
            else:
                trial_length -= 1
            print(trial_length)
        print(phrase_candidate)
        if phrase_candidate and phrase_candidate not in phrase_candidates:
            phrase_candidates.append(phrase_candidate)
            print(trial_length)

    pprint(phrase_candidates)


# def find_split(source):
#     candidate_phrases = []
#     candidate_phrase = []
#     candidate_words = []
#
#     with open('text_sources/pokemon.txt', 'r') as p:
#         lines = p.readlines()
#         words = [line.strip() for line in lines]
#
#     text = source
#
#     start = 0
#     end = 1
#     while start < len(text):
#         candidate_word = text[start:end]
#         if candidate_word in words:
#             print(f'Found the word {candidate_word}')
#             candidate_words.append(candidate_word)
#             candidate_phrase.append(candidate_word)
#             start += len(candidate_word)
#         end += 1
#         if end > len(source):
#             candidate_phrases.append(candidate_phrase)


# if __name__ == '__main__':
#     with open('text_sources/pokemon.txt', 'r') as w:
#         testing_words = w.readlines()
#     testing = random.choice(testing_words).strip() + random.choice(testing_words).strip()
#     print(f'Testing word: {testing}')
#     find_split(testing)

if __name__ == '__main__':
    find_words('sheeffortlesslyeditedit')

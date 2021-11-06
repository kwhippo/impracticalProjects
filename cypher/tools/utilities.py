import os
import random

SOURCE_FILES = {
    'common': 'text_sources/words_common.txt',
    'extended': 'text_sources/words.txt',
    'pokemon': 'text_sources/pokemon.txt',
}


def list_remove_duplicates(original_list):
    new_list = []
    for item in original_list:
        if item not in new_list:
            new_list.append(item)
    return new_list


def string_remove_duplicates(original_string):
    new_string = ''
    for symbol in original_string:
        if symbol not in new_string:
            new_string += symbol
    return new_string


def break_string(original_string, step=5):
    string_list = []
    for b in range(0, len(original_string), step):
        string_list.append(original_string[b:b + step])
    return ' '.join(string_list)


def is_prime(number):
    flag = True
    if number == 1:
        flag = False
    elif number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                flag = False
                break
    return flag


def get_factors(number):
    factors = []
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                factors.append([i, int(number / i)])
    return factors


def get_random_word(source=None):
    if source in SOURCE_FILES:
        file = SOURCE_FILES[source]
    else:
        file = SOURCE_FILES['common']
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, file), 'r') as words_file:
        word = random.choice(words_file.readlines())
    return word.strip()


def get_random_fortune():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'text_sources/fortunes.txt'), 'r') as fortune_file:
        fortune = random.choice(fortune_file.readlines())
    return fortune.strip()


def input_text(prompt="Please input text or press enter for random word:"):
    text_input = input(prompt)
    is_random = False
    if text_input == '':
        text_input = get_random_word('extended')
        is_random = True
    return text_input, is_random


def prompt_options(options, prompt=None):
    try:
        options = list(options)
    except TypeError:
        print(f'options must be a list')
    if prompt is None:
        prompt = f'Please enter an option from the list:'
    print(prompt)
    for index, option_name in enumerate(options):
        if not option_name.isupper():
            option_name = option_name.title()
        print(f'{index + 1}: {option_name}')
    option = input_valid_option(options=len(options)) - 1
    return options[option]


def input_valid_option(prompt=None, options=2):
    if prompt is None:
        prompt = f'Please enter option (1-{options}):'
    try:
        options = int(options)
        if options < 2:
            raise ValueError
    except ValueError:
        print('number_options must be an integer greater than 1')
    while True:
        try:
            option = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if option < 1 or option > options:
            print('Sorry, that is not a valid option.')
            continue
        else:
            return option


def output_to_file(source, output_file):
    try:
        with open(output_file, 'w+') as file:
            file.write(source)
    except Exception as e:
        print(f'There was an error with the output file.')
        print(f'Error: {e}')


def validate_one_kwarg(**kwargs):
    count = 0
    valid = True
    for kwarg in kwargs:
        if kwarg is not None:
            count += 1
    if count != 1:
        valid = False
    return valid

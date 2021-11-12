import cypher.cipher
import cypher.tools
from cypher import tools


def reverse_text(text):
    reversed_text = ''
    try:
        reversed_text = text[::-1]
    finally:
        return reversed_text


def reverse_file(file):
    with open(file, 'r') as text_file:
        lines = text_file.readlines()
        with open(f'{file[:-4]}_reversed.txt', 'w+') as new_file:
            for line in reversed(lines):
                new_file.write(reverse_text(line))


def main():
    print('Welcome to the Reverse Cipher')
    while True:
        options = ['reverse text', 'exit']
        option = cypher.utilities.prompt_options(options)
        if option == 'reverse text':
            user_input, random_word = cypher.utilities.input_text()
            if random_word:
                print(f'Input text: {user_input}')
            print(f'Reversed text: {reverse_text(user_input)}')
            continue
        else:
            break


if __name__ == '__main__':
    main()

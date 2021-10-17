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

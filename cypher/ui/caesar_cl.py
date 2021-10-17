def input_caesar_key():
    caesar_key_options = ['AB', 'numeric', 'random']
    keys = {'key': None, 'ab_key': None, 'numeric_key': None}
    while keys['key'] is None:
        prompt = 'Please enter a Caesar key option.'
        key_option = cypher.utilities.prompt_options(caesar_key_options, prompt=prompt)
        if key_option == 'random':
            keys = create_caesar_key()
        else:
            try:
                key_input = input(f'Enter {key_option} key:')
                keys = create_caesar_key(key_input)
            except ValueError as e:
                print(e)
                continue
    return keys
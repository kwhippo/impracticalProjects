def input_keyword_key():
    keys = {'key': None, 'keyword': None}
    while keys['key'] is None:
        keys['keyword'] = input('Enter keyword key or press enter for random:')
        if keys['keyword'] == '':
            keys = create_keyword_key()
        elif ' ' in keys['keyword']:
            print('Keyword must be a single word')
            continue
        else:
            for letter in keys['keyword']:
                if letter in ALPHABET:
                    keys = create_keyword_key(keys['keyword'])
                else:
                    print(f'Keyword must contain at least one character in {ALPHABET}')
    return keys

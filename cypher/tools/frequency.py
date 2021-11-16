def calculate_plaintext_frequency(plaintext, alphabet):
    """
    Calculate the frequency of alphabet characters in plaintext and return frequency list

    :param plaintext: Text body to calculate frequency from
    :type plaintext: str
    :param alphabet: String value of plaintext alphabet
    :return: frequency: List of frequency sorted in alphabet order
    """
    alpha_dict = {}
    for character in alphabet:
        alpha_dict[character] = 1
    for character in plaintext.upper():
        if character in alpha_dict:
            alpha_dict[character] += 1
    frequency_list = [x for x in alpha_dict.values()]
    return frequency_list

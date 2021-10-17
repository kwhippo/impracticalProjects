import itertools
from substitution import ALPHABET

count = 1

# This does not work, creates a memory error because 26! is WAAAY too big
with open('substitution_keys.txt', 'w+') as f:
    for cipher in list(itertools.permutations(ALPHABET)):
        f.write(cipher)
        count += 1
        if count > 20:
            break

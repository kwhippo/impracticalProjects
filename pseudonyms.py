# -------------------------------------------------------------------------------------------------
# Impractical Python Projects
# Chapter 1
# Silly Name Generator
# -------------------------------------------------------------------------------------------------
# Objective:
# Randomly generate funny sidekick names using Python code that conforms to established style
# guidelines
# -------------------------------------------------------------------------------------------------
# Pseudocode:
# 1. Load a list of first names
# 2. Load a list of surnames
# 3. Choose a first name at random and assign to a variable
# 4. Choose a surname at random and assign to a variable
# 5. Print the names to the screen in order and in red font
# 6. Ask the user to quit or play again
# 7. If user plays again: repeat
# 8. If user quits: exit
# -------------------------------------------------------------------------------------------------
"""Generate funny names by randomly combining names from 2 separate lists."""
import sys
import random

first = ('Baby Oil', 'Bad News', 'Big Burps', 'Dark Skies',
         'Huckleberry', 'Schlomo', 'Shmoo', 'Wheezy Joe')

last = ('Appleyard', 'Bigmeat', 'Breedslovetrout', 'Cocktoasten',
        'Overturf', 'Quakenbush', 'Wigglesworth')


def main():
    """Choose names at random from 2 tuples of names and print to screen."""
    print('Welcome to the Sidekick Name Picker')

    while True:
        first_name = random.choice(first)
        last_name = random.choice(last)
        print('{} {}'.format(first_name, last_name), file=sys.stderr)

        try_again = input('Press enter to try again or n to quit.')
        if try_again.lower() == 'n':
            break

    input('Press enter to exit.')


if __name__ == '__main__':
    main()

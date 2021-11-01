import cypher.cipher
import cypher.ui.cl.cl_substitution
import cypher.tools
import piglatin
import reverse_cipher
import route_cipher


def main():
    print('Welcome to the Cipher Project!')
    while True:
        options = [
            'pig latin',
            'route cipher',
            'substitution cipher',
            'reverse cipher',
            'exit',
        ]
        option = cypher.utilities.prompt_options(options)
        if option == 'pig latin':
            piglatin.main()
        elif option == 'route cipher':
            route_cipher.main()
        elif option == 'substitution cipher':
            cypher.ui.cl.cl_substitution.cl_main()
        elif option == 'reverse cipher':
            reverse_cipher.main()
        else:
            print('Goodbye!')
            quit()


if __name__ == '__main__':
    main()

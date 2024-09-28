from tkinter import *
import ttkbootstrap as ttk
from cypher.ui import mainframe


class App:
    """
        App class provides the main application window and initializes the user interface components such as the menu
        bar and the main frame. It allows for setting up different encryption and decryption algorithms, utilities, and
        help options.

        :param master: The parent Tkinter window.
        :param start: A boolean flag to determine if the welcome frame should be shown at startup.
    """

    def __init__(self, master, start=False):
        self.master = master
        self.menubar = Menu(master)
        self.mainframe = ttk.Frame(master)

        self.master.title('Bandercrypt')
        # self.master.geometry('450x750')
        self.master.resizable(False, False)
        self.master.option_add('*tearOff', False)
        self.setup_menubar()

        if start:
            self.setup_mainframe(setup_frame=mainframe.WelcomeFrame)
        else:
            self.setup_mainframe()

    def setup_menubar(self):
        self.master.config(menu=self.menubar)
        self.setup_menu_file()
        self.setup_menu_cipher()
        self.setup_menu_decryption()
        self.setup_menu_utilities()
        self.setup_menu_help()

    def setup_menu_file(self):
        # create the file menu
        file_menu = Menu(self.menubar)
        # add menu options
        file_menu.add_command(label='Save Key', state='disabled')
        file_menu.add_command(label='Load Key', state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label='Save Plaintext', state='disabled')
        file_menu.add_command(label='Open Plaintext', state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label='Save Ciphertext', state='disabled')
        file_menu.add_command(label='Open Ciphertext', state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.destroy)
        # add menu to the menubar
        self.menubar.add_cascade(label="File", menu=file_menu)

    def setup_menu_cipher(self):
        # create the cipher menu
        cipher_menu = Menu(self.menubar)
        # add an encoding submenu
        encoding_menu = Menu(self.menubar)
        encoding_menu.add_command(label='Base64', state='disabled')
        # add a codes submenu
        codes_menu = Menu(cipher_menu)
        codes_menu.add_command(label='Code Book', state='disabled')
        codes_menu.add_command(label='Gibberish', state='disabled')
        codes_menu.add_command(label='Oppish', state='disabled')
        codes_menu.add_command(label='Ubbi Dubbi', state='disabled')
        codes_menu.add_command(label='Double Dutch', state='disabled')
        codes_menu.add_command(label='leetspeak', state='disabled')
        # add a substitution submenu
        substitution_menu = Menu(cipher_menu)
        substitution_menu.add_command(label='Simple Substitution',
                                      command=lambda: self.setup_mainframe(
                                          mainframe.SimpleSubstitutionFrame))
        substitution_menu.add_command(label='Caesar',
                                      command=lambda: self.setup_mainframe(mainframe.CaesarFrame))
        substitution_menu.add_command(label='ROT13',
                                      command=lambda: self.setup_mainframe(mainframe.ROT13Frame))
        substitution_menu.add_command(label='Caesar Reverse',
                                      command=lambda: self.setup_mainframe(
                                          mainframe.ReverseCaesarFrame))
        substitution_menu.add_command(label='Atbash',
                                      command=lambda: self.setup_mainframe(mainframe.AtbashFrame))
        substitution_menu.add_command(label='Caesar Keyword',
                                      command=lambda: self.setup_mainframe(
                                          mainframe.CaesarKeywordFrame))
        substitution_menu.add_command(label='Homophonic Substitution',
                                      command=lambda: self.setup_mainframe(
                                          mainframe.HomophonicFrame))
        substitution_menu.add_command(label='One-Pad', state='disabled')
        substitution_menu.add_command(label='Polybius Square', state='disabled')
        substitution_menu.add_command(label='Straddle Checkerboard', state='disabled')
        substitution_menu.add_command(label='Morse', state='disabled')
        # add a polyalphabetic submenu
        polyalphabetic_menu = Menu(cipher_menu)
        polyalphabetic_menu.add_command(label='Vigenere',
                                        command=lambda: self.setup_mainframe(
                                            mainframe.VigenereFrame))
        polyalphabetic_menu.add_command(label='Autokey', state='disabled')
        polyalphabetic_menu.add_command(label='Beaufort', state='disabled')
        polyalphabetic_menu.add_command(label='Porta', state='disabled')
        # add a block submenu
        block_menu = Menu(cipher_menu)
        block_menu.add_command(label='Playfair',
                               command=lambda: self.setup_mainframe(mainframe.PlayfairFrame))
        block_menu.add_command(label='Four-Square', state='disabled')
        # add a transposition submenu
        transposition_menu = Menu(cipher_menu)
        transposition_menu.add_command(label='Simple Transposition', state='disabled')
        transposition_menu.add_command(label='Reverse', state='disabled')
        transposition_menu.add_command(label='Route', state='disabled')
        transposition_menu.add_command(label='Columnar Transposition', state='disabled')
        transposition_menu.add_command(label='Rail Fence', state='disabled')
        # add a mathematical submenu
        math_menu = Menu(cipher_menu)
        math_menu.add_command(label='Affine', state='disabled')
        math_menu.add_command(label='Hill', state='disabled')
        math_menu.add_command(label='Multiplicative', state='disabled')
        math_menu.add_command(label='Textbook RSA', state='disabled')
        # add a mixed submenu
        mixed_menu = Menu(cipher_menu)
        mixed_menu.add_command(label='ADFGX', state='disabled')
        mixed_menu.add_command(label='ADFVGX', state='disabled')
        mixed_menu.add_command(label='Bifid', state='disabled')
        mixed_menu.add_command(label='Trifid', state='disabled')
        mixed_menu.add_command(label='Fractionated Morse', state='disabled')
        # add a steganography submenu
        steganography_menu = Menu(cipher_menu)
        steganography_menu.add_command(label='Ave Maria', state='disabled')
        steganography_menu.add_command(label='Baconian', state='disabled')
        steganography_menu.add_command(label='Image', state='disabled')
        # add a machines submenu
        machines_menu = Menu(cipher_menu)
        machines_menu.add_command(label='Decoder Ring', state='disabled')
        machines_menu.add_command(label='Scytale', state='disabled')
        machines_menu.add_command(label='Enigma', state='disabled')
        machines_menu.add_command(label='Lorenz', state='disabled')
        # add the menu to the menubar
        cipher_menu.add_cascade(label='Encoding', menu=encoding_menu)
        cipher_menu.add_cascade(label="Codes", menu=codes_menu)
        cipher_menu.add_cascade(label="Substitution", menu=substitution_menu)
        cipher_menu.add_cascade(label="Polyalphabetic", menu=polyalphabetic_menu)
        cipher_menu.add_cascade(label="Block Substitution", menu=block_menu)
        cipher_menu.add_cascade(label="Transposition", menu=transposition_menu)
        cipher_menu.add_cascade(label="Mathematical", menu=math_menu)
        cipher_menu.add_cascade(label="Mixed", menu=mixed_menu)
        cipher_menu.add_cascade(label="Steganography", menu=steganography_menu)
        cipher_menu.add_cascade(label="Machines", menu=machines_menu)
        self.menubar.add_cascade(label="Ciphers", menu=cipher_menu)

    def setup_menu_decryption(self):
        # create the decryption menu
        decryption_menu = Menu(self.menubar)
        # add menu options
        decryption_menu.add_command(label='Frequency Analysis', state='disabled')
        decryption_menu.add_command(label='Crib Dragging', state='disabled')
        decryption_menu.add_command(label='Hill Climbing', state='disabled')
        decryption_menu.add_command(label='Brute Force', state='disabled')
        # add the menu to the menubar
        self.menubar.add_cascade(label="Decryption", menu=decryption_menu)

    def setup_menu_utilities(self):
        # create the utilities menu
        utilities_menu = Menu(self.menubar)
        # add menu options
        utilities_menu.add_command(label='Word Finder', state='disabled')
        utilities_menu.add_command(label='Check English', state='disabled')
        utilities_menu.add_command(label='Random', state='disabled')
        utilities_menu.add_command(label='Poetry', state='disabled')
        utilities_menu.add_command(label='Math', state='disabled')
        utilities_menu.add_command(label='Salt', state='disabled')
        # add the menu to the menubar
        self.menubar.add_cascade(label="Utilities", menu=utilities_menu)

    def setup_menu_help(self):
        # create the help menu
        help_menu = Menu(self.menubar)
        # add menu options
        help_menu.add_command(label='Welcome',
                              command=lambda: self.setup_mainframe(mainframe.WelcomeFrame))
        help_menu.add_command(label='About...',
                              command=lambda: self.setup_mainframe(mainframe.Mainframe))
        # add the menu to the menubar
        self.menubar.add_cascade(label="Help", menu=help_menu)

    def setup_mainframe(self, setup_frame=mainframe.Mainframe):
        self.mainframe.destroy()
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.pack()
        setup_frame(self.mainframe)


if __name__ == '__main__':
    root = Tk()
    App(root, start=True)
    root.mainloop()

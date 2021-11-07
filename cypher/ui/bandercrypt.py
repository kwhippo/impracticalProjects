from tkinter import *
from tkinter import ttk
from cypher.ui import mainframe


class App:
    def __init__(self, master, start=False):
        self.master = master
        self.menubar = Menu(master)
        self.mainframe = ttk.Frame(master)

        self.master.title('Bandercrypt')
        self.master.geometry('450x700')
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
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open...')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.destroy)
        # add menu to the menubar
        self.menubar.add_cascade(label="File", menu=file_menu)

    def setup_menu_cipher(self):
        # create the cipher menu
        cipher_menu = Menu(self.menubar)
        # add a codes submenu
        codes_menu = Menu(cipher_menu)
        codes_menu.add_command(label='Code Book')
        codes_menu.add_command(label='Gibberish')
        codes_menu.add_command(label='Oppish')
        codes_menu.add_command(label='Ubbi Dubbi')
        codes_menu.add_command(label='Double Dutch')
        codes_menu.add_command(label='leetspeak')
        # add a substitution submenu
        substitution_menu = Menu(cipher_menu)
        substitution_menu.add_command(label='Simple Substitution',
                                      command=lambda: self.setup_mainframe(mainframe.SimpleSubstitutionFrame))
        substitution_menu.add_command(label='Caesar',
                                      command=lambda: self.setup_mainframe(mainframe.CaesarFrame))
        substitution_menu.add_command(label='ROT13',
                                      command=lambda: self.setup_mainframe(mainframe.ROT13Frame))
        substitution_menu.add_command(label='Caesar Reverse',
                                      command=lambda: self.setup_mainframe(mainframe.ReverseCaesarFrame))
        substitution_menu.add_command(label='Atbash',
                                      command=lambda: self.setup_mainframe(mainframe.AtbashFrame))
        substitution_menu.add_command(label='Caesar Keyword')
        substitution_menu.add_command(label='Morse')
        substitution_menu.add_command(label='Homophonic Substitution')
        substitution_menu.add_command(label='One-Pad')
        substitution_menu.add_command(label='Polybius Square')
        substitution_menu.add_command(label='Straddle Checkerboard')
        substitution_menu.add_command(label='Base64')
        # add a polyalphabetic submenu
        polyalphabetic_menu = Menu(cipher_menu)
        polyalphabetic_menu.add_command(label='Vigenere')
        polyalphabetic_menu.add_command(label='Autokey')
        polyalphabetic_menu.add_command(label='Beaufort')
        polyalphabetic_menu.add_command(label='Porta')
        # add a block submenu
        block_menu = Menu(cipher_menu)
        block_menu.add_command(label='Playfair')
        block_menu.add_command(label='Four-Square')
        # add a transposition submenu
        transposition_menu = Menu(cipher_menu)
        transposition_menu.add_command(label='Simple Transposition')
        transposition_menu.add_command(label='Reverse')
        transposition_menu.add_command(label='Route')
        transposition_menu.add_command(label='Columnar Transposition')
        transposition_menu.add_command(label='Rail Fence')
        # add a mathematical submenu
        math_menu = Menu(cipher_menu)
        math_menu.add_command(label='Affine')
        math_menu.add_command(label='Hill')
        math_menu.add_command(label='Multiplicative')
        math_menu.add_command(label='Textbook RSA')
        # add a mixed submenu
        mixed_menu = Menu(cipher_menu)
        mixed_menu.add_command(label='ADFGX')
        mixed_menu.add_command(label='ADFVGX')
        mixed_menu.add_command(label='Bifid')
        mixed_menu.add_command(label='Trifid')
        mixed_menu.add_command(label='Fractionated Morse')
        # add a steganography submenu
        steganography_menu = Menu(cipher_menu)
        steganography_menu.add_command(label='Ave Maria')
        steganography_menu.add_command(label='Baconian')
        steganography_menu.add_command(label='Image')
        # add a machines submenu
        machines_menu = Menu(cipher_menu)
        machines_menu.add_command(label='Decoder Ring')
        machines_menu.add_command(label='Scytale')
        machines_menu.add_command(label='Enigma')
        machines_menu.add_command(label='Lorenz')
        # add the menu to the menubar
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
        decryption_menu.add_command(label='Frequency Analysis')
        decryption_menu.add_command(label='Crib Dragging')
        decryption_menu.add_command(label='Hill Climbing')
        decryption_menu.add_command(label='Brute Force')
        # add the menu to the menubar
        self.menubar.add_cascade(label="Decryption", menu=decryption_menu)

    def setup_menu_utilities(self):
        # create the utilities menu
        utilities_menu = Menu(self.menubar)
        # add menu options
        utilities_menu.add_command(label='Word Finder')
        utilities_menu.add_command(label='Check English')
        utilities_menu.add_command(label='Random')
        utilities_menu.add_command(label='Poetry')
        utilities_menu.add_command(label='Math')
        utilities_menu.add_command(label='Salt')
        # add the menu to the menubar
        self.menubar.add_cascade(label="Utilities", menu=utilities_menu)

    def setup_menu_help(self):
        # create the help menu
        help_menu = Menu(self.menubar)
        # add menu options
        help_menu.add_command(label='Welcome', command=lambda: self.setup_mainframe(mainframe.WelcomeFrame))
        help_menu.add_command(label='About...', command=lambda: self.setup_mainframe(mainframe.Mainframe))
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

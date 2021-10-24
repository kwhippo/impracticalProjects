from tkinter import *
from tkinter import ttk
from cypher.substitution import SubstitutionCipher, SubstitutionKey
from cypher.caesar import CaesarCipher, CaesarKey
from cypher.caesar_keyword import CaesarKeywordCipher, CaesarKeywordKey
from cypher.playfaircipher import PlayfairCipher, PlayfairKey
from cypher.utilities import get_random_fortune
from cypher.vigenere import VigenereCipher, VigenereKey

global cipher
global key


balanced_grid_kwargs = {'sticky': (N, S, E, W), 'pady': 5, 'padx': 5}
pad_5_kwargs = {'pady': 5, 'padx': 5}


class KeyGUI:
    def __init__(self, master):
        # Create Header Frame
        self.style = ttk.Style()
        self.frame_header = ttk.Frame(master)
        self.style.configure('Header.TLabel', font=('TkDefaultFont', 14, 'bold'))
        ttk.Label(self.frame_header, text=f'{cipher.NAME} Cipher', style='Header.TLabel').pack()

        # Create Key Frame
        self.frame_key = Frame(master)

        # Setup Key Variables
        self.variable_alpha_key = StringVar()
        self.variable_numeric_key = StringVar()
        self.variable_ab_key = StringVar()
        self.variable_a_key = StringVar()
        self.variable_numeric_scale = StringVar()
        self.variable_keyword = StringVar()
        self.variable_key_row_0 = StringVar()
        self.variable_key_row_1 = StringVar()
        self.variable_key_row_2 = StringVar()
        self.variable_key_row_3 = StringVar()
        self.variable_key_row_4 = StringVar()

        self.frame_key = LabelFrame(master, text='Key')

        self.frame_key_buttons = Frame(self.frame_key)
        self.button_clear = ttk.Button(self.frame_key_buttons, text='Clear',
                                       command=self.clear_key_button)
        self.button_random = ttk.Button(self.frame_key_buttons, text='Random',
                                        command=self.random_key_button)

        self.button_clear.grid(row=0, column=0, **balanced_grid_kwargs)
        self.button_random.grid(row=0, column=1, **balanced_grid_kwargs)

        # Key Variables

        self.frame_key_variables = Frame(self.frame_key)
        self.label_alpha_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        self.entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_alpha_key)
        if type(key) == CaesarKey:
            self.entry_alpha_key.state(['readonly'])
            self.label_numeric_key = ttk.Label(self.frame_key_variables, text='Numeric Key')
            self.spinbox_numeric_key = ttk.Spinbox(self.frame_key_variables, from_=-100.0, to=100.0, width=5,
                                                   format='%3.0f',
                                                   textvariable=self.variable_numeric_key,
                                                   command=self.spinbox_numeric_key_incremented)
            self.variable_numeric_key.trace_add('write', self.write_spinbox_numeric_key)
            self.label_ab_key = ttk.Label(self.frame_key_variables, text='AB Key')
            self.combobox_ab_key = ttk.Combobox(self.frame_key_variables, width=4, textvariable=self.variable_ab_key)
            self.values_ab_key = []
            for a in cipher.alphabet:
                for b in cipher.alphabet:
                    self.values_ab_key.append(f'{a}{b}')
            self.combobox_ab_key['values'] = self.values_ab_key
            self.combobox_ab_key.state(['readonly'])
            self.combobox_ab_key.bind('<<ComboboxSelected>>', self.combobox_ab_key_selected)
            self.label_a_key = ttk.Label(self.frame_key_variables, text='A Key')
            self.combobox_a_key = ttk.Combobox(self.frame_key_variables, width=3, textvariable=self.variable_a_key)
            self.combobox_a_key['values'] = list(cipher.alphabet)
            self.combobox_a_key.state(['readonly'])
            self.combobox_a_key.bind('<<ComboboxSelected>>', self.combobox_a_key_selected)
            self.scale_numeric_key = ttk.Scale(self.frame_key_variables, orient=HORIZONTAL, length=100,
                                               from_=0.0, to=25.0, variable=self.variable_numeric_scale,
                                               command=self.update_scale_numeric_key)

            self.grid_substitution_key_variables()
            self.label_numeric_key.grid(row=1, column=0, **pad_5_kwargs, sticky=E)
            self.spinbox_numeric_key.grid(row=1, column=1, **pad_5_kwargs, sticky=W,)
            self.label_ab_key.grid(row=1, column=2, **pad_5_kwargs, sticky=E)
            self.combobox_ab_key.grid(row=1, column=3, **pad_5_kwargs, sticky=W)
            self.label_a_key.grid(row=3, column=0, **pad_5_kwargs, sticky=E)
            self.combobox_a_key.grid(row=3, column=1, **pad_5_kwargs, sticky=W)
            self.scale_numeric_key.grid(row=3, column=2, columnspan=2, **pad_5_kwargs)

        elif type(key) == CaesarKeywordKey:
            self.label_keyword = ttk.Label(self.frame_key_variables, text='Keyword')
            self.entry_keyword = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_keyword)

            self.grid_substitution_key_variables()
            self.label_keyword.grid(row=1, column=0, padx=5, pady=5, sticky=E)
            self.entry_keyword.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=W)

        elif type(key) == SubstitutionKey:
            self.grid_substitution_key_variables()

        elif type(key) == PlayfairKey:
            self.label_keyword = ttk.Label(self.frame_key_variables, text='Keyword')
            self.entry_keyword = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_keyword)
            self.label_key_table = ttk.Label(self.frame_key_variables, text='Key Table')
            self.label_key_row_0 = ttk.Label(self.frame_key_variables, text='A B C D E', font=('Courier', 11),
                                             textvariable=self.variable_key_row_0)
            self.label_key_row_1 = ttk.Label(self.frame_key_variables, text='F G H I K', font=('Courier', 11),
                                             textvariable=self.variable_key_row_1)
            self.label_key_row_2 = ttk.Label(self.frame_key_variables, text='L M N O P', font=('Courier', 11),
                                             textvariable=self.variable_key_row_2)
            self.label_key_row_3 = ttk.Label(self.frame_key_variables, text='Q R S T U', font=('Courier', 11),
                                             textvariable=self.variable_key_row_3)
            self.label_key_row_4 = ttk.Label(self.frame_key_variables, text='V W X Y Z', font=('Courier', 11),
                                             textvariable=self.variable_key_row_4)

            self.label_keyword.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
            self.entry_keyword.grid(row=0, column=1, sticky=W, **pad_5_kwargs)
            self.label_key_table.grid(row=1, column=0, sticky=E, pady=(5, 0))
            self.label_key_row_0.grid(row=1, column=1, sticky=W, padx=(15, 0))
            self.label_key_row_1.grid(row=2, column=1, sticky=W, padx=(15, 0))
            self.label_key_row_2.grid(row=3, column=1, sticky=W, padx=(15, 0))
            self.label_key_row_3.grid(row=4, column=1, sticky=W, padx=(15, 0))
            self.label_key_row_4.grid(row=5, column=1, sticky=W, padx=(15, 0), pady=(0, 5))

        elif type(key) == VigenereKey:
            self.label_keyword = ttk.Label(self.frame_key_variables, text='Keyword')
            self.entry_keyword = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_keyword)

            self.label_keyword.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
            self.entry_keyword.grid(row=0, column=1, sticky=W, **pad_5_kwargs)

        else:
            self.button_clear.state(['disabled'])
            self.button_random.state(['disabled'])

        self.frame_key_variables.pack()
        self.frame_key_buttons.pack()

        # Place Frames
        self.frame_header.pack(pady=(10, 0))
        self.frame_key.pack(pady=10)

    def grid_substitution_key_variables(self):
        self.label_alpha_key.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.entry_alpha_key.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=W)

    # Caesar Key Methods
    def update_scale_numeric_key(self, value):
        key.calculate(numeric_key=int(float(value)))
        self.set_key_variables(**key.get())

    def write_spinbox_numeric_key(self, *args):
        if self.variable_numeric_key.get() != '':
            key.calculate(numeric_key=int(self.variable_numeric_key.get()))
            self.set_key_variables(**key.get())

    def combobox_ab_key_selected(self, event):
        key.calculate(ab_key=self.variable_ab_key.get())
        self.set_key_variables(**key.get())

    def combobox_a_key_selected(self, event):
        key.calculate(a_key=self.variable_a_key.get())
        self.set_key_variables(**key.get())

    def spinbox_numeric_key_incremented(self):
        key.calculate(numeric_key=int(self.variable_numeric_key.get()))
        self.set_key_variables(**key.get())

    def random_key_button(self):
        key.random()
        if type(key) == CaesarKey:
            self.variable_alpha_key.set(key.alpha_key)
            self.variable_numeric_key.set(key.numeric_key)
            self.variable_ab_key.set(key.ab_key)
            self.variable_a_key.set(key.a_key)
            self.variable_numeric_scale.set(key.numeric_key % 26)

        elif type(key) == CaesarKeywordKey:
            self.variable_alpha_key.set(key.alpha_key)
            self.variable_keyword.set(key.keyword)

        elif type(key) == SubstitutionKey:
            self.variable_alpha_key.set(key.alpha_key)

        elif type(key) == PlayfairKey:
            self.variable_keyword.set(key.keyword)
            self.variable_key_row_0.set(' '.join(key.key_table[0]))
            self.variable_key_row_1.set(' '.join(key.key_table[1]))
            self.variable_key_row_2.set(' '.join(key.key_table[2]))
            self.variable_key_row_3.set(' '.join(key.key_table[3]))
            self.variable_key_row_4.set(' '.join(key.key_table[4]))

        elif type(key) == VigenereKey:
            self.variable_keyword.set(key.keyword)

    def clear_key_button(self):
        for variable in self.__dict__.values():
            if type(variable) == StringVar:
                variable.set('')

    def set_key_variables(self, **kwargs):
        for item, value in kwargs.items():
            if item == 'alpha_key':
                self.variable_alpha_key.set(value)
            if item == 'numeric_key':
                self.variable_numeric_key.set(value)
                self.variable_numeric_scale.set(value % 26)
            if item == 'ab_key':
                self.variable_ab_key.set(value)
            if item == 'a_key':
                self.variable_a_key.set(value)
            if item == 'keyword':
                self.variable_keyword.set(value)
            if item == 'key_table' and type(key) == PlayfairKey:
                self.variable_key_row_0.set(' '.join(value[0]))
                self.variable_key_row_1.set(' '.join(value[1]))
                self.variable_key_row_2.set(' '.join(value[2]))
                self.variable_key_row_3.set(' '.join(value[3]))
                self.variable_key_row_4.set(' '.join(value[4]))


def main_menu(master):
    master.option_add('*tearOff', False)
    menubar = Menu(master)
    master.config(menu=menubar)
    ciphers = Menu(menubar)

    menubar.add_cascade(menu=ciphers, label='Ciphers')

    ciphers.add_command(label='Simple Substitution',
                        command=lambda: set_cipher(master, SubstitutionCipher, SubstitutionKey))
    ciphers.add_command(label='Caesar',
                        command=lambda: set_cipher(master, CaesarCipher, CaesarKey))
    ciphers.add_command(label='Caesar Keyword',
                        command=lambda: set_cipher(master, CaesarKeywordCipher, CaesarKeywordKey))
    ciphers.add_command(label='Playfair',
                        command=lambda: set_cipher(master, PlayfairCipher, PlayfairKey))
    ciphers.add_command(label='Vigenere',
                        command=lambda: set_cipher(master, VigenereCipher, VigenereKey))


def set_cipher(master, cipher_type, key_type):
    global cipher
    global key

    cipher = cipher_type()
    key = key_type()
    cipher.key = key

    for frame in master.winfo_children():
        if type(frame) == Menu:
            pass
        else:
            frame.destroy()
    KeyGUI(master)
    CipherGUI(master)


class CipherGUI:

    def __init__(self, master):
        master.title('Cypher')
        master.resizable(False, False)

        # Define Cipher variables
        self.variable_plaintext = ''
        self.variable_ciphertext = ''

        # Create Cipher Frame
        self.frame_cipher = ttk.Frame(master)

        self.label_plaintext = ttk.Label(self.frame_cipher, text='Plaintext')
        self.text_plaintext = Text(self.frame_cipher, width=50, height=10, wrap='word')
        self.button_clear_plaintext = ttk.Button(self.frame_cipher, text='Clear',
                                                 command=lambda: self.text_plaintext.delete('1.0', END))
        self.button_random_plaintext = ttk.Button(self.frame_cipher, text='Random',
                                                  command=self.random_plaintext)
        self.button_encrypt = ttk.Button(self.frame_cipher, text='Encrypt', command=self.encrypt_button)

        self.label_ciphertext = ttk.Label(self.frame_cipher, text='Ciphertext')
        self.text_ciphertext = Text(self.frame_cipher, width=50, height=10, wrap='word')
        self.button_clear_ciphertext = ttk.Button(self.frame_cipher, text='Clear',
                                                  command=lambda: self.text_ciphertext.delete('1.0', END))
        # self.button_random_ciphertext = ttk.Button(self.frame_cipher, text='Random')
        self.button_decrypt = ttk.Button(self.frame_cipher, text='Decrypt', command=self.decrypt_button)

        self.label_plaintext.grid(column=0, row=0, **balanced_grid_kwargs)
        self.text_plaintext.grid(column=0, row=1, columnspan=3, **balanced_grid_kwargs)
        self.button_clear_plaintext.grid(column=0, row=2, **balanced_grid_kwargs)
        self.button_random_plaintext.grid(column=1, row=2, **balanced_grid_kwargs)
        self.button_encrypt.grid(column=2, row=2, **balanced_grid_kwargs)

        self.label_ciphertext.grid(column=0, row=3, **balanced_grid_kwargs)
        self.text_ciphertext.grid(column=0, row=4, columnspan=3, **balanced_grid_kwargs)
        self.button_clear_ciphertext.grid(column=0, row=5, **balanced_grid_kwargs)
        # self.button_random_ciphertext.grid(column=1, row=5, **balanced_grid_kwargs)
        self.button_decrypt.grid(column=2, row=5, **balanced_grid_kwargs)

        # Place frames
        self.frame_cipher.pack(padx=10, pady=(0, 10))

    def random_plaintext(self):
        t = get_random_fortune()
        self.text_plaintext.replace('1.0', 'end', t)

    def encrypt_button(self):
        cipher.plaintext = self.text_plaintext.get('1.0', 'end')
        cipher.encrypt()
        self.text_ciphertext.replace('1.0', 'end', cipher.ciphertext)

    def decrypt_button(self):
        cipher.ciphertext = self.text_ciphertext.get('1.0', 'end')
        cipher.decrypt()
        self.text_plaintext.replace('1.0', 'end', cipher.plaintext)


def main():
    global cipher
    global key
    root = Tk()
    main_menu(root)
    cipher = SubstitutionCipher()
    key = SubstitutionKey()
    cipher.key = key
    KeyGUI(root)
    CipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

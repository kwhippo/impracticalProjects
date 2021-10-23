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


def clear_field(field):
    if type(field) == ttk.Entry or \
            type(field) == ttk.Spinbox or \
            type(field) == ttk.Combobox:
        field.delete(0, END)
    elif type(field) == Text:
        field.delete('1.0', END)
    elif type(field) == ttk.Scale:
        field.set(0)


def clear_fields(master):
    for widget in master.winfo_children():
        clear_field(widget)


balanced_grid_kwargs = {'sticky': (N, S, E, W), 'pady': 5, 'padx': 5}
pad_5_kwargs = {'pady': 5, 'padx': 5}


def key_frame(master):
    frame_key = LabelFrame(master, text='Key')

    frame_key_buttons = Frame(frame_key)
    button_clear = ttk.Button(frame_key_buttons, text='Clear', command=lambda: clear_fields(frame_key_variables))
    button_random = ttk.Button(frame_key_buttons, text='Random')
    # button_validate = ttk.Button(frame_key_buttons, text='Validate')

    button_clear.grid(row=0, column=0, **balanced_grid_kwargs)
    button_random.grid(row=0, column=1, **balanced_grid_kwargs)
    # button_validate.grid(row=0, column=2, **balanced_grid_kwargs)

    frame_key_variables = Frame(frame_key)
    if type(key) == CaesarKey:
        substitution_key_variables(frame_key_variables)
        label_numeric_key = ttk.Label(frame_key_variables, text='Numeric Key')
        spinbox_numeric_key = ttk.Spinbox(frame_key_variables, from_=-25.0, to=25.0, width=5, format='%3.0f')
        label_ab_key = ttk.Label(frame_key_variables, text='AB Key')
        entry_ab_key = ttk.Entry(frame_key_variables, width=2)
        label_a_key = ttk.Label(frame_key_variables, text='A Key')
        combobox_a_key = ttk.Combobox(frame_key_variables, width=3)
        combobox_a_key['values'] = list(cipher.alphabet)
        scale_a_key = ttk.Scale(frame_key_variables, orient=HORIZONTAL, length=104, from_=0.0, to=26.0)

        label_numeric_key.grid(row=1, column=0, **pad_5_kwargs, sticky=E)
        spinbox_numeric_key.grid(row=1, column=1, **pad_5_kwargs, sticky=W)
        label_ab_key.grid(row=1, column=2, **pad_5_kwargs, sticky=E)
        entry_ab_key.grid(row=1, column=3, **pad_5_kwargs, sticky=W)
        label_a_key.grid(row=3, column=0, **pad_5_kwargs, sticky=E)
        combobox_a_key.grid(row=3, column=1, **pad_5_kwargs, sticky=W)
        scale_a_key.grid(row=3, column=2, columnspan=2, **pad_5_kwargs)

    elif type(key) == CaesarKeywordKey:
        substitution_key_variables(frame_key_variables)
        label_keyword = ttk.Label(frame_key_variables, text='Keyword')
        entry_keyword = ttk.Entry(frame_key_variables, width=26)
        label_keyword.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        entry_keyword.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=W)

    elif type(key) == SubstitutionKey:
        substitution_key_variables(frame_key_variables)

    elif type(key) == PlayfairKey:
        label_keyword = ttk.Label(frame_key_variables, text='Keyword')
        entry_keyword = ttk.Entry(frame_key_variables, width=26)
        label_key_table = ttk.Label(frame_key_variables, text='Key Table')
        label_key_row_0 = ttk.Label(frame_key_variables, text='A B C D E', font=('Courier', 11))
        label_key_row_1 = ttk.Label(frame_key_variables, text='F G H I K', font=('Courier', 11))
        label_key_row_2 = ttk.Label(frame_key_variables, text='L M N O P', font=('Courier', 11))
        label_key_row_3 = ttk.Label(frame_key_variables, text='Q R S T U', font=('Courier', 11))
        label_key_row_4 = ttk.Label(frame_key_variables, text='V W X Y Z', font=('Courier', 11))

        label_keyword.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_keyword.grid(row=0, column=1, sticky=W, **pad_5_kwargs)
        label_key_table.grid(row=1, column=0, sticky=E, pady=(5, 0))
        label_key_row_0.grid(row=1, column=1, sticky=W, padx=(15, 0))
        label_key_row_1.grid(row=2, column=1, sticky=W, padx=(15, 0))
        label_key_row_2.grid(row=3, column=1, sticky=W, padx=(15, 0))
        label_key_row_3.grid(row=4, column=1, sticky=W, padx=(15, 0))
        label_key_row_4.grid(row=5, column=1, sticky=W, padx=(15, 0), pady=(0, 5))

    elif type(key) == VigenereKey:
        label_keyword = ttk.Label(frame_key_variables, text='Keyword')
        entry_keyword = ttk.Entry(frame_key_variables, width=26)

        label_keyword.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_keyword.grid(row=0, column=1, sticky=W, **pad_5_kwargs)

    else:
        button_clear.state(['disabled'])
        button_random.state(['disabled'])
        # button_validate.state(['disabled'])

    frame_key_variables.pack()
    frame_key_buttons.pack()

    return frame_key


def substitution_key_variables(frame_key_variables):
    label_alpha_key = ttk.Label(frame_key_variables, text='Alpha Key')
    entry_alpha_key = ttk.Entry(frame_key_variables, width=26)
    label_alpha_key.grid(row=0, column=0, padx=5, pady=5, sticky=E)
    entry_alpha_key.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=W)


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

    for frame in master.winfo_children():
        if type(frame) == Menu:
            pass
        else:
            frame.destroy()

    CipherGUI(master)


class CipherGUI:

    def __init__(self, master):
        master.title('Cypher')
        master.resizable(False, False)
        self.style = ttk.Style()

        # Create Header Frame
        self.frame_header = ttk.Frame(master)
        self.style.configure('Header.TLabel', font=('TkDefaultFont', 14, 'bold'))
        ttk.Label(self.frame_header, text=f'{cipher.NAME} Cipher', style='Header.TLabel').pack()

        # Create Key Frame
        self.frame_key = key_frame(master)

        # Define Cipher variables
        self.variable_plaintext = ''
        self.variable_ciphertext = ''

        # Create Cipher Frame
        self.frame_cipher = ttk.Frame(master)

        self.label_plaintext = ttk.Label(self.frame_cipher, text='Plaintext')
        self.text_plaintext = Text(self.frame_cipher, width=50, height=10)
        self.button_clear_plaintext = ttk.Button(self.frame_cipher, text='Clear',
                                                 command=lambda: clear_field(self.text_plaintext))
        self.button_random_plaintext = ttk.Button(self.frame_cipher, text='Random',
                                                  command=self.random_plaintext)
        self.button_encrypt = ttk.Button(self.frame_cipher, text='Encrypt')

        self.label_ciphertext = ttk.Label(self.frame_cipher, text='Ciphertext')
        self.text_ciphertext = Text(self.frame_cipher, width=50, height=10)
        self.button_clear_ciphertext = ttk.Button(self.frame_cipher, text='Clear',
                                                  command=lambda: clear_field(self.text_ciphertext))
        # self.button_random_ciphertext = ttk.Button(self.frame_cipher, text='Random')
        self.button_decrypt = ttk.Button(self.frame_cipher, text='Decrypt')

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

        # Place Frames
        self.frame_header.pack(pady=(10, 0))
        self.frame_key.pack(pady=10)
        self.frame_cipher.pack(padx=10, pady=(0, 10))

    def random_plaintext(self):
        t = get_random_fortune()
        self.text_plaintext.replace('1.0', 'end', t)

    def encrypt_button(self):
        self.variable_plaintext = self.text_plaintext.get('1.0', 'end')
        cipher.encrypt()
        self.text_ciphertext.replace('1.0', 'end', cipher.ciphertext)

    def decrypt_button(self):
        self.variable_ciphertext = self.text_ciphertext.get('1.0', 'end')
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
    CipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

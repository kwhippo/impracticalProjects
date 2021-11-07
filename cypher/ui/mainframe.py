from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cypher.tools.utilities import get_random_fortune
from cypher.cipher import Cipher
from cypher.substitution import SubstitutionCipher
from cypher.caesar import CaesarCipher

balanced_grid_kwargs = {'sticky': (N, S, E, W), 'pady': 5, 'padx': 5}
pad_5_kwargs = {'pady': 5, 'padx': 5}


class Mainframe:
    def __init__(self, master, title=''):
        self.master = master
        self.title_frame = ttk.Frame(master)
        self.content_frame = ttk.Frame(master)

        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('TkDefaultFont', 14, 'bold'))
        ttk.Label(self.title_frame, text=f'{title}', style='Header.TLabel').pack()

        self.title_frame.pack(pady=(10, 0))
        self.content_frame.pack(pady=10)


class WelcomeFrame(Mainframe):
    def __init__(self, master, title='Welcome to Bandercrypt'):
        super(WelcomeFrame, self).__init__(master, title)

        with open('assets/welcome.txt') as txt_file:
            welcome_text = txt_file.read()
        label_welcome = ttk.Label(self.content_frame, text=welcome_text, wraplength=400, justify='center')

        bandersnatch_gif = Image.open('assets/bandersnatch.gif')
        bandersnatch_img = bandersnatch_gif.resize((400, 310))

        label_welcome.img = ImageTk.PhotoImage(bandersnatch_img)
        label_welcome.config(image=label_welcome.img)
        label_welcome.config(compound='top')
        label_welcome.pack()


class CipherFrame(Mainframe):
    def __init__(self, master, cipher=Cipher):
        super(CipherFrame, self).__init__(master, title=cipher.NAME)
        self.cipher = cipher()
        self.cipher.set_key()
        # Setup Frames
        self.frame_key = LabelFrame(master, text='Key')
        self.frame_text = ttk.Frame(master)

        # Configure Key Frame
        # Setup Key Button Frame
        self.frame_key_buttons = Frame(self.frame_key)
        self.button_clear_key = ttk.Button(self.frame_key_buttons, text='Clear',
                                           command=self.clear_key_button)
        self.button_random_key = ttk.Button(self.frame_key_buttons, text='Random',
                                            command=self.random_key_button)
        self.button_clear_key.grid(row=0, column=0, **balanced_grid_kwargs)
        self.button_random_key.grid(row=0, column=1, **balanced_grid_kwargs)
        # Setup Key Variables Frame
        self.frame_key_variables = Frame(self.frame_key)
        # Place Key Frames
        self.frame_key_variables.pack()
        self.frame_key_buttons.pack()

        # Configure Text Frame
        self.label_plaintext = ttk.Label(self.frame_text, text='Plaintext')
        self.text_plaintext = Text(self.frame_text, width=50, height=10, wrap='word')
        self.button_clear_plaintext = ttk.Button(self.frame_text, text='Clear',
                                                 command=lambda: self.text_plaintext.delete('1.0', END))
        self.button_random_plaintext = ttk.Button(self.frame_text, text='Random',
                                                  command=self.random_plaintext_button)
        self.button_encrypt = ttk.Button(self.frame_text, text='Encrypt', command=self.encrypt_button)

        self.label_ciphertext = ttk.Label(self.frame_text, text='Ciphertext')
        self.text_ciphertext = Text(self.frame_text, width=50, height=10, wrap='word')
        self.button_clear_ciphertext = ttk.Button(self.frame_text, text='Clear',
                                                  command=lambda: self.text_ciphertext.delete('1.0', END))
        self.button_decrypt = ttk.Button(self.frame_text, text='Decrypt', command=self.decrypt_button)

        self.label_plaintext.grid(column=0, row=0, **balanced_grid_kwargs)
        self.text_plaintext.grid(column=0, row=1, columnspan=3, **balanced_grid_kwargs)
        self.button_clear_plaintext.grid(column=0, row=2, **balanced_grid_kwargs)
        self.button_random_plaintext.grid(column=1, row=2, **balanced_grid_kwargs)
        self.button_encrypt.grid(column=2, row=2, **balanced_grid_kwargs)

        self.label_ciphertext.grid(column=0, row=3, **balanced_grid_kwargs)
        self.text_ciphertext.grid(column=0, row=4, columnspan=3, **balanced_grid_kwargs)
        self.button_clear_ciphertext.grid(column=0, row=5, **balanced_grid_kwargs)
        self.button_decrypt.grid(column=2, row=5, **balanced_grid_kwargs)

        self.frame_key.pack(expand=True, fill='both', **pad_5_kwargs)
        self.frame_text.pack()

    def random_plaintext_button(self):
        t = get_random_fortune()
        self.text_plaintext.replace('1.0', 'end', t)

    def encrypt_button(self):
        self.cipher.plaintext = self.text_plaintext.get('1.0', 'end')
        try:
            self.cipher.encrypt()
        except Exception as e:
            messagebox.showerror('Encryption Error', e)
        self.text_ciphertext.replace('1.0', 'end', self.cipher.ciphertext)

    def decrypt_button(self):
        self.cipher.ciphertext = self.text_ciphertext.get('1.0', 'end')
        try:
            self.cipher.decrypt()
        except Exception as e:
            messagebox.showerror('Decryption Error', e)
        self.text_plaintext.replace('1.0', 'end', self.cipher.plaintext)

    def random_key_button(self):
        self.cipher.key.random()

    def clear_key_button(self):
        self.cipher.clear_key()


class SimpleSubstitutionFrame(CipherFrame):
    def __init__(self, master):
        super().__init__(master, SubstitutionCipher)
        # Configure Key Frame
        # Setup Key Variables
        self.variable_alpha_key = StringVar()

        # Setup Key Variable Widgets
        label_alpha_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_alpha_key)

        # Place Key Variable Widgets
        label_alpha_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_alpha_key.grid(row=0, column=1, sticky=W, **pad_5_kwargs)

    def random_key_button(self):
        super(SimpleSubstitutionFrame, self).random_key_button()
        self.variable_alpha_key.set(self.cipher.key.alpha_key)

    def clear_key_button(self):
        super(SimpleSubstitutionFrame, self).clear_key_button()
        self.variable_alpha_key.set(self.cipher.key.alpha_key)


class CaesarFrame(CipherFrame):
    def __init__(self, master):
        super(CaesarFrame, self).__init__(master, CaesarCipher)
        # Configure Key Frame
        # Setup Key Variables
        self.variable_alpha_key = StringVar()
        self.variable_numeric_key = StringVar()
        self.variable_ab_key = StringVar()
        self.variable_a_key = StringVar()
        self.variable_numeric_scale = StringVar()

        # Setup Key Variable Widgets
        label_alpha_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32, textvariable=self.variable_alpha_key)
        entry_alpha_key.state(['readonly'])
        label_numeric_key = ttk.Label(self.frame_key_variables, text='Numeric Key')
        spinbox_numeric_key = ttk.Spinbox(self.frame_key_variables, from_=-100.0, to=100.0, width=5,
                                          format='%3.0f',
                                          textvariable=self.variable_numeric_key,
                                          command=self.spinbox_numeric_key_incremented)
        self.variable_numeric_key.trace_add('write', self.write_variable_numeric_key)
        label_ab_key = ttk.Label(self.frame_key_variables, text='AB Key')
        combobox_ab_key = ttk.Combobox(self.frame_key_variables, width=4, textvariable=self.variable_ab_key)
        values_ab_key = []
        for a in self.cipher.alphabet:
            for b in self.cipher.alphabet:
                values_ab_key.append(f'{a}{b}')
        combobox_ab_key['values'] = values_ab_key
        combobox_ab_key.state(['readonly'])
        combobox_ab_key.bind('<<ComboboxSelected>>', lambda e: self.combobox_ab_key_selected())
        label_a_key = ttk.Label(self.frame_key_variables, text='A Key')
        combobox_a_key = ttk.Combobox(self.frame_key_variables, width=3, textvariable=self.variable_a_key)
        combobox_a_key['values'] = list(self.cipher.alphabet)
        combobox_a_key.state(['readonly'])
        combobox_a_key.bind('<<ComboboxSelected>>', lambda e: self.combobox_a_key_selected())
        scale_numeric_key = ttk.Scale(self.frame_key_variables, orient=HORIZONTAL, length=100,
                                      from_=0.0, to=25.0, variable=self.variable_numeric_scale,
                                      command=self.update_scale_numeric_key)

        # Place Key Variable Widgets
        label_alpha_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_alpha_key.grid(row=0, column=1, columnspan=3, sticky=W, **pad_5_kwargs)
        label_numeric_key.grid(row=1, column=0, **pad_5_kwargs, sticky=E)
        spinbox_numeric_key.grid(row=1, column=1, **pad_5_kwargs, sticky=W, )
        label_ab_key.grid(row=1, column=2, **pad_5_kwargs, sticky=E)
        combobox_ab_key.grid(row=1, column=3, **pad_5_kwargs, sticky=W)
        label_a_key.grid(row=3, column=0, **pad_5_kwargs, sticky=E)
        combobox_a_key.grid(row=3, column=1, **pad_5_kwargs, sticky=W)
        scale_numeric_key.grid(row=3, column=2, columnspan=2, **pad_5_kwargs)

    def set_key_variables(self):
        self.variable_alpha_key.set(self.cipher.key.alpha_key)
        self.variable_numeric_key.set(self.cipher.key.numeric_key)
        self.variable_numeric_scale.set(self.cipher.key.numeric_key % 26)
        self.variable_ab_key.set(self.cipher.key.ab_key)
        self.variable_a_key.set(self.cipher.key.a_key)

    def random_key_button(self):
        super(CaesarFrame, self).random_key_button()
        self.set_key_variables()

    def clear_key_button(self):
        super(CaesarFrame, self).clear_key_button()
        self.set_key_variables()

    def update_scale_numeric_key(self, value):
        self.cipher.key.calculate(numeric_key=int(float(value)))
        self.set_key_variables()

    def write_variable_numeric_key(self, *args):
        if self.variable_numeric_key.get() != '':
            self.cipher.key.calculate(numeric_key=int(self.variable_numeric_key.get()))
            self.set_key_variables()

    def combobox_ab_key_selected(self):
        self.cipher.key.calculate(ab_key=self.variable_ab_key.get())
        self.set_key_variables()

    def combobox_a_key_selected(self):
        self.cipher.key.calculate(a_key=self.variable_a_key.get())
        self.set_key_variables()

    def spinbox_numeric_key_incremented(self):
        self.cipher.key.calculate(numeric_key=int(self.variable_numeric_key.get()))
        self.set_key_variables()

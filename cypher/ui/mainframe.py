from tkinter import *
from tkinter.font import Font

import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from pprint import pprint
from cypher.tools.utilities import get_random_fortune, break_string
from cypher.tools.frequency import calculate_plaintext_frequency
from cypher.cipher import Cipher
from cypher.substitution import SubstitutionCipher
from cypher.caesar import CaesarCipher
from cypher.caesar_keyword import CaesarKeywordCipher
from cypher.vigenere import VigenereCipher
from cypher.playfair import PlayfairCipher
from cypher.homophonic import HomophonicCipher

balanced_grid_kwargs = {'sticky': (N, S, E, W), 'pady': 10, 'padx': 10}
pad_5_kwargs = {'pady': 5, 'padx': 5}


class Mainframe:
    def __init__(self, master, title=''):
        self.master = master
        self.title_frame = ttk.Frame(master)
        self.content_frame = ttk.Frame(master)

        self.style = ttk.Style('cyborg')
        self.style.configure('Header.TLabel', font=('TkDefaultFont', 14, 'bold'))
        self.label_title = ttk.Label(self.title_frame, text=f'{title}', style='Header.TLabel')
        self.label_title.pack()

        self.title_frame.pack(pady=(10, 0))
        self.content_frame.pack(padx=10, pady=10)


class WelcomeFrame(Mainframe):
    def __init__(self, master, title='Welcome to Bandercrypt'):
        super(WelcomeFrame, self).__init__(master, title)

        with open('assets/welcome.txt') as txt_file:
            welcome_text = txt_file.read()
        label_welcome = ttk.Label(self.content_frame, text=welcome_text, wraplength=400,
                                  justify='center')

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
        self.frame_key = ttk.LabelFrame(master, text='Key')
        self.frame_text = ttk.Frame(master)

        # Configure Key Frame
        # Setup Key Button Frame
        self.frame_key_buttons = ttk.Frame(self.frame_key)
        self.button_clear_key = ttk.Button(self.frame_key_buttons, text='Clear',
                                           command=self.clear_key_button, bootstyle='warning')
        self.button_random_key = ttk.Button(self.frame_key_buttons, text='Random',
                                            command=self.random_key_button, bootstyle='info')
        self.button_clear_key.grid(row=0, column=0, **balanced_grid_kwargs)
        self.button_random_key.grid(row=0, column=1, **balanced_grid_kwargs)
        # Setup Key Variables Frame
        self.frame_key_variables = ttk.Frame(self.frame_key)
        # Place Key Frames
        self.frame_key_variables.pack()
        self.frame_key_buttons.pack()

        # Configure Text Frame
        self.label_plaintext = ttk.Label(self.frame_text, text='Plaintext')
        self.text_plaintext = Text(self.frame_text, width=50, height=10, wrap='word')
        self.button_clear_plaintext = ttk.Button(self.frame_text, text='Clear', bootstyle='warning',
                                                 command=lambda: self.text_plaintext.delete('1.0',
                                                                                            END))
        self.button_random_plaintext = ttk.Button(self.frame_text, text='Random', bootstyle='info',
                                                  command=self.random_plaintext_button)
        self.button_encrypt = ttk.Button(self.frame_text, text='Encrypt', bootstyle='success',
                                         command=self.encrypt_button)

        self.label_ciphertext = ttk.Label(self.frame_text, text='Ciphertext')
        self.text_ciphertext = Text(self.frame_text, width=50, height=10, wrap='word')
        self.button_clear_ciphertext = ttk.Button(self.frame_text, text='Clear', bootstyle='warning',
                                                  command=lambda: self.text_ciphertext.delete('1.0',
                                                                                              END))
        self.button_decrypt = ttk.Button(self.frame_text, text='Decrypt', bootstyle='success',
                                         command=self.decrypt_button)

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
        print('Starting encryption...')
        self.cipher.plaintext = self.text_plaintext.get('1.0', 'end')
        print(f'Plaintext: {self.cipher.plaintext}')
        try:
            print('Encrypting...')
            self.cipher.encrypt()
        except Exception as e:
            messagebox.showerror('Encryption Error', e)
        print(f'Ciphertext: {self.cipher.ciphertext}')
        self.text_ciphertext.replace('1.0', 'end', self.cipher.ciphertext)

    def decrypt_button(self):
        print('Decrypting...')
        self.cipher.ciphertext = self.text_ciphertext.get('1.0', 'end')
        try:
            self.cipher.decrypt()
        except Exception as e:
            messagebox.showerror('Decryption Error', e)
        self.text_plaintext.replace('1.0', 'end', self.cipher.plaintext)

    def random_key_button(self):
        self.cipher.key.random()
        self.set_key_variables()

    def clear_key_button(self):
        self.cipher.clear_key()
        self.set_key_variables()

    def set_key_variables(self):
        pass


class SimpleSubstitutionFrame(CipherFrame):
    def __init__(self, master):
        super().__init__(master, SubstitutionCipher)
        # Configure Key Frame
        # Setup Key Variables
        self.variable_alpha_key = StringVar()

        # Setup Key Variable Widgets
        label_alpha_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32,
                                    textvariable=self.variable_alpha_key)

        # Place Key Variable Widgets
        label_alpha_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_alpha_key.grid(row=0, column=1, sticky=W, **pad_5_kwargs)

    def set_key_variables(self):
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
        self.entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32,
                                         textvariable=self.variable_alpha_key)
        self.entry_alpha_key.state(['readonly'])
        label_numeric_key = ttk.Label(self.frame_key_variables, text='Numeric Key')
        self.spinbox_numeric_key = ttk.Spinbox(self.frame_key_variables, from_=-100.0, to=100.0,
                                               width=5,
                                               format='%3.0f',
                                               textvariable=self.variable_numeric_key,
                                               command=self.spinbox_numeric_key_incremented)
        self.variable_numeric_key.trace_add('write', self.write_variable_numeric_key)
        label_ab_key = ttk.Label(self.frame_key_variables, text='AB Key')
        self.combobox_ab_key = ttk.Combobox(self.frame_key_variables, width=4,
                                            textvariable=self.variable_ab_key)
        values_ab_key = []
        for a in self.cipher.key.alphabet:
            for b in self.cipher.key.alphabet:
                values_ab_key.append(f'{a}{b}')
        self.combobox_ab_key['values'] = values_ab_key
        self.combobox_ab_key.state(['readonly'])
        self.combobox_ab_key.bind('<<ComboboxSelected>>', lambda e: self.combobox_ab_key_selected())
        label_a_key = ttk.Label(self.frame_key_variables, text='A Key')
        self.combobox_a_key = ttk.Combobox(self.frame_key_variables, width=3,
                                           textvariable=self.variable_a_key)
        self.combobox_a_key['values'] = list(self.cipher.key.alphabet)
        self.combobox_a_key.state(['readonly'])
        self.combobox_a_key.bind('<<ComboboxSelected>>', lambda e: self.combobox_a_key_selected())
        self.scale_numeric_key = ttk.Scale(self.frame_key_variables, orient=HORIZONTAL, length=100,
                                           from_=0.0, to=25.0, variable=self.variable_numeric_scale,
                                           command=self.update_scale_numeric_key)

        # Place Key Variable Widgets
        label_alpha_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        self.entry_alpha_key.grid(row=0, column=1, columnspan=3, sticky=W, **pad_5_kwargs)
        label_numeric_key.grid(row=1, column=0, **pad_5_kwargs, sticky=E)
        self.spinbox_numeric_key.grid(row=1, column=1, **pad_5_kwargs, sticky=W, )
        label_ab_key.grid(row=1, column=2, **pad_5_kwargs, sticky=E)
        self.combobox_ab_key.grid(row=1, column=3, **pad_5_kwargs, sticky=W)
        label_a_key.grid(row=3, column=0, **pad_5_kwargs, sticky=E)
        self.combobox_a_key.grid(row=3, column=1, **pad_5_kwargs, sticky=W)
        self.scale_numeric_key.grid(row=3, column=2, columnspan=2, **pad_5_kwargs)

    def set_key_variables(self):
        self.variable_alpha_key.set(self.cipher.key.alpha_key)
        self.variable_numeric_key.set(self.cipher.key.numeric_key)
        self.variable_numeric_scale.set(self.cipher.key.numeric_key % 26)
        self.variable_ab_key.set(self.cipher.key.ab_key)
        self.variable_a_key.set(self.cipher.key.a_key)

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


class ROT13Frame(CaesarFrame):
    def __init__(self, master):
        super(ROT13Frame, self).__init__(master)
        self.label_title.config(text='ROT13 Cipher')

        self.spinbox_numeric_key.state(['disabled'])
        self.combobox_ab_key.state(['disabled'])
        self.combobox_a_key.state(['disabled'])
        self.scale_numeric_key.state(['disabled'])
        self.button_clear_key.state(['disabled'])
        self.button_random_key.state(['disabled'])

        self.cipher.key.calculate(numeric_key=13)
        self.set_key_variables()


class ReverseCaesarFrame(CaesarFrame):
    def __init__(self, master):
        super(ReverseCaesarFrame, self).__init__(master)
        self.label_title.config(text='Reverse Caesar Cipher')
        self.cipher.key.reverse = True


class AtbashFrame(CaesarFrame):
    def __init__(self, master):
        super(AtbashFrame, self).__init__(master)
        self.label_title.config(text='Atbash Cipher')
        self.cipher.key.reverse = True

        self.spinbox_numeric_key.state(['disabled'])
        self.combobox_ab_key.state(['disabled'])
        self.combobox_a_key.state(['disabled'])
        self.scale_numeric_key.state(['disabled'])
        self.button_clear_key.state(['disabled'])
        self.button_random_key.state(['disabled'])

        self.cipher.key.calculate(numeric_key=0)
        self.set_key_variables()


class CaesarKeywordFrame(CipherFrame):
    def __init__(self, master):
        super(CaesarKeywordFrame, self).__init__(master, CaesarKeywordCipher)
        # Configure Key Frame
        # Setup Key Variables
        self.variable_alpha_key = StringVar()
        self.variable_keyword = StringVar()

        self.variable_keyword.trace_add('write', self.write_variable_keyword)

        # Setup Key Variable Widgets
        label_alpha_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        entry_alpha_key = ttk.Entry(self.frame_key_variables, width=32,
                                    textvariable=self.variable_alpha_key,
                                    state=['readonly'])
        label_keyword = ttk.Label(self.frame_key_variables, text='Keyword')
        entry_keyword = ttk.Entry(self.frame_key_variables, width=32,
                                  textvariable=self.variable_keyword)

        # Place Key Variable Widgets
        label_alpha_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_alpha_key.grid(row=0, column=1, sticky=W, **pad_5_kwargs)
        label_keyword.grid(row=1, column=0, sticky=E, **pad_5_kwargs)
        entry_keyword.grid(row=1, column=1, sticky=W, **pad_5_kwargs)

    def set_key_variables(self):
        self.variable_alpha_key.set(self.cipher.key.alpha_key)
        self.variable_keyword.set(self.cipher.key.keyword)

    def write_variable_keyword(self, *args):
        if self.variable_keyword.get() != '':
            self.cipher.key.calculate(keyword=self.variable_keyword.get())
            self.set_key_variables()


class KeywordFrame(CipherFrame):
    def __init__(self, master, cipher=Cipher):
        super().__init__(master, cipher)
        # Configure Key Frame
        # Setup Key Variables
        self.variable_keyword = StringVar()

        # Setup Key Variable Widgets
        label_keyword = ttk.Label(self.frame_key_variables, text='Keyword')
        entry_keyword = ttk.Entry(self.frame_key_variables, width=32,
                                  textvariable=self.variable_keyword)

        # Place Key Variable Widgets
        label_keyword.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_keyword.grid(row=0, column=1, sticky=W, **pad_5_kwargs)

    def set_key_variables(self):
        self.variable_keyword.set(self.cipher.key.keyword)


class VigenereFrame(KeywordFrame):
    def __init__(self, master):
        super(VigenereFrame, self).__init__(master, VigenereCipher)


class PlayfairFrame(KeywordFrame):
    def __init__(self, master):
        super(PlayfairFrame, self).__init__(master, PlayfairCipher)

        # Setup Key Variables
        self.variable_key_row_0 = StringVar()
        self.variable_key_row_1 = StringVar()
        self.variable_key_row_2 = StringVar()
        self.variable_key_row_3 = StringVar()
        self.variable_key_row_4 = StringVar()

        # Setup Key Variable Widgets
        label_key_table = ttk.Label(self.frame_key_variables, text='Key Table')
        label_key_row_0 = ttk.Label(self.frame_key_variables, text='A B C D E',
                                    font=('Courier', 11),
                                    textvariable=self.variable_key_row_0)
        label_key_row_1 = ttk.Label(self.frame_key_variables, text='F G H I K',
                                    font=('Courier', 11),
                                    textvariable=self.variable_key_row_1)
        label_key_row_2 = ttk.Label(self.frame_key_variables, text='L M N O P',
                                    font=('Courier', 11),
                                    textvariable=self.variable_key_row_2)
        label_key_row_3 = ttk.Label(self.frame_key_variables, text='Q R S T U',
                                    font=('Courier', 11),
                                    textvariable=self.variable_key_row_3)
        label_key_row_4 = ttk.Label(self.frame_key_variables, text='V W X Y Z',
                                    font=('Courier', 11),
                                    textvariable=self.variable_key_row_4)

        # Place Key Variable Widgets
        label_key_table.grid(row=1, column=0, sticky=E, pady=(5, 0))
        label_key_row_0.grid(row=1, column=1, sticky=W, padx=(15, 0))
        label_key_row_1.grid(row=2, column=1, sticky=W, padx=(15, 0))
        label_key_row_2.grid(row=3, column=1, sticky=W, padx=(15, 0))
        label_key_row_3.grid(row=4, column=1, sticky=W, padx=(15, 0))
        label_key_row_4.grid(row=5, column=1, sticky=W, padx=(15, 0), pady=(0, 5))

    def set_key_variables(self):
        super(PlayfairFrame, self).set_key_variables()
        self.variable_key_row_0.set(' '.join(self.cipher.key.key_table[0]))
        self.variable_key_row_1.set(' '.join(self.cipher.key.key_table[1]))
        self.variable_key_row_2.set(' '.join(self.cipher.key.key_table[2]))
        self.variable_key_row_3.set(' '.join(self.cipher.key.key_table[3]))
        self.variable_key_row_4.set(' '.join(self.cipher.key.key_table[4]))


class HomophonicFrame(CipherFrame):
    def __init__(self, master, cipher=HomophonicCipher):
        super().__init__(master, cipher)
        # Configure Key Frame
        self.window_configure_key = None
        # Setup Key Variables
        self.variable_optimize = StringVar()
        self.variable_a_key = StringVar()
        self.variable_b_key = StringVar()
        self.variable_c_key = StringVar()
        self.variable_d_key = StringVar()
        self.variable_e_key = StringVar()
        self.variable_f_key = StringVar()
        self.variable_g_key = StringVar()
        self.variable_h_key = StringVar()
        self.variable_i_key = StringVar()
        self.variable_j_key = StringVar()
        self.variable_k_key = StringVar()
        self.variable_l_key = StringVar()
        self.variable_m_key = StringVar()
        self.variable_n_key = StringVar()
        self.variable_o_key = StringVar()
        self.variable_p_key = StringVar()
        self.variable_q_key = StringVar()
        self.variable_r_key = StringVar()
        self.variable_s_key = StringVar()
        self.variable_t_key = StringVar()
        self.variable_u_key = StringVar()
        self.variable_v_key = StringVar()
        self.variable_w_key = StringVar()
        self.variable_x_key = StringVar()
        self.variable_y_key = StringVar()
        self.variable_z_key = StringVar()

        self.variable_optimize.set(self.cipher.key.optimize)

        # Setup Key Variable Widgets
        label_key = ttk.Label(self.frame_key_variables, text='Alpha Key')
        fixed_width_font = Font(family='Courier New', size=11)
        self.text_key = Text(self.frame_key_variables, width=32, height=5, state='disabled', font=fixed_width_font)
        self.setup_optimize_widgets(self.frame_key_variables)
        label_key.grid(row=0, column=0, sticky=(N, E), **pad_5_kwargs)
        self.text_key.grid(row=0, column=1, sticky=W, columnspan=3, **pad_5_kwargs)

        # Override Key Button Frame from Cipher Frame
        self.button_configure_key = ttk.Button(self.frame_key_buttons, text='Configure',
                                               command=self.configure_key_button)
        self.button_clear_key.grid_forget()
        self.button_random_key.grid_forget()

        self.button_configure_key.grid(row=0, column=0, **balanced_grid_kwargs)
        self.button_clear_key.grid(row=0, column=1, **balanced_grid_kwargs)
        self.button_random_key.grid(row=0, column=3, **balanced_grid_kwargs)

    def setup_optimize_widgets(self, master_frame):
        label_optimize = ttk.Label(master_frame, text='Optimize')
        radio_common = ttk.Radiobutton(master_frame, text='Common', value='common',
                                       variable=self.variable_optimize,
                                       command=self.radio_optimize_selected)
        radio_plaintext = ttk.Radiobutton(master_frame, text='Plaintext',
                                          value='plaintext', variable=self.variable_optimize,
                                          command=self.radio_optimize_selected)
        radio_random = ttk.Radiobutton(master_frame, text='Random', value='random',
                                       variable=self.variable_optimize,
                                       command=self.radio_optimize_selected)

        label_optimize.grid(row=1, column=0, sticky=E, **pad_5_kwargs)
        radio_common.grid(row=1, column=1, **pad_5_kwargs)
        radio_plaintext.grid(row=1, column=2, **pad_5_kwargs)
        radio_random.grid(row=1, column=3, **pad_5_kwargs)

    def configure_key_button(self):
        self.window_configure_key = Toplevel(self.master)
        self.window_configure_key.title('Configure Key')
        frame_configure_key = ttk.Frame(self.window_configure_key)
        frame_configure_key.pack()

        # Setup Key Variable Frame
        frame_key_variables = ttk.Frame(frame_configure_key)
        # A-Z Keys
        label_a_key = ttk.Label(frame_key_variables, text='A')
        entry_a_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_a_key)
        label_b_key = ttk.Label(frame_key_variables, text='B')
        entry_b_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_b_key)
        label_c_key = ttk.Label(frame_key_variables, text='C')
        entry_c_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_c_key)
        label_d_key = ttk.Label(frame_key_variables, text='D')
        entry_d_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_d_key)
        label_e_key = ttk.Label(frame_key_variables, text='E')
        entry_e_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_e_key)
        label_f_key = ttk.Label(frame_key_variables, text='F')
        entry_f_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_f_key)
        label_g_key = ttk.Label(frame_key_variables, text='G')
        entry_g_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_g_key)
        label_h_key = ttk.Label(frame_key_variables, text='H')
        entry_h_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_h_key)
        label_i_key = ttk.Label(frame_key_variables, text='I')
        entry_i_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_i_key)
        label_j_key = ttk.Label(frame_key_variables, text='J')
        entry_j_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_j_key)
        label_k_key = ttk.Label(frame_key_variables, text='K')
        entry_k_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_k_key)
        label_l_key = ttk.Label(frame_key_variables, text='L')
        entry_l_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_l_key)
        label_m_key = ttk.Label(frame_key_variables, text='M')
        entry_m_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_m_key)
        label_n_key = ttk.Label(frame_key_variables, text='N')
        entry_n_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_n_key)
        label_o_key = ttk.Label(frame_key_variables, text='O')
        entry_o_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_o_key)
        label_p_key = ttk.Label(frame_key_variables, text='P')
        entry_p_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_p_key)
        label_q_key = ttk.Label(frame_key_variables, text='Q')
        entry_q_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_q_key)
        label_r_key = ttk.Label(frame_key_variables, text='R')
        entry_r_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_r_key)
        label_s_key = ttk.Label(frame_key_variables, text='S')
        entry_s_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_s_key)
        label_t_key = ttk.Label(frame_key_variables, text='T')
        entry_t_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_t_key)
        label_u_key = ttk.Label(frame_key_variables, text='U')
        entry_u_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_u_key)
        label_v_key = ttk.Label(frame_key_variables, text='V')
        entry_v_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_v_key)
        label_w_key = ttk.Label(frame_key_variables, text='W')
        entry_w_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_w_key)
        label_x_key = ttk.Label(frame_key_variables, text='X')
        entry_x_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_x_key)
        label_y_key = ttk.Label(frame_key_variables, text='Y')
        entry_y_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_y_key)
        label_z_key = ttk.Label(frame_key_variables, text='Z')
        entry_z_key = ttk.Entry(frame_key_variables, width=10,
                                textvariable=self.variable_z_key)

        label_a_key.grid(row=0, column=0, sticky=E, **pad_5_kwargs)
        entry_a_key.grid(row=0, column=1, sticky=W, **pad_5_kwargs)
        label_b_key.grid(row=1, column=0, sticky=E, **pad_5_kwargs)
        entry_b_key.grid(row=1, column=1, sticky=W, **pad_5_kwargs)
        label_c_key.grid(row=2, column=0, sticky=E, **pad_5_kwargs)
        entry_c_key.grid(row=2, column=1, sticky=W, **pad_5_kwargs)
        label_d_key.grid(row=3, column=0, sticky=E, **pad_5_kwargs)
        entry_d_key.grid(row=3, column=1, sticky=W, **pad_5_kwargs)
        label_e_key.grid(row=4, column=0, sticky=E, **pad_5_kwargs)
        entry_e_key.grid(row=4, column=1, sticky=W, **pad_5_kwargs)
        label_f_key.grid(row=5, column=0, sticky=E, **pad_5_kwargs)
        entry_f_key.grid(row=5, column=1, sticky=W, **pad_5_kwargs)
        label_g_key.grid(row=6, column=0, sticky=E, **pad_5_kwargs)
        entry_g_key.grid(row=6, column=1, sticky=W, **pad_5_kwargs)
        label_h_key.grid(row=7, column=0, sticky=E, **pad_5_kwargs)
        entry_h_key.grid(row=7, column=1, sticky=W, **pad_5_kwargs)
        label_i_key.grid(row=8, column=0, sticky=E, **pad_5_kwargs)
        entry_i_key.grid(row=8, column=1, sticky=W, **pad_5_kwargs)
        label_j_key.grid(row=9, column=0, sticky=E, **pad_5_kwargs)
        entry_j_key.grid(row=9, column=1, sticky=W, **pad_5_kwargs)
        label_k_key.grid(row=10, column=0, sticky=E, **pad_5_kwargs)
        entry_k_key.grid(row=10, column=1, sticky=W, **pad_5_kwargs)
        label_l_key.grid(row=11, column=0, sticky=E, **pad_5_kwargs)
        entry_l_key.grid(row=11, column=1, sticky=W, **pad_5_kwargs)
        label_m_key.grid(row=12, column=0, sticky=E, **pad_5_kwargs)
        entry_m_key.grid(row=12, column=1, sticky=W, **pad_5_kwargs)
        label_n_key.grid(row=0, column=2, sticky=E, **pad_5_kwargs)
        entry_n_key.grid(row=0, column=3, sticky=W, **pad_5_kwargs)
        label_o_key.grid(row=1, column=2, sticky=E, **pad_5_kwargs)
        entry_o_key.grid(row=1, column=3, sticky=W, **pad_5_kwargs)
        label_p_key.grid(row=2, column=2, sticky=E, **pad_5_kwargs)
        entry_p_key.grid(row=2, column=3, sticky=W, **pad_5_kwargs)
        label_q_key.grid(row=3, column=2, sticky=E, **pad_5_kwargs)
        entry_q_key.grid(row=3, column=3, sticky=W, **pad_5_kwargs)
        label_r_key.grid(row=4, column=2, sticky=E, **pad_5_kwargs)
        entry_r_key.grid(row=4, column=3, sticky=W, **pad_5_kwargs)
        label_s_key.grid(row=5, column=2, sticky=E, **pad_5_kwargs)
        entry_s_key.grid(row=5, column=3, sticky=W, **pad_5_kwargs)
        label_t_key.grid(row=6, column=2, sticky=E, **pad_5_kwargs)
        entry_t_key.grid(row=6, column=3, sticky=W, **pad_5_kwargs)
        label_u_key.grid(row=7, column=2, sticky=E, **pad_5_kwargs)
        entry_u_key.grid(row=7, column=3, sticky=W, **pad_5_kwargs)
        label_v_key.grid(row=8, column=2, sticky=E, **pad_5_kwargs)
        entry_v_key.grid(row=8, column=3, sticky=W, **pad_5_kwargs)
        label_w_key.grid(row=9, column=2, sticky=E, **pad_5_kwargs)
        entry_w_key.grid(row=9, column=3, sticky=W, **pad_5_kwargs)
        label_x_key.grid(row=10, column=2, sticky=E, **pad_5_kwargs)
        entry_x_key.grid(row=10, column=3, sticky=W, **pad_5_kwargs)
        label_y_key.grid(row=11, column=2, sticky=E, **pad_5_kwargs)
        entry_y_key.grid(row=11, column=3, sticky=W, **pad_5_kwargs)
        label_z_key.grid(row=12, column=2, sticky=E, **pad_5_kwargs)
        entry_z_key.grid(row=12, column=3, sticky=W, **pad_5_kwargs)

        # Setup Optimize Frame
        frame_optimize_key = ttk.Frame(frame_configure_key)
        self.setup_optimize_widgets(frame_optimize_key)

        # Setup Key Button Frame
        frame_key_buttons = ttk.Frame(frame_configure_key)
        button_clear_key = ttk.Button(frame_key_buttons, text='Clear',
                                      command=self.clear_key_button)
        button_random_key = ttk.Button(frame_key_buttons, text='Random',
                                       command=self.random_key_button)
        button_save_key = ttk.Button(frame_key_buttons, text='Save',
                                     command=self.save_key_button)

        button_clear_key.grid(row=0, column=0, **balanced_grid_kwargs)
        button_random_key.grid(row=0, column=1, **balanced_grid_kwargs)
        button_save_key.grid(row=0, column=2, **balanced_grid_kwargs)

        # Place Frames
        frame_key_variables.pack()
        frame_optimize_key.pack()
        frame_key_buttons.pack()

    def random_key_button(self):
        self.cipher.key.calculate_frequency(self.text_plaintext.get('1.0', END))
        super().random_key_button()
        self.cipher.key.print()

    def save_key_button(self):
        self.write_variable_letter_key()
        self.set_key_variables()
        self.window_configure_key.destroy()

    def set_key_variables(self):
        pprint(self.cipher.key.alpha_dict_key)
        for index, value in self.cipher.key.alpha_dict_key.items():
            self.__getattribute__(f'variable_{index.lower()}_key').set(''.join(value))
        self.cipher.key.calculate()
        self.text_key.config(state='normal')
        self.text_key.replace('1.0', 'end', self.cipher.key.alpha_text_key)
        self.text_key.config(state='disabled')

    def radio_optimize_selected(self):
        self.cipher.key.optimize = self.variable_optimize.get()
        self.cipher.key.calculate_frequency(self.text_plaintext.get('1.0', END))

    def write_variable_letter_key(self):
        self.cipher.key.alpha_dict_key['A'] = break_string(self.variable_a_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['B'] = break_string(self.variable_b_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['C'] = break_string(self.variable_c_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['D'] = break_string(self.variable_d_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['E'] = break_string(self.variable_e_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['F'] = break_string(self.variable_f_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['G'] = break_string(self.variable_g_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['H'] = break_string(self.variable_h_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['I'] = break_string(self.variable_i_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['J'] = break_string(self.variable_j_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['K'] = break_string(self.variable_k_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['L'] = break_string(self.variable_l_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['M'] = break_string(self.variable_m_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['N'] = break_string(self.variable_n_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['O'] = break_string(self.variable_o_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['P'] = break_string(self.variable_p_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['Q'] = break_string(self.variable_q_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['R'] = break_string(self.variable_r_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['S'] = break_string(self.variable_s_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['T'] = break_string(self.variable_t_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['U'] = break_string(self.variable_u_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['V'] = break_string(self.variable_v_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['W'] = break_string(self.variable_w_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['X'] = break_string(self.variable_x_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['Y'] = break_string(self.variable_y_key.get(), 1).split()
        self.cipher.key.alpha_dict_key['Z'] = break_string(self.variable_z_key.get(), 1).split()
        self.cipher.key.calculate()

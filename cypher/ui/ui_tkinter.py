from tkinter import *
from tkinter import ttk
from cypher.substitution import SubstitutionCipher, SubstitutionKey
from cypher.tools.alphabet import random_alpha_key
from cypher.utilities import get_random_fortune

# Setup Main Application Window
root = Tk()
root.title('Cypher')

# Setup the Menu
root.option_add('*tearOff', False)
menubar = Menu(root)
root['menu'] = menubar

menu_ciphers = Menu(menubar)
menu_utilities = Menu(menubar)
menubar.add_cascade(menu=menu_ciphers, label='Ciphers')
menubar.add_cascade(menu=menu_utilities, label='Utilities')

# Substitution Ciphers
menu_ciphers.add_command(label='Random Substitution')
menu_ciphers.add_command(label='Caesar')
menu_ciphers.add_command(label='Caesar Keyword')
menu_ciphers.add_command(label='Vigenere')
menu_ciphers.add_command(label='Playfair')
menu_ciphers.add_separator()

# Transposition Ciphers
menu_ciphers.add_command(label='Reverse')
menu_ciphers.add_command(label='Route')
menu_ciphers.add_command(label='Rail Fence')
menu_ciphers.add_separator()

# Other Ciphers
menu_ciphers.add_command(label='Pig Latin')

# Utilities
menu_utilities.add_command(label='Primality')
menu_utilities.add_command(label='Factors')
menu_utilities.add_command(label='Random Words')

# Create a Content Frame
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# SUBSTITUTION CIPHER
ttk.Label(mainframe, text='Random Substitution Cipher').grid(column=1, row=1, sticky=N, columnspan=3)


# Key Section
def random_alpha_key():
    alpha_key.set(random_alpha_key())


keyframe = ttk.Labelframe(mainframe, text='Key')
keyframe.grid(column=0, row=2, sticky=(N, W, E, S), columnspan=3)

ttk.Label(keyframe, text='Alpha Key').grid(column=0, row=0, sticky=E)
alpha_key = StringVar()
alpha_key_entry = ttk.Entry(keyframe, width=26, textvariable=alpha_key)
alpha_key_entry.grid(column=1, row=0, sticky=(W, E))
ttk.Button(keyframe, text='Randomize', command=random_alpha_key).grid(column=2, row=0, sticky=(W, E))

for child in keyframe.winfo_children():
    child.grid_configure(padx=5, pady=5)


# Plaintext Section
def random_plaintext():
    t = get_random_fortune()
    pt.replace('1.0', 'end', t)


ttk.Label(mainframe, text='Plaintext').grid(column=1, row=3, sticky=(N, E))
pt = Text(mainframe, width=40, height=10, wrap='word')
pt.grid(column=2, row=3, sticky=(W, E), columnspan=2)
ttk.Button(mainframe, text='Randomize', command=random_plaintext).grid(column=3, row=4, sticky=(W, E))

# Ciphertext Section
ttk.Label(mainframe, text='Ciphertext').grid(column=1, row=5, sticky=(N, E))
ct = Text(mainframe, width=40, height=10, wrap='word')
ct.grid(column=2, row=5, sticky=(W, E), columnspan=2)


# Action Section
def encrypt_button():
    plain = pt.get('1.0', 'end')
    key = SubstitutionKey(alpha_key.get())
    cipher = SubstitutionCipher(plaintext=plain, key=key)
    cipher.encrypt()
    ct.replace('1.0', 'end', cipher.ciphertext)


def decrypt_button():
    ciphert = ct.get('1.0', 'end')
    key = SubstitutionKey(alpha_key.get())
    cipher = SubstitutionCipher(ciphertext=ciphert, key=key)
    cipher.decrypt()
    pt.replace('1.0', 'end', cipher.plaintext)


ttk.Button(mainframe, text='Encrypt', command=encrypt_button).grid(column=2, row=6, sticky=E)
ttk.Button(mainframe, text='Decrypt', command=decrypt_button).grid(column=3, row=6, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

pt.focus()
root.mainloop()

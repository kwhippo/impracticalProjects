from tkinter import *
from tkinter import ttk


class MainMenu:

    def __init__(self, master):
        self.menubar = Menu(master)
        self.menu_ciphers = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_ciphers, label='Ciphers')


class CipherWindow:

    def __init__(self, master):
        pass


def main():
    root = Tk()
    root.title('Cypher')
    root.option_add('*tearOff', False)
    main_menu = MainMenu(root)
    root['menu'] = main_menu
    CipherWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()

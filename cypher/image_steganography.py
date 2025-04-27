import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from cypher.ui.mainframe import Mainframe


class ImageSteganographyFrame(Mainframe):
    def __init__(self, master, title='Image Steganography', *args, **kwargs):
        super().__init__(master, title)

        # Setup Frames
        self.frame_plainimage = ttk.LabelFrame(master, text='Image')
        self.frame_plaintext = ttk.LabelFrame(master, text='Plaintext')
        self.frame_cipherimage = ttk.LabelFrame(master, text='Cipherimage')

        # Configure Image Frame
        self.frame_plainimage_image = ttk.Frame(self.frame_plainimage, width=200, height=200)
        self.frame_plainimage_image.grid(column=0, row=0, fill=BOTH, expand=YES, padx=10, pady=10)
        self.label_plainimage = ttk.Label(self.frame_plainimage_image, text='Drag and drop an image here')
        self.label_plainimage.pack(fill=BOTH, expand=YES)


        self.frame_plainimage.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.frame_plaintext.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.frame_cipherimage.pack(fill=BOTH, expand=YES, padx=10, pady=10)

class DragDropApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drag and Drop File")

        self.style = ttk.Style('darkly')
        self.frame = ttk.Frame(master, padding=10)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.dnd_text = ttk.Label(self.frame, text="Drag and drop a file here", bootstyle="primary")
        self.dnd_text.grid(row=0, column=0, pady=10)

        self.file_path = tk.StringVar()
        self.file_label = ttk.Label(self.frame, textvariable=self.file_path, bootstyle="info")
        self.file_label.grid(row=1, column=0, pady=10)

        # Enable drop target
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        # Store the file path in a variable
        self.file_path.set(event.data)
        print(f"File path: {self.file_path.get()}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DragDropApp(root)
    root.mainloop()

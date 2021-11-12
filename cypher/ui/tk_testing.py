import tkinter as tk

root = tk.Tk()
root.title('Pack Demo')
root.geometry("300x200")

# box 1
box1 = tk.Label(
    root,
    text="Box 1",
    bg="green",
    fg="white"
)

box1.pack(
    ipadx=10,
    ipady=10,
    expand=True,
    fill='both'
)

# box 2
box2 = tk.Label(
    root,
    text="Box 2",
    bg="red",
    fg="white"
)

box2.pack(
    ipadx=10,
    ipady=10,
)

box2.config(text="Box 2\n\n\n\n\n\n")

root.mainloop()

import tkinter as tk
from tkinter import filedialog

def pick_file(file_types: list[str]) -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Allowed Files", file_types)]
    )

    return file_path

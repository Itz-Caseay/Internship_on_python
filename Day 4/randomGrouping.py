import tkinter as tk
from tkinter import messagebox
import random

def generate_groups():
    # Get names from the text box
    names = text_input.get("1.0", tk.END).strip().split("\n")
    names == [name.strip() for name in names if name.strip()]
    
    if len(names)<3:
        messagebox.showerror("Error": "Please enter atleast 3 names.")
        return
    
    # shuffle names
    random.shuffle(names)
    
    # create groups of 3
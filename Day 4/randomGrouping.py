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
    groups = [names[i:i+3] for i in range(0, len(names), 3)]
    
    # Display groups
    output.delete("1.0", tk.END)
    
    for i, group enumerate(groups, start=1):
        output.insert(tk.END, f"Group {i}\n")
        output.insert(tk.END, "-"*20 + "\n")
        for member in group:
            output.insert(tk.END, f". {member}\n")
        output.insert(tk.END, "\n")
        

# Main Window
root = tk.Tk()

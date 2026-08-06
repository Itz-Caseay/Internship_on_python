from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


def calculate_loan():
    
root = tk.Tk()
root.title("Loan Management System")
root.geometry("1020x710")
root.resizable(False, False)

MainFrame = Frame(root, bd=10, width=1020, height=7, relief=RIDGE)
MainFrame.grid()

TopFrame = Frame(root, bd=10, width=1020, height=7, relief=RIDGE)
TopFrame.grid(row=0, column=0, sticky="w")

TopFrame2 = Frame(root, bd=10, width=1020, height=7, relief=RIDGE)
TopFrame2.grid(row=0, column=0, sticky="w")

ButtonsFrame = Frame(root, bd=10, width=1020, height=7, relief=RIDGE)
ButtonsFrame.grid(row=0, column=0, sticky="w")

TopFrameLeft = Frame(root, bd=10, width=1020, height=7, relief=RIDGE)
TopFrameLeft.pack(side=LEFT)

TopFrameRight = Frame(TopFrame2, bd=5, width=500, height=600, relief=RIDGE)
TopFrameRight.pack(side=RIGHT)

root.mainloop()
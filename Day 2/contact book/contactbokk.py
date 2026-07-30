import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book CLI")
        self.root.geometry("500x500")
        
    
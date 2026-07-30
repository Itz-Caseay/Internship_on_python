import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book CLI")
        self.root.geometry("500x500")
        
        self.contacts = {}
        self.file_path = "contacts.json"
        self.load_contacts()
        
    def load_contacts(self): #1 usage
        if os.path.exists(self, self.file_path):
            with open(self.file_path, "r") as file:
                self.contacts
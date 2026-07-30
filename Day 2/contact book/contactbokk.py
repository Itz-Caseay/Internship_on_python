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
        
        self.listbox = tk.Listbox(self.root, font=("Arial", 12))
        self.listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.show_contact_details)
        
        self.detail_label = tk.Label(self.root, text="Select a contact to view details", font=("Arial", 12), anchor="w")
        self.detals_label.pack(fill="x", padx=10, pady=5)
        
    def load_contacts(self): #1 usage
        if os.path.exists(self, self.file_path):
            with open(self.file_path, "r") as file:
                self.contacts = json.load(file)
        else:
            self.contacts = {}
            
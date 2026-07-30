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
        
        self.add_button = tk.Button(self.root, text="Add Contacts", command=self.add_contact)
        self.add_button.pack(side="left", padx=10, pady=10)
        
        self.edit_button = tk.Button(self.root, text="Edit Contacts", command=self.edit_button, state="disabled")
        self.edit_button.pack(side="left", padx=10, pady=10)
        
        self.delete_button = tk.Button(self.root, text="Delete Contacts", command=self.delete_button, state="disabled")
        self.delete_button.pack(side="left", padx=10, pady=10)
        
        self.refresh_list()
        
            
    def load_contacts(self): #1 usage
        if os.path.exists(self, self.file_path):
            with open(self.file_path, "r") as file:
                self.contacts = json.load(file)
        else:
            self.contacts = {}
              
    def save_contacts(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.contacts, file)
            
    def refresh_list(self): #1 usage
        self.listbox.delete(first: 0, tk.END)
        for name in sorted(self.contacts.keys())
#!/usr/bin/env python3
"""
Contact Book - Beautiful Tkinter UI
A modern, feature-rich contact management application with a stunning GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
import uuid

# ============================================================================
# DATA LAYER
# ============================================================================

class Contact:
    """Contact model representing a person in the contact book"""
    
    def __init__(self, 
                 first_name: str,
                 last_name: str,
                 phone: str,
                 email: str = "",
                 address: str = "",
                 company: str = "",
                 job_title: str = "",
                 notes: str = "",
                 tags: List[str] = None):
        
        self.id = str(uuid.uuid4())[:8]
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = self._format_phone(phone)
        self.email = email.strip().lower() if email else ""
        self.address = address.strip()
        self.company = company.strip()
        self.job_title = job_title.strip()
        self.notes = notes.strip()
        self.tags = [tag.strip().lower() for tag in (tags or []) if tag.strip()]
        self.favorite = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        self._validate()
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number to a standard format"""
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return phone
    
    def _validate(self):
        """Validate contact data"""
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if not self.phone:
            raise ValueError("Phone number is required")
        
        if self.email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValueError("Invalid email format")
    
    def get_full_name(self) -> str:
        """Get the full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self) -> dict:
        """Convert contact to dictionary for serialization"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'company': self.company,
            'job_title': self.job_title,
            'notes': self.notes,
            'tags': self.tags,
            'favorite': self.favorite,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        """Create a Contact instance from a dictionary"""
        contact = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            email=data.get('email', ''),
            address=data.get('address', ''),
            company=data.get('company', ''),
            job_title=data.get('job_title', ''),
            notes=data.get('notes', ''),
            tags=data.get('tags', [])
        )
        contact.id = data['id']
        contact.favorite = data.get('favorite', False)
        contact.created_at = datetime.fromisoformat(data['created_at'])
        contact.updated_at = datetime.fromisoformat(data['updated_at'])
        return contact

# ============================================================================
# STORAGE HANDLER
# ============================================================================

class StorageHandler:
    """Handles reading and writing contacts to file"""
    
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.data_dir = Path.home() / ".contact_book"
        self.file_path = self.data_dir / filename
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        self.data_dir.mkdir(exist_ok=True)
    
    def save(self, contacts: List[dict]) -> bool:
        """Save contacts to file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(contacts, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving contacts: {e}")
            return False
    
    def load(self) -> List[dict]:
        """Load contacts from file"""
        if not self.file_path.exists():
            return []
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        except Exception as e:
            print(f"Error loading contacts: {e}")
            return []

# ============================================================================
# SERVICE LAYER
# ============================================================================

class ContactService:
    """Service layer for managing contacts"""
    
    def __init__(self):
        self.storage = StorageHandler()
        self.contacts: Dict[str, Contact] = {}
        self._load_contacts()
    
    def _load_contacts(self):
        """Load contacts from storage"""
        contacts_data = self.storage.load()
        for data in contacts_data:
            try:
                contact = Contact.from_dict(data)
                self.contacts[contact.id] = contact
            except Exception:
                continue
    
    def _save_contacts(self):
        """Save contacts to storage"""
        contacts_data = [contact.to_dict() for contact in self.contacts.values()]
        self.storage.save(contacts_data)
    
    def add(self, **kwargs) -> Contact:
        """Add a new contact"""
        contact = Contact(**kwargs)
        self.contacts[contact.id] = contact
        self._save_contacts()
        return contact
    
    def get(self, contact_id: str) -> Optional[Contact]:
        """Get a contact by ID"""
        return self.contacts.get(contact_id)
    
    def get_all(self, sort_by: str = "last_name") -> List[Contact]:
        """Get all contacts sorted"""
        contacts = list(self.contacts.values())
        
        sort_map = {
            "first_name": lambda c: c.first_name.lower(),
            "last_name": lambda c: c.last_name.lower(),
            "full_name": lambda c: c.get_full_name().lower(),
            "company": lambda c: c.company.lower()
        }
        
        key_func = sort_map.get(sort_by, lambda c: c.last_name.lower())
        return sorted(contacts, key=key_func)
    
    def search(self, query: str) -> List[Contact]:
        """Search contacts by multiple fields"""
        if not query:
            return []
        
        query = query.lower().strip()
        results = []
        
        for contact in self.contacts.values():
            searchable_fields = [
                contact.first_name.lower(),
                contact.last_name.lower(),
                contact.get_full_name().lower(),
                contact.phone,
                contact.email.lower(),
                contact.company.lower(),
                contact.job_title.lower(),
                contact.address.lower(),
                ' '.join(contact.tags).lower()
            ]
            
            if any(query in field for field in searchable_fields):
                results.append(contact)
        
        return results
    
    def update(self, contact_id: str, **kwargs) -> Optional[Contact]:
        """Update a contact"""
        contact = self.get(contact_id)
        if not contact:
            return None
        
        for key, value in kwargs.items():
            if hasattr(contact, key) and value is not None:
                if key == 'phone':
                    value = contact._format_phone(str(value))
                elif key == 'email':
                    value = value.strip().lower() if value else ""
                setattr(contact, key, value)
        
        contact.updated_at = datetime.now()
        self._save_contacts()
        return contact
    
    def delete(self, contact_id: str) -> bool:
        """Delete a contact"""
        if contact_id in self.contacts:
            del self.contacts[contact_id]
            self._save_contacts()
            return True
        return False
    
    def toggle_favorite(self, contact_id: str) -> Optional[bool]:
        """Toggle favorite status"""
        contact = self.get(contact_id)
        if not contact:
            return None
        
        contact.favorite = not contact.favorite
        contact.updated_at = datetime.now()
        self._save_contacts()
        return contact.favorite
    
    def add_tag(self, contact_id: str, tag: str) -> bool:
        """Add a tag to a contact"""
        contact = self.get(contact_id)
        if not contact:
            return False
        
        tag = tag.strip().lower()
        if tag and tag not in contact.tags:
            contact.tags.append(tag)
            contact.updated_at = datetime.now()
            self._save_contacts()
            return True
        return False
    
    def remove_tag(self, contact_id: str, tag: str) -> bool:
        """Remove a tag from a contact"""
        contact = self.get(contact_id)
        if not contact:
            return False
        
        tag = tag.strip().lower()
        if tag in contact.tags:
            contact.tags.remove(tag)
            contact.updated_at = datetime.now()
            self._save_contacts()
            return True
        return False
    
    def get_favorites(self) -> List[Contact]:
        """Get all favorite contacts"""
        return [c for c in self.contacts.values() if c.favorite]
    
    def get_by_tag(self, tag: str) -> List[Contact]:
        """Get contacts by tag"""
        tag = tag.lower().strip()
        return [c for c in self.contacts.values() if tag in [t.lower() for t in c.tags]]
    
    def get_all_tags(self) -> Set[str]:
        """Get all unique tags"""
        tags = set()
        for contact in self.contacts.values():
            tags.update(contact.tags)
        return tags
    
    def get_count(self) -> int:
        """Get total number of contacts"""
        return len(self.contacts)

# ============================================================================
# MAIN APPLICATION - BEAUTIFUL TKINTER UI
# ============================================================================

class ContactBookApp:
    """Beautiful Contact Book Application with Tkinter"""
    
    # Color scheme - Modern and elegant
    COLORS = {
        'primary': '#6C63FF',
        'primary_dark': '#5A52D5',
        'primary_light': '#7C73FF',
        'secondary': '#F8F9FA',
        'success': '#28A745',
        'danger': '#DC3545',
        'warning': '#FFC107',
        'info': '#17A2B8',
        'dark': '#343A40',
        'light': '#F8F9FA',
        'white': '#FFFFFF',
        'gray': '#6C757D',
        'light_gray': '#E9ECEF',
        'border': '#DEE2E6',
        'shadow': '#0000001A',
        'gradient_start': '#6C63FF',
        'gradient_end': '#4A43CC'
    }
    
    FONTS = {
        'title': ('Segoe UI', 20, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'small': ('Segoe UI', 9),
        'small_bold': ('Segoe UI', 9, 'bold'),
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Contact Book")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Set window icon (emoji as text since we can't use actual icons)
        self.root.configure(bg=self.COLORS['light'])
        
        # Initialize service
        self.service = ContactService()
        self.current_contact_id = None
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._load_contacts()
        
        # Center the window
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_styles(self):
        """Configure ttk styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview
        style.configure('Treeview', 
                       background=self.COLORS['white'],
                       foreground=self.COLORS['dark'],
                       rowheight=35,
                       font=self.FONTS['body'])
        style.configure('Treeview.Heading',
                       background=self.COLORS['primary'],
                       foreground=self.COLORS['white'],
                       font=self.FONTS['body_bold'])
        style.map('Treeview.Heading',
                 background=[('active', self.COLORS['primary_dark'])])
        
        # Configure buttons
        style.configure('Primary.TButton',
                       background=self.COLORS['primary'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=8)
        style.map('Primary.TButton',
                 background=[('active', self.COLORS['primary_dark'])])
        
        style.configure('Success.TButton',
                       background=self.COLORS['success'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=8)
        style.map('Success.TButton',
                 background=[('active', '#218838')])
        
        style.configure('Danger.TButton',
                       background=self.COLORS['danger'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=8)
        style.map('Danger.TButton',
                 background=[('active', '#C82333')])
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.COLORS['light'])
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Top header
        self._create_header()
        
        # Content area (split into left and right)
        self.content_frame = tk.Frame(self.main_container, bg=self.COLORS['light'])
        self.content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left panel - Contact list
        self._create_contact_list()
        
        # Right panel - Contact details
        self._create_contact_details()
    
    def _create_header(self):
        """Create the header with title, search, and stats"""
        header_frame = tk.Frame(self.main_container, bg=self.COLORS['white'], relief='flat', bd=1)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Title
        title_label = tk.Label(header_frame, 
                               text="📒 Contact Book",
                               font=self.FONTS['title'],
                               bg=self.COLORS['white'],
                               fg=self.COLORS['primary'])
        title_label.pack(side='left', padx=20, pady=10)
        
        # Search frame
        search_frame = tk.Frame(header_frame, bg=self.COLORS['white'])
        search_frame.pack(side='left', padx=20, fill='x', expand=True)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._search_contacts())
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light_gray'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        search_entry.pack(fill='x', pady=5, ipady=5)
        search_entry.insert(0, "🔍 Search contacts...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "🔍 Search contacts..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "🔍 Search contacts...") if not search_entry.get() else None)
        
        # Stats
        self.stats_label = tk.Label(header_frame,
                                    text="0 contacts",
                                    font=self.FONTS['body'],
                                    bg=self.COLORS['white'],
                                    fg=self.COLORS['gray'])
        self.stats_label.pack(side='right', padx=20, pady=10)
    
    def _create_contact_list(self):
        """Create the contact list panel"""
        left_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        left_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Panel header
        header_label = tk.Label(left_panel,
                               text="📋 Contacts",
                               font=self.FONTS['heading'],
                               bg=self.COLORS['white'],
                               fg=self.COLORS['dark'])
        header_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame)
        v_scroll.pack(side='right', fill='y')
        
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        h_scroll.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame,
                                columns=('name', 'phone', 'email'),
                                show='headings',
                                yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set,
                                selectmode='browse')
        
        # Configure columns
        self.tree.heading('name', text='Name', anchor='w')
        self.tree.heading('phone', text='Phone', anchor='w')
        self.tree.heading('email', text='Email', anchor='w')
        
        self.tree.column('name', width=200, minwidth=150)
        self.tree.column('phone', width=150, minwidth=120)
        self.tree.column('email', width=200, minwidth=150)
        
        self.tree.pack(fill='both', expand=True)
        
        # Configure scrollbars
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_contact_select)
        
        # Button frame
        button_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Left buttons
        left_buttons = tk.Frame(button_frame, bg=self.COLORS['white'])
        left_buttons.pack(side='left')
        
        self.add_btn = tk.Button(left_buttons,
                                text="➕ Add Contact",
                                font=self.FONTS['body_bold'],
                                bg=self.COLORS['primary'],
                                fg=self.COLORS['white'],
                                relief='flat',
                                padx=15,
                                pady=5,
                                cursor='hand2',
                                command=self._add_contact)
        self.add_btn.pack(side='left', padx=(0, 5))
        
        # Hover effects
        self._add_hover_effect(self.add_btn, self.COLORS['primary'], self.COLORS['primary_dark'])
        
        self.delete_btn = tk.Button(left_buttons,
                                   text="🗑 Delete",
                                   font=self.FONTS['body'],
                                   bg=self.COLORS['danger'],
                                   fg=self.COLORS['white'],
                                   relief='flat',
                                   padx=15,
                                   pady=5,
                                   cursor='hand2',
                                   state='disabled',
                                   command=self._delete_contact)
        self.delete_btn.pack(side='left', padx=(0, 5))
        self._add_hover_effect(self.delete_btn, self.COLORS['danger'], '#C82333')
        
        # Right buttons
        right_buttons = tk.Frame(button_frame, bg=self.COLORS['white'])
        right_buttons.pack(side='right')
        
        self.fav_filter_btn = tk.Button(right_buttons,
                                       text="⭐ Favorites",
                                       font=self.FONTS['body'],
                                       bg=self.COLORS['light_gray'],
                                       fg=self.COLORS['dark'],
                                       relief='flat',
                                       padx=15,
                                       pady=5,
                                       cursor='hand2',
                                       command=self._toggle_favorite_filter)
        self.fav_filter_btn.pack(side='left', padx=(0, 5))
        self._add_hover_effect(self.fav_filter_btn, self.COLORS['light_gray'], self.COLORS['border'])
        
        self.refresh_btn = tk.Button(right_buttons,
                                    text="🔄 Refresh",
                                    font=self.FONTS['body'],
                                    bg=self.COLORS['info'],
                                    fg=self.COLORS['white'],
                                    relief='flat',
                                    padx=15,
                                    pady=5,
                                    cursor='hand2',
                                    command=self._load_contacts)
        self.refresh_btn.pack(side='left')
        self._add_hover_effect(self.refresh_btn, self.COLORS['info'], '#138496')
        
        # Favorite filter state
        self.show_favorites_only = False
    
    def _create_contact_details(self):
        """Create the contact details panel"""
        right_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        right_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Panel header with favorite button
        header_frame = tk.Frame(right_panel, bg=self.COLORS['white'])
        header_frame.pack(fill='x', padx=15, pady=(10, 5))
        
        self.detail_title = tk.Label(header_frame,
                                     text="Contact Details",
                                     font=self.FONTS['heading'],
                                     bg=self.COLORS['white'],
                                     fg=self.COLORS['dark'])
        self.detail_title.pack(side='left')
        
        self.fav_btn = tk.Button(header_frame,
                                text="☆",
                                font=('Segoe UI', 18),
                                bg=self.COLORS['white'],
                                fg=self.COLORS['gray'],
                                relief='flat',
                                cursor='hand2',
                                state='disabled',
                                command=self._toggle_favorite)
        self.fav_btn.pack(side='right')
        
        # Details form
        form_frame = tk.Frame(right_panel, bg=self.COLORS['white'])
        form_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Create form fields
        fields = [
            ('first_name', "First Name:"),
            ('last_name', "Last Name:"),
            ('phone', "Phone:"),
            ('email', "Email:"),
            ('company', "Company:"),
            ('job_title', "Job Title:"),
            ('address', "Address:"),
        ]
        
        self.entry_vars = {}
        
        for i, (field, label) in enumerate(fields):
            # Label
            label_widget = tk.Label(form_frame,
                                   text=label,
                                   font=self.FONTS['body_bold'],
                                   bg=self.COLORS['white'],
                                   fg=self.COLORS['dark'])
            label_widget.grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            # Entry
            var = tk.StringVar()
            entry = tk.Entry(form_frame,
                            textvariable=var,
                            font=self.FONTS['body'],
                            bg=self.COLORS['light_gray'],
                            relief='flat',
                            bd=0,
                            highlightthickness=1,
                            highlightcolor=self.COLORS['primary'],
                            highlightbackground=self.COLORS['border'],
                            state='disabled')
            entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
            
            self.entry_vars[field] = var
        
        # Tags section
        tag_label = tk.Label(form_frame,
                            text="Tags:",
                            font=self.FONTS['body_bold'],
                            bg=self.COLORS['white'],
                            fg=self.COLORS['dark'])
        tag_label.grid(row=len(fields), column=0, sticky='w', pady=(5, 2))
        
        tag_frame = tk.Frame(form_frame, bg=self.COLORS['white'])
        tag_frame.grid(row=len(fields), column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        self.tag_var = tk.StringVar()
        self.tag_entry = tk.Entry(tag_frame,
                                 textvariable=self.tag_var,
                                 font=self.FONTS['body'],
                                 bg=self.COLORS['light_gray'],
                                 relief='flat',
                                 bd=0,
                                 highlightthickness=1,
                                 highlightcolor=self.COLORS['primary'],
                                 highlightbackground=self.COLORS['border'],
                                 state='disabled')
        self.tag_entry.pack(side='left', fill='x', expand=True)
        
        self.add_tag_btn = tk.Button(tag_frame,
                                    text="Add",
                                    font=self.FONTS['small'],
                                    bg=self.COLORS['primary'],
                                    fg=self.COLORS['white'],
                                    relief='flat',
                                    padx=10,
                                    pady=2,
                                    cursor='hand2',
                                    state='disabled',
                                    command=self._add_tag)
        self.add_tag_btn.pack(side='right', padx=(5, 0))
        self._add_hover_effect(self.add_tag_btn, self.COLORS['primary'], self.COLORS['primary_dark'])
        
        # Tags display
        self.tags_frame = tk.Frame(form_frame, bg=self.COLORS['white'])
        self.tags_frame.grid(row=len(fields) + 1, column=1, sticky='ew', padx=(10, 0), pady=(2, 10))
        
        # Notes section
        notes_label = tk.Label(form_frame,
                              text="Notes:",
                              font=self.FONTS['body_bold'],
                              bg=self.COLORS['white'],
                              fg=self.COLORS['dark'])
        notes_label.grid(row=len(fields) + 2, column=0, sticky='nw', pady=(5, 2))
        
        self.notes_text = scrolledtext.ScrolledText(form_frame,
                                                   height=4,
                                                   font=self.FONTS['body'],
                                                   bg=self.COLORS['light_gray'],
                                                   relief='flat',
                                                   bd=0,
                                                   highlightthickness=1,
                                                   highlightcolor=self.COLORS['primary'],
                                                   highlightbackground=self.COLORS['border'],
                                                   state='disabled')
        self.notes_text.grid(row=len(fields) + 2, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        # Save button
        save_frame = tk.Frame(right_panel, bg=self.COLORS['white'])
        save_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        self.save_btn = tk.Button(save_frame,
                                 text="💾 Save Changes",
                                 font=self.FONTS['body_bold'],
                                 bg=self.COLORS['success'],
                                 fg=self.COLORS['white'],
                                 relief='flat',
                                 padx=30,
                                 pady=10,
                                 cursor='hand2',
                                 state='disabled',
                                 command=self._save_contact)
        self.save_btn.pack()
        self._add_hover_effect(self.save_btn, self.COLORS['success'], '#218838')
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
    
    def _add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to a button"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button['background'] = hover_color
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button['background'] = normal_color
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    # ========================================================================
    # BUSINESS LOGIC METHODS
    # ========================================================================
    
    def _load_contacts(self):
        """Load and display all contacts"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get contacts
        if self.show_favorites_only:
            contacts = self.service.get_favorites()
        else:
            contacts = self.service.get_all()
        
        # Add to tree
        for contact in contacts:
            values = (
                contact.get_full_name(),
                contact.phone,
                contact.email
            )
            item = self.tree.insert('', 'end', values=values, tags=(contact.id,))
            if contact.favorite:
                self.tree.item(item, tags=('favorite', contact.id))
        
        # Update stats
        self.stats_label.config(text=f"{len(contacts)} contacts")
        
        # Enable/disable favorite filter button
        if self.show_favorites_only:
            self.fav_filter_btn.config(bg=self.COLORS['warning'], text="⭐ All Contacts")
        else:
            self.fav_filter_btn.config(bg=self.COLORS['light_gray'], text="⭐ Favorites")
        
        # Clear details if no contact selected
        if not contacts:
            self._clear_details()
    
    def _search_contacts(self):
        """Search contacts based on query"""
        query = self.search_var.get()
        if query == "🔍 Search contacts...":
            query = ""
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search
        results = self.service.search(query) if query else self.service.get_all()
        
        # Filter favorites if needed
        if self.show_favorites_only:
            results = [c for c in results if c.favorite]
        
        # Add to tree
        for contact in results:
            values = (
                contact.get_full_name(),
                contact.phone,
                contact.email
            )
            item = self.tree.insert('', 'end', values=values, tags=(contact.id,))
            if contact.favorite:
                self.tree.item(item, tags=('favorite', contact.id))
        
        # Update stats
        self.stats_label.config(text=f"{len(results)} contacts")
    
    def _on_contact_select(self, event):
        """Handle contact selection in tree"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        contact_id = self.tree.item(item, 'tags')[0] if self.tree.item(item, 'tags') else None
        
        if not contact_id:
            return
        
        # If tag is 'favorite', get the next tag
        if contact_id == 'favorite':
            tags = self.tree.item(item, 'tags')
            contact_id = tags[1] if len(tags) > 1 else None
        
        if not contact_id:
            return
        
        self.current_contact_id = contact_id
        self._display_contact(contact_id)
        
        # Enable buttons
        self.delete_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.fav_btn.config(state='normal')
    
    def _display_contact(self, contact_id: str):
        """Display contact details in the right panel"""
        contact = self.service.get(contact_id)
        if not contact:
            return
        
        # Set entry values
        self.entry_vars['first_name'].set(contact.first_name)
        self.entry_vars['last_name'].set(contact.last_name)
        self.entry_vars['phone'].set(contact.phone)
        self.entry_vars['email'].set(contact.email)
        self.entry_vars['company'].set(contact.company)
        self.entry_vars['job_title'].set(contact.job_title)
        self.entry_vars['address'].set(contact.address)
        
        # Set notes
        self.notes_text.config(state='normal')
        self.notes_text.delete('1.0', tk.END)
        self.notes_text.insert('1.0', contact.notes)
        self.notes_text.config(state='disabled')
        
        # Set tags
        self._update_tags_display(contact)
        
        # Enable entries
        for var in self.entry_vars.values():
            var.trace('w', lambda *args: self._on_field_change())
        
        for entry in self.entry_vars.values():
            entry.config(state='normal')
        
        self.tag_entry.config(state='normal')
        self.add_tag_btn.config(state='normal')
        self.notes_text.config(state='normal')
        
        # Update favorite button
        self._update_favorite_button(contact.favorite)
        
        # Update title
        self.detail_title.config(text=contact.get_full_name())
    
    def _clear_details(self):
        """Clear the details panel"""
        for var in self.entry_vars.values():
            var.set('')
        
        self.notes_text.config(state='normal')
        self.notes_text.delete('1.0', tk.END)
        self.notes_text.config(state='disabled')
        
        self.detail_title.config(text="No Contact Selected")
        self.fav_btn.config(text="☆", state='disabled')
        self.delete_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.tag_entry.config(state='disabled')
        self.add_tag_btn.config(state='disabled')
        self.notes_text.config(state='disabled')
        
        # Clear tags
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
        
        self.current_contact_id = None
    
    def _update_tags_display(self, contact):
        """Update the tags display"""
        # Clear existing tags
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
        
        # Add tag buttons
        for tag in contact.tags:
            tag_btn = tk.Button(self.tags_frame,
                               text=f"#{tag}",
                               font=self.FONTS['small'],
                               bg=self.COLORS['primary_light'],
                               fg=self.COLORS['white'],
                               relief='flat',
                               padx=8,
                               pady=2,
                               cursor='hand2')
            tag_btn.pack(side='left', padx=(0, 5), pady=2)
            
            # Remove tag on right-click
            tag_btn.bind('<Button-3>', lambda e, t=tag: self._remove_tag(t))
            
            # Tooltip
            self._create_tooltip(tag_btn, f"Right-click to remove '{tag}'")
    
    def _update_favorite_button(self, is_favorite):
        """Update the favorite button state"""
        if is_favorite:
            self.fav_btn.config(text="⭐", fg=self.COLORS['warning'])
        else:
            self.fav_btn.config(text="☆", fg=self.COLORS['gray'])
    
    def _on_field_change(self):
        """Enable save button when fields change"""
        if self.current_contact_id:
            self.save_btn.config(state='normal')
    
    def _toggle_favorite_filter(self):
        """Toggle favorite filter"""
        self.show_favorites_only = not self.show_favorites_only
        self._load_contacts()
    
    # ========================================================================
    # CONTACT OPERATIONS
    # ========================================================================
    
    def _add_contact(self):
        """Open add contact dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Add New Contact")
        dialog.geometry("400x550")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"400x550+{x}+{y}")
        
        # Title
        tk.Label(dialog,
                text="Add New Contact",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Fields
        fields = [
            ('first_name', "First Name *"),
            ('last_name', "Last Name *"),
            ('phone', "Phone *"),
            ('email', "Email"),
            ('company', "Company"),
            ('job_title', "Job Title"),
            ('address', "Address"),
            ('tags', "Tags (comma-separated)"),
            ('notes', "Notes"),
        ]
        
        entry_vars = {}
        
        for i, (field, label) in enumerate(fields):
            tk.Label(form_frame,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            if field == 'notes':
                entry = scrolledtext.ScrolledText(form_frame,
                                                 height=3,
                                                 font=self.FONTS['body'],
                                                 bg=self.COLORS['light_gray'],
                                                 relief='flat',
                                                 bd=0,
                                                 highlightthickness=1,
                                                 highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entry_vars[field] = entry
            else:
                var = tk.StringVar()
                entry = tk.Entry(form_frame,
                                textvariable=var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light_gray'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entry_vars[field] = var
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        button_frame.pack(fill='x', padx=30, pady=20)
        
        def save_contact():
            try:
                # Get values
                first_name = entry_vars['first_name'].get().strip()
                last_name = entry_vars['last_name'].get().strip()
                phone = entry_vars['phone'].get().strip()
                email = entry_vars['email'].get().strip()
                company = entry_vars['company'].get().strip()
                job_title = entry_vars['job_title'].get().strip()
                address = entry_vars['address'].get().strip()
                tags = [t.strip() for t in entry_vars['tags'].get().split(',') if t.strip()]
                notes = entry_vars['notes'].get('1.0', tk.END).strip()
                
                # Validate
                if not first_name or not last_name or not phone:
                    messagebox.showerror("Error", "First name, last name, and phone are required!")
                    return
                
                # Add contact
                contact = self.service.add(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    company=company,
                    job_title=job_title,
                    address=address,
                    tags=tags,
                    notes=notes
                )
                
                # Ask to add to favorites
                if messagebox.askyesno("Add to Favorites", "Would you like to add this contact to favorites?"):
                    self.service.toggle_favorite(contact.id)
                
                self._load_contacts()
                dialog.destroy()
                messagebox.showinfo("Success", f"Contact {contact.get_full_name()} added successfully!")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add contact: {e}")
        
        tk.Button(button_frame,
                 text="Save Contact",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=save_contact).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(button_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light_gray'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    def _save_contact(self):
        """Save the current contact"""
        if not self.current_contact_id:
            return
        
        try:
            # Get values
            first_name = self.entry_vars['first_name'].get().strip()
            last_name = self.entry_vars['last_name'].get().strip()
            phone = self.entry_vars['phone'].get().strip()
            email = self.entry_vars['email'].get().strip()
            company = self.entry_vars['company'].get().strip()
            job_title = self.entry_vars['job_title'].get().strip()
            address = self.entry_vars['address'].get().strip()
            notes = self.notes_text.get('1.0', tk.END).strip()
            
            # Validate
            if not first_name or not last_name or not phone:
                messagebox.showerror("Error", "First name, last name, and phone are required!")
                return
            
            # Update
            self.service.update(
                self.current_contact_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                company=company,
                job_title=job_title,
                address=address,
                notes=notes
            )
            
            self._load_contacts()
            self.save_btn.config(state='disabled')
            messagebox.showinfo("Success", "Contact updated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update contact: {e}")
    
    def _delete_contact(self):
        """Delete the current contact"""
        if not self.current_contact_id:
            return
        
        contact = self.service.get(self.current_contact_id)
        if not contact:
            return
        
        if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {contact.get_full_name()}?"):
            self.service.delete(self.current_contact_id)
            self._load_contacts()
            self._clear_details()
            messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def _toggle_favorite(self):
        """Toggle favorite status of current contact"""
        if not self.current_contact_id:
            return
        
        is_favorite = self.service.toggle_favorite(self.current_contact_id)
        self._update_favorite_button(is_favorite)
        self._load_contacts()
    
    def _add_tag(self):
        """Add a tag to the current contact"""
        if not self.current_contact_id:
            return
        
        tag = self.tag_var.get().strip()
        if not tag:
            return
        
        if self.service.add_tag(self.current_contact_id, tag):
            self.tag_var.set('')
            contact = self.service.get(self.current_contact_id)
            if contact:
                self._update_tags_display(contact)
            self._load_contacts()
    
    def _remove_tag(self, tag):
        """Remove a tag from the current contact"""
        if not self.current_contact_id:
            return
        
        if self.service.remove_tag(self.current_contact_id, tag):
            contact = self.service.get(self.current_contact_id)
            if contact:
                self._update_tags_display(contact)
            self._load_contacts()
    
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip,
                            text=text,
                            font=self.FONTS['small'],
                            bg=self.COLORS['dark'],
                            fg=self.COLORS['white'],
                            padx=5,
                            pady=3)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the application"""
    try:
        root = tk.Tk()
        app = ContactBookApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
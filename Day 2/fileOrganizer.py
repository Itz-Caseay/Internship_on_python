# import os
# import shutil

# path = input("Enter Path: ")
# files = os.listdir(path)

# for file in files:
#     filename,extension = os.path.splitext(file)
#     extension = extension[1:]
            
#     if os.path.exists(path+'/'+extension):
#         shutil.move(path+'/'+file, path+'/'+extension+'/'+file)
#     else:
#         os.makedirs(path+'/'+extension)
#         shutil.move(path+'/'+file, path+'/'+extension+'/'+file)

# import os
# import shutil
# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# from tkinter import font as tkfont

# class FileOrganizerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("CA File Organizer")
#         self.root.geometry("600x450")
#         self.root.resizable(False, False)
        
#         # Set style
#         self.root.configure(bg='#f0f0f0')
        
#         # Title
#         title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
#         title_label = tk.Label(root, text="📁 CA File Organizer", font=title_font, bg='#f0f0f0', pady=10)
#         title_label.pack()
        
#         # Path selection frame
#         path_frame = tk.Frame(root, bg='#f0f0f0')
#         path_frame.pack(pady=20, padx=20, fill='x')
        
#         tk.Label(path_frame, text="Select Folder:", font=("Helvetica", 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        
#         self.path_var = tk.StringVar()
#         path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=40, font=("Helvetica", 10))
#         path_entry.grid(row=1, column=0, padx=(0, 10), sticky='ew')
        
#         browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_folder, 
#                                bg='#4CAF50', fg='white', font=("Helvetica", 10), padx=15, pady=5)
#         browse_btn.grid(row=1, column=1)
        
#         path_frame.columnconfigure(0, weight=1)
        
#         # Info frame
#         info_frame = tk.Frame(root, bg='#f0f0f0')
#         info_frame.pack(pady=20, padx=20, fill='x')
        
#         self.folder_info = tk.Label(info_frame, text="No folder selected", font=("Helvetica", 9), 
#                                     bg='#f0f0f0', fg='#666')
#         self.folder_info.pack()
        
#         self.file_count = tk.Label(info_frame, text="", font=("Helvetica", 9), 
#                                    bg='#f0f0f0', fg='#666')
#         self.file_count.pack()
        
#         # Organize button
#         self.organize_btn = tk.Button(root, text="🚀 Organize Files", command=self.organize_files,
#                                       bg='#2196F3', fg='white', font=("Helvetica", 12, "bold"),
#                                       padx=30, pady=10, state='disabled')
#         self.organize_btn.pack(pady=20)
        
#         # Progress bar
#         self.progress = ttk.Progressbar(root, length=400, mode='determinate')
#         self.progress.pack(pady=10)
        
#         # Status
#         self.status_label = tk.Label(root, text="Ready", font=("Helvetica", 9), 
#                                      bg='#f0f0f0', fg='#333')
#         self.status_label.pack(pady=5)
        
#         # Log text area
#         log_frame = tk.LabelFrame(root, text="Log", bg='#f0f0f0', font=("Helvetica", 9))
#         log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
#         self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9), bg='#2b2b2b', 
#                                 fg='#00ff00', insertbackground='white')
#         self.log_text.pack(padx=5, pady=5, fill='both', expand=True)
        
#         scrollbar = tk.Scrollbar(self.log_text)
#         scrollbar.pack(side='right', fill='y')
#         self.log_text.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.log_text.yview)
        
#     def browse_folder(self):
#         folder_path = filedialog.askdirectory(title="Select Folder to Organize")
#         if folder_path:
#             self.path_var.set(folder_path)
#             self.folder_info.config(text=f"📂 {folder_path}")
#             self.update_file_count(folder_path)
#             self.organize_btn.config(state='normal')
#             self.log_text.delete(1.0, tk.END)
#             self.log_text.insert(tk.END, f"Selected folder: {folder_path}\n")
#             self.log_text.insert(tk.END, "Ready to organize files.\n")
            
#     def update_file_count(self, folder_path):
#         try:
#             files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
#             self.file_count.config(text=f"Files found: {len(files)}")
#         except:
#             self.file_count.config(text="Error reading folder")
            
#     def organize_files(self):
#         path = self.path_var.get()
#         if not path:
#             messagebox.showerror("Error", "Please select a folder first!")
#             return
            
#         try:
#             files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            
#             if not files:
#                 self.log_text.insert(tk.END, "No files to organize.\n")
#                 self.status_label.config(text="No files found")
#                 self.progress['value'] = 100
#                 return
                
#             self.organize_btn.config(state='disabled')
#             self.status_label.config(text="Organizing files...")
#             self.progress['maximum'] = len(files)
#             self.progress['value'] = 0
            
#             moved_count = 0
#             for i, file in enumerate(files, 1):
#                 filename, extension = os.path.splitext(file)
#                 extension = extension[1:] if extension else "no_extension"
                
#                 if extension:
#                     extension_folder = os.path.join(path, extension.upper())
#                 else:
#                     extension_folder = os.path.join(path, "NO_EXTENSION")
                
#                 try:
#                     if not os.path.exists(extension_folder):
#                         os.makedirs(extension_folder)
#                         self.log_text.insert(tk.END, f"Created folder: {extension.upper()}\n")
                    
#                     source = os.path.join(path, file)
#                     destination = os.path.join(extension_folder, file)
                    
#                     # Handle duplicate files
#                     if os.path.exists(destination):
#                         base, ext = os.path.splitext(file)
#                         counter = 1
#                         while os.path.exists(os.path.join(extension_folder, f"{base}_{counter}{ext}")):
#                             counter += 1
#                         destination = os.path.join(extension_folder, f"{base}_{counter}{ext}")
#                         self.log_text.insert(tk.END, f"File exists, renamed to: {base}_{counter}{ext}\n")
                    
#                     shutil.move(source, destination)
#                     moved_count += 1
#                     self.log_text.insert(tk.END, f"Moved: {file} → {extension.upper()}/\n")
                    
#                 except Exception as e:
#                     self.log_text.insert(tk.END, f"Error moving {file}: {str(e)}\n")
                
#                 self.progress['value'] = i
#                 self.root.update_idletasks()
                
#             self.progress['value'] = len(files)
#             self.status_label.config(text=f"✅ Organized {moved_count} files successfully!")
#             self.log_text.insert(tk.END, f"\n✅ Completed! Organized {moved_count} files.\n")
#             self.organize_btn.config(state='normal')
            
#             messagebox.showinfo("Success", f"Successfully organized {moved_count} files!")
            
#         except Exception as e:
#             self.log_text.insert(tk.END, f"❌ Error: {str(e)}\n")
#             self.status_label.config(text="❌ Error occurred")
#             self.organize_btn.config(state='normal')
#             messagebox.showerror("Error", f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = FileOrganizerApp(root)
#     root.mainloop()

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont
import threading
from datetime import datetime

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        
        # Variables
        self.path_var = tk.StringVar()
        self.is_organizing = False
        
        # Classic color scheme
        self.colors = {
            'bg': '#f0f0f0',
            'frame_bg': '#e8e8e8',
            'button': '#d4d0c8',
            'button_active': '#c0b8b0',
            'text': '#000000',
            'status': '#404040',
            'log_bg': '#ffffff'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.setup_ui()
        self.setup_menu()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Folder", command=self.browse_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_ui(self):
        # Main container with classic border
        main_frame = tk.Frame(
            self.root,
            bg=self.colors['frame_bg'],
            relief='raised',
            bd=2
        )
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        self.create_title(main_frame)
        
        # Path selection
        self.create_path_section(main_frame)
        
        # Separator
        self.create_separator(main_frame)
        
        # File info
        self.create_info_section(main_frame)
        
        # Buttons
        self.create_button_section(main_frame)
        
        # Progress
        self.create_progress_section(main_frame)
        
        # Log
        self.create_log_section(main_frame)
        
        # Status bar
        self.create_status_bar()
        
    def create_title(self, parent):
        title_frame = tk.Frame(parent, bg=self.colors['frame_bg'])
        title_frame.pack(fill='x', pady=(5, 10))
        
        # Classic title
        title = tk.Label(
            title_frame,
            text="File Organizer",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        )
        title.pack(side='left')
        
        # Version
        version = tk.Label(
            title_frame,
            text="v1.0",
            font=("Segoe UI", 8),
            bg=self.colors['frame_bg'],
            fg='#666666'
        )
        version.pack(side='left', padx=(8, 0))
        
        # Organization count
        self.org_count_label = tk.Label(
            title_frame,
            text="",
            font=("Segoe UI", 8),
            bg=self.colors['frame_bg'],
            fg='#666666'
        )
        self.org_count_label.pack(side='right')
        
    def create_path_section(self, parent):
        path_frame = tk.Frame(parent, bg=self.colors['frame_bg'])
        path_frame.pack(fill='x', pady=(0, 10))
        
        # Label
        label = tk.Label(
            path_frame,
            text="Folder:",
            font=("Segoe UI", 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            width=8,
            anchor='w'
        )
        label.pack(side='left')
        
        # Entry
        self.path_entry = tk.Entry(
            path_frame,
            textvariable=self.path_var,
            font=("Segoe UI", 9),
            bg='white',
            relief='sunken',
            bd=1,
            width=45
        )
        self.path_entry.pack(side='left', padx=(0, 5), fill='x', expand=True)
        
        # Browse button
        browse_btn = tk.Button(
            path_frame,
            text="Browse...",
            command=self.browse_folder,
            font=("Segoe UI", 9),
            bg=self.colors['button'],
            relief='raised',
            bd=2,
            padx=10,
            pady=1,
            cursor='hand2'
        )
        browse_btn.pack(side='right')
        
    def create_separator(self, parent):
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', pady=8)
        
    def create_info_section(self, parent):
        info_frame = tk.Frame(parent, bg=self.colors['frame_bg'])
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Info labels in a grid
        self.file_count_label = tk.Label(
            info_frame,
            text="Files: 0",
            font=("Segoe UI", 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            anchor='w',
            width=20
        )
        self.file_count_label.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        self.folder_count_label = tk.Label(
            info_frame,
            text="Folders: 0",
            font=("Segoe UI", 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            anchor='w',
            width=20
        )
        self.folder_count_label.grid(row=0, column=1, sticky='w')
        
        self.ext_count_label = tk.Label(
            info_frame,
            text="File types: 0",
            font=("Segoe UI", 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            anchor='w',
            width=20
        )
        self.ext_count_label.grid(row=0, column=2, sticky='w')
        
        # Configure grid weights
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(2, weight=1)
        
    def create_button_section(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['frame_bg'])
        button_frame.pack(fill='x', pady=(0, 10))
        
        # Organize button (prominent)
        self.organize_btn = tk.Button(
            button_frame,
            text="▶ Organize Files",
            command=self.start_organization,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['button'],
            relief='raised',
            bd=2,
            padx=20,
            pady=4,
            cursor='hand2',
            state='disabled'
        )
        self.organize_btn.pack(side='left', padx=(0, 8))
        
        # Preview button
        self.preview_btn = tk.Button(
            button_frame,
            text="Preview",
            command=self.preview_files,
            font=("Segoe UI", 9),
            bg=self.colors['button'],
            relief='raised',
            bd=2,
            padx=15,
            pady=4,
            cursor='hand2',
            state='disabled'
        )
        self.preview_btn.pack(side='left', padx=(0, 8))
        
        # Clear log button
        clear_btn = tk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            font=("Segoe UI", 9),
            bg=self.colors['button'],
            relief='raised',
            bd=2,
            padx=15,
            pady=4,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=(0, 8))
        
        # Separator line
        sep = ttk.Separator(button_frame, orient='vertical')
        sep.pack(side='left', fill='y', padx=8, pady=2)
        
        # Stop button (hidden initially)
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_organization,
            font=("Segoe UI", 9, "bold"),
            bg='#ff6b6b',
            relief='raised',
            bd=2,
            padx=15,
            pady=4,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left')
        
    def create_progress_section(self, parent):
        progress_frame = tk.Frame(parent, bg=self.colors['frame_bg'])
        progress_frame.pack(fill='x', pady=(0, 10))
        
        # Classic progress bar
        self.progress = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress.pack(fill='x')
        
        # Progress text
        self.progress_text = tk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 8),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        )
        self.progress_text.pack(anchor='e', pady=(2, 0))
        
    def create_log_section(self, parent):
        log_frame = tk.LabelFrame(
            parent,
            text="Log",
            bg=self.colors['frame_bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief='groove',
            bd=2
        )
        log_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Log container
        log_container = tk.Frame(log_frame, bg='white', relief='sunken', bd=1)
        log_container.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Log text with scrollbar
        self.log_text = tk.Text(
            log_container,
            height=8,
            font=("Consolas", 9),
            bg='white',
            fg='#000000',
            wrap='word',
            relief='flat',
            bd=0,
            selectbackground='#cce8ff'
        )
        self.log_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure tags for log messages
        self.log_text.tag_configure('info', foreground='#0066cc')
        self.log_text.tag_configure('success', foreground='#008000')
        self.log_text.tag_configure('error', foreground='#cc0000')
        self.log_text.tag_configure('warning', foreground='#cc6600')
        
        # Initial log message
        self.log_message("Ready. Select a folder to begin.", 'info')
        
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg='#d4d0c8', relief='sunken', bd=1, height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=("Segoe UI", 8),
            bg='#d4d0c8',
            fg=self.colors['text'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=5)
        
        # Current file being processed
        self.current_file_label = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 8),
            bg='#d4d0c8',
            fg='#404040',
            anchor='e'
        )
        self.current_file_label.pack(side='right', padx=5)
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Organize")
        if folder_path:
            self.path_var.set(folder_path)
            self.update_info(folder_path)
            self.organize_btn.config(state='normal')
            self.preview_btn.config(state='normal')
            self.log_message(f"Selected folder: {folder_path}", 'info')
            
    def update_info(self, folder_path):
        try:
            total_files = 0
            total_folders = 0
            extensions = set()
            
            for root, dirs, files in os.walk(folder_path):
                total_folders += len(dirs)
                total_files += len(files)
                for file in files:
                    _, ext = os.path.splitext(file)
                    if ext:
                        extensions.add(ext[1:].lower())
            
            self.file_count_label.config(text=f"Files: {total_files}")
            self.folder_count_label.config(text=f"Folders: {total_folders}")
            self.ext_count_label.config(text=f"File types: {len(extensions)}")
            
        except Exception as e:
            self.log_message(f"Error reading folder: {str(e)}", 'error')
            
    def preview_files(self):
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
            
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            
            if not files:
                messagebox.showinfo("Preview", "No files found in this folder.")
                return
                
            # Classic preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("File Preview")
            preview_window.geometry("450x400")
            preview_window.resizable(False, False)
            preview_window.configure(bg=self.colors['frame_bg'])
            
            # Title
            tk.Label(
                preview_window,
                text="Files to organize",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['frame_bg']
            ).pack(pady=10)
            
            # Listbox with scrollbar
            frame = tk.Frame(preview_window, bg='white', relief='sunken', bd=1)
            frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            listbox = tk.Listbox(
                frame,
                yscrollcommand=scrollbar.set,
                font=("Consolas", 9),
                bg='white',
                selectmode='single',
                relief='flat',
                bd=0
            )
            listbox.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=listbox.yview)
            
            # Group files by extension
            extension_groups = {}
            for file in sorted(files):
                _, ext = os.path.splitext(file)
                ext = ext[1:].upper() if ext else "NO EXTENSION"
                if ext not in extension_groups:
                    extension_groups[ext] = []
                extension_groups[ext].append(file)
            
            # Add to listbox
            for ext, file_list in sorted(extension_groups.items()):
                listbox.insert(tk.END, f"[{ext}] ({len(file_list)} files)")
                for file in file_list:
                    listbox.insert(tk.END, f"  {file}")
                listbox.insert(tk.END, "")
            
            # Close button
            tk.Button(
                preview_window,
                text="Close",
                command=preview_window.destroy,
                font=("Segoe UI", 9),
                bg=self.colors['button'],
                relief='raised',
                bd=2,
                padx=30,
                pady=4,
                cursor='hand2'
            ).pack(pady=10)
            
        except Exception as e:
            self.log_message(f"Preview error: {str(e)}", 'error')
            
    def start_organization(self):
        if self.is_organizing:
            return
            
        path = self.path_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
            
        # Confirm
        if not messagebox.askyesno("Confirm", "Organize files in this folder?"):
            return
            
        self.is_organizing = True
        self.stop_btn.config(state='normal')
        self.organize_btn.config(state='disabled', text="⏳ Organizing...")
        self.preview_btn.config(state='disabled')
        self.progress['value'] = 0
        self.progress_text.config(text="0%")
        self.org_count_label.config(text="")
        self.current_file_label.config(text="")
        
        thread = threading.Thread(target=self.organize_files, args=(path,))
        thread.daemon = True
        thread.start()
        
    def stop_organization(self):
        if self.is_organizing:
            self.is_organizing = False
            self.log_message("⏹ Organization stopped by user", 'warning')
            self.organization_complete()
        
    def organize_files(self, path):
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            
            if not files:
                self.root.after(0, lambda: self.log_message("No files found to organize.", 'warning'))
                self.root.after(0, self.organization_complete)
                return
                
            self.root.after(0, lambda: self.log_message(f"Organizing {len(files)} files...", 'info'))
            
            moved_count = 0
            error_count = 0
            
            for i, file in enumerate(files, 1):
                if not self.is_organizing:
                    break
                    
                file_path = os.path.join(path, file)
                filename, extension = os.path.splitext(file)
                extension = extension[1:] if extension else "NO_EXTENSION"
                extension_folder = os.path.join(path, extension.upper())
                
                try:
                    # Update status
                    self.root.after(0, lambda f=file: self.current_file_label.config(text=f"Processing: {f}"))
                    
                    if not os.path.exists(extension_folder):
                        os.makedirs(extension_folder)
                        self.root.after(0, lambda e=extension: self.log_message(f"Created folder: {e.upper()}", 'info'))
                    
                    source = file_path
                    destination = os.path.join(extension_folder, file)
                    
                    if os.path.exists(destination):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(os.path.join(extension_folder, f"{base}_{counter}{ext}")):
                            counter += 1
                        destination = os.path.join(extension_folder, f"{base}_{counter}{ext}")
                        self.root.after(0, lambda f=file, n=f"{base}_{counter}{ext}": 
                                      self.log_message(f"Renamed: {f} → {n}", 'warning'))
                    
                    shutil.move(source, destination)
                    moved_count += 1
                    self.root.after(0, lambda f=file, e=extension: 
                                  self.log_message(f"Moved: {f} → {e.upper()}/", 'success'))
                    
                except Exception as e:
                    error_count += 1
                    self.root.after(0, lambda f=file, err=str(e): 
                                  self.log_message(f"Error moving {f}: {err}", 'error'))
                
                # Update progress
                progress = (i / len(files)) * 100
                self.root.after(0, lambda p=progress: self.update_progress(p))
                
            # Complete
            self.root.after(0, lambda: self.org_count_label.config(
                text=f"Moved: {moved_count} | Errors: {error_count}"))
            self.root.after(0, lambda: self.log_message(
                f"Completed! Moved {moved_count} files with {error_count} errors.", 'info'))
            self.root.after(0, lambda: self.update_info(path))
            self.root.after(0, self.organization_complete)
            
            if error_count == 0 and moved_count > 0:
                self.root.after(0, lambda: messagebox.showinfo("Complete", 
                    f"Successfully organized {moved_count} files!"))
                    
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error: {str(e)}", 'error'))
            self.root.after(0, self.organization_complete)
            
    def update_progress(self, value):
        self.progress['value'] = value
        self.progress_text.config(text=f"{int(value)}%")
        
    def organization_complete(self):
        self.is_organizing = False
        self.organize_btn.config(state='normal', text="▶ Organize Files")
        self.preview_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.current_file_label.config(text="")
        self.status_label.config(text="Status: Ready")
        
    def clear_log(self):
        if messagebox.askyesno("Clear Log", "Clear the log?"):
            self.log_text.delete(1.0, tk.END)
            self.log_message("Log cleared.", 'info')
            
    def log_message(self, message, tag=''):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, tag)
        self.log_text.see(tk.END)
        
        # Update status
        self.status_label.config(text=f"Status: {message[:40]}{'...' if len(message) > 40 else ''}")
        
    def show_about(self):
        about_text = """File Organizer v1.0
        
A simple file organization tool that sorts files
into folders based on their extensions.

Features:
• Automatic file sorting by extension
• Preview before organizing
• Progress tracking
• Detailed activity log

Created with Python and Tkinter"""
        
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
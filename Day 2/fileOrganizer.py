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

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CA File Organizer")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Set style
        self.root.configure(bg='#f0f0f0')
        
        # Title
        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        title_label = tk.Label(root, text="📁 CA File Organizer", font=title_font, bg='#f0f0f0', pady=10)
        title_label.pack()
        
        # Path selection frame
        path_frame = tk.Frame(root, bg='#f0f0f0')
        path_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(path_frame, text="Select Folder:", font=("Helvetica", 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=40, font=("Helvetica", 10))
        path_entry.grid(row=1, column=0, padx=(0, 10), sticky='ew')
        
        browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_folder, 
                               bg='#4CAF50', fg='white', font=("Helvetica", 10), padx=15, pady=5)
        browse_btn.grid(row=1, column=1)
        
        path_frame.columnconfigure(0, weight=1)
        
        # Info frame
        info_frame = tk.Frame(root, bg='#f0f0f0')
        info_frame.pack(pady=20, padx=20, fill='x')
        
        self.folder_info = tk.Label(info_frame, text="No folder selected", font=("Helvetica", 9), 
                                    bg='#f0f0f0', fg='#666')
        self.folder_info.pack()
        
        self.file_count = tk.Label(info_frame, text="", font=("Helvetica", 9), 
                                   bg='#f0f0f0', fg='#666')
        self.file_count.pack()
        
        # Organize button
        self.organize_btn = tk.Button(root, text="🚀 Organize Files", command=self.organize_files,
                                      bg='#2196F3', fg='white', font=("Helvetica", 12, "bold"),
                                      padx=30, pady=10, state='disabled')
        self.organize_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(root, text="Ready", font=("Helvetica", 9), 
                                     bg='#f0f0f0', fg='#333')
        self.status_label.pack(pady=5)
        
        # Log text area
        log_frame = tk.LabelFrame(root, text="Log", bg='#f0f0f0', font=("Helvetica", 9))
        log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9), bg='#2b2b2b', 
                                fg='#00ff00', insertbackground='white')
        self.log_text.pack(padx=5, pady=5, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Organize")
        if folder_path:
            self.path_var.set(folder_path)
            self.folder_info.config(text=f"📂 {folder_path}")
            self.update_file_count(folder_path)
            self.organize_btn.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"Selected folder: {folder_path}\n")
            self.log_text.insert(tk.END, "Ready to organize files.\n")
            
    def update_file_count(self, folder_path):
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            self.file_count.config(text=f"Files found: {len(files)}")
        except:
            self.file_count.config(text="Error reading folder")
            
    def organize_files(self):
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Error", "Please select a folder first!")
            return
            
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            
            if not files:
                self.log_text.insert(tk.END, "No files to organize.\n")
                self.status_label.config(text="No files found")
                self.progress['value'] = 100
                return
                
            self.organize_btn.config(state='disabled')
            self.status_label.config(text="Organizing files...")
            self.progress['maximum'] = len(files)
            self.progress['value'] = 0
            
            moved_count = 0
            for i, file in enumerate(files, 1):
                filename, extension = os.path.splitext(file)
                extension = extension[1:] if extension else "no_extension"
                
                if extension:
                    extension_folder = os.path.join(path, extension.upper())
                else:
                    extension_folder = os.path.join(path, "NO_EXTENSION")
                
                try:
                    if not os.path.exists(extension_folder):
                        os.makedirs(extension_folder)
                        self.log_text.insert(tk.END, f"Created folder: {extension.upper()}\n")
                    
                    source = os.path.join(path, file)
                    destination = os.path.join(extension_folder, file)
                    
                    # Handle duplicate files
                    if os.path.exists(destination):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(os.path.join(extension_folder, f"{base}_{counter}{ext}")):
                            counter += 1
                        destination = os.path.join(extension_folder, f"{base}_{counter}{ext}")
                        self.log_text.insert(tk.END, f"File exists, renamed to: {base}_{counter}{ext}\n")
                    
                    shutil.move(source, destination)
                    moved_count += 1
                    self.log_text.insert(tk.END, f"Moved: {file} → {extension.upper()}/\n")
                    
                except Exception as e:
                    self.log_text.insert(tk.END, f"Error moving {file}: {str(e)}\n")
                
                self.progress['value'] = i
                self.root.update_idletasks()
                
            self.progress['value'] = len(files)
            self.status_label.config(text=f"✅ Organized {moved_count} files successfully!")
            self.log_text.insert(tk.END, f"\n✅ Completed! Organized {moved_count} files.\n")
            self.organize_btn.config(state='normal')
            
            messagebox.showinfo("Success", f"Successfully organized {moved_count} files!")
            
        except Exception as e:
            self.log_text.insert(tk.END, f"❌ Error: {str(e)}\n")
            self.status_label.config(text="❌ Error occurred")
            self.organize_btn.config(state='normal')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
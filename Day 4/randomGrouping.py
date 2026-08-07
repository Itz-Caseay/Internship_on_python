import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import random
import re
from datetime import datetime

class GroupGeneratorApp:
    """Beautiful Group Generator Application"""
    
    # Modern color scheme
    COLORS = {
        'primary': '#6C63FF',
        'primary_dark': '#5A52D5',
        'primary_light': '#8B83FF',
        'secondary': '#FF6584',
        'success': '#2ECC71',
        'warning': '#F1C40F',
        'danger': '#E74C3C',
        'dark': '#2C3E50',
        'gray': '#95A5A6',
        'light_gray': '#ECF0F1',
        'white': '#FFFFFF',
        'background': '#F0F2F5',
        'card_bg': '#FFFFFF',
        'border': '#DEE2E6',
        'shadow': '#0000001A',
        'output_bg': '#1E1E2E',  # Dark background for output
        'output_text': '#FFFFFF',  # White text for output
        'group_header': '#FF6B6B',  # Red for group headers
        'group_separator': '#4ECDC4',  # Teal for separators
        'member_name': '#95E1D3',  # Light green for members
        'member_bullet': '#FFE66D'  # Yellow for bullets
    }
    
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'subtitle': ('Segoe UI', 14),
        'heading': ('Segoe UI', 16, 'bold'),
        'body': ('Segoe UI', 11),
        'body_bold': ('Segoe UI', 11, 'bold'),
        'small': ('Segoe UI', 9),
        'small_bold': ('Segoe UI', 9, 'bold'),  # ADDED MISSING FONT
        'mono': ('Consolas', 11)
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Group Generator Pro")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        self.root.configure(bg=self.COLORS['background'])
        
        # Variables
        self.group_size_var = tk.StringVar(value="3")
        self.shuffle_mode_var = tk.BooleanVar(value=True)
        self.remove_duplicates_var = tk.BooleanVar(value=True)
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._center_window()
        
        # Add sample data for demo
        self._add_sample_data()
    
    def _setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles for buttons
        style.configure('Primary.TButton',
                       background=self.COLORS['primary'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', self.COLORS['primary_dark'])])
        
        style.configure('Success.TButton',
                       background=self.COLORS['success'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=10)
        style.map('Success.TButton',
                 background=[('active', '#27AE60')])
        
        style.configure('Danger.TButton',
                       background=self.COLORS['danger'],
                       foreground='white',
                       font=self.FONTS['body_bold'],
                       padding=10)
        style.map('Danger.TButton',
                 background=[('active', '#C0392B')])
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.COLORS['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with gradient effect
        self._create_header(main_container)
        
        # Main content
        content_frame = tk.Frame(main_container, bg=self.COLORS['background'])
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left panel - Input
        left_panel = self._create_input_panel(content_frame)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right panel - Output
        right_panel = self._create_output_panel(content_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Status bar
        self._create_status_bar(main_container)
    
    def _create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.COLORS['white'], relief='flat', bd=0)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Main header
        header_content = tk.Frame(header_frame, bg=self.COLORS['white'])
        header_content.pack(fill='x', padx=20, pady=15)
        
        # Title with icon
        title_label = tk.Label(
            header_content,
            text="🎯 Group Generator Pro",
            font=self.FONTS['title'],
            bg=self.COLORS['white'],
            fg=self.COLORS['primary']
        )
        title_label.pack(side='left')
        
        # Subtitle
        subtitle = tk.Label(
            header_content,
            text="Random Team Group Maker",
            font=self.FONTS['subtitle'],
            bg=self.COLORS['white'],
            fg=self.COLORS['gray']
        )
        subtitle.pack(side='left', padx=(10, 0))
        
        # Stats badge
        self.stats_badge = tk.Label(
            header_content,
            text="👥 0 members",
            font=self.FONTS['body_bold'],
            bg=self.COLORS['primary_light'],
            fg=self.COLORS['white'],
            padx=15,
            pady=5
        )
        self.stats_badge.pack(side='right')
    
    def _create_input_panel(self, parent):
        """Create the input panel"""
        panel = tk.Frame(parent, bg=self.COLORS['white'], relief='flat', bd=0)
        panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Panel header
        header = tk.Frame(panel, bg=self.COLORS['primary'], height=40)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📝 Enter Names",
            font=self.FONTS['heading'],
            bg=self.COLORS['primary'],
            fg=self.COLORS['white']
        ).pack(side='left', padx=15, pady=8)
        
        # Member count
        self.member_count = tk.Label(
            header,
            text="0 members",
            font=self.FONTS['small'],
            bg=self.COLORS['primary'],
            fg=self.COLORS['white']
        )
        self.member_count.pack(side='right', padx=15)
        
        # Input area
        input_frame = tk.Frame(panel, bg=self.COLORS['white'])
        input_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Instructions
        tk.Label(
            input_frame,
            text="Enter one name per line:",
            font=self.FONTS['body_bold'],
            bg=self.COLORS['white'],
            fg=self.COLORS['dark']
        ).pack(anchor='w', pady=(0, 5))
        
        # Text input with scrollbar
        text_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        text_frame.pack(fill='both', expand=True)
        
        self.text_input = scrolledtext.ScrolledText(
            text_frame,
            height=10,
            font=self.FONTS['body'],
            bg=self.COLORS['white'],
            fg=self.COLORS['dark'],
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightcolor=self.COLORS['primary'],
            highlightbackground=self.COLORS['border']
        )
        self.text_input.pack(fill='both', expand=True)
        self.text_input.bind('<KeyRelease>', self._update_stats)
        
        # Options frame
        options_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        options_frame.pack(fill='x', pady=(10, 0))
        
        # Group size
        size_frame = tk.Frame(options_frame, bg=self.COLORS['white'])
        size_frame.pack(side='left', padx=(0, 15))
        
        tk.Label(
            size_frame,
            text="Group Size:",
            font=self.FONTS['body_bold'],
            bg=self.COLORS['white'],
            fg=self.COLORS['dark']
        ).pack(side='left', padx=(0, 5))
        
        size_spinbox = tk.Spinbox(
            size_frame,
            from_=2,
            to=10,
            textvariable=self.group_size_var,
            width=4,
            font=self.FONTS['body'],
            bg=self.COLORS['white'],
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.COLORS['primary']
        )
        size_spinbox.pack(side='left')
        
        # Checkboxes
        checks_frame = tk.Frame(options_frame, bg=self.COLORS['white'])
        checks_frame.pack(side='right')
        
        # Shuffle checkbox
        self.shuffle_check = tk.Checkbutton(
            checks_frame,
            text="🔀 Shuffle",
            variable=self.shuffle_mode_var,
            font=self.FONTS['body'],
            bg=self.COLORS['white'],
            fg=self.COLORS['dark'],
            selectcolor=self.COLORS['white']
        )
        self.shuffle_check.pack(side='left', padx=(0, 10))
        
        # Remove duplicates checkbox
        self.dup_check = tk.Checkbutton(
            checks_frame,
            text="🚫 Remove Duplicates",
            variable=self.remove_duplicates_var,
            font=self.FONTS['body'],
            bg=self.COLORS['white'],
            fg=self.COLORS['dark'],
            selectcolor=self.COLORS['white']
        )
        self.dup_check.pack(side='left')
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Generate button
        self.generate_btn = tk.Button(
            button_frame,
            text="🚀 Generate Groups",
            font=self.FONTS['body_bold'],
            bg=self.COLORS['primary'],
            fg=self.COLORS['white'],
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.generate_groups
        )
        self.generate_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self._add_hover_effect(self.generate_btn, self.COLORS['primary'], self.COLORS['primary_dark'])
        
        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=self.FONTS['body'],
            bg=self.COLORS['light_gray'],
            fg=self.COLORS['dark'],
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.clear_input
        )
        self.clear_btn.pack(side='left', padx=(5, 0))
        self._add_hover_effect(self.clear_btn, self.COLORS['light_gray'], self.COLORS['border'])
        
        return panel
    
    def _create_output_panel(self, parent):
        """Create the output panel - FIXED VISIBILITY"""
        panel = tk.Frame(parent, bg=self.COLORS['white'], relief='flat', bd=0)
        panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Panel header
        header = tk.Frame(panel, bg=self.COLORS['secondary'], height=40)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📋 Generated Groups",
            font=self.FONTS['heading'],
            bg=self.COLORS['secondary'],
            fg=self.COLORS['white']
        ).pack(side='left', padx=15, pady=8)
        
        # Group count badge
        self.group_count = tk.Label(
            header,
            text="0 groups",
            font=self.FONTS['small'],
            bg=self.COLORS['secondary'],
            fg=self.COLORS['white']
        )
        self.group_count.pack(side='left', padx=10)
        
        # Copy button
        self.copy_btn = tk.Button(
            header,
            text="📋 Copy",
            font=self.FONTS['small_bold'],  # Now this exists
            bg=self.COLORS['white'],
            fg=self.COLORS['secondary'],
            relief='flat',
            padx=15,
            pady=4,
            cursor='hand2',
            state='disabled',
            command=self.copy_output
        )
        self.copy_btn.pack(side='right', padx=10)
        
        # Output area - FIXED VISIBILITY
        output_frame = tk.Frame(panel, bg=self.COLORS['dark'])
        output_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.output = scrolledtext.ScrolledText(
            output_frame,
            height=14,
            font=self.FONTS['mono'],
            bg=self.COLORS['dark'],  # Dark background
            fg=self.COLORS['white'],  # White text for visibility
            insertbackground='white',
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightcolor=self.COLORS['secondary'],
            highlightbackground=self.COLORS['border'],
            wrap='word'
        )
        self.output.pack(fill='both', expand=True)
        
        # Configure text tags for styling - CLEARLY VISIBLE COLORS
        self.output.tag_configure('group_header', 
                                 foreground='#FF6B6B',  # Bright red
                                 font=('Consolas', 13, 'bold'))
        self.output.tag_configure('group_separator', 
                                 foreground='#4ECDC4',  # Teal
                                 font=('Consolas', 10))
        self.output.tag_configure('member_name', 
                                 foreground='#95E1D3',  # Light green
                                 font=('Consolas', 11))
        self.output.tag_configure('member_bullet', 
                                 foreground='#FFE66D',  # Yellow
                                 font=('Consolas', 11, 'bold'))
        self.output.tag_configure('summary', 
                                 foreground='#FF9FF3',  # Pink
                                 font=('Consolas', 11, 'bold'))
        
        # Initial message
        self._show_welcome_message()
        
        return panel
    
    def _show_welcome_message(self):
        """Show welcome message in output"""
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", "🎯 Click 'Generate Groups' to create teams!\n\n", 'group_header')
        self.output.insert("end", "━" * 40 + "\n\n", 'group_separator')
        self.output.insert("end", "💡 Tips:\n", 'summary')
        self.output.insert("end", "  • Enter one name per line\n", 'member_name')
        self.output.insert("end", "  • Adjust group size with the spinbox\n", 'member_name')
        self.output.insert("end", "  • Toggle shuffle and duplicate removal\n", 'member_name')
        self.output.insert("end", "  • Groups will appear here with colors\n", 'member_name')
    
    def _create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = tk.Frame(parent, bg=self.COLORS['dark'], height=30)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready",
            font=self.FONTS['small'],
            bg=self.COLORS['dark'],
            fg=self.COLORS['white'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10)
        
        self.status_time = tk.Label(
            status_frame,
            text=datetime.now().strftime('%H:%M:%S'),
            font=self.FONTS['small'],
            bg=self.COLORS['dark'],
            fg=self.COLORS['white'],
            anchor='e'
        )
        self.status_time.pack(side='right', padx=10)
        
        # Update time
        self._update_time()
    
    def _update_time(self):
        """Update status bar time"""
        self.status_time.config(text=datetime.now().strftime('%H:%M:%S'))
        self.root.after(1000, self._update_time)
    
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
    
    def _update_stats(self, event=None):
        """Update member count stats"""
        text = self.text_input.get("1.0", tk.END).strip()
        names = [name.strip() for name in text.split('\n') if name.strip()]
        count = len(names)
        
        self.member_count.config(text=f"{count} members")
        self.stats_badge.config(text=f"👥 {count} members")
    
    def _add_sample_data(self):
        """Add sample data for demo"""
        sample_names = [
            "Alice Johnson",
            "Bob Smith",
            "Charlie Brown",
            "Diana Prince",
            "Evan Wright",
            "Fiona Gallagher",
            "George Harrison",
            "Hannah Montana",
            "Ian Malcolm",
            "Julia Roberts",
            "Kevin Hart",
            "Laura Palmer",
            "Michael Scott",
            "Nancy Drew",
            "Oscar Wilde",
            "Patricia Arquette",
            "Quentin Tarantino",
            "Rachel Green",
            "Steve Jobs",
            "Tina Fey",
            "Uma Thurman",
            "Victor Hugo",
            "Wendy Williams",
            "Xavier Riddle",
            "Yvonne Strahovski",
            "Zachary Quinto"
        ]
        
        self.text_input.insert("1.0", "\n".join(sample_names))
        self._update_stats()
    
    def clear_input(self):
        """Clear the input field"""
        if messagebox.askyesno("Clear Input", "Clear all names?"):
            self.text_input.delete("1.0", tk.END)
            self._update_stats()
            self.set_status("Input cleared")
            self._show_welcome_message()
            self.copy_btn.config(state='disabled')
            self.group_count.config(text="0 groups")
    
    def set_status(self, message, is_error=False):
        """Set status bar message"""
        color = self.COLORS['danger'] if is_error else self.COLORS['white']
        self.status_label.config(text=f"{'❌' if is_error else '✅'} {message}", fg=color)
    
    def generate_groups(self):
        """Generate groups from input names - FIXED VISIBILITY"""
        try:
            # Get names
            text = self.text_input.get("1.0", tk.END).strip()
            names = [name.strip() for name in text.split('\n') if name.strip()]
            
            # Remove duplicates if enabled
            if self.remove_duplicates_var.get():
                # Preserve order while removing duplicates
                seen = set()
                names = [x for x in names if not (x in seen or seen.add(x))]
            
            # Validate
            if len(names) < 3:
                messagebox.showerror(
                    "Error",
                    f"Please enter at least 3 names.\nCurrent count: {len(names)}"
                )
                self.set_status("Not enough names", True)
                return
            
            # Shuffle if enabled
            if self.shuffle_mode_var.get():
                random.shuffle(names)
            
            # Get group size
            group_size = int(self.group_size_var.get())
            
            # Create groups
            groups = [names[i:i+group_size] for i in range(0, len(names), group_size)]
            
            # Clear output
            self.output.delete("1.0", tk.END)
            
            # Display groups with CLEAR VISIBILITY
            for i, group in enumerate(groups, start=1):
                # Group header - BRIGHT RED
                self.output.insert(
                    tk.END,
                    f"🎯 GROUP {i}\n",
                    'group_header'
                )
                self.output.insert(
                    tk.END,
                    "═" * 35 + "\n",
                    'group_separator'
                )
                
                # Members with CLEAR VISIBILITY
                for member in group:
                    self.output.insert(
                        tk.END,
                        "● ",
                        'member_bullet'
                    )
                    self.output.insert(
                        tk.END,
                        f"{member}\n",
                        'member_name'
                    )
                
                self.output.insert(tk.END, "\n")
            
            # Statistics summary - PINK
            total_members = len(names)
            total_groups = len(groups)
            avg_size = total_members / total_groups
            
            self.output.insert(
                tk.END,
                "━" * 35 + "\n",
                'group_separator'
            )
            self.output.insert(
                tk.END,
                f"📊 SUMMARY\n",
                'summary'
            )
            self.output.insert(
                tk.END,
                f"   Members: {total_members}\n",
                'member_name'
            )
            self.output.insert(
                tk.END,
                f"   Groups: {total_groups}\n",
                'member_name'
            )
            self.output.insert(
                tk.END,
                f"   Avg Group Size: {avg_size:.1f}\n",
                'member_name'
            )
            
            # Enable copy button
            self.copy_btn.config(state='normal')
            self.group_count.config(text=f"{total_groups} groups")
            
            # Update status
            self.set_status(f"Generated {total_groups} groups with {total_members} members")
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"✅ Generated {total_groups} groups!\n"
                f"👥 {total_members} members\n"
                f"📊 Average group size: {avg_size:.1f}"
            )
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            self.set_status("Error generating groups", True)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            self.set_status("Error generating groups", True)
    
    def copy_output(self):
        """Copy output to clipboard"""
        output_text = self.output.get("1.0", tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            self.set_status("Copied to clipboard")
            messagebox.showinfo("Success", "📋 Groups copied to clipboard!")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = GroupGeneratorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
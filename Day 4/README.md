# 🎯 Group Generator
A beautiful, modern desktop application for randomly grouping names into teams. Perfect for classrooms, workshops, hackathons, and any event where you need to randomly assign people to groups.

![Group Generator Pro](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![Tkinter](https://img.shields.io/badge/tkinter-GUI-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [How to Use](#-how-to-use)
- [UI Layout](#-ui-layout)
- [Customization](#-customization)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Features
- **Random Group Generation**: Automatically creates random groups from a list of names
- **Customizable Group Size**: Choose group size from 2 to 10 members
- **Shuffle Mode**: Randomize the order of names before grouping
- **Duplicate Removal**: Automatically remove duplicate names from the list
- **Beautiful UI**: Modern, clean interface with vibrant colors
- **Copy to Clipboard**: One-click copy of generated groups

### Visual Features
- **Dark Theme Output**: Groups displayed on dark background for better visibility
- **Color-Coded Output**: Different colors for headers, members, and summaries
- **Hover Effects**: Interactive buttons with smooth transitions
- **Real-time Statistics**: Live member count updates
- **Responsive Design**: Resizable window with 40/60 split layout

## 📸 Screenshots

### Main Interface
```
┌──────────────────────────────────────────────────────────────┐
│  🎯 Group Generator Pro    Random Team Group Maker    👥 0 │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────────────────────────┐  │
│  │ 📝 Enter Names│    │ 📋 Generated Groups    0 groups │  │
│  │              │    │ ┌─────────────────────────────┐ │  │
│  │ Alice Johnson│    │ │ 🎯 GROUP 1                  │ │  │
│  │ Bob Smith    │    │ │ ════════════════════════════ │ │  │
│  │ Charlie Brown│    │ │ ● Alice Johnson             │ │  │
│  │ Diana Prince │    │ │ ● Bob Smith                 │ │  │
│  │ ...          │    │ │ ● Charlie Brown             │ │  │
│  │              │    │ │                             │ │  │
│  │ Group Size: 3│    │ │ 🎯 GROUP 2                  │ │  │
│  │ ☑ Shuffle    │    │ │ ════════════════════════════ │ │  │
│  │ ☑ Remove Dup │    │ │ ● Diana Prince              │ │  │
│  │              │    │ │ ● Evan Wright               │ │  │
│  │ [Generate]   │    │ │                             │ │  │
│  │ [Clear]      │    │ │ 📊 SUMMARY                  │ │  │
│  └─────────────┘    │ │    Members: 26               │ │  │
│                     │ │    Groups: 9                 │ │  │
│                     │ │    Avg Size: 2.9             │ │  │
│                     │ └─────────────────────────────┘ │  │
│                     │    [📋 Copy]                    │  │
│                     └──────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│  ✅ Ready                              14:30:25            │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

### Step 1: Clone or Download
```bash
# Clone the repository
git clone https://github.com/yourusername/group-generator-pro.git

# Navigate to the directory
cd group-generator-pro
```

### Step 2: Save the File
Save the Python code as `randomGrouping.py` in your project directory.

### Step 3: Run the Application
```bash
python randomGrouping.py
```

### No Installation Required!
The application uses only Python's standard library, so no additional dependencies are needed!

## 🎮 Quick Start

1. **Launch the application**:
   ```bash
   python randomGrouping.py
   ```

2. **Add names**: Enter one name per line in the input box (sample data pre-loaded)

3. **Adjust settings**:
   - Choose group size (2-10 members)
   - Toggle shuffle mode
   - Toggle duplicate removal

4. **Generate groups**: Click the "🚀 Generate Groups" button

5. **Copy results**: Click "📋 Copy" to copy groups to clipboard

## 📖 How to Use

### Entering Names
```
Enter one name per line:
Alice Johnson
Bob Smith
Charlie Brown
Diana Prince
Evan Wright
```

### Adjusting Group Size
- Use the spinbox to select group size (2-10)
- Example: "Group Size: 3" creates groups of 3

### Options
- **🔀 Shuffle**: Randomizes the order of names before grouping
- **🚫 Remove Duplicates**: Automatically removes duplicate names

### Generating Groups
1. Click the "🚀 Generate Groups" button
2. Groups appear in the right panel with color coding:
   - 🎯 **GROUP X**: Red header
   - **● Member Name**: Green text with yellow bullets
   - **━ Separators**: Teal lines
   - **📊 SUMMARY**: Pink summary section

### Copying Results
- Click the "📋 Copy" button to copy all groups to clipboard
- Paste anywhere (Word, Excel, email, etc.)

## 🎨 UI Layout

### 40/60 Split Design
```
Left Panel (40%)          Right Panel (60%)
┌──────────────────┐      ┌────────────────────────────┐
│  Input Section   │      │  Output Section             │
│  - Names input   │      │  - Colored group display   │
│  - Group size    │      │  - Copy button             │
│  - Options       │      │  - Statistics              │
│  - Buttons       │      │                           │
└──────────────────┘      └────────────────────────────┘
```

### Color Scheme
- **Primary**: Purple (#6C63FF)
- **Secondary**: Pink (#FF6584)
- **Success**: Green (#2ECC71)
- **Warning**: Yellow (#F1C40F)
- **Danger**: Red (#E74C3C)
- **Dark Background**: Dark blue-gray (#1E1E2E)

### Output Colors
- **Group Headers**: Bright Red (#FF6B6B)
- **Separators**: Teal (#4ECDC4)
- **Member Names**: Light Green (#95E1D3)
- **Bullet Points**: Yellow (#FFE66D)
- **Summary**: Pink (#FF9FF3)

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Generate groups (when button focused) |
| `Ctrl+A` | Select all text in input/output |
| `Ctrl+C` | Copy text |
| `Ctrl+V` | Paste text |

## 🔧 Customization

### Changing Colors
Modify the `COLORS` dictionary in the code:
```python
COLORS = {
    'primary': '#6C63FF',      # Change to your preferred color
    'secondary': '#FF6584',    # Change to your preferred color
    # ... etc
}
```

### Changing Group Size Range
Modify the spinbox range:
```python
size_spinbox = tk.Spinbox(
    from_=2,      # Minimum group size
    to=10,        # Maximum group size
    # ...
)
```

### Changing Fonts
Modify the `FONTS` dictionary:
```python
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),  # Font name, size, style
    # ...
}
```

### Adding More Sample Data
Modify the `_add_sample_data()` method:
```python
sample_names = [
    "Your Name 1",
    "Your Name 2",
    # Add more names here
]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "No module named tkinter"
**Solution**: Install Tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# Tkinter comes pre-installed with Python
```

#### 2. Error: 'small_bold' KeyError
**Solution**: Make sure the FONTS dictionary includes 'small_bold':
```python
'small_bold': ('Segoe UI', 9, 'bold'),
```

#### 3. Application doesn't start
**Solution**: Check Python version
```bash
python --version
# Should be Python 3.6 or higher
```

#### 4. Groups not visible
**Solution**: The output has dark background with colored text. If not visible:
- Check your screen brightness
- The output area should show colored text on dark background

#### 5. Copy button not working
**Solution**: 
- Make sure groups are generated first
- Click "Generate Groups" to enable the copy button

### Log Files
The application displays status messages in the status bar. If an error occurs, check:
- The status bar for error messages
- The console/terminal for traceback

## 📝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes before submitting
- Update the README if needed

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2024 Group Generator Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Built with Python's Tkinter library
- Inspired by the need for quick random group generation
- UI design influenced by modern design principles

## 📞 Contact

For questions, issues, or suggestions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/group-generator-pro/issues)
- **Email**: your.email@example.com

---

## ⭐ Show Your Support

If you find this tool useful, please:
- ⭐ Star the repository
- 📢 Share with others
- 🐛 Report issues
- 💡 Suggest features

---

**Made with ❤️ using Python and Tkinter**
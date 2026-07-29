# 📂 File Organizer

A desktop application built with **Python** and **Tkinter** that automatically organizes files into folders based on their file extensions.

For example:

```text
Downloads/
│
├── PDF/
│   ├── report.pdf
│   └── assignment.pdf
│
├── JPG/
│   ├── image1.jpg
│   └── photo.jpg
│
├── MP4/
│   ├── video.mp4
│
└── PY/
    └── main.py
```

---

# Features

* 📁 Browse and select any folder.
* 👀 Preview files before organizing.
* 📊 Progress bar showing organization status.
* 📝 Activity log with timestamps.
* 📈 Displays:

  * Total files
  * Total folders
  * Number of file types
* 🛑 Stop organization at any time.
* ⚠ Automatically renames duplicate files.
* 🎨 Classic Windows-style graphical interface.

---

# Technologies Used

* Python 3
* Tkinter
* Threading
* OS Module
* Shutil

---

# Requirements

* Python 3.8+
* Tkinter (included with Python)

Check Tkinter installation:

```bash
python -m tkinter
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/file-organizer.git
```

Navigate into the project:

```bash
cd file-organizer
```

Run:

```bash
python main.py
```

---

# How It Works

1. Launch the application.
2. Click **Browse**.
3. Select a folder.
4. Click **Preview** to review files.
5. Click **Organize Files**.
6. Files are automatically moved into folders based on their extensions.

Example:

```
holiday.jpg
resume.pdf
movie.mp4
song.mp3
```

becomes

```
JPG/
PDF/
MP4/
MP3/
```

---

# Project Structure

```
FileOrganizer/
│
├── main.py
├── README.md
├── assets/
│   └── screenshots
└── LICENSE
```

---

# Future Improvements

* Drag-and-drop support
* Undo organization
* Dark mode
* File search
* File compression
* Duplicate finder
* Automatic scheduled organization
* Custom organization rules

---

# Author

Developed by **Caseay**

---

# License

MIT License

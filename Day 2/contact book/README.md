# 📒 Contact Book - Beautiful Tkinter UI

A modern desktop Contact Book application built with **Python** and **Tkinter**. The application provides a clean and intuitive graphical interface for storing, searching, editing, and organizing contacts. Contact information is saved locally using JSON, ensuring data persistence between sessions.

---

## ✨ Features

* Modern and responsive Tkinter GUI
* Add new contacts
* Edit existing contacts
* Delete contacts
* Real-time contact search
* Favorite contacts management
* Contact tagging system
* Notes for every contact
* Phone number formatting
* Email validation
* Automatic data persistence using JSON
* Contacts sorted alphabetically
* Clean Object-Oriented Programming (OOP) architecture

---

## 📂 Project Structure

```
ContactBook/
│
├── contact_book.py        # Main application
├── contacts.json          # Automatically created contact database
├── README.md              # Project documentation
└── assets/                # Optional icons and screenshots
```

---

## 🛠 Technologies Used

* Python 3.x
* Tkinter
* ttk Widgets
* JSON
* Object-Oriented Programming (OOP)

---

## 🏗 Architecture

The project follows a layered architecture:

### 1. Data Layer

Responsible for representing contact objects.

Class:

* Contact

Responsibilities:

* Contact information
* Data validation
* Phone formatting
* JSON serialization

---

### 2. Storage Layer

Class:

* StorageHandler

Responsibilities:

* Save contacts
* Load contacts
* Manage JSON storage

---

### 3. Service Layer

Class:

* ContactService

Responsibilities:

* Add contacts
* Update contacts
* Delete contacts
* Search contacts
* Favorite management
* Tag management

---

### 4. Presentation Layer

Class:

* ContactBookApp

Responsibilities:

* Display GUI
* Handle user interactions
* Update interface
* Connect UI with business logic

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/contact-book.git
```

Navigate into the project folder:

```bash
cd contact-book
```

---

## Install Python

Download Python from:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

or

```bash
python3 --version
```

---

## ▶ Running the Application

Run:

```bash
python contact_book.py
```

or

```bash
python3 contact_book.py
```

The Contact Book window will open automatically.

---

## 📋 How to Use

### Add a Contact

1. Click **Add Contact**
2. Fill in the required information
3. Click **Save Contact**

---

### Edit a Contact

1. Select a contact
2. Modify the information
3. Click **Save Changes**

---

### Delete a Contact

1. Select a contact
2. Click **Delete**
3. Confirm deletion

---

### Search

Use the search bar to find contacts by:

* Name
* Phone
* Email
* Company
* Job Title
* Address
* Tags

---

### Favorites

Click the star button to mark or remove a contact as a favorite.

Use the **Favorites** button to filter favorite contacts.

---

### Tags

Add tags such as:

```
friend
family
school
work
business
client
```

Right-click a tag to remove it.

---

## 💾 Data Storage

Contacts are automatically saved in a JSON file located in:

```
~/.contact_book/
```

No manual saving is required.

---

## 📸 Screenshots

You may include screenshots like:

```
assets/
├── home.png
├── add_contact.png
├── search.png
├── favorites.png
```

Example:

```markdown
![Home](assets/home.png)
```

---

## 🔒 Validation

The application validates:

* Required first name
* Required last name
* Required phone number
* Valid email format

This helps ensure accurate and consistent contact information.

---

## 📈 Future Improvements

Possible future enhancements include:

* SQLite database support
* MySQL/PostgreSQL integration
* User authentication
* Contact photos
* CSV import/export
* Excel export
* vCard support
* Dark mode
* Backup and restore
* Cloud synchronization
* Mobile application
* Birthday reminders

---

## 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

## 📜 License

This project is released under the MIT License.

---

## 👨‍💻 Author

**Caseay (Caseay Off)**

Software Developer | Python Developer | Django Developer | Desktop Application Developer

GitHub: https://github.com/Itz-Caseay

---

## ⭐ Acknowledgements

* Python Software Foundation
* Tkinter Development Team
* Open Source Community

---

If you found this project useful, consider giving it a ⭐ on GitHub.

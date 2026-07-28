# 🧮 Tkinter Calculator

A simple desktop calculator built with **Python** and **Tkinter** that performs basic arithmetic operations through a clean graphical user interface.

## Features

* Addition (+)
* Subtraction (-)
* Multiplication (×)
* Division (÷)
* Percentage (%)
* Positive/Negative toggle (+/-)
* Decimal number support
* Clear All (AC)
* Responsive button layout
* Centered application window

## Screenshot

> Add a screenshot of your calculator here.

```
+-------------------------+
|                     125 |
+-------------------------+
| AC | +/- |  % |  ÷      |
|  7 |  8  |  9 |  ×      |
|  4 |  5  |  6 |  -      |
|  1 |  2  |  3 |  +      |
|  0 |  .  |  √ |  =      |
+-------------------------+
```

## Requirements

* Python 3.8 or later
* Tkinter (included with most Python installations)

To verify Tkinter is installed:

```bash
python -m tkinter
```

If a small Tkinter window appears, it is installed correctly.

## Installation

1. Clone the repository.

```bash
git clone https://github.com/Itz-Caseay/Internship_on_python.git
```

2. Navigate into the project directory.

```bash
cd Internship_on_python
```

3. Run the application.

```bash
python calculator.py
```

## Project Structure

```
Internship_on_python/
│
├── calculator.py
├── README.md
└── screenshot.png
```

## How It Works

The calculator stores:

* **A** → First operand
* **Operator** → Selected arithmetic operator
* **B** → Second operand

When the **=** button is pressed:

1. The first number is converted to a float.
2. The second number is converted to a float.
3. The selected operation is performed.
4. The result is displayed.
5. The calculator state is reset for the next calculation.

## Color Scheme

| Component      | Color                |
| -------------- | -------------------- |
| Background     | Black (#1C1C1C)      |
| Number Buttons | Dark Gray (#505050)  |
| Operators      | Orange (#FF9500)     |
| Top Buttons    | Light Gray (#D4D4D2) |
| Display Text   | White                |

## Supported Operations

| Button | Description      |
| ------ | ---------------- |
| +      | Addition         |
| -      | Subtraction      |
| ×      | Multiplication   |
| ÷      | Division         |
| %      | Percentage       |
| +/-    | Change sign      |
| AC     | Clear calculator |
| .      | Decimal point    |
| =      | Calculate result |

## Known Limitations

* The √ (square root) button is present in the interface but has not yet been implemented.
* Division by zero is not currently handled and will raise an error.
* Only one operation can be performed at a time (no expression chaining such as `5 + 3 × 2`).

## Future Improvements

* Implement square root functionality.
* Handle division-by-zero gracefully.
* Add keyboard input support.
* Add calculation history.
* Support chained expressions.
* Improve UI responsiveness.
* Add scientific calculator functions.

## Technologies Used

* Python
* Tkinter

## Author

Developed by **Caseay**

## License

This project is open-source and available under the MIT License.

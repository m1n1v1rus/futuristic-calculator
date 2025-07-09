<p align="center">
  <img src="https://raw.githubusercontent.com/m1n1v1rus/futuristic-calculator/main/assets/banner.png" alt="Futuristic Calculator Banner" width="100%" />
</p>

# Futuristic Engineering Calculator 🧠

A modern, multi-functional calculator built with **PyQt5**, combining scientific calculations, voice interaction, graph plotting, unit conversions, keyboard shortcuts, and a dynamic UI inspired by real calculators and engineering tools.

---

## 🚀 Features

### 🧮 Scientific Calculator
- Handles basic and complex expressions
- Supports `sin`, `cos`, `tan`, `log`, `ln`, `√`, `π`, `e`, factorial, power, etc.
- Bracket auto-completion
- Error handling and expression validation
- Supports **keyboard input** and **shortcut keys**

### 📢 Voice Command Mode
- Real-time speech recognition for hands-free calculation
- Commands like:
  - "Graph mode"
  - "Unit converter"
  - "Dark mode"
  - "sin x plus 2 into x" → 🧠 gets parsed and evaluated

### 📈 Graph Plotting (2D & 3D)
- Enter expressions like `x**2`, `sin(x)`, or `x**2 + y**2`
- Toggle between 2D/3D mode automatically
- Features:
  - Color picker for each expression
  - Zoom/pan toolbar
  - Export graph as image
  - Animate variable (`a`) using a slider

### 🔁 Unit Converter
- Supports length, temperature, volume, mass, and more
- Converts between metric and imperial units
- Clean interface with instant updates

### 🌙 Theme Support
- Toggle between **Dark** and **Light** mode
- Full theming for calculator, graph, and converter views

### ⌨️ Keyboard Shortcuts
| Shortcut     | Action                  |
|--------------|--------------------------|
| `Ctrl + G`   | Open Graph Plotter       |
| `Ctrl + U`   | Open Unit Converter      |
| `Ctrl + D`   | Toggle Dark/Light Theme  |
| `Enter`      | Evaluate Expression      |
| `Esc`        | Clear Expression         |

---

## 📦 Tech Stack
- **Python 3.10+**
- **PyQt5** - UI framework
- **SymPy** - Expression parsing
- **Matplotlib** - Graph plotting
- **NumPy** - Array and math functions
- **SpeechRecognition** - Voice input

---

## 📸 Screenshots
> ## 📸 Screenshots

### 🧮 Scientific Calculator
<img src="https://raw.githubusercontent.com/m1n1v1rus/futuristic-calculator/main/assets/screenshots/calculator.png" width="700"/>

### 📈 Graph Plotter
<img src="https://raw.githubusercontent.com/m1n1v1rus/futuristic-calculator/main/assets/screenshots/graph_plotter.png" width="700"/>

### 🔁 Unit Converter
<img src="https://raw.githubusercontent.com/m1n1v1rus/futuristic-calculator/main/assets/screenshots/unit_converter.png" width="700"/>


---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
https://github.com/m1n1v1rus/futuristic-calculator.git

# 2. Move into project
cd futuristic-calculator

# 3. Create virtual environment (optional)
python -m venv .venv
source .venv/Scripts/activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the calculator
python main.py
```

---

## 👤 Author
**Ayush Mani**  
🔗 [GitHub: @m1n1v1rus](https://github.com/m1n1v1rus)

---

## 🌟 Star the repo if you like futuristic tools!

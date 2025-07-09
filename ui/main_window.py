from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QGridLayout, QShortcut
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from ui.themes import dark_theme, light_theme
from logic.solver import evaluate_expression
import math
import speech_recognition as sr
from ui.graph_view import GraphView
from ui.unit_converter import UnitConverterView


class CalculatorWindow(QWidget):
    def __init__(self, input_field=None):
        super().__init__()
        self.setWindowTitle("Advanced Calculator")
        self.setGeometry(100, 100, 400, 640)
        self.is_dark_mode = False
        self.expression = ""
        self.buttons = {}
        self.scientific_visible = False
        self.voice_mode_active = False
        self.external_input = input_field
        self.init_ui()
        self.setup_shortcuts()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setFont(QFont("Consolas", 14))
        self.layout.addWidget(self.display)

        self.result_label = QLabel("Result: ")
        self.result_label.setFont(QFont("Arial", 11))
        self.layout.addWidget(self.result_label)

        self.keypad_layout = QVBoxLayout()
        self.scientific_layout = QGridLayout()

        basic_buttons = [
            ['C', '(', ')', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '=']
        ]

        for row_idx, row in enumerate(basic_buttons):
            row_layout = QHBoxLayout()
            for col_idx, btn_text in enumerate(row):
                button = self.create_button(btn_text, row_idx, col_idx)
                row_layout.addWidget(button)
            self.keypad_layout.addLayout(row_layout)

        self.layout.addLayout(self.keypad_layout)

        scientific_buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('log', 0, 3),
            ('ln', 1, 0),  ('√', 1, 1),  ('^', 1, 2),   ('!', 1, 3),
            ('π', 2, 0),  ('e', 2, 1)
        ]
        for text, row, col in scientific_buttons:
            button = self.create_button(text, row, col, is_scientific=True)
            self.scientific_layout.addWidget(button, row, col)

        self.scientific_widget = QWidget()
        self.scientific_widget.setLayout(self.scientific_layout)
        self.scientific_widget.setVisible(False)
        self.layout.addWidget(self.scientific_widget)

        self.voice_toggle_btn = QPushButton("🎤 Start Voice Mode")
        self.voice_toggle_btn.clicked.connect(self.toggle_voice_mode)
        self.layout.addWidget(self.voice_toggle_btn)

        self.toggle_sci_btn = QPushButton("Show Scientific Mode")
        self.toggle_sci_btn.clicked.connect(self.toggle_scientific)
        self.layout.addWidget(self.toggle_sci_btn)

        self.theme_btn = QPushButton("Switch to Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_btn)

        self.apply_theme()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+G"), self, self.open_graph_plotter)
        QShortcut(QKeySequence("Ctrl+U"), self, self.open_unit_converter)
        QShortcut(QKeySequence("Ctrl+D"), self, self.toggle_theme)

    def open_graph_plotter(self):
        self.graph_view = GraphView()
        self.graph_view.show()

    def open_unit_converter(self):
        self.unit_view = UnitConverterView()
        self.unit_view.show()

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        allowed = "0123456789+-*/().^"
        functions = {
            's': 'math.sin(', 'c': 'math.cos(', 't': 'math.tan(',
            'l': 'math.log10(', 'n': 'math.log(', 'e': 'math.e', 'p': 'math.pi'
        }

        if text in allowed:
            self.expression += text
        elif key == Qt.Key_Backspace:
            self.expression = self.expression[:-1]
        elif key in (Qt.Key_Enter, Qt.Key_Return):
            safe_expr = self.format_expression(self.expression)
            result = evaluate_expression(safe_expr)
            self.result_label.setText(result)
            if self.external_input:
                self.external_input.setText(self.expression)
        elif key == Qt.Key_Escape:
            self.expression = ""
        elif text.lower() in functions:
            self.expression += functions[text.lower()]
        else:
            return

        self.display.setText(self.expression)
        self.validate_expression()

    def create_button(self, text, row, col, is_scientific=False):
        button = QPushButton(text)
        button.setFixedSize(70, 50)
        unique_key = f"{text}_{row}_{col}"
        self.buttons[unique_key] = button

        if text in ['+', '-', '×', '÷', '^']:
            bg_color = "#44bba4"
            text_color = "#fff"
        elif text in ['C', '⌫']:
            bg_color = "#e74c3c"
            text_color = "#fff"
        elif is_scientific:
            bg_color = "#3b3b98"
            text_color = "#fff"
        else:
            bg_color = "#dddddd" if not self.is_dark_mode else "#333333"
            text_color = "#000000" if not self.is_dark_mode else "#ffffff"

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #888;
            }}
            QPushButton:pressed {{
                background-color: #555;
            }}
        """)
        button.clicked.connect(lambda _, t=text, k=unique_key: self.animated_button_click(t, k))
        return button

    def animated_button_click(self, text, key):
        button = self.buttons.get(key)
        if button:
            original_style = button.styleSheet()
            button.setStyleSheet(original_style + "background-color: #888;")
            QTimer.singleShot(150, lambda: button.setStyleSheet(original_style))
        self.on_button_click(text)

    def on_button_click(self, button_text):
        if button_text == 'C':
            self.expression = ""
        elif button_text == '⌫':
            self.expression = self.expression[:-1]
        elif button_text == '=':
            while self.expression.count('(') > self.expression.count(')'):
                self.expression += ')'
            safe_expr = self.format_expression(self.expression)
            result = evaluate_expression(safe_expr)
            self.result_label.setText(result)
            if self.external_input:
                self.external_input.setText(self.expression)
        elif button_text == ')':
            if self.expression.count('(') > self.expression.count(')'):
                self.expression += button_text
        elif button_text == '^':
            self.expression += '**'
        elif button_text == '√':
            self.expression += 'math.sqrt('
        elif button_text == 'log':
            self.expression += 'math.log10('
        elif button_text == 'ln':
            self.expression += 'math.log('
        elif button_text == '!':
            self.expression += 'math.factorial('
        elif button_text == 'π':
            self.expression += 'math.pi'
        elif button_text == 'e':
            self.expression += 'math.e'
        elif button_text in ['sin', 'cos', 'tan']:
            self.expression += f"math.{button_text}("
        else:
            if self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ')') and button_text == '(':
                self.expression += '*' + button_text
            else:
                self.expression += button_text

        self.display.setText(self.expression)
        self.validate_expression()

    def format_expression(self, expr):
        formatted = ""
        prev = ""
        for ch in expr:
            if (ch == '(' and prev.isdigit()) or (prev == ')' and ch.isdigit()) or (prev == ')' and ch == '('):
                formatted += '*' + ch
            else:
                formatted += ch
            prev = ch
        return formatted.replace('×', '*').replace('÷', '/')

    def validate_expression(self):
        try:
            expr = self.format_expression(self.expression)
            compile(expr, "<string>", "eval")
            self.display.setStyleSheet("color: black; background-color: white;" if not self.is_dark_mode else "color: white; background-color: #222222;")
        except:
            self.display.setStyleSheet("color: red; background-color: #fff;" if not self.is_dark_mode else "color: red; background-color: #222;")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(dark_theme)
            self.display.setStyleSheet("color: white; background-color: #222222;")
            self.result_label.setStyleSheet("color: white;")
            self.theme_btn.setText("Switch to Light Mode")
        else:
            self.setStyleSheet(light_theme)
            self.display.setStyleSheet("color: black; background-color: white;")
            self.result_label.setStyleSheet("color: black;")
            self.theme_btn.setText("Switch to Dark Mode")

    def toggle_scientific(self):
        self.scientific_visible = not self.scientific_visible
        self.scientific_widget.setVisible(self.scientific_visible)
        self.toggle_sci_btn.setText("Hide Scientific Mode" if self.scientific_visible else "Show Scientific Mode")

    def voice_to_expression(self, voice_text):
        voice_text = voice_text.lower()
        replacements = {
            "x": "*", "times": "*", "into": "*", "plus": "+", "minus": "-",
            "divide": "/", "mod": "%", "power": "**",
            "open bracket": "(", "close bracket": ")"
        }
        for word, symbol in replacements.items():
            voice_text = voice_text.replace(word, symbol)
        return voice_text

    def voice_input(self):
        if not self.voice_mode_active:
            return

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.result_label.setText("Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                self.result_label.setText("Recognized: " + command)

                if "stop voice" in command:
                    self.voice_mode_active = False
                    self.voice_toggle_btn.setText("🎤 Start Voice Mode")
                    return
                elif "scientific" in command:
                    self.toggle_scientific()
                elif "graph" in command:
                    self.open_graph_plotter()
                elif "unit" in command:
                    self.open_unit_converter()
                elif "dark mode" in command:
                    if not self.is_dark_mode:
                        self.toggle_theme()
                elif "light mode" in command:
                    if self.is_dark_mode:
                        self.toggle_theme()
                else:
                    self.expression = self.voice_to_expression(command)
                    self.display.setText(self.expression)
                    result = evaluate_expression(self.format_expression(self.expression))
                    self.result_label.setText("Result: " + result)

        except sr.UnknownValueError:
            self.result_label.setText("Could not understand audio")
        except sr.RequestError:
            self.result_label.setText("Speech service unavailable")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

        if self.voice_mode_active:
            QTimer.singleShot(1000, self.voice_input)

    def toggle_voice_mode(self):
        self.voice_mode_active = not self.voice_mode_active
        if self.voice_mode_active:
            self.voice_toggle_btn.setText("🛑 Stop Voice Mode")
            self.voice_input()
        else:
            self.voice_toggle_btn.setText("🎤 Start Voice Mode")
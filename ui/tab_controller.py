from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QLabel, QLineEdit, QShortcut
)
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtCore import Qt

from ui.main_window import CalculatorWindow
from ui.graph_view import GraphView
from ui.unit_converter import UnitConverterView  # ✅ FIXED: Correct class name

import sys


class AdvancedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Futuristic Engineering Calculator")
        self.setGeometry(100, 100, 960, 720)
        self.setMinimumSize(800, 600)
        self.is_dark_mode = False

        main_layout = QVBoxLayout()

        # Top Theme Toggle
        top_bar = QHBoxLayout()
        self.theme_btn = QPushButton("🌙 Switch to Dark Mode")
        self.theme_btn.setFixedHeight(35)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_bar.addStretch()
        top_bar.addWidget(self.theme_btn)
        main_layout.addLayout(top_bar)

        # Input bar with evaluate button
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter expression (e.g., sin(x), log(10), x^2)")
        self.input_field.setClearButtonEnabled(True)
        self.input_field.setFont(QFont("Consolas", 12))
        self.input_field.setStyleSheet("padding: 6px;")

        self.eval_button = QPushButton("Evaluate")
        self.eval_button.setFixedHeight(32)
        self.eval_button.clicked.connect(self.evaluate_input_expression)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.eval_button)
        main_layout.addLayout(input_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px 20px;
                border-radius: 8px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #44bba4;
                color: white;
            }
            QTabBar::tab:hover {
                background: #a1ded7;
            }
        """)

        # Child tabs
        self.calculator_tab = CalculatorWindow(self.input_field)
        self.graph_tab = GraphView()
        self.unit_tab = UnitConverterView()

        self.tabs.addTab(self.calculator_tab, QIcon(), "🧮 Calculator")
        self.tabs.addTab(self.graph_tab, QIcon(), "📈 Graph Plotter")
        self.tabs.addTab(self.unit_tab, QIcon(), "🔁 Unit Converter")

        main_layout.addWidget(self.tabs)

        # Quick Math Shortcuts
        quick_math_layout = QHBoxLayout()
        quick_math_label = QLabel("Quick Functions:")
        quick_math_label.setFont(QFont("Arial", 10))
        quick_math_layout.addWidget(quick_math_label)

        function_map = {
            "sin(x)": "sin(x)",
            "cos(x)": "cos(x)",
            "tan(x)": "tan(x)",
            "log(x)": "log(x)",
            "sqrt(x)": "sqrt(x)",
            "exp(x)": "exp(x)",
            "x^2": "x**2",
            "1/x": "1/x"
        }

        for label, func in function_map.items():
            btn = QPushButton(label)
            btn.setFixedSize(80, 30)
            btn.clicked.connect(lambda _, f=func: self.insert_function(f))
            quick_math_layout.addWidget(btn)

        main_layout.addLayout(quick_math_layout)

        self.setLayout(main_layout)
        self.apply_theme()

        # Keyboard shortcut for Enter = evaluate
        QShortcut(QKeySequence(Qt.Key_Return), self, self.evaluate_input_expression)
        QShortcut(QKeySequence(Qt.Key_Enter), self, self.evaluate_input_expression)

    def insert_function(self, func_text):
        try:
            self.input_field.insert(func_text)
        except Exception as e:
            print("[Insert Error]:", e)

    def evaluate_input_expression(self):
        expr = self.input_field.text().strip()
        if expr:
            self.input_field.setText(expr)
            self.tabs.setCurrentIndex(0)
            if hasattr(self.calculator_tab, 'evaluate_expression'):
                self.calculator_tab.evaluate_expression()
            else:
                print("[Error] Calculator does not support evaluate_expression()")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2c2c2c;
                    color: white;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QLineEdit {
                    background-color: #3c3c3c;
                    color: white;
                    border: 1px solid #777;
                }
            """)
            self.theme_btn.setText("☀️ Switch to Light Mode")
        else:
            self.setStyleSheet("")
            self.theme_btn.setText("🌙 Switch to Dark Mode")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AdvancedCalculator()
    win.show()
    sys.exit(app.exec_())


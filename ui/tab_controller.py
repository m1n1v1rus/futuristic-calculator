from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from ui.main_window import CalculatorWindow
from ui.graph_view import GraphView
from ui.unit_converter import UnitConverterView


class AdvancedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Futuristic Engineering Calculator")
        self.setGeometry(100, 100, 640, 700)
        self.setMinimumSize(600, 600)

        main_layout = QVBoxLayout()

        # Theme toggle button
        top_bar = QHBoxLayout()
        self.theme_btn = QPushButton("🌙 Switch to Dark Mode")
        self.theme_btn.setFixedHeight(35)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_bar.addStretch()
        top_bar.addWidget(self.theme_btn)
        main_layout.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)

        # Add custom style (optional)
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

        # Tabs content
        self.calculator_tab = CalculatorWindow()
        self.graph_tab = GraphView()
        self.unit_tab = UnitConverterView()

        # Add tabs
        self.tabs.addTab(self.calculator_tab, QIcon(), "🧮 Calculator")
        self.tabs.addTab(self.graph_tab, QIcon(), "📈 Graph Plotter")
        self.tabs.addTab(self.unit_tab, QIcon(), "🔁 Unit Converter")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.is_dark_mode = False
        self.apply_theme()

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
            """)
            self.theme_btn.setText("☀️ Switch to Light Mode")
        else:
            self.setStyleSheet("")
            self.theme_btn.setText("🌙 Switch to Dark Mode")


# Test only this file
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = AdvancedCalculator()
    win.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QFileDialog, QColorDialog, QHBoxLayout, QSlider, QTextEdit, QApplication
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import math


class GraphView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Plotter")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_label = QLabel("Enter expression (use x or x,y):")
        self.layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., sin(x), x**2, x**2 + y**2")
        self.layout.addWidget(self.input_field)

        paste_layout = QHBoxLayout()
        self.paste_btn = QPushButton("Paste Expression")
        self.paste_btn.clicked.connect(self.paste_expression)
        paste_layout.addWidget(self.paste_btn)
        self.layout.addLayout(paste_layout)

        self.add_expr_btn = QPushButton("Add Expression")
        self.add_expr_btn.clicked.connect(self.add_expression)
        self.layout.addWidget(self.add_expr_btn)

        self.color_btn = QPushButton("Choose Curve Color")
        self.color_btn.clicked.connect(self.choose_color)
        self.layout.addWidget(self.color_btn)

        self.plot_btn = QPushButton("Plot")
        self.plot_btn.clicked.connect(self.plot_graphs)
        self.layout.addWidget(self.plot_btn)

        self.export_btn = QPushButton("Export Graph as Image")
        self.export_btn.clicked.connect(self.export_graph)
        self.layout.addWidget(self.export_btn)

        self.slider_label = QLabel("Animation Slider:")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.animate_plot)
        self.layout.addWidget(self.slider_label)
        self.layout.addWidget(self.slider)

        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.layout.addWidget(self.canvas)

        self.expressions = []
        self.colors = []
        self.current_color = 'blue'

    def paste_expression(self):
        try:
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            self.input_field.setText(text)
        except Exception as e:
            print(f"Clipboard paste failed: {e}")

    def sanitize_expression(self, expr):
        replacements = {
            '^': '**',
            'π': 'pi',
            'e': 'E'
        }
        for key, val in replacements.items():
            expr = expr.replace(key, val)
        return expr

    def add_expression(self):
        expr = self.input_field.text().strip()
        if expr and not any(ch in expr for ch in ['import', '__', ';']):
            expr = self.sanitize_expression(expr)
            self.expressions = [expr]  # Overwrite to avoid stacking
            self.colors = [self.current_color]
            self.input_field.clear()
            self.plot_graphs()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color.name()

    def plot_graphs(self):
        input_expr = self.input_field.text().strip()
        if input_expr:
            if not any(ch in input_expr for ch in ['import', '__', ';']):
                self.expressions = [input_expr]
                self.colors = [self.current_color]
                self.input_field.clear()

        if not self.expressions:
            self.ax.clear()
            self.ax.set_title("❌ No expression to plot!", fontsize=10, color='red')
            self.canvas.draw()
            return

        self.canvas.figure.clf()

        try:
            is_3d = any('y' in expr for expr in self.expressions)
            self.ax = self.canvas.figure.add_subplot(111, projection='3d' if is_3d else None)
        except Exception as e:
            print(f"Error initializing canvas: {e}")
            self.ax = self.canvas.figure.add_subplot(111)

        x = sp.Symbol('x')
        y = sp.Symbol('y')
        a = self.slider.value() / 10.0
        x_vals = np.linspace(-10, 10, 500)
        y_vals = np.linspace(-10, 10, 500)
        X, Y = np.meshgrid(x_vals, y_vals)

        has_labels = False

        for expr, color in zip(self.expressions, self.colors):
            try:
                expr = expr.replace("^", "**").replace("π", "pi").replace("e", "E").replace("a", str(a))
                parsed = sp.sympify(expr)

                if 'y' in expr:
                    func = sp.lambdify((x, y), parsed, modules=["numpy"])
                    Z = func(X, Y)
                    if np.isnan(Z).all() or np.isinf(Z).all():
                        raise ValueError("NaN or Inf in Z values")
                    self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidth=0.2, alpha=0.9)
                else:
                    func = sp.lambdify(x, parsed, modules=["numpy"])
                    y_vals_plot = func(x_vals)
                    if np.isnan(y_vals_plot).all() or np.isinf(y_vals_plot).all():
                        raise ValueError("NaN or Inf in y values")
                    self.ax.plot(x_vals, y_vals_plot, color=color, label=expr, linewidth=2.2)
                    self.ax.axhline(0, color='gray', linewidth=0.8)
                    self.ax.axvline(0, color='gray', linewidth=0.8)
                    self.ax.grid(True, which='both', linestyle='--', alpha=0.3)
                    has_labels = True

            except Exception as e:
                print(f"❌ Failed to plot: {expr} | {e}")
                self.ax.set_title(f"❌ Error in expression:\n{expr}\n{e}", fontsize=9, color='red')

        self.ax.set_title("📉 Graph Output", fontsize=11)
        self.ax.set_xlabel("x", fontsize=10)
        if is_3d:
            self.ax.set_ylabel("y", fontsize=10)
            self.ax.set_zlabel("z", fontsize=10)
        else:
            self.ax.set_ylabel("y", fontsize=10)

        if has_labels:
            self.ax.legend()

        self.canvas.draw()

    def animate_plot(self):
        self.plot_graphs()

    def export_graph(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "graph.png", "PNG Files (*.png)")
        if path:
            self.canvas.figure.savefig(path)

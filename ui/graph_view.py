from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
    QFileDialog, QColorDialog, QHBoxLayout, QSlider
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


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
        self.use_3d = False

    def add_expression(self):
        expr = self.input_field.text()
        if expr:
            self.expressions.append(expr)
            self.colors.append(self.current_color)
            self.input_field.clear()
            self.plot_graphs()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color.name()

    def plot_graphs(self):
        self.canvas.figure.clf()
        is_3d = any('y' in expr for expr in self.expressions)
        self.ax = self.canvas.figure.add_subplot(111, projection='3d' if is_3d else None)

        x = sp.Symbol('x')
        y = sp.Symbol('y')
        a = self.slider.value() / 10.0
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)

        for expr, color in zip(self.expressions, self.colors):
            try:
                parsed = sp.sympify(expr.replace("a", str(a)))
                if 'y' in expr:
                    func = sp.lambdify((x, y), parsed, modules='numpy')
                    Z = func(X, Y)
                    self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.7)
                else:
                    func = sp.lambdify(x, parsed, modules='numpy')
                    y_vals = func(x_vals)
                    self.ax.plot(x_vals, y_vals, color=color, label=expr)
            except Exception as e:
                print(f"Error plotting '{expr}': {e}")

        self.ax.legend()
        self.canvas.draw()

    def animate_plot(self):
        self.plot_graphs()

    def export_graph(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "graph.png", "PNG Files (*.png)")
        if path:
            self.canvas.figure.savefig(path)

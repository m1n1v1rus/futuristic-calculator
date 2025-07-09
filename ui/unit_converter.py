from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class UnitConverterView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔁 Unit Converter")
        self.setMinimumSize(420, 280)
        self.setFont(QFont("Arial", 10))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value")
        self.input_field.setToolTip("Enter a numeric value to convert")
        self.input_field.setFixedHeight(35)
        layout.addWidget(self.input_field)

        # Category Dropdown
        self.category_box = QComboBox()
        self.units = {
            "Length": ["cm", "m", "inch", "ft"],
            "Temperature": ["C", "F", "K"],
            "Weight": ["kg", "g", "lb"]
        }
        self.category_box.addItems(self.units.keys())
        self.category_box.currentTextChanged.connect(self.update_units)
        layout.addWidget(self.category_box)

        # From/To Unit Selection
        unit_layout = QHBoxLayout()
        self.from_unit = QComboBox()
        self.to_unit = QComboBox()
        self.from_unit.setToolTip("Convert from unit")
        self.to_unit.setToolTip("Convert to unit")
        unit_layout.addWidget(self.from_unit)
        unit_layout.addWidget(QLabel("→"))
        unit_layout.addWidget(self.to_unit)
        layout.addLayout(unit_layout)

        # Convert Button
        convert_btn = QPushButton("Convert")
        convert_btn.setFixedHeight(35)
        convert_btn.clicked.connect(self.convert_units)
        layout.addWidget(convert_btn)

        # Result Label
        self.result_label = QLabel("Result: ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.update_units(self.category_box.currentText())

    def update_units(self, category):
        self.from_unit.clear()
        self.to_unit.clear()
        self.from_unit.addItems(self.units[category])
        self.to_unit.addItems(self.units[category])

    def convert_units(self):
        try:
            value_text = self.input_field.text().strip()
            if not value_text:
                self.result_label.setText("Please enter a value.")
                return

            value = float(value_text)
            from_u = self.from_unit.currentText()
            to_u = self.to_unit.currentText()
            category = self.category_box.currentText()

            if category == "Length":
                result = self.convert_length(value, from_u, to_u)
            elif category == "Temperature":
                result = self.convert_temperature(value, from_u, to_u)
            elif category == "Weight":
                result = self.convert_weight(value, from_u, to_u)
            else:
                self.result_label.setText("Invalid category.")
                return

            self.result_label.setText(f"Result: {result} {to_u}")

        except ValueError:
            self.result_label.setText("Invalid input. Enter a number.")

    def convert_length(self, value, from_u, to_u):
        conversions = {
            "cm": 0.01,
            "m": 1.0,
            "inch": 0.0254,
            "ft": 0.3048
        }
        meters = value * conversions[from_u]
        return round(meters / conversions[to_u], 4)

    def convert_temperature(self, value, from_u, to_u):
        if from_u == to_u:
            return round(value, 2)

        # Convert to Celsius
        if from_u == "C":
            temp_c = value
        elif from_u == "F":
            temp_c = (value - 32) * 5 / 9
        elif from_u == "K":
            temp_c = value - 273.15
        else:
            return "Unsupported unit"

        # Convert from Celsius to target
        if to_u == "C":
            return round(temp_c, 2)
        elif to_u == "F":
            return round((temp_c * 9 / 5) + 32, 2)
        elif to_u == "K":
            return round(temp_c + 273.15, 2)

    def convert_weight(self, value, from_u, to_u):
        conversions = {
            "kg": 1.0,
            "g": 0.001,
            "lb": 0.453592
        }
        kg = value * conversions[from_u]
        return round(kg / conversions[to_u], 4)


# Testing standalone
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = UnitConverterView()
    win.show()
    sys.exit(app.exec_())

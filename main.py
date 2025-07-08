from PyQt5.QtWidgets import QApplication
from ui.tab_controller import AdvancedCalculator
import sys

app = QApplication(sys.argv)
window = AdvancedCalculator()
window.show()
sys.exit(app.exec_())

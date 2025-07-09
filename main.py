# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.tab_controller import AdvancedCalculator


def main():
    """
    Entry point for the Futuristic Calculator application.
    Sets up the Qt application, loads the AdvancedCalculator UI,
    and starts the event loop.
    """
    app = QApplication(sys.argv)

    # App metadata (good for settings, themes, etc.)
    app.setApplicationName("Futuristic Calculator")
    app.setOrganizationName("AyushTech")

    try:
        window = AdvancedCalculator()
        window.setWindowTitle("🧠 Futuristic Calculator")
        window.resize(1000, 700)  # Optimal for modern screens
        window.show()
    except Exception as e:
        print(f"[ERROR] Failed to launch UI: {e}")
        sys.exit(1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



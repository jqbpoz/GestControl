import sys
from PyQt6.QtWidgets import QApplication
from gui import HandVolumeControlApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandVolumeControlApp()
    window.show()
    sys.exit(app.exec())

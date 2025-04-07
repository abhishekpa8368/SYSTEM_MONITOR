from PyQt6.QtWidgets import QApplication
from gui import SystemMonitorApp

if __name__ == "__main__":
    app = QApplication([])
    window = SystemMonitorApp()
    window.show()
    app.exec()

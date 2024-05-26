from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #dd9671;")
        self.setWindowTitle('Modern School Education')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(600, 300, 600, 600)

        self.label = QLabel("Hello from main.py!", self)
        self.label.setGeometry(175, 200, 250, 40)
        self.label.setAlignment(Qt.AlignCenter)

        self.show()


def run_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

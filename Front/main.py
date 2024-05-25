from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import random

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #dd9671;")
        self.setWindowTitle('Modern School Education')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(600, 300, 600, 600)

        self.l1 = QLabel("", self)
        self.l1.setGeometry(175, 200, 250, 40)
        self.l1.setAlignment(Qt.AlignCenter)

        self.show()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())

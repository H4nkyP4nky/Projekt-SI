import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QLabel,
)
from PyQt5.QtGui import QPixmap
import sqlite3


class TabelaObecnosci(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Obecność pracowników w pracy')
        self.setStyleSheet("background-color: lightblue;")  # Ustawienie tła na jasnoniebieskie
        self.resize(400, 300)

        # Połączenie z bazą danych SQLite
        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()

        # Pobranie danych pracowników z bazy danych
        cur.execute('SELECT name, position FROM pracownicy')
        pracownicy = cur.fetchall()

        # Tworzenie i konfiguracja tabeli do wyświetlenia danych
        table = QTableWidget(len(pracownicy), 3)  # Liczba kolumn: Imię, Stanowisko, Obecność
        table.setHorizontalHeaderLabels(['Imię', 'Stanowisko', 'Obecność'])

        # Wypełnienie tabeli danymi pracowników i obecnością jako 0
        for row, pracownik in enumerate(pracownicy):
            name, position = pracownik
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(position))
            table.setItem(row, 2, QTableWidgetItem('0'))  # Obecność jako 0

        # Stylizacja tabeli
        table.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                border: 2px solid #001F3F; /* ciemnoniebieska ramka */
                border-radius: 10px; /* zaokrąglone rogi */
            }
            QTableWidgetItem {
                color: #336274; /* kolor tekstu */
                font-weight: bold; /* pogrubiona czcionka */
            }
            """
        )

        # Układ interfejsu użytkownika
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


class SprawdzObecnosc(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Przycisk do sprawdzania obecności pracowników
        self.btn_sprawdz_obecnosc = QPushButton('Sprawdź obecność w pracy')
        self.btn_sprawdz_obecnosc.clicked.connect(self.sprawdzObecnosc)

        # Stylizacja przycisku
        self.btn_sprawdz_obecnosc.setStyleSheet(
            """
            QPushButton {
                background-color: #336274; /* ciemnoniebieskie tło */
                color: white; /* biały tekst */
                border: 2px solid #001F3F; /* ciemnoniebieska ramka */
                border-radius: 10px; /* zaokrąglone rogi */
                padding: 10px 20px; /* większy padding */
                font-size: 16px; /* większa czcionka */
                font-weight: bold; /* pogrubiona czcionka */
                box-shadow: 3px 3px 5px grey; /* cień dookoła */
            }
            """
        )

        # Układ interfejsu użytkownika
        layout = QVBoxLayout()
        layout.addWidget(self.btn_sprawdz_obecnosc)
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Wyśrodkowanie przycisku
        self.setStyleSheet("background-color: lightblue;")  # Ustawienie tła na jasnoniebieskie
        self.setLayout(layout)

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap('../UI_designs/logo.png')
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)  # Wyśrodkowanie logo
        logo_label.setScaledContents(True)  # Skalowanie logo
        layout.addWidget(logo_label)


    def sprawdzObecnosc(self):
        # Utworzenie i wyświetlenie okna z tabelą obecności
        dialog = TabelaObecnosci(self)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SprawdzObecnosc()
    window.setWindowTitle('Sprawdzanie Obecności')
    window.show()
    sys.exit(app.exec_())

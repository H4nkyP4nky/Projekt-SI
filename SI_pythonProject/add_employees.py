import sqlite3
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QLabel,
    QLineEdit,
)
from PyQt5.QtGui import QPixmap, QFont


class DodajPracownika(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap('../UI_designs/logo.png')
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)  # Wyśrodkowanie logo
        logo_label.setScaledContents(True)  # Skalowanie logo

        # Przycisk do dodawania pracownika
        self.btn_dodaj_pracownika = QPushButton('Dodaj pracownika')
        self.btn_dodaj_pracownika.clicked.connect(self.dodajPracownika)
        self.btn_dodaj_pracownika.setStyleSheet(
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
                min-width: 150px; /* minimalna szerokość */
                max-width: 450px;
            }
            """
        )

        # Układ interfejsu użytkownika
        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(self.btn_dodaj_pracownika)
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Wyśrodkowanie przycisku
        self.setLayout(layout)
        self.setWindowTitle('Dodawanie Pracowników')
        self.setStyleSheet("background-color: lightblue;")  # Ustawienie tła na jasnoniebieskie

    def dodajPracownika(self):
        # Okno dialogowe do dodawania pracownika
        dialog = QDialog(self)
        dialog.setWindowTitle('Dodaj pracownika')
        dialog.setStyleSheet(
            """
            QDialog {
                background-color: lightblue; /* tło */
                border-radius: 10px; /* zaokrąglone rogi */
            }
            QLabel {
                font-weight: bold; /* pogrubiona czcionka */
            }
            """
        )

        layout = QVBoxLayout()

        name_label = QLabel('Imię i nazwisko:')
        name_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        name_label.setStyleSheet("color: #336274;")  # Zmiana koloru czcionki
        self.name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        position_label = QLabel('Stanowisko:')
        position_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        position_label.setStyleSheet("color: #336274;")  # Zmiana koloru czcionki
        self.position_input = QLineEdit()
        layout.addWidget(position_label)
        layout.addWidget(self.position_input)

        salary_label = QLabel('Wynagrodzenie:')
        salary_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        salary_label.setStyleSheet("color: #336274;")  # Zmiana koloru czcionki
        self.salary_input = QLineEdit()
        layout.addWidget(salary_label)
        layout.addWidget(self.salary_input)

        email_label = QLabel('Email:')
        email_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        email_label.setStyleSheet("color: #336274;")  # Zmiana koloru czcionki
        self.email_input = QLineEdit()
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        phone_number_label = QLabel('Numer telefonu:')
        phone_number_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        phone_number_label.setStyleSheet("color: #336274;")  # Zmiana koloru czcionki
        self.phone_number_input = QLineEdit()
        layout.addWidget(phone_number_label)
        layout.addWidget(self.phone_number_input)

        hire_date_label = QLabel('Data zatrudnienia:')
        hire_date_label.setFont(QFont('Arial', 12))  # Ustawienie większej i pogrubionej czcionki
        hire_date_label.setStyleSheet("color: #336274;")
        self.hire_date_input = QLineEdit()
        layout.addWidget(hire_date_label)
        layout.addWidget(self.hire_date_input)

        btn_dodaj = QPushButton('Dodaj')
        btn_dodaj.setStyleSheet(
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
        btn_dodaj.clicked.connect(self.zapiszPracownika)
        layout.addWidget(btn_dodaj)

        dialog.setLayout(layout)
        dialog.exec_()

        # Po zamknięciu okna dialogowego wyświetl komunikat w terminalu
        print("Pracownik dodany poprawnie.")

    def zapiszPracownika(self):
        name = self.name_input.text()
        position = self.position_input.text()
        salary = self.salary_input.text()
        email = self.email_input.text()
        phone_number = self.phone_number_input.text()
        hire_date = self.hire_date_input.text()

        # Połączenie z bazą danych SQLite
        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()

        # Dodanie danych nowego pracownika do bazy danych
        cur.execute('''
            INSERT INTO pracownicy (name, position, salary, email, phone_number, hire_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, position, salary, email, phone_number, hire_date))

        # Zatwierdzenie zmian w bazie danych
        conn.commit()
        conn.close()  # Zamknięcie połączenia

        print("Pracownik dodany do bazy danych.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DodajPracownika()
    window.setGeometry(100, 100, 500, 500)  # Ustawienie większego rozmiaru okna
    window.show()
    sys.exit(app.exec_())
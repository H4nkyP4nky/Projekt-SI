import sqlite3
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QLabel,
    QLineEdit,
)
from PyQt5.QtGui import QFont

class DisplayEmployees(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Table to display employees
        self.table = QTableWidget()
        self.table.setColumnCount(8)  # 8 columns now: 7 for data + 1 for the "Edytuj" button
        self.table.setHorizontalHeaderLabels(
            ["ID", "Imię i nazwisko", "Stanowisko", "Wynagrodzenie", "Email", "Numer telefonu", "Data zatrudnienia", ""] # Empty header for the button column
        )
        layout.addWidget(self.table)

        # Button to refresh the table
        refresh_button = QPushButton("Odśwież tabelę")
        refresh_button.clicked.connect(self.load_data)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.setWindowTitle("Lista pracowników")
        self.setStyleSheet("background-color: lightblue;")
        self.load_data()  # Load data initially

    def load_data(self):
        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pracownicy")
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

            # Edit button for each row
            edit_button = QPushButton("Edytuj")
            edit_button.clicked.connect(lambda _, row_id=row[0]: self.edit_employee(row_id))
            self.table.setCellWidget(i, 7, edit_button)

    def edit_employee(self, row_id):
        # Fetch the employee's data from the database
        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pracownicy WHERE id=?", (row_id,))
        employee_data = cur.fetchone()
        conn.close()

        # Dialog for editing employee data
        dialog = QDialog(self)
        dialog.setWindowTitle('Edytuj pracownika')
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

        # Input fields (pre-filled with existing data)
        name_label = QLabel('Imię i nazwisko:')
        name_label.setFont(QFont('Arial', 12))
        name_label.setStyleSheet("color: #336274;")
        self.name_input = QLineEdit(employee_data[1])
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        position_label = QLabel('Stanowisko:')
        position_label.setFont(QFont('Arial', 12))
        position_label.setStyleSheet("color: #336274;")
        self.position_input = QLineEdit(employee_data[2])
        layout.addWidget(position_label)
        layout.addWidget(self.position_input)

        salary_label = QLabel('Wynagrodzenie:')
        salary_label.setFont(QFont('Arial', 12))
        salary_label.setStyleSheet("color: #336274;")
        self.salary_input = QLineEdit(str(employee_data[3]))  # Salary might be a number, so convert to string
        layout.addWidget(salary_label)
        layout.addWidget(self.salary_input)

        email_label = QLabel('Email:')
        email_label.setFont(QFont('Arial', 12))
        email_label.setStyleSheet("color: #336274;")
        self.email_input = QLineEdit(employee_data[4])
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        phone_number_label = QLabel('Numer telefonu:')
        phone_number_label.setFont(QFont('Arial', 12))
        phone_number_label.setStyleSheet("color: #336274;")
        self.phone_number_input = QLineEdit(employee_data[5])
        layout.addWidget(phone_number_label)
        layout.addWidget(self.phone_number_input)

        hire_date_label = QLabel('Data zatrudnienia:')
        hire_date_label.setFont(QFont('Arial', 12))
        hire_date_label.setStyleSheet("color: #336274;")
        self.hire_date_input = QLineEdit(employee_data[6])
        layout.addWidget(hire_date_label)
        layout.addWidget(self.hire_date_input)

        # Save button
        btn_zapisz = QPushButton('Zapisz zmiany')
        btn_zapisz.setStyleSheet(
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
        btn_zapisz.clicked.connect(lambda: self.zapiszZmianyPracownika(row_id))
        layout.addWidget(btn_zapisz)

        dialog.setLayout(layout)
        dialog.exec_()

    def zapiszZmianyPracownika(self, row_id):
        name = self.name_input.text()
        position = self.position_input.text()
        salary = self.salary_input.text()
        email = self.email_input.text()
        phone_number = self.phone_number_input.text()
        hire_date = self.hire_date_input.text()

        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()

        # Update the employee's data in the database
        cur.execute('''
            UPDATE pracownicy
            SET name=?, position=?, salary=?, email=?, phone_number=?, hire_date=?
            WHERE id=?
        ''', (name, position, salary, email, phone_number, hire_date, row_id))  # Use row_id

        conn.commit()
        conn.close()

        self.load_data()  # Refresh the table to show the changes
        print("Zmiany zapisane.")


from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QMessageBox,
)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy setup
engine = create_engine("sqlite:///users.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


Base.metadata.create_all(engine)  # Create the table
Session = sessionmaker(bind=engine)


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Login Form
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)

        login_button = QPushButton("Zaloguj się")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Sign Up Form (initially hidden, available only for admins)
        self.signup_form = SignUpApp()  # Create an instance of SignUpApp
        layout.addWidget(self.signup_form)
        self.signup_form.hide()

        self.setLayout(layout)
        self.setWindowTitle("Logowanie")
        self.setGeometry(100, 100, 400, 400)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        session = Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()

        if user and user.password == password:
            if user.role == "Administracja":
                self.signup_form.show()
                # Hide login form when login is successful
                for i in range(self.layout().count()):
                    widget = self.layout().itemAt(i).widget()
                    if widget not in [self.signup_form]:
                        widget.hide()
            else:
                QMessageBox.information(
                    self, "Zalogowano", "Zalogowano pomyślnie jako {}".format(user.role)
                )
        else:
            QMessageBox.warning(self, "Błąd logowania", "Nieprawidłowy email lub hasło.")




class SignUpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Sign Up Form
        self.signup_form = QWidget()
        signup_layout = QVBoxLayout(self.signup_form)

        self.name_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input2 = QLineEdit()
        self.password_input2.setEchoMode(QLineEdit.Password)

        role_layout = QHBoxLayout()
        self.role_buttons = [
            QRadioButton(role)
            for role in [
                "Uczeń",
                "Pracownik",
                "Administracja",
            ]
        ]
        for button in self.role_buttons:
            role_layout.addWidget(button)

        signup_layout.addWidget(QLabel("Imię"))
        signup_layout.addWidget(self.name_input)
        signup_layout.addWidget(QLabel("Nazwisko"))
        signup_layout.addWidget(self.lastname_input)
        signup_layout.addWidget(QLabel("Adres e-mail"))
        signup_layout.addWidget(self.email_input)
        signup_layout.addWidget(QLabel("Hasło"))
        signup_layout.addWidget(self.password_input2)
        signup_layout.addLayout(role_layout)

        signup_button = QPushButton("Dodaj użytkownika")
        signup_button.clicked.connect(self.signup)
        signup_layout.addWidget(signup_button)
        layout.addWidget(self.signup_form)  # Add the signup form directly

        self.setLayout(layout)
        self.setWindowTitle("Rejestracja")
        self.setGeometry(100, 100, 400, 400)

    def signup(self):
        role = [rb.text() for rb in self.role_buttons if rb.isChecked()][0]

        session = Session()
        new_user = User(
            name=self.name_input.text(),
            lastname=self.lastname_input.text(),
            email=self.email_input.text(),
            password=self.password_input2.text(),
            role=role,
        )
        try:
            session.add(new_user)
            session.commit()
            QMessageBox.information(self, "Sukces", "Użytkownik dodany pomyślnie!")
        except Exception as e:
            session.rollback()
            QMessageBox.warning(self, "Błąd", f"Nie udało się dodać użytkownika... {e}")
        finally:
            session.close()


if __name__ == "__main__":
    app = QApplication([])
    style = """

        QWidget{
            background-color: #FFFFFF;
        }

        QRadioButton{
            font-size: 18px;
        }
        QLabel{
            font-size: 20px;
            margin-bottom: 0px;
        }

        QLineEdit{
            height: 50px;
            font-size: 20px;
            border: 1px solid #326273;
            background-color: #EEEEEE;
        }

        QPushButton{
        font-weight: bold;
            margin-top: 50px;
            padding: 10px;
            height: 70px;
            border: none;
            font-size: 30px;
            color: #EEEEEE;
            background-color: #326273;
        }

        QPushButton:pressed {
            background-color: #E39774;
        }

        """
    app.setStyleSheet(style)
    login_app = LoginApp()  # Create an instance of LoginApp
    login_app.show()
    app.exec_()

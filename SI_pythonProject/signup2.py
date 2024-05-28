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
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# SQLAlchemy setup
engine = create_engine("sqlite:///users.db")  # Create SQLite database
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


class SignUpApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Admin Authentication
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Nazwa użytkownika"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Hasło dostępu"))
        layout.addWidget(self.password_input)

        auth_button = QPushButton("Autoryzuj")
        auth_button.clicked.connect(self.authenticate)
        layout.addWidget(auth_button)

        # Sign Up Form (initially hidden)
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
                "Nauczyciel",
                "Obsługa szkoły",
                "Administracja szkoły",
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
        layout.addWidget(self.signup_form)
        self.signup_form.hide()

        self.setLayout(layout)
        self.setWindowTitle("Rejestracja")
        self.setGeometry(100, 100, 400, 400)

    def authenticate(self):
        if (
            self.username_input.text() == "admin"
            and self.password_input.text() == "admin"
        ):
            self.signup_form.show()
        else:
            QMessageBox.warning(self, "Brak dostępu", "Błędne dane.")

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
    ex = SignUpApp()
    ex.show()
    app.exec_()

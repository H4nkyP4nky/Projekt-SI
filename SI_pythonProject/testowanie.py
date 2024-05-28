from app import db, Employee
from flask import Flask
from datetime import date

# flask app's instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database
db.init_app(app)

# create tables
with app.app_context():
    db.create_all()

    # Dodaj kilka rekordów testowych
    employee1 = Employee(
        name='John Doe', 
        position='Teacher', 
        salary=50000, 
        email='john.doe@example.com', 
        phone_number=1234567890, 
        hire_date=date(2023, 1, 15)
    )
    employee2 = Employee(
        name='Jane Smith', 
        position='Administrator', 
        salary=60000, 
        email='jane.smith@example.com', 
        phone_number=9876543210, 
        hire_date=date(2022, 12, 1)
    )

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.commit()

    print("Test records added successfully!")
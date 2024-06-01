from flask import Flask, jsonify
from app import db, EmptyTable, Employee
from main import MainWindow, run_main_window
from PyQt5.QtCore import QThread
import sys

# flask app's instance
api = Flask(__name__)

# configurations
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database
db.init_app(api)

# create tables
with api.app_context():
    db.create_all()


# Thread to run PyQt app
class MainWindowThread(QThread):
    def run(self):
        run_main_window()


# Create instance of MainWindowThread
main_window_thread = MainWindowThread()


# endpoint
@api.route('/')
def home():
    # Start PyQt app in a separate thread
    main_window_thread.start()
    return "API dla sieci szkół"  # welcome message


# api endpoint, json format
@api.route('/api/test', methods=['GET'])
def test():
    # python dictionary to json
    return jsonify({"message": "endpoint"}), 200  # 200 = http status


@api.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': employee.id,
        'name': employee.name,
        'position': employee.position,
        'salary': employee.salary,
        'email': employee.email
    } for employee in employees]), 200

# Endpoint to add a new employee

@api.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        name=data['name'],
        position=data['position'],
        salary=data['salary'],
        email=data['email']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully!'}), 201


# local, easy reloading
if __name__ == '__main__':
    api.run(debug=True)
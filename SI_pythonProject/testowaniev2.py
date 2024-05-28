import requests

def main():
    url = 'http://localhost:5000/api/employees'  # Zmień na odpowiedni URL, na którym uruchamia się twoja aplikacja Flask
    response = requests.get(url)

    if response.status_code == 200:
        employees_data = response.json()  # Odczytujemy odpowiedź jako JSON
        for employee in employees_data:
            print(f"ID: {employee['id']}, Name: {employee['name']}, Position: {employee['position']}, Salary: {employee['salary']}, Email: {employee['email']}")
    else:
        print(f"Failed to retrieve employees. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
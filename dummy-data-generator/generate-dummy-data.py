from faker import Faker
import csv, random

CSV_FILE_NAME = '../data/employees.csv'
COLUMNS = ['name', 'age', 'email', 'department', 'salary']
ROWS = 100
DEPARTMENTS = ["Human Resources", "Engineering", "IT", "Accounting", "Sales"]

fake = Faker()

with open(CSV_FILE_NAME, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(COLUMNS)
    for i in range(ROWS):
        name = fake.name()
        age = random.randint(22, 50)
        email = fake.email()
        department = random.choice(DEPARTMENTS)
        salary = random.randint(10000, 200000)
        writer.writerow([name, age, email, department, salary])


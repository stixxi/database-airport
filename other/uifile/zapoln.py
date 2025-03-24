import sqlite3
import random
from faker import Faker
import requests
fake = Faker()
FLIGHTS_API_URL = "https://jsonplaceholder.typicode.com/posts"
def fetch_flights_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении данных с API: {url}")
        return []
def generate_random_passengers(num):
    passengers = []
    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        passport_number = f"{random.randint(100000000, 999999999)}"
        passengers.append((first_name, last_name, passport_number))
    return passengers
def generate_random_airplanes(num):
    airplanes = []
    for _ in range(num):
        model = random.choice(["Boeing 737", "Airbus A320", "Bombardier CRJ-200", "Embraer E190"])
        capacity = random.randint(100, 300)
        airplanes.append((model, capacity))
    return airplanes
def generate_random_employees(num):
    employees = []
    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        position = random.choice(["Pilot", "Flight Attendant", "Ground Crew", "Engineer", "Security"])
        employees.append((first_name, last_name, position))
    return employees
def insert_passengers(passengers):
    con = sqlite3.connect('airport.db')
    cursor = con.cursor()
    cursor.executemany('''
        INSERT INTO passengers (first_name, last_name, passport_number)
        VALUES (?, ?, ?)
    ''', passengers)
    con.commit()
    con.close()
def insert_flights(flights):
    con = sqlite3.connect('airport.db')
    cursor = con.cursor()
    cursor.executemany('''
        INSERT INTO flights (flight_number, departure_airport, arrival_airport, departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
    ''', flights)
    con.commit()
    con.close()
def insert_airplanes(airplanes):
    con = sqlite3.connect('airport.db')
    cursor = con.cursor()
    cursor.executemany('''
        INSERT INTO airplanes (model, capacity)
        VALUES (?, ?)
    ''', airplanes)
    con.commit()
    con.close()
def insert_employees(employees):
    con = sqlite3.connect('airport.db')
    cursor = con.cursor()
    cursor.executemany('''
        INSERT INTO employees (first_name, last_name, position)
        VALUES (?, ?, ?)
    ''', employees)
    con.commit()
    con.close()
def fill_database():
    flights_data = fetch_flights_data_from_api(FLIGHTS_API_URL)
    flights = []
    for flight in flights_data:
        flight_number = f"AI{random.randint(100, 999)}"
        departure_airport = random.choice(["Sheremetyevo", "Domodedovo", "Vnukovo"])
        arrival_airport = random.choice(["Vnukovo", "Domodedovo", "Sheremetyevo"])
        departure_time = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M")
        arrival_time = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M")
        flights.append((flight_number, departure_airport, arrival_airport, departure_time, arrival_time))
    insert_flights(flights)
    passengers = generate_random_passengers(500)
    insert_passengers(passengers)
    airplanes = generate_random_airplanes(50)
    insert_airplanes(airplanes)
    employees = generate_random_employees(100)
    insert_employees(employees)
    print("База данных успешно заполнена")
if __name__ == "__main__":
    fill_database()

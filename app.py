import os
import psycopg2
from email import message
from dotenv import load_dotenv
from flask import Flask, request
from multiprocessing import connection
from datetime import datetime, timezone

#######################################

CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)

GLOBAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""

ROOM_NAME = """SELECT name FROM rooms WHERE id = (%s)"""
ROOM_NUMBER_OF_DAYS = """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures WHERE room_id = (%s);"""
ROOM_ALL_TIME_AVG = (
    "SELECT AVG(temperature) as average FROM temperatures WHERE room_id = (%s);"
)

#######################################
load_dotenv()

app = Flask(__name__)

url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.get("/")
def home():
    return "Hello Quicks"


@app.route('/api/create-room', methods=['POST'])
def create_room():
    data = request.get_json()
    # expected field from client
    name = data["name"]
    with connection:
        # cursor is an iterator mainly used for db operations
        with connection.cursor() as cursor:
            # this creates the room table if it doesnt exist
            cursor.execute(CREATE_ROOMS_TABLE)
            # this inserts the recieved value into the db
            # note that the name is in a turple
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            # this returns the id from the cursor
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {name} created."}, 201


@app.route('/api/temperature', methods=['POST'])
def add_temperature():
    data = request.get_json()
    # clients sends temperature
    temperature = data["temperature"]
    # clients selects (specifies) which room has the temparature
    room_id = data["room"]
    # checking to recieve datetime field from client
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    # if date field not provided by client
    except KeyError:
        # we get the current date time to insert as date
        date = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            # creates temperature table if it doesnt exist
            cursor.execute(CREATE_TEMPS_TABLE)
            # insert temperature to specified room
            cursor.execute(INSERT_TEMP, (room_id, temperature, date))
    return {"message": "Temperature added successfully."}, 201


@app.get('/api/average')
def get_global_average():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average, 2), "days": days}, 200


@app.get("/api/room/<int:room_id>")
def get_room_all(room_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOM_NAME, (room_id,))
            name = cursor.fetchone()[0]
            cursor.execute(ROOM_ALL_TIME_AVG, (room_id,))
            average = cursor.fetchone()[0]
            cursor.execute(ROOM_NUMBER_OF_DAYS, (room_id,))
            days = cursor.fetchone()[0]
    return {"name": name, "average": round(average, 2), "days": days}, 200

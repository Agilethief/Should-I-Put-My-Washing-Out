import sqlite3
from sqlite3 import Error
from datetime import datetime


def CreateReport(weatherConditions, predictedTimeToDry, reportedTimeToDry):
    database = r"database/postcodedata.sqlite"

    conn = create_connection(database)
    cur = conn.cursor()
    # Insert weather data into database
    cur.execute("INSERT INTO Reports (dateCreated, weatherTemp, weatherWind, weatherHumidity, predictedTimeToDry, reportedTimeToDry) VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now(), weatherConditions['weatherTemp'], weatherConditions['weatherWind'], weatherConditions['weatherHumidity'], predictedTimeToDry, reportedTimeToDry))
    print("Report created")
    conn.commit()
    conn.close()


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        exit()

    # Ensure table named "Reports" exists and if not, create one
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Reports (id INTEGER PRIMARY KEY, dateCreated TEXT, weatherTemp INTEGER, weatherWind INTEGER, weatherHumidity, predictedTimeToDry INTEGER, reportedTimeToDry INTEGER)")

    return conn


# For testing purposes
if __name__ == "__main__":
    weatherTemp = input("Enter weather temp: ")
    weatherWind = input("Enter weather wind: ")
    weatherHumidity = input("Enter weather humidity: ")
    weatherData = {'weatherTemp': weatherTemp,
                   'weatherWind': weatherWind,
                   'weatherHumidity': weatherHumidity
                   }

    predictedTimeToDry = input("Enter predicted time to dry: ")
    reportedTimeToDry = input("Enter reported time to dry: ")
    CreateReport(weatherData, predictedTimeToDry, reportedTimeToDry)

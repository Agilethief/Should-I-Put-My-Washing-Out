import sqlite3
from sqlite3 import Error
from datetime import datetime


def CreateReport(weatherConditions, predictedTimeToDry, reportedTimeToDry):
    if (EnsureAllInputsAreValid(weatherConditions, predictedTimeToDry, reportedTimeToDry) == False):
        print("Invalid/Unsafe input")
        return

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


def EnsureAllInputsAreValid(weatherData, predictedTimeToDry, reportedTimeToDry):
    try:
        int(weatherData['weatherTemp'])
    except ValueError:
        return False
    try:
        int(weatherData['weatherWind'])
    except ValueError:
        return False
    try:
        int(weatherData['weatherHumidity'])
    except ValueError:
        return False
    try:
        int(predictedTimeToDry)
    except ValueError:
        return False
    try:
        int(reportedTimeToDry)
    except ValueError:
        return False

    return True


def numericInput(prompt):
    while True:
        try:
            userInput = int(input(prompt))
        except ValueError:
            print("Please enter a number")
            continue
        else:
            return userInput
            break


# For testing purposes
if __name__ == "__main__":
    weatherTemp = numericInput("Enter weather temp: ")
    weatherWind = numericInput("Enter weather wind: ")
    weatherHumidity = numericInput("Enter weather humidity: ")
    weatherData = {'weatherTemp': weatherTemp,
                   'weatherWind': weatherWind,
                   'weatherHumidity': weatherHumidity
                   }

    predictedTimeToDry = numericInput("Enter predicted time to dry: ")
    reportedTimeToDry = input("Enter reported time to dry: ")
    CreateReport(weatherData, predictedTimeToDry, reportedTimeToDry)

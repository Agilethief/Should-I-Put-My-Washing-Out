import sqlite3
from sqlite3 import Error
from datetime import datetime


def CreateReport(weatherConditions, predictedTimeToDry, reportedTimeToDry):
    if (EnsureAllInputsAreValid(weatherConditions, predictedTimeToDry, reportedTimeToDry) == False):
        print("Invalid/Unsafe input")
        return

    database = r"database/postcodedata.sqlite"

    conn = create_connection_reports(database)
    cur = conn.cursor()
    # Insert weather data into database
    cur.execute("INSERT INTO Reports (dateCreated, weatherTemp, weatherWind, weatherHumidity, predictedTimeToDry, reportedTimeToDry) VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now(), weatherConditions['weatherTemp'], weatherConditions['weatherWind'], weatherConditions['weatherHumidity'], predictedTimeToDry, reportedTimeToDry))
    print("Report created")
    conn.commit()
    conn.close()


def create_connection_reports(db_file):
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


def create_connection_search(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        exit()

    # Ensure table named "Reports" exists and if not, create one
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, dateSearched TEXT, postcode INTEGER, longitude INTEGER, latitude, currenthour INTEGER, temp INTEGER, temp_2h INTEGER, predictedTimeToDry INTEGER, windspeed INTEGER, windspeed_2h INTEGER, precipitationProbability INTEGER, precipitationProbability_2h INTEGER, precipitation INTEGER, precipitation_2h INTEGER, precipitationIncreasing INTEGER, isDaytime INTEGER, timeToChange INTEGER, timeOfSunset INTEGER, timeOfSunrise INTEGER, tempMax INTEGER, tempMin INTEGER, tempCooling INTEGER, cloudCover INTEGER, cloudCover_2h INTEGER)")

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


def AddWeatherSearchToDatabase(weatherData, postcode, long, lat):
    print("adding Search data to  db")
    database = r"weatherdata/database/postcodedata.sqlite"

    conn = create_connection_search(database)
    cur = conn.cursor()
    # Insert weather data into database
    cur.execute(
        '''INSERT INTO searches 
        (dateSearched, 
         postcode, 
         longitude, latitude, 
         currenthour, 
         temp, temp_2h, 
         predictedTimeToDry, 
         windspeed, windspeed_2h, 
         precipitationProbability, precipitationProbability_2h, 
         precipitation, precipitation_2h, 
         isDaytime, 
         timeToChange, 
         timeOfSunset, timeOfSunrise, 
         tempMax, tempMin, tempCooling, 
         cloudCover, cloudCover_2h
         ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (datetime.now(),
         postcode,
         long, lat,
         weatherData['currenthour'],
         weatherData['temp'], weatherData['temp_2h'],
         weatherData['TimeToDry'],
         weatherData['windspeed'], weatherData['windspeed_2h'],
         weatherData['precipitationProbability'], weatherData['precipitationProbability_2h'],
         weatherData['precipitation'], weatherData['precipitation_2h'],
         weatherData['isDaytime'],
         weatherData['timeToChange'].hour,
         weatherData['timeOfSunset'], weatherData['timeOfSunrise'],
         weatherData['tempMax'], weatherData['tempMin'], weatherData['tempCooling'],
         weatherData['cloudCover'], weatherData['cloudCover_2h']))

    print("Search data created")
    conn.commit()
    conn.close()


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

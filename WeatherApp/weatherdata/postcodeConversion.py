import sqlite3
from sqlite3 import Error
import csv


def PostCodeToLongLat(postcode):
    print("Converting", postcode, "to long and lat")
    conn = GetDBConnection()
    cur = conn.cursor()

    long = 0
    lat = 0

    try:
        print("Searching for postcode", (postcode,))
        cur.execute(
            "SELECT long FROM postcodes WHERE postcode = ?", (postcode,))
        long = cur.fetchone()[0]
        print(long)
        cur.execute(
            "SELECT lat FROM postcodes WHERE postcode = ?", (postcode,))
        lat = cur.fetchone()[0]
        print(lat)
    except:
        print("Could not find postcode in database")

    conn.commit()
    conn.close()

    long_lat = (long, lat)
    return long_lat


def GetDBConnection():
    database = r"database/postcodedata.sqlite"

    conn = create_connection(database)
    return conn
    # I concur!

# database setup and reading


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        exit()

    print("Connected to database")
    return conn

# a function that reads an sql file and executes it


def execute_sql_file(conn, sql_file):
    try:
        c = conn.cursor()
        sql_file = open(sql_file)
        sql_as_string = sql_file.read()
        c.executescript(sql_as_string)
    except Error as e:
        print(e)


def load_csv_to_database(conn, csv_file):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE postcodes (id, postcode, suburb, state, long, lat)")

    with open(csv_file, 'r') as file:
        dictreader = csv.DictReader(file)
        to_db = [(i['id'], i['postcode'], i['locality'], i['state'],
                  i['long'], i['lat']) for i in dictreader]

    cur.executemany(
        "INSERT INTO postcodes (id, postcode, suburb, state, long, lat) VALUES (?, ?, ?, ?, ?, ?);", to_db)


def CreateDatabase():
    database = r"database/postcodedata.sqlite"

    conn = create_connection(database)
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='postcodes';")
        databaseTables = cur.fetchall()
        print(databaseTables)
    except:
        print("Could not search database")
        print("Exited early.")
        exit()

    # check if the postcodes table exists
    # check if table exists
    print(databaseTables, "databaseTables")
    if not databaseTables:
        print('No postcodetable exists, loading CSV file into database')
        load_csv_to_database(conn, "database/australian_postcodes.csv")

    conn.commit()
    conn.close()

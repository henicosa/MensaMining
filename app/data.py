import pandas as pd
import sqlite3
import analyzer
import os
import glob

import pprint
pp = pprint.PrettyPrinter(indent=4)

def init_db():
    conn = sqlite3.connect('meals.db')
    cursor = conn.cursor()
    # Create a table to store the meal information
    try:
        cursor.execute('''
            CREATE TABLE meals (
                date TEXT,
                city TEXT,
                facility TEXT,
                name TEXT,
                diet TEXT,
                allergens TEXT,
                additives TEXT,
                badges TEXT,
                prices TEXT,
                quicklikes INTEGER,
                primary key (city, facility, date, name)
            )
        ''')
    except:
        print("Database already initiated")
    conn.commit()
    conn.close()

def write_data_to_database(meal):
    # Connect to a SQLite database
    conn = sqlite3.connect('meals.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO meals (date, name, city, facility, diet, allergens, additives, badges, prices, quicklikes)
        VALUES (?,?,?,?,?,?,?,?,?,?)''', (meal["date"], meal['name'], meal["city"], meal["facility"], meal['diet'], str(meal['allergens']), str(meal['additives']), str(meal['badges']), str(meal['prices']), meal['quicklikes']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def raw_data_to_database():
    path = 'app/raw'
    init_db()
    html_files = [file for file in glob.glob(path + '/**/*.html', recursive=True)]
    for filepath in html_files:
        meals = analyzer.analyze_mensa(filepath)
        filename = os.path.basename(filepath).replace(".html", "").split("_")

        # Insert the meal information into the table
        for meal in meals:
            meal["date"] = filename[0]
            meal["city"] = filename[1]
            meal["facility"] = filename[2]
            write_data_to_database(meal)

raw_data_to_database()

# Dictionary to convert



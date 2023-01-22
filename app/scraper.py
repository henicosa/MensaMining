from datetime import datetime
import time

import json
import os

#from database import *

# import web crawler
from bs4 import BeautifulSoup
import logging
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

mensen = {
    "Weimar_Mensa am Park": "https://www.stw-thueringen.de/mensen/weimar/mensa-am-park.html",
    "Weimar_Cafeteria am Horn": "https://www.stw-thueringen.de/mensen/weimar/cafeteria-am-horn.html",
    "Weimar_Cafeteria Coudraystrasse": "https://www.stw-thueringen.de/mensen/weimar/cafeteria-coudraystrasse.html",
    "Erfurt_Mensa Nordhäuser Strasse": "https://www.stw-thueringen.de/mensen/erfurt/mensa-nordhaeuser-strasse.html",
    "Erfurt_Mensa Altonaer Strasse": "https://www.stw-thueringen.de/mensen/erfurt/mensa-altonaer-strasse.html",
    "Erfurt_Cafeteria Hörsaal 7": "https://www.stw-thueringen.de/mensen/erfurt/cafeteria-hoersaal-7.html",
    "Erfurt_Glasbox": "https://www.stw-thueringen.de/mensen/erfurt/glasbox.html",
    "Erfurt_Food-Truck": "https://www.stw-thueringen.de/mensen/erfurt/food-truck.html",
    "Erfurt_Cafeteria Schlüterstrasse": "https://www.stw-thueringen.de/mensen/erfurt/cafeteria-schlueterstrasse.html",
    "Erfurt_Cafeteria Leipziger Strasse": "https://www.stw-thueringen.de/mensen/erfurt/cafeteria-leipziger-strasse.html",
    "Jena_Mensa Ernst Abbe Platz": "https://www.stw-thueringen.de/mensen/jena/mensa-ernst-abbe-platz.html",
    "Jena_Mensa Carl Zeiss Promenade": "https://www.stw-thueringen.de/mensen/jena/mensa-carl-zeiss-promenade.html",
    "Jena_Mensa Philosophenweg": "https://www.stw-thueringen.de/mensen/jena/mensa-philosophenweg.html",
    "Jena_Cafeteria Vegetable": "https://www.stw-thueringen.de/mensen/jena/cafeteria-vegetable.html",
    "Jena_Cafeteria EAH": "https://www.stw-thueringen.de/mensen/jena/cafeteria-eah.html",
    "Jena_Cafeteria Carl Zeiss Strasse 3": "https://www.stw-thueringen.de/mensen/jena/cafeteria-carl-zeiss-strasse-3.html",
    "Jena_Cafeteria zur Rosen": "https://www.stw-thueringen.de/mensen/jena/cafeteria-zur-rosen.html",
    "Jena_Cafeteria Uni Hauptgebäude": "https://www.stw-thueringen.de/mensen/jena/cafeteria-uni-hauptgebaeude.html",
    "Jena_Cafeteria Bibliothek": "https://www.stw-thueringen.de/mensen/jena/cafeteria-bibliothek.html",
    "Ilmenau_Mensa Ehrenberg": "https://www.stw-thueringen.de/mensen/ilmenau/mensa-ehrenberg.html",
    "Ilmenau_Cafeteria Mensa Ehrenberg": "https://www.stw-thueringen.de/mensen/ilmenau/cafeteria-mensa-ehrenberg.html",
    "Ilmenau_Cafeteria Mini": "https://www.stw-thueringen.de/mensen/ilmenau/cafeteria-mini.html",
    "Ilmenau_Nanoteria": "https://www.stw-thueringen.de/mensen/ilmenau/nanoteria.html",
    "Ilmenau_Tower Cafe": "https://www.stw-thueringen.de/mensen/ilmenau/tower-cafe.html",
    "Ilmenau_Cafeteria Röntgenbau": "https://www.stw-thueringen.de/mensen/ilmenau/cafeteria-roentgenbau.html",
    "Gera_Mensa Weg der Freundschaft": "https://www.stw-thueringen.de/mensen/gera/mensa-weg-der-freundschaft.html",
    "Eisenach_Mensa am Wartenberg": "https://www.stw-thueringen.de/mensen/eisenach/mensa-am-wartenberg.html",
    "Nordhausen_Mensa Weinberghof": "https://www.stw-thueringen.de/mensen/nordhausen/mensa-weinberghof.html",
    "Schmalkaden_Mensa Blechhammer": "https://www.stw-thueringen.de/mensen/schmalkalden/mensa-blechhammer.html",
    "Schmalkaden_Cafeteria Mensa Blechhammer": "https://www.stw-thueringen.de/mensen/schmalkalden/cafeteria-mensa-blechhammer.html"
    }

def say(text):
    logging.info(text)
    print(text)

logging.basicConfig(filename="app/log/botlog.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

def get_todays_mealpage():
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")
    current_day = datetime.now().strftime("%d")

    current_date = datetime.now().strftime("%Y-%m-%d")

    directory_name = './raw/' + current_year + "/" + current_month + "/" + current_day
    path = os.getcwd()

    try:
        os.makedirs(path + '/' + directory_name)
        say("Directory " + directory_name + " Created ")
    except FileExistsError:
        say("Directory " + directory_name + " already exists")


    for mensa, url in mensen.items():
        try:
            save_page(url, path + "/" + directory_name + "/" + current_date + "_" + mensa + ".html")
        except:
            say("Request error with " + current_date + "_" + mensa)

    say("Processed Mensen for " + current_date)


def save_page(url, filepath):
    r = requests.get(url, headers=headers)
    with open(filepath, 'w') as f:
        f.write(r.text)


def uptime_heartbeat():
    print("send alive signal to uptime bot")
    requests.get(secrets["uptime_url"])

def scheduled_backup():
    backup_dicts_to_json()

def backup_db_to_json():
    print("start backup")
    json_object = json.dumps(db.users, indent=4)
    print("json object created")
    with open("./log/users.json", "w") as outfile:
        outfile.write(json_object)
        print("wrote it to file")

def restore_db_if_possible():
    if exists('log/users.json'):
        with open('./log/users.json', 'r') as openfile:
            dict_object = json.load(openfile)
            db.users = dict_object

#db = Database()
    
headers = {'user-agent': 'mensamining_2023 (Mail: lm82enbdz@mozmail.com)'}
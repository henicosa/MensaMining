import schedule
import time
import scraper
import logging

import os

# change the working directory to the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

logging.basicConfig(filename='log/error.log', level=logging.ERROR)

schedule.every().day.at("19:00").do(scraper.get_todays_mealpage)
print("Started scheduling")

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        logging.error(e)
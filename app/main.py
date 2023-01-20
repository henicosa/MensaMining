import schedule
import time
import scraper
import logging
logging.basicConfig(filename='app/log/error.log', level=logging.ERROR)

schedule.every().day.at("23:08").do(scraper.get_todays_mealpage)
print("Started scheduling")

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        logging.error(e)
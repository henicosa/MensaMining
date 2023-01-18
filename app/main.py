import schedule
import time
import scraper

schedule.every().day.at("22:50").do(scraper.get_todays_mealpage())

while True:
    schedule.run_pending()
    time.sleep(60)
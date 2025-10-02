import schedule
import time
from parser import update_prices

schedule.every().day.at("02:00").do(update_prices)

if __name__ == "__main__":
    update_prices()
    while True:
        schedule.run_pending()
        time.sleep(60)
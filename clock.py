import schedule
import time
import worker

# schedule.every().day.at("22:15").do(worker.main)
schedule.every(12).seconds.do(worker.main)


while True:
    schedule.run_pending()
    time.sleep(1)
